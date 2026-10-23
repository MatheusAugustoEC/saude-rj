"""Viabilidade: os dados de dívida (RGF Anexo 02) e de restos a pagar (RREO Anexo 07) trazem o que a hipótese precisa?

Uso: python -u -I scripts/07_viabilidade_divida_restos.py
Não calcula conclusão nenhuma: só confere quais campos existem e para quantos entes.
"""
from pathlib import Path

import pandas as pd

PASTA = Path(__file__).resolve().parent.parent / "dados_brutos"
COD_RJ = "33"
pd.set_option("display.width", 220)
pd.set_option("display.max_colwidth", 95)
pd.set_option("display.max_rows", 200)
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

rgf = pd.read_csv(PASTA / "siconfi_rgf_2024.csv", dtype={"cod_ibge": str})
rreo = pd.read_csv(PASTA / "siconfi_rreo_2024.csv", dtype={"cod_ibge": str})
TOTAL_ENTES = 119

print("1. RGF Anexo 02 (dívida consolidada): RJ, colunas e contas principais")
d = rgf[rgf.anexo == "RGF-Anexo 02"]
print("   colunas:", sorted(d.coluna.unique()))
rj = d[d.cod_ibge == COD_RJ]
print(rj[rj.coluna.str.contains(r"RCL|Valor|SALDO|Saldo", regex=True)][["cod_conta", "conta", "coluna", "valor"]].head(40).to_string())

print("\n2. Para quantos entes existe cada conta de dívida (entre 119)?")
contagem = d.groupby("cod_conta").cod_ibge.nunique().sort_values(ascending=False)
print(contagem.head(25).to_string())

print("\n3. RREO Anexo 07 (restos a pagar): contas e colunas no RJ")
r7 = rreo[rreo.anexo == "RREO-Anexo 07"]
print("   rótulos:", list(r7.rotulo.unique()))
print("   colunas:", sorted(r7.coluna.unique()))
print(r7[r7.cod_ibge == COD_RJ].drop_duplicates("cod_conta")[["rotulo", "cod_conta", "conta"]].head(25).to_string())
print("\n   Para quantos entes existe cada conta (entre 119)?")
print(r7.groupby("cod_conta").cod_ibge.nunique().sort_values(ascending=False).head(15).to_string())
