"""Coleta a DCA (prestação de contas anual) Anexo I-E, despesas por função, de 2024, para conferir a saúde do RREO.

Uso: python -u -I scripts/13_coleta_dca_funcao_saude.py
Lê os entes de dados_tratados/indicadores_2024.csv (92 municípios, 26 estados e o DF).
Grava em dados_brutos/:
  siconfi_dca_ie_2024.csv        linhas da DCA Anexo I-E (todas as funções, todas as colunas)
  siconfi_dca_ie_chamadas_2024.csv   registro de cada chamada (ente, status, linhas, erro)
Uma chamada que falha é registrada como falha, nunca ignorada. A API do Siconfi tem falhas intermitentes: cada
ente tem até 3 tentativas.
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca"
ANO = 2024
ANEXO = "DCA-Anexo I-E"
SAIDA = RAIZ / "dados_brutos" / "siconfi_dca_ie_2024.csv"
CHAMADAS = RAIZ / "dados_brutos" / "siconfi_dca_ie_chamadas_2024.csv"


def buscar(cod_ibge):
    url = BASE + "?" + urllib.parse.urlencode({"an_exercicio": ANO, "id_ente": cod_ibge, "no_anexo": ANEXO})
    pedido = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
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
    entes = pd.read_csv(RAIZ / "dados_tratados" / "indicadores_2024.csv")[["cod_ibge", "ente", "esfera"]]
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
