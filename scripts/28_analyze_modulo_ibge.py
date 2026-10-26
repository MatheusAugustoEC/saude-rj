"""Módulo IBGE (D2): idade (65 anos ou mais) e saneamento (esgoto ligado à rede), Censo 2022, no modelo do Analyze. Hipóteses M1 a M5 em docs/09.

Uso: python -X utf8 scripts/28_analyze_modulo_ibge.py
Entrada: dados_brutos/ibge_idade_censo2022_10157.json e ibge_esgoto_censo2022_6805.json (IBGE, SIDRA); indicadores de 2024 e de 2023.
Saída: dados_tratados/analyze_ibge_indicadores.csv e analyze_ibge_coeficientes.csv.
Os percentuais entram divididos por 10, então o coeficiente é o efeito de +10 pontos percentuais; vira % com exp(10*b)-1 sobre o log do gasto.
"""
import json
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

import _mapa_comum as c

warnings.filterwarnings("ignore")
BR, TR = c.RAIZ / "dados_brutos", c.RAIZ / "dados_tratados"
pct = lambda b: (np.exp(b) - 1) * 100


def serie(arquivo):
    r = json.load(open(BR / arquivo, encoding="utf-8"))[0]["resultados"]
    out = {}
    for res in r:
        cat = list(res["classificacoes"][-1]["categoria"])[0]
        out[cat] = {s["localidade"]["id"]: float(s["serie"]["2022"]) for s in res["series"] if s["serie"]["2022"] not in ("-", "...", "X")}
    return out


idade = serie("ibge_idade_censo2022_10157.json")
esgoto = serie("ibge_esgoto_censo2022_6805.json")
ibge = pd.DataFrame({"pop": pd.Series(idade["95253"]),
                     "p65": pd.Series({k: sum(idade[g].get(k, np.nan) for g in ("1153", "1154", "1155", "2503")) for k in idade["95253"]}),
                     "dom": pd.Series(esgoto["46292"]), "dom_rede": pd.Series(esgoto["46290"])})
ibge["idoso10"] = ibge.p65 / ibge["pop"] * 10     # percentual de 65 anos ou mais, dividido por 10
ibge["esgoto10"] = ibge.dom_rede / ibge.dom * 10  # percentual de domicílios com esgoto ligado à rede, dividido por 10
assert len(ibge) == 92 and ibge[["idoso10", "esgoto10"]].notna().all().all()

mun, _, _ = c.carrega_dados()
t24 = mun[["cod_ibge", "ente", "grupo", "regiao8", "populacao", "saude", "receita"]].copy()
t23 = pd.read_csv(TR / "indicadores_2023_replicacao.csv", dtype={"cod_ibge": str})[["cod_ibge", "ente", "grupo", "regiao8", "pop2023", "saude", "receita"]].rename(columns={"pop2023": "populacao"})


def prepara(t):
    t = t.join(ibge[["idoso10", "esgoto10"]], on="cod_ibge")
    t["y"] = np.log(t.saude / t.populacao)
    t["x"] = np.log(t.receita / t.populacao)
    t["Baixada"] = (t.grupo == c.BAIXADA).astype(float)
    t["Resto"] = (t.grupo == c.RESTO).astype(float)
    return t


t24, t23 = prepara(t24), prepara(t23)
pd.concat([t24.assign(ano=2024), t23.assign(ano=2023)])[["ano", "cod_ibge", "ente", "grupo", "idoso10", "esgoto10"]].to_csv(TR / "analyze_ibge_indicadores.csv", index=False, encoding="utf-8-sig")
print("mediana por grupo (% 65+ | % esgoto ligado à rede):")
print(pd.DataFrame({"idosos %": t24.groupby("grupo").idoso10.median() * 10, "esgoto %": t24.groupby("grupo").esgoto10.median() * 10, "n": t24.groupby("grupo").size()}).round(1).sort_values("esgoto %").to_string())
print("extremos de esgoto:", t24.sort_values("esgoto10")[["ente", "esgoto10"]].assign(esgoto10=lambda d: (d.esgoto10 * 10).round(1)).head(4).values.tolist(), "...", t24.sort_values("esgoto10")[["ente", "esgoto10"]].assign(esgoto10=lambda d: (d.esgoto10 * 10).round(1)).tail(3).values.tolist())
print("extremos de idosos:", t24.sort_values("idoso10")[["ente", "idoso10"]].assign(idoso10=lambda d: (d.idoso10 * 10).round(1)).head(3).values.tolist(), "...", t24.sort_values("idoso10")[["ente", "idoso10"]].assign(idoso10=lambda d: (d.idoso10 * 10).round(1)).tail(3).values.tolist())

linhas = []


def ajusta(df, cols):
    return sm.OLS(df.y, sm.add_constant(df[cols])).fit(cov_type="HC3")


def mostra(ano, nome, m, cols):
    ci = m.conf_int(0.05)
    print(f"  {nome} (n={int(m.nobs)}, R2={m.rsquared:.3f})")
    for k in cols:
        if k == "x":
            print(f"    elasticidade da receita {m.params[k]:.3f} [{ci.loc[k,0]:.3f}; {ci.loc[k,1]:.3f}]")
        elif k in ("idoso10", "esgoto10"):
            print(f"    {k:9s} (+10 pp): {pct(m.params[k]):+6.1f}%  [{pct(ci.loc[k,0]):+6.1f}%; {pct(ci.loc[k,1]):+6.1f}%]")
        else:
            print(f"    {k:9s}: {pct(m.params[k]):+6.1f}%  [{pct(ci.loc[k,0]):+6.1f}%; {pct(ci.loc[k,1]):+6.1f}%]")
        linhas.append({"ano": ano, "modelo": nome, "termo": k, "coef": m.params[k], "ic_baixo": ci.loc[k, 0], "ic_alto": ci.loc[k, 1], "r2": m.rsquared, "n": int(m.nobs)})


for ano, t in ((2024, t24), (2023, t23)):
    sem = t[t.grupo != c.CAPITAL]
    cap = t[t.grupo == c.CAPITAL].iloc[0]
    print(f"\n=== {ano}: {len(sem)} cidades sem a capital ===")
    base = ["x", "Baixada", "Resto"]
    for nome, cols in (("0 base (receita + grupos)", base), ("A + idosos", base + ["idoso10"]), ("B + esgoto", base + ["esgoto10"]), ("C + idosos + esgoto", base + ["idoso10", "esgoto10"])):
        mostra(ano, nome, ajusta(sem, cols), cols)
    mc = ajusta(sem, base + ["idoso10", "esgoto10"])
    m0 = ajusta(sem, base)
    print(f"  M3: efeito do Resto da Metropolitana, base {pct(m0.params['Resto']):+.1f}% -> com idade e saneamento {pct(mc.params['Resto']):+.1f}% (mudança de {pct(mc.params['Resto']) - pct(m0.params['Resto']):+.1f} pontos percentuais)")
    X = sm.add_constant(sem[base + ["idoso10", "esgoto10"]]).values
    vif = {n: variance_inflation_factor(X, i) for i, n in enumerate(["const"] + base + ["idoso10", "esgoto10"]) if n != "const"}
    print("  VIF:", {k: round(v, 2) for k, v in vif.items()})
    print("  correlação (Pearson) entre receita, idosos, esgoto:", sem[["x", "idoso10", "esgoto10"]].corr().round(2).values.tolist())
    for v in ("idoso10", "esgoto10"):
        rho = stats.spearmanr(sem[v], sem.y)
        print(f"  Spearman {v} x ln(gasto/hab): {rho[0]:+.2f} (p={rho[1]:.3f})")
    # capital prevista pelo modelo C
    cols = base + ["idoso10", "esgoto10"]
    m = sm.OLS(sem.y, sm.add_constant(sem[cols])).fit()
    x0 = np.array([[1, cap.x, 0, 1, cap.idoso10, cap.esgoto10]])
    pr = m.get_prediction(x0).summary_frame(alpha=0.05).iloc[0]
    print(f"  Capital pelo modelo C: real R$ {np.exp(cap.y):.0f}; previsto R$ {np.exp(pr['mean']):.0f} [R$ {np.exp(pr['obs_ci_lower']):.0f}; R$ {np.exp(pr['obs_ci_upper']):.0f}]; {pct(cap.y - pr['mean']):+.1f}%; fora do intervalo: {cap.y < pr['obs_ci_lower']}")
    print(f"  Capital: {cap.idoso10*10:.1f}% de idosos; {cap.esgoto10*10:.1f}% com esgoto ligado à rede")
    sem2 = sem.copy()
    sem2["res"] = pct(mc.resid)
    print("  resíduo mediano do modelo C por grupo (%):", sem2.groupby("grupo").res.median().round(0).sort_values().to_dict())

pd.DataFrame(linhas).to_csv(TR / "analyze_ibge_coeficientes.csv", index=False, encoding="utf-8-sig")
