"""Improve: contas das recomendações R1 a R7. Critérios fixados antes de rodar em docs/13-improve-criterios.md.

Uso: python -X utf8 scripts/30_improve_recomendacoes.py
Entrada: indicadores de 2024 e 2023 (Measure e replicação), RREO Anexo 01 de 2023 e 2024, Censo 2022 (uso ocasional), SIOPS 2024 (LCL141.xlsx).
Saída: dados_tratados/improve_*.csv. Modelo da R1, R3 e R4: log do gasto por habitante contra log da receita por habitante e grupos (capital fora, prevista de fora), como no Analyze.
"""
import json
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.power import NormalIndPower

import _mapa_comum as c

warnings.filterwarnings("ignore")
BR, TR = c.RAIZ / "dados_brutos", c.RAIZ / "dados_tratados"
pct = lambda b: (np.exp(b) - 1) * 100
COLS = ["x", "Baixada", "Resto"]
INTERIOR_LIT = "Baixadas Litorâneas"
rng = np.random.default_rng(20261024)


def receitas(arquivo):
    r = pd.read_csv(BR / arquivo, dtype={"cod_ibge": str}, low_memory=False)
    r = r[(r.anexo == "RREO-Anexo 01") & (r.coluna == "Até o Bimestre (c)")]
    p = r.pivot_table(index="cod_ibge", columns="cod_conta", values="valor", aggfunc="first")
    out = pd.DataFrame({"total": p["ReceitasExcetoIntraOrcamentarias"], "transf": p["TransferenciasCorrentes"] + p["TransferenciasDeCapital"].fillna(0)})
    out["propria"] = out.total - out.transf
    out["periodo"] = r.groupby("cod_ibge").periodo.first()
    return out


def prepara(t):
    t = t.dropna(subset=["saude", "receita", "populacao"]).copy()
    t["y"] = np.log(t.saude / t.populacao)
    t["x"] = np.log(t.receita / t.populacao)
    t["Baixada"] = (t.grupo == c.BAIXADA).astype(float)
    t["Resto"] = (t.grupo == c.RESTO).astype(float)
    return t


mun, _, _ = c.carrega_dados()
t24 = prepara(mun[["cod_ibge", "ente", "grupo", "regiao8", "populacao", "saude", "receita"]])
t23 = prepara(pd.read_csv(TR / "indicadores_2023_replicacao.csv", dtype={"cod_ibge": str})[["cod_ibge", "ente", "grupo", "regiao8", "pop2023", "saude", "receita"]].rename(columns={"pop2023": "populacao"}))
print(f"Cidades: 2024 = {len(t24)}; 2023 = {len(t23)} (fora de 2023: {sorted(set(t24.ente) - set(t23.ente))})")


# =========================================================================================== R1 triagem
def deixa_uma_fora(t):
    """Para cada cidade: previsão sem ela (capital fora do ajuste, prevista de fora com o grupo Resto, como no Analyze)."""
    sem = t[t.grupo != c.CAPITAL]
    linhas = []
    for i, r in t.iterrows():
        base = sem.drop(i, errors="ignore")
        m = sm.OLS(base.y, sm.add_constant(base[COLS])).fit()
        resto = 1.0 if r.grupo == c.CAPITAL else r.Resto
        pr = m.get_prediction(np.array([[1, r.x, r.Baixada, resto]])).summary_frame(alpha=0.05).iloc[0]
        linhas.append({"cod_ibge": r.cod_ibge, "res_pct": pct(r.y - pr["mean"]), "fora_ic": bool(r.y < pr["obs_ci_lower"]),
                       "dif_rs": (np.exp(pr["mean"]) - np.exp(r.y)) * r.populacao})
    return pd.DataFrame(linhas).set_index("cod_ibge")


print("\n=== R1: triagem (deixa-uma-fora, intervalo de previsão de 95%) ===")
l24, l23 = deixa_uma_fora(t24), deixa_uma_fora(t23)
r1 = t24.set_index("cod_ibge")[["ente", "grupo", "populacao"]].join(l24.add_suffix("_24")).join(l23.add_suffix("_23"))
r1["sinal"] = r1.fora_ic_24 & (r1.res_pct_23 < 0)
print(f"Abaixo do intervalo em 2024: {int(r1.fora_ic_24.sum())}; em 2023: {int(r1.fora_ic_23.fillna(False).sum())}; sinalizadas pela regra (fora em 2024 e resíduo negativo em 2023): {int(r1.sinal.sum())}")
print(r1[r1.fora_ic_24 | r1.fora_ic_23.fillna(False)][["ente", "grupo", "res_pct_24", "fora_ic_24", "res_pct_23", "fora_ic_23"]].round(1).sort_values("res_pct_24").to_string())
print("Sinalizadas por grupo:", r1[r1.sinal].grupo.value_counts().to_dict(), "| total de cada grupo:", r1.grupo.value_counts().to_dict())
ambos = r1.dropna(subset=["res_pct_23"])
tab = pd.crosstab(ambos.fora_ic_23, ambos.fora_ic_24)
print("Retroteste: fora em 2023 (linhas) x fora em 2024 (colunas)\n", tab.to_string())
if tab.shape == (2, 2):
    odds, p = stats.fisher_exact(tab.values, alternative="greater")
    rep = tab.loc[True, True] / tab.loc[True].sum()
    base = ambos.fora_ic_24.mean()
    print(f"  entre as {int(tab.loc[True].sum())} fora em 2023, {int(tab.loc[True, True])} ({rep:.0%}) repetem em 2024; taxa-base de 2024: {base:.0%}; Fisher unilateral p={p:.4f}")
rho, p = stats.spearmanr(ambos.res_pct_23, ambos.res_pct_24)
print(f"Persistência do resíduo (Spearman 2023 x 2024): {rho:+.2f} (p={p:.4f})")
k = int(r1.sinal.sum())
print("Cenários de adesão (parcela das sinalizadas sem explicação legítima): achados esperados e desvio em R$ das sinalizadas")
desvio = r1[r1.sinal].dif_rs_24.sum()
for nome, p_ in (("pessimista", 0.2), ("provável", 0.5), ("otimista", 0.8)):
    print(f"  {nome:10s} p={p_:.0%}: {k * p_:.1f} cidades com achado; desvio total das sinalizadas R$ {desvio / 1e6:,.1f} milhões (soma do que a receita prevê a mais; não é ganho)")
print("Ponto de indiferença p* = 1/v:", {f"v={v}": f"{1 / v:.0%}" for v in (2, 5, 10)})
if k >= 2:
    pot = NormalIndPower()
    h = pot.solve_power(nobs1=k, alpha=0.05, power=0.8, ratio=1.0)
    p0 = 0.2
    p1 = np.sin(np.arcsin(np.sqrt(p0)) + h / 2) ** 2
    h_alvo = 2 * (np.arcsin(np.sqrt(0.5)) - np.arcsin(np.sqrt(p0)))
    n_alvo = pot.solve_power(effect_size=h_alvo, alpha=0.05, power=0.8, ratio=1.0)
    print(f"Teste: com {k} sinalizadas e {k} controles, poder 80%, nível 5%, taxa-base de achado de 20%, só se detecta taxa de {p1:.0%} ou mais; para distinguir 20% de 50% seriam necessárias {int(np.ceil(n_alvo))} cidades por grupo")
r1.to_csv(TR / "improve_r1_triagem.csv", encoding="utf-8-sig")

# =========================================================================================== R2 pares
print("\n=== R2: pares por receita contra a região ===")
t = t24.copy()
t["rh"] = t.receita / t.populacao
t["faixa"] = pd.qcut(t.rh, 5, labels=False)


def mad_sem_si(t, g):
    dev = pd.Series(np.nan, index=t.index)
    for i in t.index:
        outros = t[(t[g] == t.loc[i, g]) & (t.index != i)]
        if len(outros) >= 2:
            dev[i] = t.loc[i, "y"] - outros.y.median()
    return dev


d_reg, d_par = mad_sem_si(t, "regiao8"), mad_sem_si(t, "faixa")
ok = d_reg.notna() & d_par.notna()
mad_reg, mad_par = d_reg[ok].abs().mean(), d_par[ok].abs().mean()
red = 1 - mad_par / mad_reg
print(f"Desvio absoluto médio do log do gasto por habitante em relação à mediana do grupo (sem a própria cidade), {int(ok.sum())} cidades: região = {mad_reg:.3f}; pares = {mad_par:.3f}; redução de {red:.0%}")
sim = []
for _ in range(2000):
    t["sorteio"] = rng.permutation(t.faixa.values)
    d = mad_sem_si(t, "sorteio")
    sim.append(d[ok].abs().mean())
sim = np.array(sim)
print(f"Placebo (5 grupos sorteados com os mesmos tamanhos, 2.000 vezes): desvio médio {sim.mean():.3f} (5º percentil {np.percentile(sim, 5):.3f}); o dos pares ({mad_par:.3f}) fica {'abaixo' if mad_par < np.percentile(sim, 5) else 'dentro'} do 5º percentil")
t["dev_reg"], t["dev_par"] = pct(d_reg), pct(d_par)
print("Desvio mediano (%) em relação à região e em relação aos pares, por grupo:")
print(t.groupby("grupo")[["dev_reg", "dev_par"]].median().round(1).assign(n=t.groupby("grupo").size()).sort_values("dev_reg").to_string())
print("Tamanho das 8 regiões:", t.regiao8.value_counts().to_dict())
print("Cidades cuja leitura muda de sinal (abaixo/acima da mediana do grupo) ao trocar região por pares:", int((np.sign(d_reg[ok]) != np.sign(d_par[ok])).sum()), "de", int(ok.sum()))
print("Limite: agrupar por receita explica o gasto em boa parte por construção (gasto = receita × fatia); o ganho é de leitura para o gestor, não de causa.")
t[["cod_ibge", "ente", "grupo", "regiao8", "rh", "faixa", "dev_reg", "dev_par"]].to_csv(TR / "improve_r2_pares.csv", index=False, encoding="utf-8-sig")

# =========================================================================================== R3 veraneio
print("\n=== R3: ajuste da base nas cidades de veraneio ===")
oc = json.load(open(BR / "ibge_domicilios_uso_ocasional_9866.json", encoding="utf-8"))[0]["resultados"][0]["series"]
oc = {s["localidade"]["id"]: float(s["serie"]["2022"]) if s["serie"]["2022"] not in ("-", "...", "X") else 0.0 for s in oc}
t = t24.copy()
t["oc_dom"] = t.cod_ibge.map(oc)
assert t.oc_dom.notna().all()
sem = t[t.grupo != c.CAPITAL]


def res_mediano(k):
    pop = sem.populacao + k * sem.oc_dom
    d = sem.assign(y=np.log(sem.saude / pop), x=np.log(sem.receita / pop))
    m = sm.OLS(d.y, sm.add_constant(d[COLS])).fit()
    return pd.Series(pct(m.resid.values), index=d.index).groupby(d.grupo).median()


linhas = []
for k_ in (0, 1, 2, 3):
    rr = res_mediano(k_)
    linhas.append({"pessoas_por_domicilio_ocasional": k_, **rr.round(1).to_dict()})
tabela = pd.DataFrame(linhas)
print("Resíduo mediano (%) por grupo, conforme o número de não residentes por domicílio de uso ocasional:")
print(tabela[["pessoas_por_domicilio_ocasional", INTERIOR_LIT, "Costa Verde", c.RESTO, c.BAIXADA]].to_string(index=False))
grade = np.arange(0, 10.01, 0.1)
vals = np.array([res_mediano(g)[INTERIOR_LIT] for g in grade])
cruza = grade[np.argmax(vals >= 0)] if (vals >= 0).any() else None
print(f"Ponto de indiferença: resíduo mediano das Baixadas Litorâneas chega a zero com {cruza if cruza is None else f'{cruza:.1f}'} pessoas por domicílio de uso ocasional (limite plausível definido antes: 3)")
print(f"Resíduo em ±5% em algum cenário de 0 a 3? {bool((tabela[INTERIOR_LIT].abs() <= 5).any())}")
tabela.to_csv(TR / "improve_r3_veraneio.csv", index=False, encoding="utf-8-sig")

# =========================================================================================== R4 estresse
print("\n=== R4: teste de estresse dos repasses ===")
r24, r23 = receitas("siconfi_rreo_2024.csv"), receitas("siconfi_rreo_anexo01_2023.csv")
a = t24.set_index("cod_ibge").join(r24[["transf", "propria", "total", "periodo"]])
b = t23.set_index("cod_ibge").join(r23[["transf", "propria", "periodo"]], rsuffix="_23", lsuffix="_p")
b = b.rename(columns={"transf": "transf_23", "propria": "propria_23", "periodo": "periodo_23", "saude": "saude_23", "populacao": "pop_23"})
fd = a.join(b[["transf_23", "propria_23", "periodo_23", "saude_23", "pop_23"]], how="inner")
fd = fd[(fd.periodo == fd.periodo_23) & (fd.propria > 0) & (fd.propria_23 > 0)]
fd["dy"] = np.log(fd.saude / fd.populacao) - np.log(fd.saude_23 / fd.pop_23)
fd["dt"] = np.log(fd.transf / fd.populacao) - np.log(fd.transf_23 / fd.pop_23)
fd["dp"] = np.log(fd.propria / fd.populacao) - np.log(fd.propria_23 / fd.pop_23)
print(f"Primeiras diferenças 2023→2024: {len(fd)} cidades com o mesmo bimestre nos dois anos")
for nome, d in (("com a capital", fd), ("sem a capital", fd[fd.grupo != c.CAPITAL])):
    m = sm.OLS(d.dy, sm.add_constant(d[["dt", "dp"]])).fit(cov_type="HC3")
    ci = m.conf_int(0.05)
    print(f"  {nome} (n={int(m.nobs)}, R2={m.rsquared:.3f}): Δln(repasses) {m.params['dt']:.3f} [{ci.loc['dt', 0]:.3f}; {ci.loc['dt', 1]:.3f}]; Δln(própria) {m.params['dp']:.3f} [{ci.loc['dp', 0]:.3f}; {ci.loc['dp', 1]:.3f}]")
    if nome == "sem a capital":
        fd_b, fd_lo, fd_hi = m.params["dt"], ci.loc["dt", 0], ci.loc["dt", 1]
sec = a[a.grupo != c.CAPITAL].copy()
sec["xp"], sec["xt"] = np.log(sec.propria / sec.populacao), np.log(sec.transf / sec.populacao)
mt = sm.OLS(sec.y, sm.add_constant(sec[["xp", "xt"]])).fit(cov_type="HC3")
ci = mt.conf_int(0.05)
b_pt, b_lo, b_hi = mt.params["xt"], ci.loc["xt", 0], ci.loc["xt", 1]
print(f"Corte transversal 2024 (referência H6): elasticidade dos repasses {b_pt:.3f} [{b_lo:.3f}; {b_hi:.3f}]")
usa_dif = fd_lo > 0
print(f"Critério: coeficiente em primeiras diferenças positivo com intervalo sem zero? {'SIM, o teste de estresse vale' if usa_dif else 'NÃO, o teste de estresse é só ilustração (associação entre cidades não é efeito dentro de uma cidade)'}")
gasto_total = a.saude.sum()
print("Cenários (queda dos repasses; gasto em saúde cai pela elasticidade do corte transversal; pior caso = limite superior, melhor = limite inferior):")
linhas = []
for s in (0.10, 0.20, 0.30):
    for nome, bb in (("otimista", b_lo), ("provável", b_pt), ("pessimista", b_hi)):
        q = (1 - s) ** bb - 1
        linhas.append({"queda_repasses": s, "cenario": nome, "elasticidade": bb, "queda_gasto_pct": q * 100, "queda_gasto_rs_milhoes": q * gasto_total / 1e6})
        print(f"  repasses −{s:.0%} | {nome:10s} (b={bb:.2f}): gasto em saúde {q * 100:+.1f}% = R$ {q * gasto_total / 1e6:,.0f} milhões nas 92 cidades")
print("Cenários com a elasticidade de ano a ano (primeiras diferenças, sem a capital; o limite inferior encosta no zero):")
for s in (0.10, 0.20, 0.30):
    for nome, bb in (("otimista", max(fd_lo, 0.0)), ("provável", fd_b), ("pessimista", fd_hi)):
        q = (1 - s) ** bb - 1
        linhas.append({"queda_repasses": s, "cenario": nome + " (ano a ano)", "elasticidade": bb, "queda_gasto_pct": q * 100, "queda_gasto_rs_milhoes": q * gasto_total / 1e6})
        print(f"  repasses −{s:.0%} | {nome:10s} (b={bb:.3f}): gasto em saúde {q * 100:+.1f}% = R$ {q * gasto_total / 1e6:,.0f} milhões")
ind = lambda b_: 1 - 0.9 ** (1 / b_)
print(f"Indiferença com a elasticidade de ano a ano: provável {ind(fd_b):.1%}; pessimista {ind(fd_hi):.1%}; otimista: o intervalo toca o zero, não há queda que leve a −10%")
print(f"Ponto de indiferença: queda de repasses que reduz o gasto em 10%: {ind(b_pt):.1%} (provável); {ind(b_hi):.1%} (pessimista); {ind(b_lo):.1%} (otimista)")
a["parte_transf"] = a.transf / a.total
print("Exposição (parte da receita que vem de repasses), mediana por grupo (%):", (a.groupby("grupo").parte_transf.median() * 100).round(0).sort_values(ascending=False).to_dict())
print("Cidades mais dependentes de repasses:", a.sort_values("parte_transf", ascending=False).head(6)[["ente", "parte_transf"]].assign(parte_transf=lambda d: (d.parte_transf * 100).round(0)).values.tolist())
pd.DataFrame(linhas).to_csv(TR / "improve_r4_estresse.csv", index=False, encoding="utf-8-sig")
a[["ente", "grupo", "parte_transf"]].to_csv(TR / "improve_r4_dependencia.csv", encoding="utf-8-sig")

# =========================================================================================== R5 e R6 SIOPS
print("\n=== R5: folga sobre o mínimo de 15% (SIOPS 2024) ===")
s = pd.read_excel(BR / "LCL141.xlsx")
s = s[s.UF == "RJ"].copy()
s["aplicado_pct"] = s["Aplicado em ASPS"].map(lambda v: float(str(v).replace("%", "").replace(",", ".").strip()))
s["chave"] = s.Ente.map(c.norma)
x = t24.assign(chave=t24.ente.map(c.norma)).merge(s[["chave", "aplicado_pct", "Valor Aplicado", "Valor Mínimo", "Valor Acima do Mínimo", "Valor Abaixo do Mínimo"]], on="chave", how="left")
assert x.aplicado_pct.notna().all(), x[x.aplicado_pct.isna()].ente.tolist()
x["folga_pp"] = x.aplicado_pct - 15
x["folga_rs"] = x["Valor Aplicado"] - x["Valor Mínimo"]
x["folga_hab"] = x.folga_rs / x.populacao
x["queda_zera_pct"] = x.folga_rs / x["Valor Aplicado"] * 100
print(f"Cidades com valor abaixo do mínimo: {int((x['Valor Abaixo do Mínimo'] > 0).sum())}")
bx = x.sort_values("folga_pp")
print("Dez menores folgas:")
print(bx.head(10)[["ente", "grupo", "aplicado_pct", "folga_pp", "folga_rs", "folga_hab", "queda_zera_pct"]].round(1).to_string(index=False))
flag5 = x.folga_pp < 3
print(f"Sinalizadas (folga abaixo de 3 pp): {int(flag5.sum())}: {x[flag5].ente.tolist()}")
print(f"Folga mediana: {x.folga_pp.median():.1f} pp; R$ {x.folga_hab.median():.0f} por habitante")
print(f"Descritivo, fora do critério fixado: folga abaixo de 1 pp em {int((x.folga_pp < 1).sum())} cidades: {x[x.folga_pp < 1].ente.tolist()}")
print("Capital e Niterói:", x[x.ente.isin(['Rio de Janeiro', 'Niterói'])][["ente", "aplicado_pct", "folga_pp", "folga_rs", "queda_zera_pct"]].round(1).values.tolist())
print("\n=== R6: reconciliação Siconfi x SIOPS ===")
x["razao"] = x["Valor Aplicado"] / x.saude
q1, q3 = x.razao.quantile([0.25, 0.75])
med = x.razao.median()
mad = (x.razao - med).abs().median()
x["fora6"] = (x.razao - med).abs() > 2 * mad
print(f"Razão recursos próprios do SIOPS ÷ gasto em saúde do Siconfi: mediana {med:.2f}; quartis {q1:.2f} a {q3:.2f} (amplitude {q3 - q1:.2f}); mín {x.razao.min():.2f}; máx {x.razao.max():.2f}")
print(f"Critério: amplitude entre os quartis acima de 0,30? {'SIM, baixa especificidade: só como pergunta' if q3 - q1 > 0.30 else 'NÃO'}")
print(f"Fora de mediana ± 2 desvios absolutos ({2 * mad:.2f}): {int(x.fora6.sum())} cidades: {x[x.fora6].ente.tolist()}")
print(f"Razão acima de 1 (próprios do SIOPS maiores que o gasto do Siconfi): {int((x.razao > 1).sum())}: {x[x.razao > 1].ente.tolist()}")
r1s = set(r1[r1.sinal].ente)
print(f"Cruzamento R6 x R1: fora da faixa na R6 e sinalizadas na R1: {sorted(set(x[x.fora6].ente) & r1s)}; sinalizadas na R1 = {sorted(r1s)}")
x[["cod_ibge", "ente", "grupo", "aplicado_pct", "folga_pp", "folga_rs", "folga_hab", "queda_zera_pct", "razao", "fora6"]].to_csv(TR / "improve_r5_r6_siops.csv", index=False, encoding="utf-8-sig")

# =========================================================================================== R7 limites
print("\n=== R7: painel de limites da LRF (descritivo) ===")
ind24 = pd.read_csv(TR / "indicadores_2024.csv", dtype={"cod_ibge": str})
m7 = ind24[ind24.esfera == "M"].copy()
m7["acima_prud"] = m7.pessoal_pct_rcl > m7.limite_prudencial_pct
m7["acima_max"] = m7.pessoal_pct_rcl > m7.limite_max_pct
m7["div_80"] = m7.dcl_pct_rcl >= 0.8 * 120
q75 = m7.rp_pct_receita.quantile(0.75)
m7["rp_q4"] = m7.rp_pct_receita >= q75
print(f"Municípios: acima do limite prudencial de pessoal: {int(m7.acima_prud.sum())} (acima do máximo: {int(m7.acima_max.sum())}); dívida a partir de 80% do limite (96% da RCL): {int(m7.div_80.sum())}; restos a pagar no quartil superior (≥ {q75:.1f}% da receita): {int(m7.rp_q4.sum())}")
print("Acima do prudencial:", m7[m7.acima_prud][["ente", "pessoal_pct_rcl", "limite_prudencial_pct", "limite_max_pct", "flag_especial"]].round(1).values.tolist())
print("Dívida a partir de 80% do limite:", m7[m7.div_80][["ente", "dcl_pct_rcl"]].round(1).values.tolist())
print("Maiores restos a pagar sobre a receita:", m7.sort_values("rp_pct_receita", ascending=False).head(5)[["ente", "rp_pct_receita"]].round(1).values.tolist())
print("Entes com sinalizador especial no Measure (marcados, não retirados):", m7[m7.flag_especial.notna()][["ente", "flag_especial"]].values.tolist())
print(f"Dívida líquida: mediana {m7.dcl_pct_rcl.median():.1f}% da RCL; entes com dívida líquida negativa (credores líquidos): {int((m7.dcl_pct_rcl < 0).sum())}")
rj = ind24[(ind24.esfera == "E") & (ind24.ente == "Rio de Janeiro")].iloc[0]
print(f"Estado do RJ: pessoal {rj.pessoal_pct_rcl:.1f}% da RCL (prudencial {rj.limite_prudencial_pct:.1f}%, máximo {rj.limite_max_pct:.1f}%); dívida líquida {rj.dcl_pct_rcl:.1f}% da RCL (limite {rj.limite_dcl_pct:.0f}%); restos a pagar {rj.rp_pct_receita:.1f}% da receita")
m7["ente_estado"] = False
m7[["cod_ibge", "ente", "grupo", "pessoal_pct_rcl", "limite_prudencial_pct", "limite_max_pct", "folga_pessoal_pp", "dcl_pct_rcl", "rp_pct_receita", "acima_prud", "acima_max", "div_80", "rp_q4", "flag_especial"]].to_csv(TR / "improve_r7_limites.csv", index=False, encoding="utf-8-sig")
