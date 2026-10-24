"""Analyze A2: modelo em log nas 92 cidades (hipóteses H1, H2, H3 e H5 de docs/09-analyze-hipoteses.md).

Uso: python -X utf8 scripts/20_analyze_a2_modelo.py
Grava dados_tratados/analyze_a2_coeficientes.csv e dados_tratados/analyze_a2_residuos.csv.

Modelo: ln(gasto/hab) = a + b*ln(receita/hab) + efeitos de grupo + erro.
Grupos: Baixada (núcleo de 6) e Resto da Metropolitana (15); referência = interior (as 7 outras regiões, 70 cidades).
A capital NÃO entra com variável própria: uma variável para uma só cidade absorve a cidade (resíduo zero, alavanca 1) e não testa nada.
Ela é estimada de fora: o modelo é ajustado nas outras 91 e prevê a capital, com intervalo de previsão.
Erros-padrão robustos HC3 (poucos grupos, cluster por região seria instável); intervalo de 95% por bootstrap das cidades como conferência.
"""
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
import _mapa_comum as c

warnings.filterwarnings("ignore")
rng = np.random.default_rng(2024)
mun, _, _ = c.carrega_dados()
d = mun[["cod_ibge", "ente", "grupo", "populacao", "saude", "receita"]].copy()
d["y"] = np.log(d.saude / d.populacao)
d["x"] = np.log(d.receita / d.populacao)
d["Capital"] = (d.grupo == c.CAPITAL).astype(float)
d["Baixada"] = (d.grupo == c.BAIXADA).astype(float)
d["Resto_Metropolitana"] = (d.grupo == c.RESTO).astype(float)
GR = ["Baixada", "Resto_Metropolitana"]
sem = d[d.Capital == 0]
pct = lambda b: (np.exp(b) - 1) * 100


def ajusta(df, cols, peso=None):
    X = sm.add_constant(df[cols])
    m = (sm.WLS(df.y, X, weights=peso) if peso is not None else sm.OLS(df.y, X)).fit(cov_type="HC3")
    return m


def boot(df, cols, peso_col=None, B=5000):
    out = []
    n = len(df)
    for _ in range(B):
        s = df.iloc[rng.integers(0, n, n)]
        try:
            m = ajusta(s, cols, s[peso_col] if peso_col else None) if peso_col else ajusta(s, cols)
            out.append(m.params.values)
        except Exception:
            pass
    return pd.DataFrame(out, columns=["const"] + cols).quantile([0.025, 0.975])


linhas = []
specs = [("M1 só receita (92)", d, ["x"], None),
         ("M2 só receita, sem a capital (91)", sem, ["x"], None),
         ("M3 receita + grupos, sem a capital (91)", sem, ["x"] + GR, None),
         ("M4 receita + grupos, ponderado por população, sem a capital (91)", sem, ["x"] + GR, "populacao")]
for nome, df, cols, pw in specs:
    m = ajusta(df, cols, df[pw] if pw else None)
    b = boot(df, cols, pw) if pw is None else None
    ci = m.conf_int(0.05)
    for k in cols:
        linhas.append({"modelo": nome, "termo": k, "coef": m.params[k], "ic95_baixo": ci.loc[k, 0], "ic95_alto": ci.loc[k, 1],
                       "boot_baixo": b.loc[0.025, k] if b is not None else np.nan, "boot_alto": b.loc[0.975, k] if b is not None else np.nan,
                       "n": int(m.nobs), "r2": m.rsquared})
    print(f"\n{nome} (n={int(m.nobs)}, R2={m.rsquared:.3f})")
    for k in cols:
        if k == "x":
            print(f"  elasticidade da receita: {m.params[k]:.3f}  IC95 [{ci.loc[k,0]:.3f}; {ci.loc[k,1]:.3f}]" + (f"  bootstrap [{b.loc[0.025,k]:.3f}; {b.loc[0.975,k]:.3f}]" if b is not None else ""))
        else:
            print(f"  {k:20s}: {pct(m.params[k]):+6.1f}%  IC95 [{pct(ci.loc[k,0]):+6.1f}%; {pct(ci.loc[k,1]):+6.1f}%]" + (f"  bootstrap [{pct(b.loc[0.025,k]):+6.1f}%; {pct(b.loc[0.975,k]):+6.1f}%]" if b is not None else ""))
pd.DataFrame(linhas).to_csv(c.RAIZ / "dados_tratados" / "analyze_a2_coeficientes.csv", index=False, encoding="utf-8-sig")

# capital: previsão fora da amostra (modelo ajustado nas 91, capital tratada como Resto_Metropolitana, sua região no CEPERJ)
cap = d[d.Capital == 1].iloc[0]
for nome, cols, linha in (("M2 (só receita)", ["x"], [1, cap.x]), ("M3 (receita + grupos)", ["x"] + GR, [1, cap.x, 0, 1])):
    m = sm.OLS(sem.y, sm.add_constant(sem[cols])).fit()
    pr = m.get_prediction(np.array([linha])).summary_frame(alpha=0.05).iloc[0]
    real = cap.y
    print(f"Capital contra {nome}: gasto/hab real R$ {np.exp(real):.0f}; previsto R$ {np.exp(pr['mean']):.0f}, intervalo de previsão 95% [R$ {np.exp(pr['obs_ci_lower']):.0f}; R$ {np.exp(pr['obs_ci_upper']):.0f}]; real em relação ao previsto {pct(real - pr['mean']):+.1f}%")

m3 = ajusta(sem, ["x"] + GR)
d["residuo_pct"] = pct(d.y - (m3.params["const"] + m3.params["x"] * d.x + m3.params["Baixada"] * d.Baixada + m3.params["Resto_Metropolitana"] * d.Resto_Metropolitana))
d[["cod_ibge", "ente", "grupo", "residuo_pct"]].to_csv(c.RAIZ / "dados_tratados" / "analyze_a2_residuos.csv", index=False, encoding="utf-8-sig")
print("Mediana do resíduo do M3 por grupo (%; a capital é previsão fora da amostra):")
print(d.groupby("grupo").residuo_pct.median().round(0).sort_values().to_string())

from scipy import stats
res = m3.resid
print(f"Diagnóstico M3: Shapiro-Wilk dos resíduos p={stats.shapiro(res)[1]:.3f}; Breusch-Pagan p={sm.stats.diagnostic.het_breuschpagan(res, m3.model.exog)[1]:.3f}")
infl = sm.OLS(sem.y, sm.add_constant(sem[["x"] + GR])).fit().get_influence()
cook = pd.Series(infl.cooks_distance[0], index=sem.ente.values)
print("Maiores distâncias de Cook (M3):", cook.sort_values(ascending=False).head(4).round(3).to_dict(), "| referência 4/n =", round(4 / len(sem), 3))

# H5 descrição: quartil de maior receita por habitante
d["receita_hab"] = np.exp(d.x)
d["fatia"] = d.saude / d.receita
q = d.sort_values("receita_hab", ascending=False).head(23)
print(f"Quartil de maior receita/hab (23): fatia mediana {q.fatia.median()*100:.1f}% contra {d.fatia.median()*100:.1f}% nas 92; corte de receita/hab R$ {q.receita_hab.min():.0f}")
