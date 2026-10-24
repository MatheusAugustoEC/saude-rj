"""Analyze A5: replicação da decomposição (A1) e do modelo (A2) com os dados de 2023.

Uso: python -X utf8 scripts/23_analyze_a5_replicacao_2023.py
Entrada: dados_brutos/siconfi_rreo_anexo01_2023.csv, siconfi_dca_ie_2023.csv (script 22), populações do IBGE.
Saída: dados_tratados/indicadores_2023_replicacao.csv e dados_tratados/analyze_a5_coeficientes.csv.
Definições iguais às de 2024: receita = RREO Anexo 01 "RECEITAS (EXCETO INTRA-ORÇAMENTÁRIAS)" até o bimestre; saúde = DCA I-E função 10, empenhada.
População de 2023: o IBGE não publicou estimativa municipal para 2023 (tabela 6579 vai 2021, 2022, 2024, 2025); uso a média geométrica entre o Censo 2022
e a estimativa de 2024, que equivale a crescimento constante entre os dois anos.
O modelo é idêntico ao M3 do A2 (91 cidades, sem a capital), mais o M1 com as 92.
"""
import json
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

import _mapa_comum as c

warnings.filterwarnings("ignore")
BR = c.RAIZ / "dados_brutos"


def populacao_por_codigo(arquivo, chave):
    bruto = json.load(open(BR / arquivo, encoding="utf-8"))
    bloco = bruto[chave] if chave else bruto
    return {l["D1C"]: float(l["V"]) for l in bloco[1:] if l["V"] not in ("-", "...", "X")}


censo = populacao_por_codigo("ibge_populacao_censo2022_4714.json", "censo2022_mun")
raw24 = json.load(open(BR / "ibge_populacao_6579.json", encoding="utf-8"))["2024"]
est24 = {}
for bloco in raw24:
    for l in bloco[1:]:
        if l["V"] not in ("-", "...", "X"):
            est24[l["D1C"]] = float(l["V"])

mun, _, _ = c.carrega_dados()
base = mun[["cod_ibge", "ente", "grupo", "regiao8", "populacao"]].copy()
base["pop2024"] = base.populacao
base["pop2022"] = base.cod_ibge.map(censo)
assert base.pop2022.notna().all(), base[base.pop2022.isna()].ente.tolist()
base["pop2023"] = np.sqrt(base.pop2022 * base.pop2024)

r = pd.read_csv(BR / "siconfi_rreo_anexo01_2023.csv", dtype={"cod_ibge": str}, low_memory=False)
rec = r[r.conta.str.startswith("RECEITAS (EXCETO INTRA") & (r.coluna == "Até o Bimestre (c)")].groupby("cod_ibge").agg(receita=("valor", "first"), periodo=("periodo", "first"))
d = pd.read_csv(BR / "siconfi_dca_ie_2023.csv", dtype={"cod_ibge": str}, low_memory=False)
sau = d[d.conta.str.startswith("10 - Sa") & (d.coluna == "Despesas Empenhadas")].groupby("cod_ibge").valor.first().rename("saude")
t = base.set_index("cod_ibge").join(rec).join(sau).reset_index()
print("municípios com RREO até o 6º bimestre:", int((t.periodo == 6).sum()), "| outros:", t[t.periodo != 6][["ente", "periodo"]].values.tolist())
t = t[t.periodo == 6].copy()  # receita de ano incompleto não é comparável
print("cidades na replicação:", len(t))
t["gasto_hab"] = t.saude / t.pop2023
t["receita_hab"] = t.receita / t.pop2023
t["fatia"] = t.saude / t.receita
t.to_csv(c.RAIZ / "dados_tratados" / "indicadores_2023_replicacao.csv", index=False, encoding="utf-8-sig")
pct = lambda b: (np.exp(b) - 1) * 100

# ---- A1 em 2023
for k in ("gasto_hab", "receita_hab", "fatia"):
    t["ln_" + k] = np.log(t[k])
    t["dev_" + k] = t["ln_" + k] - t["ln_" + k].mean()
print(f"\nReferência 2023 (média geométrica): gasto/hab R$ {np.exp(t.ln_gasto_hab.mean()):.0f}, receita/hab R$ {np.exp(t.ln_receita_hab.mean()):.0f}, fatia {np.exp(t.ln_fatia.mean())*100:.1f}%")
print(f"correlação (log) gasto x receita: {np.corrcoef(t.ln_gasto_hab, t.ln_receita_hab)[0,1]:.2f}; gasto x fatia: {np.corrcoef(t.ln_gasto_hab, t.ln_fatia)[0,1]:.2f}")
g = t.groupby("grupo")[["dev_gasto_hab", "dev_receita_hab", "dev_fatia"]].median().apply(lambda s: (np.exp(s) - 1) * 100)
g["n"] = t.groupby("grupo").size()
print("desvio da mediana do grupo contra a referência (%):\n", g.sort_values("dev_gasto_hab").round(0).to_string())
cap = t[t.grupo == c.CAPITAL].iloc[0]
print(f"Capital 2023: gasto {cap.gasto_hab:.0f}, receita {cap.receita_hab:.0f}, fatia {cap.fatia*100:.1f}% (mediana {t.fatia.median()*100:.1f}%)")
menores = t.sort_values("gasto_hab").head(10)
print("10 que menos gastam em 2023:", menores.ente.tolist())
print("  na Metropolitana:", int((menores.regiao8 == "Metropolitana").sum()), "de 10")

# ---- A2 em 2023
t["y"] = t.ln_gasto_hab
t["x"] = t.ln_receita_hab
t["Baixada"] = (t.grupo == c.BAIXADA).astype(float)
t["Resto"] = (t.grupo == c.RESTO).astype(float)
cap = t[t.grupo == c.CAPITAL].iloc[0]
sem = t[t.grupo != c.CAPITAL]
linhas = []
for nome, df, cols in (("M1 só receita", t, ["x"]), ("M3 receita + grupos, sem a capital", sem, ["x", "Baixada", "Resto"])):
    m = sm.OLS(df.y, sm.add_constant(df[cols])).fit(cov_type="HC3")
    ci = m.conf_int(0.05)
    print(f"\n{nome} (n={len(df)}, R2={m.rsquared:.3f})  elasticidade {m.params['x']:.3f} [{ci.loc['x',0]:.3f}; {ci.loc['x',1]:.3f}]")
    linhas.append({"modelo": nome, "termo": "x", "coef": m.params["x"], "ic_baixo": ci.loc["x", 0], "ic_alto": ci.loc["x", 1], "n": len(df)})
    for k in cols[1:]:
        print(f"  {k:8s} {pct(m.params[k]):+6.1f}%  [{pct(ci.loc[k,0]):+6.1f}%; {pct(ci.loc[k,1]):+6.1f}%]")
        linhas.append({"modelo": nome, "termo": k, "coef": m.params[k], "ic_baixo": ci.loc[k, 0], "ic_alto": ci.loc[k, 1], "n": len(df)})
m = sm.OLS(sem.y, sm.add_constant(sem[["x", "Baixada", "Resto"]])).fit()
pr = m.get_prediction(np.array([[1, cap.x, 0, 1]])).summary_frame(alpha=0.05).iloc[0]
print(f"\nCapital 2023: real R$ {cap.gasto_hab:.0f}; previsto R$ {np.exp(pr['mean']):.0f}, intervalo de previsão 95% [R$ {np.exp(pr['obs_ci_lower']):.0f}; R$ {np.exp(pr['obs_ci_upper']):.0f}]; real em relação ao previsto {pct(np.log(cap.gasto_hab) - pr['mean']):+.1f}%")
sem2 = sem.copy()
sem2["res"] = pct(m.resid)
print("Mediana do resíduo por grupo (%):\n", sem2.groupby("grupo").res.median().round(0).sort_values().to_string())
mm = sem[~sem.ente.isin(["Niterói", "Maricá", "Saquarema"])]
m2 = sm.OLS(mm.y, sm.add_constant(mm[["x", "Baixada", "Resto"]])).fit(cov_type="HC3")
ci = m2.conf_int(0.05)
print(f"\nSem Niterói, Maricá, Saquarema (n={len(mm)}): elasticidade {m2.params['x']:.3f} [{ci.loc['x',0]:.3f}; {ci.loc['x',1]:.3f}]; Resto {pct(m2.params['Resto']):+.1f}% [{pct(ci.loc['Resto',0]):+.1f}%; {pct(ci.loc['Resto',1]):+.1f}%]")
pd.DataFrame(linhas).to_csv(c.RAIZ / "dados_tratados" / "analyze_a5_coeficientes.csv", index=False, encoding="utf-8-sig")
