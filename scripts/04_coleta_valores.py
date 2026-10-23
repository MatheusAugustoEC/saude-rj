"""Coleta dos valores das contas (Siconfi) para a EDA: 27 estados e 92 municípios do RJ, exercício 2024.

Uso: python -u -I scripts/04_coleta_valores.py
Fonte: API do Tesouro Nacional (https://apidatalake.tesouro.gov.br/ords/siconfi/tt/).

O que coleta:
  RREO (último bimestre entregue): Anexo 01 (balanço orçamentário), Anexo 02 (despesa por função)
                                   e Anexo 07 (restos a pagar).
  RGF  (último período entregue):  Anexo 01 (despesa com pessoal e RCL), por Poder, e
                                   Anexo 02 (dívida consolidada).
O tipo de relatório (normal ou "Simplificado"), o período e a periodicidade de cada ente
são lidos do extrato de entregas do próprio ente. Nada é suposto.

Grava em dados_brutos/ os registros exatamente como a API devolveu (um CSV por relatório) e
um CSV com o registro de cada chamada (linhas devolvidas, tempo, erro).
Chamada que falha ou volta vazia é registrada e listada no fim, nunca ignorada.
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt"
ANO = 2024
PASTA = Path(__file__).resolve().parent.parent / "dados_brutos"
ANEXOS_RREO = ["RREO-Anexo 01", "RREO-Anexo 02", "RREO-Anexo 07"]
PODERES_ESTADO = ["E", "L", "J", "M", "D"]
PODERES_MUNICIPIO = ["E", "L"]
# RGF: o Anexo 01 (pessoal) vem por Poder; o Anexo 02 (dívida consolidada) é do ente, consultado pelo Executivo
ANEXOS_RGF = {"RGF-Anexo 01": None, "RGF-Anexo 02": ["E"]}   # None = todos os Poderes do ente
TENTATIVAS = 3


def consultar(caminho, params):
    url = BASE + caminho + "?" + urllib.parse.urlencode(params)
    for tentativa in range(1, TENTATIVAS + 1):
        inicio = time.time()
        try:
            with urllib.request.urlopen(url, timeout=180) as resposta:
                dados = json.loads(resposta.read().decode("utf-8"))
            return dados, round(time.time() - inicio, 1), ""
        except Exception as erro:
            if tentativa == TENTATIVAS:
                return None, round(time.time() - inicio, 1), str(erro)[:120]
            time.sleep(5 * tentativa)


def escolher(itens, palavra_chave):
    """Entre as entregas do ente, escolhe o último período do relatório pedido.

    Devolve (simplificado, periodo, periodicidade) ou None se o ente não entregou.
    """
    candidatos = [i for i in itens if palavra_chave in i["entregavel"]]
    if not candidatos:
        return None
    ultimo = max(candidatos, key=lambda i: (i["periodo"], not i["entregavel"].endswith("Simplificado")))
    return ultimo["entregavel"].endswith("Simplificado"), ultimo["periodo"], ultimo["periodicidade"]


def main():
    PASTA.mkdir(exist_ok=True)
    coleta = datetime.now().isoformat(timespec="seconds")
    entes, _, erro = consultar("/entes", {})
    if entes is None:
        raise SystemExit(f"Falha ao ler /entes: {erro}")
    estados = [e for e in entes["items"] if e["esfera"] in ("E", "D")]
    municipios = [e for e in entes["items"] if e["uf"] == "RJ" and e["esfera"] == "M"]
    print(f"Estados (incluindo DF): {len(estados)} | municípios do RJ: {len(municipios)}")

    registros = {"rreo": [], "rgf": []}
    chamadas = []
    extrato_estados = {}

    def registrar(ente, relatorio, params, dados, segundos, erro):
        linhas = len(dados["items"]) if dados else 0
        chamadas.append({"cod_ibge": ente["cod_ibge"], "ente": ente["ente"], "esfera": ente["esfera"],
                         "relatorio": relatorio, "parametros": json.dumps(params, ensure_ascii=False),
                         "linhas": linhas, "tem_mais_paginas": dados.get("hasMore") if dados else "",
                         "segundos": segundos, "erro": erro})
        return dados["items"] if dados else []

    for numero, ente in enumerate(estados + municipios, start=1):
        extrato, segundos, erro = consultar("/extrato_entregas", {"id_ente": ente["cod_ibge"], "an_referencia": ANO})
        registrar(ente, "extrato_entregas", {"id_ente": ente["cod_ibge"], "an_referencia": ANO}, extrato, segundos, erro)
        if extrato is None:
            continue
        if ente in estados:
            extrato_estados[ente["cod_ibge"]] = extrato["items"]
        eh_estado = ente["esfera"] in ("E", "D")
        # O cadastro marca o DF com esfera "D", mas a API de RREO/RGF só o encontra com "E" (verificado em 21/10/2026).
        base = {"id_ente": ente["cod_ibge"], "an_exercicio": ANO, "co_esfera": "E" if eh_estado else ente["esfera"]}

        rreo = escolher(extrato["items"], "Resumido")
        if rreo:
            simplificado, periodo, _ = rreo
            demonstrativo = "RREO Simplificado" if simplificado else "RREO"
            for anexo in ANEXOS_RREO:
                params = {**base, "nr_periodo": periodo, "co_tipo_demonstrativo": demonstrativo, "no_anexo": anexo}
                dados, segundos, erro = consultar("/rreo", params)
                registros["rreo"] += registrar(ente, f"{demonstrativo} / {anexo} / período {periodo}",
                                               params, dados, segundos, erro)
        else:
            registrar(ente, "RREO", {}, None, 0, "ente não entregou RREO em 2024 (extrato)")

        rgf = escolher(extrato["items"], "Gest")
        if rgf:
            simplificado, periodo, periodicidade = rgf
            demonstrativo = "RGF Simplificado" if simplificado else "RGF"
            for anexo_rgf, poderes in ANEXOS_RGF.items():
                for poder in (poderes or (PODERES_ESTADO if eh_estado else PODERES_MUNICIPIO)):
                    params = {**base, "nr_periodo": periodo, "co_tipo_demonstrativo": demonstrativo,
                              "no_anexo": anexo_rgf, "co_poder": poder, "in_periodicidade": periodicidade}
                    dados, segundos, erro = consultar("/rgf", params)
                    registros["rgf"] += registrar(ente, f"{demonstrativo} / {anexo_rgf} / poder {poder} / período {periodo}",
                                                  params, dados, segundos, erro)
        else:
            registrar(ente, "RGF", {}, None, 0, "ente não entregou RGF em 2024 (extrato)")
        if numero % 10 == 0:
            print(f"  {numero} de {len(estados) + len(municipios)} entes processados")

    for nome, linhas in registros.items():
        arquivo = PASTA / f"siconfi_{nome}_{ANO}.csv"
        campos = sorted({k for r in linhas for k in r})
        with open(arquivo, "w", newline="", encoding="utf-8-sig") as f:
            escritor = csv.DictWriter(f, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(linhas)
        print(f"Gravado: {arquivo} ({len(linhas)} linhas)")
    with open(PASTA / f"siconfi_chamadas_{ANO}.csv", "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.DictWriter(f, fieldnames=list(chamadas[0].keys()))
        escritor.writeheader()
        escritor.writerows(chamadas)
    (PASTA / f"siconfi_extrato_estados_{ANO}.json").write_text(
        json.dumps({"coletado_em": coleta, "ano": ANO, "estados": extrato_estados}, ensure_ascii=False),
        encoding="utf-8")

    com_erro = [c for c in chamadas if c["erro"]]
    vazias = [c for c in chamadas if not c["erro"] and c["linhas"] == 0]
    com_mais = [c for c in chamadas if c["tem_mais_paginas"] is True]
    print(f"\nChamadas: {len(chamadas)} | com erro: {len(com_erro)} | vazias: {len(vazias)} | com mais páginas: {len(com_mais)}")
    for c in com_erro[:30]:
        print("  ERRO", c["cod_ibge"], c["ente"], c["relatorio"], c["erro"])
    for c in vazias[:30]:
        print("  VAZIA", c["cod_ibge"], c["ente"], c["relatorio"])


if __name__ == "__main__":
    main()
