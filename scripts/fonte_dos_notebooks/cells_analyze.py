"""Células do notebook do Analyze (03_analyze_gasto_saude.ipynb). Montado por build_analyze.py."""
CELULAS = []


def md(t):
    CELULAS.append(("md", t.strip("\n")))


def code(t):
    CELULAS.append(("code", t.strip("\n")))


md("""
# Analyze: o que explica o gasto baixo em saúde por habitante?

**Projeto:** Saúde fiscal do Rio de Janeiro (Siconfi 2024, replicação em 2023). **Fase:** 3 · Analyze. **Notebooks anteriores:** `01_eda_siconfi_2024.ipynb`, `02_measure_qualidade_e_baseline.ipynb`.

**Pergunta central:** o gasto baixo em saúde por habitante da Região Metropolitana se explica pela receita por habitante?

**Como ler.** Hipóteses e critérios estão em `docs/09-analyze-hipoteses.md` (escritas antes dos modelos; a falha de ordem do A1 está declarada lá). Cada método (o que é, por que foi escolhido, como foi feito) está em `docs/10-metodos-estatisticos.md`. Todos os números abaixo são calculados a partir dos dados, e a última seção **confere cada número do relatório** (`fases/fase-3-analyze/relatorio.md`) contra esta execução.

**Ressalvas gerais.** Dados declarados pelos entes, não auditados. Gasto em saúde por habitante não mede qualidade. O gasto é empenhado, não pago.

**Roteiro.** 1. Preparação · 2. A1: decomposição · 3. A2: modelo · 4. Capital · 5. A2b: sensibilidade · 6. A5: replicação em 2023 · 7. H6: receita própria · 8. H7: uso ocasional · 9. H8: SIOPS · 10. Conferência com o relatório.
""")

md("""
## 1. Preparação

Usa o agrupamento do projeto (capital; Baixada, núcleo de 6; resto da Metropolitana; e as 7 outras regiões do CEPERJ), definido em `scripts/_mapa_comum.py`. A capital fica **fora** dos modelos de grupo (uma variável para uma cidade só decora a cidade) e é prevista de fora.
""")

code(r"""
import json, sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

warnings.filterwarnings("ignore")
PROJETO = Path.cwd().parent
sys.path.insert(0, str(PROJETO / "scripts"))
import _mapa_comum as c

BR, TR = PROJETO / "dados_brutos", PROJETO / "dados_tratados"
pct = lambda b: (np.exp(b) - 1) * 100

mun, _, _ = c.carrega_dados()
t = mun[["cod_ibge", "ente", "grupo", "regiao8", "populacao", "saude", "receita"]].copy()
t["gasto_hab"] = t.saude / t.populacao
t["receita_hab"] = t.receita / t.populacao
t["fatia"] = t.saude / t.receita
t["y"] = np.log(t.gasto_hab)
t["x"] = np.log(t.receita_hab)
t["Baixada"] = (t.grupo == c.BAIXADA).astype(float)
t["Resto"] = (t.grupo == c.RESTO).astype(float)
sem = t[t.grupo != c.CAPITAL].copy()
cap = t[t.grupo == c.CAPITAL].iloc[0]
print(len(t), "municípios;", len(sem), "sem a capital")
print(t.grupo.value_counts().to_dict())

def ajusta(df, cols, peso=None):
    X = sm.add_constant(df[cols])
    m = sm.WLS(df.y, X, weights=peso) if peso is not None else sm.OLS(df.y, X)
    return m.fit(cov_type="HC3")

def mostra(nome, m, cols):
    ci = m.conf_int(0.05)
    print(f"{nome} (n={int(m.nobs)}, R2={m.rsquared:.3f})")
    for k in cols:
        if k in ("x", "x_total", "x_propria", "x_transf", "x_oc"):
            print(f"  {k:10s} elasticidade {m.params[k]:.3f}  IC95 [{ci.loc[k,0]:.3f}; {ci.loc[k,1]:.3f}]")
        else:
            print(f"  {k:10s} {pct(m.params[k]):+6.1f}%  IC95 [{pct(ci.loc[k,0]):+6.1f}%; {pct(ci.loc[k,1]):+6.1f}%]")
""")

md("""
## 2. A1: decomposição exata

**Identidade:** gasto por habitante = receita por habitante × fatia (saúde ÷ receita). **Log:** transforma o produto em soma, então o desvio do gasto em relação à referência é a soma do desvio da receita e do desvio da fatia, sem sobra. **Referência:** média geométrica das 92 cidades (a mediana não se decompõe em produto). Cada cidade pesa 1. Detalhes em `docs/10`, seção A1.
""")

code(r"""
d = t.copy()
for k in ("gasto_hab", "receita_hab", "fatia"):
    d["ln_" + k] = np.log(d[k])
    d["dev_" + k] = d["ln_" + k] - d["ln_" + k].mean()
assert np.allclose(d.dev_gasto_hab, d.dev_receita_hab + d.dev_fatia)
ref = {k: float(np.exp(d["ln_" + k].mean())) for k in ("gasto_hab", "receita_hab", "fatia")}
print("referência (média geométrica):", {k: round(v, 3) for k, v in ref.items()})
print("correlação (log) gasto x receita:", round(np.corrcoef(d.ln_gasto_hab, d.ln_receita_hab)[0, 1], 2),
      "| gasto x fatia:", round(np.corrcoef(d.ln_gasto_hab, d.ln_fatia)[0, 1], 2))
g = d.groupby("grupo")[["dev_gasto_hab", "dev_receita_hab", "dev_fatia"]].median().apply(lambda s: (np.exp(s) - 1) * 100)
g["n"] = d.groupby("grupo").size()
print(g.sort_values("dev_gasto_hab").round(0).to_string())
print(f"Capital: gasto {cap.gasto_hab:.0f}, receita {cap.receita_hab:.0f}, fatia {cap.fatia*100:.1f}%; mediana da fatia nas 92: {t.fatia.median()*100:.1f}%")
""")

md("""
## 3. A2: modelo em log nas 92 cidades (91 nos modelos de grupo)

**Modelo:** ln(gasto por habitante) = a + b · ln(receita por habitante) + efeito do grupo. O coeficiente b é uma **elasticidade** (se a receita sobe 10%, o gasto sobe b × 10%). Efeitos de grupo viram porcentagem com exp(coef) − 1. **Erros robustos HC3** (variância desigual; poucas regiões inviabilizam o agrupamento por região). **Margem de relevância:** ±10% (escolha de julgamento, fixada antes). **Intervalo:** 95%.
""")

code(r"""
M1 = ajusta(t, ["x"]);                       mostra("M1 só receita (92)", M1, ["x"])
M2 = ajusta(sem, ["x"]);                     mostra("M2 só receita, sem a capital", M2, ["x"])
M3 = ajusta(sem, ["x", "Baixada", "Resto"]); mostra("M3 receita + grupos, sem a capital", M3, ["x", "Baixada", "Resto"])
M4 = ajusta(sem, ["x", "Baixada", "Resto"], sem.populacao); mostra("M4 ponderado por população, sem a capital", M4, ["x", "Baixada", "Resto"])
""")

md("""
**Conferência por bootstrap das cidades** (2.000 sorteios com reposição; semente fixa). Não depende de fórmula; se concorda com o HC3, o intervalo é confiável.
""")

code(r"""
rng = np.random.default_rng(2024)
cols = ["x", "Baixada", "Resto"]
out = []
for _ in range(2000):
    s = sem.iloc[rng.integers(0, len(sem), len(sem))]
    out.append(sm.OLS(s.y, sm.add_constant(s[cols])).fit().params[cols].values)
b = pd.DataFrame(out, columns=cols).quantile([0.025, 0.975])
print("bootstrap, elasticidade:", b.x.round(3).tolist(), "| Baixada %:", pct(b.Baixada).round(1).tolist(), "| Resto %:", pct(b.Resto).round(1).tolist())
""")

md("""
**Diagnóstico dos resíduos.** Shapiro-Wilk (normalidade) e Breusch-Pagan (variância constante): p alto significa que não há evidência contra o modelo (não prova que ele está certo). Distância de Cook: quanto uma cidade sozinha mexe no modelo; alerta em 4/n.
""")

code(r"""
res = M3.resid
print(f"Shapiro-Wilk p={stats.shapiro(res)[1]:.3f}; Breusch-Pagan p={sm.stats.diagnostic.het_breuschpagan(res, M3.model.exog)[1]:.3f}")
infl = sm.OLS(sem.y, sm.add_constant(sem[cols])).fit().get_influence()
sem["cook"] = infl.cooks_distance[0]
corte = 4 / len(sem)
alto = sem[sem.cook > corte].sort_values("cook", ascending=False)
print(f"corte 4/n = {corte:.3f}; acima:", alto[["ente", "cook"]].round(3).values.tolist())
""")

md("""
## 4. A capital, prevista de fora

Ajusta-se o modelo nas outras 91 cidades e **prevê-se** a capital (tratada como "resto da Metropolitana", sua região no CEPERJ), com **intervalo de previsão** de 95%. Se o gasto real cai fora do intervalo, a capital gasta menos do que a receita dela sugere.
""")

code(r"""
def prever_capital(df_sem, cols, linha, y_real):
    m = sm.OLS(df_sem.y, sm.add_constant(df_sem[cols])).fit()
    pr = m.get_prediction(np.array([linha])).summary_frame(alpha=0.05).iloc[0]
    return np.exp(pr["mean"]), np.exp(pr["obs_ci_lower"]), np.exp(pr["obs_ci_upper"]), pct(y_real - pr["mean"])

for nome, cols_, linha in (("M2 (só receita)", ["x"], [1, cap.x]), ("M3 (receita + grupos)", ["x", "Baixada", "Resto"], [1, cap.x, 0, 1])):
    prev, lo, hi, dif = prever_capital(sem, cols_, linha, cap.y)
    print(f"{nome}: real R$ {cap.gasto_hab:.0f}; previsto R$ {prev:.0f} [R$ {lo:.0f}; R$ {hi:.0f}]; real em relação ao previsto {dif:+.1f}%; fora do intervalo: {cap.gasto_hab < lo}")
cap_m2, cap_m3 = prever_capital(sem, ["x"], [1, cap.x], cap.y)[3], prever_capital(sem, ["x", "Baixada", "Resto"], [1, cap.x, 0, 1], cap.y)[3]
""")

md("""
## 5. A2b: sensibilidade às cidades de maior influência

Refaz o modelo sem as cidades com distância de Cook acima de 4/n (regra fixada antes) e sem as três de receita mais extrema (Niterói, Maricá, Saquarema). Não é "tirar outlier para melhorar o resultado": a conferência DCA × RREO fecha para elas; a pergunta é só se a conclusão resiste.
""")

code(r"""
sens = {}
for nome, df in (("todas as 91", sem), ("sem as de Cook alto", sem[~sem.ente.isin(alto.ente)]),
                 ("sem Niterói, Maricá, Saquarema", sem[~sem.ente.isin(["Niterói", "Maricá", "Saquarema"])])):
    m = ajusta(df, cols)
    sens[nome] = m
    mostra(nome, m, cols)
""")

md("""
## 6. A5: replicação em 2023

Mesmas definições, dados coletados no Siconfi (`scripts/22`) e processados em `scripts/23` (`dados_tratados/indicadores_2023_replicacao.csv`). **População de 2023:** o IBGE não publicou estimativa municipal; usa-se a média geométrica entre o Censo 2022 e a estimativa de 2024. **Carmo fora:** entregou o RREO só até o 5º bimestre. **Limite:** são as mesmas cidades; os dois anos não são amostras independentes.
""")

code(r"""
r23 = pd.read_csv(TR / "indicadores_2023_replicacao.csv", dtype={"cod_ibge": str})
r23["y"] = np.log(r23.gasto_hab); r23["x"] = np.log(r23.receita_hab)
r23["Baixada"] = (r23.grupo == c.BAIXADA).astype(float); r23["Resto"] = (r23.grupo == c.RESTO).astype(float)
s23 = r23[r23.grupo != c.CAPITAL]; cap23 = r23[r23.grupo == c.CAPITAL].iloc[0]
print(len(r23), "cidades;", len(s23), "sem a capital")
R1 = ajusta(r23, ["x"]);                       mostra("2023, M1 só receita", R1, ["x"])
R3 = ajusta(s23, ["x", "Baixada", "Resto"]);   mostra("2023, M3 receita + grupos, sem a capital", R3, ["x", "Baixada", "Resto"])
prev, lo, hi, dif = prever_capital(s23, ["x", "Baixada", "Resto"], [1, cap23.x, 0, 1], cap23.y)
print(f"capital 2023: real R$ {cap23.gasto_hab:.0f}; previsto R$ {prev:.0f} [R$ {lo:.0f}; R$ {hi:.0f}]; {dif:+.1f}%")
menores = r23.sort_values("gasto_hab").head(10)
n_metro_23 = int((menores.regiao8 == "Metropolitana").sum())
print("dos 10 que menos gastam em 2023, na Metropolitana:", n_metro_23, "|", menores.ente.tolist())
n_metro_24 = int((t.sort_values("gasto_hab").head(10).regiao8 == "Metropolitana").sum())
print("em 2024:", n_metro_24)
""")

md("""
## 7. H6: receita própria contra transferências

**Receita própria** = receita (exceto intra-orçamentárias) menos transferências correntes e de capital, do RREO Anexo 01. **Limites:** os repasses do SUS e os royalties entram em transferências, sem separar; a "própria" é o que sobra e inclui rendimentos financeiros. A receita total do RREO bate com a `receita` do projeto.
""")

code(r"""
def receitas(arquivo):
    r = pd.read_csv(BR / arquivo, dtype={"cod_ibge": str}, low_memory=False)
    r = r[(r.anexo == "RREO-Anexo 01") & (r.coluna == "Até o Bimestre (c)")]
    p = r.pivot_table(index="cod_ibge", columns="cod_conta", values="valor", aggfunc="first")
    o = pd.DataFrame({"total": p["ReceitasExcetoIntraOrcamentarias"], "tc": p["TransferenciasCorrentes"], "tk": p["TransferenciasDeCapital"].fillna(0)})
    o["transf"] = o.tc + o.tk
    o["propria"] = o.total - o.transf
    return o

def junta_receitas(df, arq, pop):
    o = receitas(arq)
    df = df.join(o[["total", "transf", "propria"]], on="cod_ibge")
    df["x_total"] = np.log(df.receita / pop); df["x_propria"] = np.log(df.propria / pop); df["x_transf"] = np.log(df.transf / pop)
    df["parte_propria"] = df.propria / df.receita
    return df

t = junta_receitas(t, "siconfi_rreo_2024.csv", t.populacao)
print("diferença máxima entre a receita do projeto e o RREO total:", float((t.receita / t.total - 1).abs().max()))
r23 = junta_receitas(r23, "siconfi_rreo_anexo01_2023.csv", r23.pop2023)
sem = t[t.grupo != c.CAPITAL].copy(); cap = t[t.grupo == c.CAPITAL].iloc[0]
s23 = r23[r23.grupo != c.CAPITAL].copy(); cap23 = r23[r23.grupo == c.CAPITAL].iloc[0]
prop = {}
for ano, df in ((2024, sem), (2023, s23)):
    print(f"--- {ano}")
    for nome, cs in (("A total", ["x_total"]), ("B própria", ["x_propria"]), ("C própria + transferências", ["x_propria", "x_transf"])):
        m = ajusta(df, cs); prop[(ano, nome)] = m; mostra(nome, m, cs)
    mb = sm.OLS(df.y, sm.add_constant(df[["x_propria"]])).fit()
    capx = (cap if ano == 2024 else cap23)
    pr = mb.get_prediction(np.array([[1, capx.x_propria]])).summary_frame(alpha=0.05).iloc[0]
    prop[(ano, "capital")] = pct(capx.y - pr["mean"])
    print(f"capital contra a receita própria: real R$ {np.exp(capx.y):.0f}; previsto R$ {np.exp(pr['mean']):.0f} [R$ {np.exp(pr['obs_ci_lower']):.0f}; R$ {np.exp(pr['obs_ci_upper']):.0f}]; {prop[(ano, 'capital')]:+.1f}%")
print("parte da receita que é própria (mediana por grupo, %):", (t.groupby("grupo").parte_propria.median() * 100).round(0).sort_values().to_dict())
""")

md("""
## 8. H7: domicílios de uso ocasional (Censo 2022)

**Variável:** domicílios particulares permanentes não ocupados **de uso ocasional** por 100 moradores (IBGE, Censo 2022, tabela 9866; moradores do Censo 2022, tabela 4714). **Spearman:** correlação de postos, que não é puxada por valores extremos. **No modelo:** `ln(1 + x)` para não zerar a cidade sem nenhum. **Limite:** o Censo é de 2022, o gasto de 2024; correlação não é causa.
""")

code(r"""
oc = json.load(open(BR / "ibge_domicilios_uso_ocasional_9866.json", encoding="utf-8"))[0]["resultados"][0]["series"]
oc = {s["localidade"]["id"]: float(s["serie"]["2022"]) if s["serie"]["2022"] not in ("-", "...", "X") else 0.0 for s in oc}
censo = {l["D1C"]: float(l["V"]) for l in json.load(open(BR / "ibge_populacao_censo2022_4714.json", encoding="utf-8"))["censo2022_mun"][1:] if l["V"] not in ("-", "...", "X")}
t["ocas_100"] = t.cod_ibge.map(oc) / t.cod_ibge.map(censo) * 100
assert t.ocas_100.notna().all()
sem = t[t.grupo != c.CAPITAL].copy()
print("mediana por grupo:", t.groupby("grupo").ocas_100.median().round(1).sort_values(ascending=False).to_dict())
rho = {}
for v in ("receita_hab", "fatia", "gasto_hab"):
    rho[v] = stats.spearmanr(sem.ocas_100, sem[v])
    print(f"Spearman uso ocasional x {v}: {rho[v][0]:+.2f} (p={rho[v][1]:.3f})")
sem["x_oc"] = np.log1p(sem.ocas_100)
m_sem = ajusta(sem, ["x", "Baixada", "Resto"]); m_com = ajusta(sem, ["x", "x_oc", "Baixada", "Resto"])
sem["res_sem"], sem["res_com"] = pct(m_sem.resid), pct(m_com.resid)
mostra("com uso ocasional", m_com, ["x", "x_oc", "Baixada", "Resto"])
gr = sem.groupby("grupo")[["res_sem", "res_com"]].median().round(0)
print(gr.sort_values("res_sem").to_string())
""")

md("""
## 9. H8: SIOPS (percentual aplicado em saúde contra o mínimo de 15%)

**Fonte:** arquivo LCL141 do SIOPS (2024), dado declarado. **Parte aplicada:** valor aplicado (SIOPS) ÷ gasto em saúde do Siconfi. **Limite:** bases diferentes (o SIOPS conta só recursos próprios dentro das regras da LC 141), então a razão é ordem de grandeza.
""")

code(r"""
s = pd.read_excel(BR / "LCL141.xlsx")
s = s[s.UF == "RJ"].copy()
s["aplicado_pct"] = s["Aplicado em ASPS"].map(lambda v: float(str(v).replace("%", "").replace(",", ".").strip()))
s["chave"] = s.Ente.map(c.norma); t["chave"] = t.ente.map(c.norma)
j = t.merge(s[["chave", "aplicado_pct", "Valor Aplicado"]], on="chave", how="left")
print("casadas por nome:", int(j.aplicado_pct.notna().sum()), "de", len(j))
j["parte_aplicada"] = j["Valor Aplicado"] / j.saude * 100
menos = j.sort_values("gasto_hab").head(10)
sio = dict(acima15=int((j.aplicado_pct >= 15).sum()), mediana=j.aplicado_pct.median(), menos10=menos.aplicado_pct.median(),
           parte=j.parte_aplicada.median(), rho=stats.spearmanr(j.aplicado_pct, j.gasto_hab))
print(f"acima de 15%: {sio['acima15']} de {len(j)}; mediana {sio['mediana']:.1f}%; menor {j.aplicado_pct.min():.1f}% ({j.loc[j.aplicado_pct.idxmin(), 'ente']})")
print(f"as 10 que menos gastam: mediana {sio['menos10']:.1f}%; Spearman aplicado x gasto/hab: {sio['rho'][0]:+.2f} (p={sio['rho'][1]:.3f})")
print(f"parte do gasto coberta pelos recursos próprios do SIOPS: mediana {sio['parte']:.0f}%;",
      j.groupby("grupo").parte_aplicada.median().round(0)[[c.BAIXADA, c.CAPITAL]].to_dict())
""")

md("""
## 10. Conferência com o relatório

Cada número do relatório `fases/fase-3-analyze/relatorio.md` é comparado com esta execução (tolerância de arredondamento). Se alguma conferência falhar, o relatório precisa ser corrigido, e a célula para.
""")

code(r"""
def ok(nome, obtido, esperado, tol):
    assert abs(obtido - esperado) <= tol, f"{nome}: relatório diz {esperado}, notebook deu {obtido:.3f}"
    print(f"OK  {nome}: {obtido:.3f} (relatório {esperado})")

ci3 = M3.conf_int(0.05); ci4 = M4.conf_int(0.05); ci1 = M1.conf_int(0.05)
ok("referência gasto/hab", ref["gasto_hab"], 2322, 1); ok("referência receita/hab", ref["receita_hab"], 7983, 1); ok("referência fatia (%)", ref["fatia"] * 100, 29.1, 0.06)
ok("correlação gasto x receita", np.corrcoef(d.ln_gasto_hab, d.ln_receita_hab)[0, 1], 0.89, 0.006)
ok("correlação gasto x fatia", np.corrcoef(d.ln_gasto_hab, d.ln_fatia)[0, 1], 0.04, 0.006)
ok("capital: fatia (%)", cap.fatia * 100, 19.6, 0.06); ok("mediana da fatia (%)", t.fatia.median() * 100, 29.2, 0.06)
ok("M1 elasticidade", M1.params["x"], 0.81, 0.006); ok("M1 IC baixo", ci1.loc["x", 0], 0.72, 0.006); ok("M1 IC alto", ci1.loc["x", 1], 0.90, 0.006)
ok("M3 Resto (%)", pct(M3.params["Resto"]), -4.4, 0.06); ok("M3 Resto IC baixo", pct(ci3.loc["Resto", 0]), -18, 0.2); ok("M3 Resto IC alto", pct(ci3.loc["Resto", 1]), 11.5, 0.06)
ok("M3 Baixada (%)", pct(M3.params["Baixada"]), -3.5, 0.06)
ok("M4 Baixada (%)", pct(M4.params["Baixada"]), -8.2, 0.06); ok("M4 Baixada IC baixo", pct(ci4.loc["Baixada", 0]), -32.5, 0.06); ok("M4 Baixada IC alto", pct(ci4.loc["Baixada", 1]), 24.8, 0.06)
ok("capital vs previsto M2 (%)", cap_m2, -37.0, 0.06); ok("capital vs previsto M3 (%)", cap_m3, -35.0, 0.06)
ok("sensibilidade sem 6, elasticidade", sens["sem as de Cook alto"].params["x"], 0.86, 0.006)
ok("sensibilidade sem 3, elasticidade", sens["sem Niterói, Maricá, Saquarema"].params["x"], 0.89, 0.006)
ok("sensibilidade sem 3, IC alto", sens["sem Niterói, Maricá, Saquarema"].conf_int(0.05).loc["x", 1], 0.996, 0.0006)
ok("sensibilidade sem 6, Resto (%)", pct(sens["sem as de Cook alto"].params["Resto"]), 1.2, 0.06)
ok("sensibilidade sem 3, Resto (%)", pct(sens["sem Niterói, Maricá, Saquarema"].params["Resto"]), 6.6, 0.06)
ok("2023 M1 elasticidade", R1.params["x"], 0.80, 0.006); ok("2023 M3 Resto (%)", pct(R3.params["Resto"]), -6.8, 0.06); ok("2023 M3 Baixada (%)", pct(R3.params["Baixada"]), -7.9, 0.06)
ok("2023 capital vs previsto (%)", dif, -32.7, 0.06); ok("2023 dos 10 na Metropolitana", n_metro_23, 9, 0); ok("2024 dos 10 na Metropolitana", n_metro_24, 8, 0)
ok("própria R2", prop[(2024, "B própria")].rsquared, 0.35, 0.006); ok("própria elasticidade", prop[(2024, "B própria")].params["x_propria"], 0.45, 0.006)
ok("total R2", prop[(2024, "A total")].rsquared, 0.80, 0.006)
ok("própria+transf: transferências", prop[(2024, "C própria + transferências")].params["x_transf"], 0.68, 0.006)
ok("própria+transf: própria", prop[(2024, "C própria + transferências")].params["x_propria"], 0.12, 0.006)
ok("capital vs própria 2024 (%)", prop[(2024, "capital")], -66.8, 0.06); ok("capital vs própria 2023 (%)", prop[(2023, "capital")], -65.5, 0.06)
ok("parte própria da capital (%)", t[t.grupo == c.CAPITAL].parte_propria.iloc[0] * 100, 66, 0.6)
ok("Spearman ocasional x receita", rho["receita_hab"][0], 0.51, 0.006); ok("Spearman ocasional x fatia", rho["fatia"][0], -0.44, 0.006)
ok("resíduo Baixadas Litorâneas sem", gr.loc["Baixadas Litorâneas", "res_sem"], -15, 0.6); ok("resíduo Baixadas Litorâneas com", gr.loc["Baixadas Litorâneas", "res_com"], -9, 0.6)
ok("SIOPS: acima de 15%", sio["acima15"], 92, 0); ok("SIOPS: mediana (%)", sio["mediana"], 23.3, 0.06); ok("SIOPS: 10 que menos gastam (%)", sio["menos10"], 20.9, 0.06)
ok("SIOPS: Spearman aplicado x gasto", sio["rho"][0], 0.15, 0.006); ok("SIOPS: parte aplicada (%)", sio["parte"], 37, 0.6)
print("\nTodas as conferências com o relatório passaram.")
""")

md("""
## 11. Registro

| Item | Onde |
|---|---|
| Hipóteses e critérios (A0) | `docs/09-analyze-hipoteses.md` |
| Métodos (o que, por que, como) | `docs/10-metodos-estatisticos.md` |
| Relatório da fase | `fases/fase-3-analyze/relatorio.md` |
| Scripts (a mesma lógica, fora do notebook) | `scripts/19` a `scripts/24` |
| Curiosidades por uso | `docs/08-banco-de-curiosidades.md` |

**Não feito nesta fase:** gráficos finais (ficam para a página de entrega); royalties por município (ANP) e atividade econômica (extensão futura).
""")
