"""Analyze A1: decomposição exata do gasto em saúde por habitante das 92 cidades.

Uso: python -X utf8 scripts/19_analyze_a1_decomposicao.py
Grava dados_tratados/analyze_a1_decomposicao.csv.

gasto/hab = receita/hab x fatia, com fatia = saúde / receita. Em logaritmo a conta é uma soma exata:
ln(gasto) - média ln(gasto) = [ln(receita) - média ln(receita)] + [ln(fatia) - média ln(fatia)].
A referência é a média geométrica das 92 cidades (a mediana não se decompõe em produto).
"""
import numpy as np
import pandas as pd
import _mapa_comum as c

mun, _, _ = c.carrega_dados()
d = mun[["cod_ibge", "ente", "grupo", "regiao8", "populacao", "saude", "receita"]].copy()
d["gasto_hab"] = d.saude / d.populacao
d["receita_hab"] = d.receita / d.populacao
d["fatia"] = d.saude / d.receita
for col in ("gasto_hab", "receita_hab", "fatia"):
    d["ln_" + col] = np.log(d[col])
    d["dev_" + col] = d["ln_" + col] - d["ln_" + col].mean()
assert np.allclose(d.dev_gasto_hab, d.dev_receita_hab + d.dev_fatia)
d["parte_receita"] = d.dev_receita_hab / d.dev_gasto_hab
d.drop(columns=[x for x in d if x.startswith("ln_")]).to_csv(c.RAIZ / "dados_tratados" / "analyze_a1_decomposicao.csv", index=False, encoding="utf-8-sig")

ref = np.exp(d.ln_gasto_hab.mean()), np.exp(d.ln_receita_hab.mean()), np.exp(d.ln_fatia.mean())
print(f"referência (média geométrica): gasto/hab R$ {ref[0]:.0f}, receita/hab R$ {ref[1]:.0f}, fatia {ref[2]*100:.1f}%")
print(f"correlação (log) gasto x receita por hab: {np.corrcoef(np.log(d.gasto_hab), np.log(d.receita_hab))[0,1]:.2f}; gasto x fatia: {np.corrcoef(np.log(d.gasto_hab), np.log(d.fatia))[0,1]:.2f}")
g = d.groupby("grupo").agg(n=("ente", "size"), dev_gasto=("dev_gasto_hab", "median"), dev_receita=("dev_receita_hab", "median"), dev_fatia=("dev_fatia", "median"))
for k in ("dev_gasto", "dev_receita", "dev_fatia"):
    g[k] = (np.exp(g[k]) - 1) * 100
print("desvio da mediana do grupo contra a referência, em %:")
print(g.sort_values("dev_gasto").round(0).to_string())
print("\n10 que menos gastam:")
t = d.sort_values("gasto_hab").head(10)
print(t.assign(rec=(np.exp(t.dev_receita_hab) - 1) * 100, fat=(np.exp(t.dev_fatia) - 1) * 100)[["ente", "grupo", "gasto_hab", "receita_hab", "fatia", "rec", "fat"]].round(1).to_string(index=False))
r = d[d.grupo == c.CAPITAL].iloc[0]
print(f"\nCapital: gasto {r.gasto_hab:.0f}, receita {r.receita_hab:.0f}, fatia {r.fatia*100:.1f}%; mediana da fatia nas 92: {d.fatia.median()*100:.1f}%")
