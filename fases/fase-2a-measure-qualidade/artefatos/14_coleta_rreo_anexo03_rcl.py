"""Coleta o RREO Anexo 03 (demonstrativo da receita corrente líquida, 6º bimestre) de 2024 para conferir a RCL do RGF.

Uso: python -u -I scripts/14_coleta_rreo_anexo03_rcl.py
Lê os entes de dados_tratados/indicadores_2024.csv (92 municípios, 26 estados e o DF).
Grava em dados_brutos/:
  siconfi_rreo_anexo03_2024.csv            linhas do Anexo 03 (todas as contas e colunas)
  siconfi_rreo_anexo03_chamadas_2024.csv   registro de cada chamada (ente, linhas, erro)
Uma chamada que falha é registrada como falha, nunca ignorada. Cada ente tem até 3 tentativas.
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo"
SAIDA = RAIZ / "dados_brutos" / "siconfi_rreo_anexo03_2024.csv"
CHAMADAS = RAIZ / "dados_brutos" / "siconfi_rreo_anexo03_chamadas_2024.csv"


def buscar(cod_ibge):
    params = {"an_exercicio": 2024, "nr_periodo": 6, "co_tipo_demonstrativo": "RREO",
              "no_anexo": "RREO-Anexo 03", "id_ente": cod_ibge}
    pedido = urllib.request.Request(BASE + "?" + urllib.parse.urlencode(params), headers={"User-Agent": "Mozilla/5.0"})
    ultimo_erro = ""
    for tentativa in range(3):
        try:
            with urllib.request.urlopen(pedido, timeout=60) as resposta:
                dados = json.load(resposta)
            if dados.get("hasMore"):
                raise RuntimeError("a resposta tem mais de uma página; o script não pagina")
            return dados["items"], ""
        except Exception as erro:
            ultimo_erro = str(erro)[:120]
            time.sleep(2 * (tentativa + 1))
    return [], ultimo_erro


def main():
    entes = pd.read_csv(RAIZ / "dados_tratados" / "indicadores_2024.csv", dtype={"cod_ibge": str})[["cod_ibge", "ente", "esfera"]]
    linhas = []
    with open(CHAMADAS, "w", newline="", encoding="utf-8-sig") as f:
        registro = csv.writer(f)
        registro.writerow(["cod_ibge", "ente", "esfera", "linhas", "erro"])
        for ente in entes.itertuples(index=False):
            itens, erro = buscar(ente.cod_ibge)
            linhas.extend(itens)
            registro.writerow([ente.cod_ibge, ente.ente, ente.esfera, len(itens), erro])
            print(f"{'OK  ' if itens else 'FALHA'} | {ente.cod_ibge} {ente.ente} | {len(itens)} linhas {erro}")
    pd.DataFrame(linhas).to_csv(SAIDA, index=False, encoding="utf-8-sig")
    print(f"Gravado {len(linhas)} linhas em {SAIDA.name}")


if __name__ == "__main__":
    main()
