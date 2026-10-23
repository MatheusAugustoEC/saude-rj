"""Despesa com pessoal: só o Executivo ou a soma dos Poderes? (RGF Anexo 01, 2024)

Uso: python -u -I scripts/06_pessoal_por_poder.py
Lê dados_brutos/siconfi_rgf_2024.csv (gerado por 04_coleta_valores.py) e imprime os resultados.
Não altera nenhum arquivo.
"""
from pathlib import Path

import pandas as pd

PASTA = Path(__file__).resolve().parent.parent / "dados_brutos"
COD_RJ = "33"
NOMES = {"E": "Executivo", "L": "Legislativo", "J": "Judiciário", "M": "Min. Público", "D": "Defensoria"}

pd.set_option("display.width", 200)
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

rgf = pd.read_csv(PASTA / "siconfi_rgf_2024.csv", dtype={"cod_ibge": str})
a1 = rgf[rgf.anexo == "RGF-Anexo 01"]


def pegar(cod_conta, coluna_regex, nome):
    f = a1[(a1.cod_conta == cod_conta) & a1.coluna.str.contains(coluna_regex, regex=True)]
    return f.groupby(["cod_ibge", "co_poder"]).valor.first().rename(nome)


p = pd.concat([pegar("DespesaComPessoalTotal", r"^Valor$", "pessoal"),
               pegar("DespesaComPessoalTotal", r"RCL Ajustada", "pct"),
               pegar("ReceitaCorrenteLiquidaAjustada", r"^Valor$", "rcl"),
               pegar("LimiteMaximoDespesaComPessoalTotal", r"RCL Ajustada", "limite_pct")], axis=1).reset_index()
nomes = rgf.drop_duplicates("cod_ibge").set_index("cod_ibge").instituicao
p["estado"] = p.cod_ibge.str.len() == 2

print("1. O RJ (estado), por Poder, 2024")
rj = p[p.cod_ibge == COD_RJ].copy()
rj["poder"] = rj.co_poder.map(NOMES)
print(rj[["poder", "pessoal", "rcl", "pct", "limite_pct"]].to_string(index=False))
print(f"   Soma dos % dos Poderes: {rj.pct.sum():.2f}% | soma dos limites declarados: {rj.limite_pct.sum():.2f}%")

print("\n2. A RCL é a mesma para todos os Poderes do mesmo ente? (diferença máxima relativa entre Poderes)")
for rotulo, grupo in (("estados", p[p.estado]), ("municípios", p[~p.estado])):
    d = grupo.groupby("cod_ibge").rcl.agg(["min", "max"])
    rel = ((d["max"] - d["min"]) / d["max"]).fillna(0)
    print(f"   {rotulo}: entes com RCL diferente entre Poderes (>0,5%): {int((rel > 0.005).sum())} de {len(d)} | maior diferença: {rel.max():.2%}")

print("\n3. Soma dos Poderes x só Executivo, entre os estados")
est = p[p.estado].groupby("cod_ibge").agg(soma_pct=("pct", "sum"), poderes=("co_poder", "count"))
est["exec_pct"] = p[p.estado & (p.co_poder == "E")].set_index("cod_ibge").pct
est["nome"] = est.index.map(nomes)
est["pos_exec"] = est.exec_pct.rank(ascending=False, method="min").astype(int)
est["pos_soma"] = est.soma_pct.rank(ascending=False, method="min").astype(int)
print(est.sort_values("soma_pct", ascending=False)[["nome", "poderes", "exec_pct", "soma_pct", "pos_exec", "pos_soma"]].to_string())

print("\n4. Municípios: Executivo + Legislativo")
mun = p[~p.estado].groupby("cod_ibge").agg(soma_pct=("pct", "sum"), poderes=("co_poder", "count"))
print(mun.poderes.value_counts().rename("entes por nº de Poderes com dado"))
mun["exec_pct"] = p[~p.estado & (p.co_poder == "E")].set_index("cod_ibge").pct
print(mun[["exec_pct", "soma_pct"]].describe())

print("\n5. Municípios: somar percentuais de cada Poder x somar os valores e dividir pela RCL do Executivo")
m = p[~p.estado]
rcl_exec = m[m.co_poder == "E"].set_index("cod_ibge").rcl
alt = m.groupby("cod_ibge").pessoal.sum() / rcl_exec * 100
dif = (mun.soma_pct - alt)
print(f"   Entes em que os dois métodos diferem em mais de 0,5 p.p.: {int((dif.abs() > 0.5).sum())} de {len(dif)}")
print("   Maior diferença (p.p.):", round(dif.abs().max(), 2))
detalhe = pd.DataFrame({"nome": dif.index.map(nomes), "soma_percentuais": mun.soma_pct, "soma_valores_rcl_exec": alt, "diferenca": dif})
print(detalhe[dif.abs() > 0.5].sort_values("diferenca", key=abs, ascending=False).head(10).to_string())
print("   Municípios com RCL do Legislativo diferente da do Executivo: ", int(((m[m.co_poder == 'L'].set_index('cod_ibge').rcl - rcl_exec).abs() / rcl_exec > 0.005).sum()))
