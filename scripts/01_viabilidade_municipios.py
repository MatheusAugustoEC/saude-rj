"""Checagem de viabilidade: os 92 municípios do RJ entregaram dados ao Siconfi em 2024?

Uso: python -I scripts/01_viabilidade_municipios.py
Grava as respostas brutas em dados_brutos/ e escreve o resumo na tela.
Falhas de consulta são listadas no fim, nunca ignoradas.
"""
import json
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt"
ANO = 2024
PASTA = Path(__file__).resolve().parent.parent / "dados_brutos"


def consultar(caminho, params=None):
    url = BASE + caminho
    if params:
        url += "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=120) as resposta:
        bruto = resposta.read()
    try:
        texto, codificacao = bruto.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        texto, codificacao = bruto.decode("latin-1"), "latin-1"
    return json.loads(texto), codificacao


def main():
    PASTA.mkdir(exist_ok=True)
    coleta = datetime.now().isoformat(timespec="seconds")

    entes, codificacao_entes = consultar("/entes")
    municipios = [e for e in entes["items"] if e["uf"] == "RJ" and e["esfera"] == "M"]
    print(f"Municípios do RJ em /entes: {len(municipios)} (codificação: {codificacao_entes})")

    resultados, falhas, codificacoes = [], [], Counter()
    for ente in municipios:
        try:
            dados, cod = consultar("/extrato_entregas", {"id_ente": ente["cod_ibge"], "an_referencia": ANO})
        except Exception as erro:
            falhas.append((ente["cod_ibge"], ente["ente"], str(erro)))
            continue
        codificacoes[cod] += 1
        resultados.append({"cod_ibge": ente["cod_ibge"], "ente": ente["ente"],
                           "populacao": ente["populacao"], "itens": dados["items"],
                           "tem_mais_paginas": dados.get("hasMore")})

    saida = PASTA / f"extrato_entregas_municipios_rj_{ANO}.json"
    saida.write_text(json.dumps({"coletado_em": coleta, "ano": ANO, "municipios": resultados,
                                 "falhas": falhas}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Gravado: {saida}")
    print(f"Codificação das respostas: {dict(codificacoes)}")

    # Quantos municípios entregaram cada relatório (qualquer status) e com qual status
    entregou = {"RREO": 0, "RGF": 0, "DCA": 0}
    status = Counter()
    sem_nada = []
    for r in resultados:
        tipos = set()
        for i in r["itens"]:
            nome = i["entregavel"]
            if nome.startswith("Relat") and "Resumido" in nome:
                tipos.add("RREO")
            elif nome.startswith("Relat") and "Gest" in nome:
                tipos.add("RGF")
            elif "DCA" in nome:
                tipos.add("DCA")
            status[(nome, i["status_relatorio"])] += 1
        for t in tipos:
            entregou[t] += 1
        if not r["itens"]:
            sem_nada.append(r["ente"])
    print(f"\nMunicípios consultados com sucesso: {len(resultados)} de {len(municipios)}")
    for t, n in entregou.items():
        print(f"  com ao menos um {t} em {ANO}: {n}")
    print(f"  sem nenhuma entrega listada: {len(sem_nada)} {sem_nada}")
    print("\nStatus dos relatórios (entregável, status): contagem")
    for chave, n in sorted(status.items()):
        print(f"  {chave}: {n}")
    print(f"\nFalhas de consulta: {len(falhas)}")
    for f in falhas:
        print("  ", f)


if __name__ == "__main__":
    main()
