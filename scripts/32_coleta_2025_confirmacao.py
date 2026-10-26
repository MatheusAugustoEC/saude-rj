"""Control, passo 3a: coleta de 2025 para o recorte de confirmação (C5): receita (RREO Anexo 01) e despesa por função (DCA Anexo I-E) dos 92 municípios do RJ.

Uso: python -X utf8 -u scripts/32_coleta_2025_confirmacao.py   (rodar UMA vez; as previsões estão em docs/14-control-previsoes-2025.md)
Mesma definição de 2023 e 2024: receita = ReceitasExcetoIntraOrcamentarias, "Até o Bimestre (c)", último período entregue (extrato de entregas do ente);
saúde = DCA Anexo I-E, função "10 - Saúde", coluna "Despesas Empenhadas".
Grava em dados_brutos/: siconfi_rreo_anexo01_2025.csv, siconfi_dca_ie_2025.csv, siconfi_chamadas_2025.csv. Chamada que falha ou volta vazia fica registrada.
"""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt"
ANO = 2025
PASTA = RAIZ / "dados_brutos"


def consultar(caminho, params):
    url = BASE + caminho + "?" + urllib.parse.urlencode(params)
    erro = ""
    for tentativa in range(1, 4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=120) as r:
                dados = json.load(r)
            if dados.get("hasMore"):
                raise RuntimeError("resposta com mais de uma página; o script não pagina")
            return dados["items"], ""
        except Exception as e:
            erro = str(e)[:120]
            time.sleep(3 * tentativa)
    return [], erro


def main():
    entes = pd.read_csv(RAIZ / "dados_tratados" / "indicadores_2024.csv", dtype={"cod_ibge": str})
    entes = entes[entes.esfera == "M"][["cod_ibge", "ente"]]
    assert len(entes) == 92
    rreo, dca, chamadas = [], [], []
    for n, e in enumerate(entes.itertuples(index=False), 1):
        extrato, erro_e = consultar("/extrato_entregas", {"id_ente": e.cod_ibge, "an_referencia": ANO})
        cand = [i for i in extrato if "Resumido" in i["entregavel"]]
        itens_r, erro_r, rotulo = [], "", ""
        if cand:
            ult = max(cand, key=lambda i: (i["periodo"], not i["entregavel"].endswith("Simplificado")))
            simpl = ult["entregavel"].endswith("Simplificado")
            tipo = "RREO Simplificado" if simpl else "RREO"
            rotulo = f"{tipo} período {ult['periodo']}"
            itens_r, erro_r = consultar("/rreo", {"id_ente": e.cod_ibge, "an_exercicio": ANO, "co_esfera": "M", "nr_periodo": ult["periodo"],
                                                  "co_tipo_demonstrativo": tipo, "no_anexo": "RREO-Anexo 01"})
        else:
            erro_r = erro_e or "ente não entregou RREO em 2025 (extrato)"
        rreo += itens_r
        itens_d, erro_d = consultar("/dca", {"an_exercicio": ANO, "id_ente": e.cod_ibge, "no_anexo": "DCA-Anexo I-E"})
        dca += itens_d
        chamadas.append({"cod_ibge": e.cod_ibge, "ente": e.ente, "rreo": rotulo, "linhas_rreo": len(itens_r), "erro_rreo": erro_r,
                         "linhas_dca": len(itens_d), "erro_dca": erro_d})
        print(f"{n:2d} {e.ente:28s} RREO {len(itens_r):3d} {erro_r} | DCA {len(itens_d):4d} {erro_d}", flush=True)
    for nome, linhas in (("siconfi_rreo_anexo01_2025.csv", rreo), ("siconfi_dca_ie_2025.csv", dca)):
        pd.DataFrame(linhas).to_csv(PASTA / nome, index=False, encoding="utf-8-sig")
        print(f"Gravado {nome}: {len(linhas)} linhas")
    pd.DataFrame(chamadas).to_csv(PASTA / "siconfi_chamadas_2025.csv", index=False, encoding="utf-8-sig")
    falhas = [c for c in chamadas if c["linhas_rreo"] == 0 or c["linhas_dca"] == 0]
    print(f"Chamadas com falha ou vazias: {len(falhas)}", [c["ente"] for c in falhas])


if __name__ == "__main__":
    main()
