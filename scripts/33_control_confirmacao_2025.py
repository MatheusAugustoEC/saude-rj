"""Control, passo 3b: recorte de confirmação de 2025 (C5). Previsões, critérios e desempates em docs/14-control-previsoes-2025.md, fixados antes de abrir.

Uso: python -X utf8 scripts/33_control_confirmacao_2025.py   (aberto UMA vez; a saída fica em dados_tratados/control_2025_saida.txt)
Entrada: dados_brutos/siconfi_rreo_anexo01_2025.csv, siconfi_dca_ie_2025.csv (script 32), teste_acesso_2025.csv (script 31, população 2025 e data da DCA).
Saída: dados_tratados/control_2025_resultados.csv (classificação de K1 a K9, com e sem as DCAs "recentes") e control_2025_residuos.csv.
Cada K é classificado por regra, sem julgamento depois do resultado. Classificação final = a pior entre a leitura com todas e a leitura sem as DCAs entregues depois de 31/08/2026.
"""
import json
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import _mapa_comum as c

warnings.filterwarnings("ignore")
BR, TR = c.RAIZ / "dados_brutos", c.RAIZ / "dados_tratados"
pct = lambda b: (np.exp(b) - 1) * 100
COLS = ["x", "Baixada", "Resto"]
LIT = "Baixadas Litorâneas"
ORDEM = {"sustenta": 2, "enfraquece": 1, "cai": 0}
NITEROI, SPA, CAPITAL = "3303302", "3305208", "3304557"


def receitas(arquivo):
    r = pd.read_csv(BR / arquivo, dtype={"cod_ibge": str}, low_memory=False)
    r = r[(r.anexo == "RREO-Anexo 01") & (r.coluna == "Até o Bimestre (c)")]
    p = r.pivot_table(index="cod_ibge", columns="cod_conta", values="valor", aggfunc="first")
    out = pd.DataFrame({"total": p["ReceitasExcetoIntraOrcamentarias"], "transf": p["TransferenciasCorrentes"] + p["TransferenciasDeCapital"].fillna(0)})
    out["propria"] = out.total - out.transf
    out["periodo"] = r.groupby("cod_ibge").periodo.first()
    return out


# ------------------------------------------------------------------------------------------- monta 2025
mun, _, _ = c.carrega_dados()
pre = pd.read_csv(BR / "teste_acesso_2025.csv", dtype={"cod_ibge": str})
r25 = receitas("siconfi_rreo_anexo01_2025.csv")
d = pd.read_csv(BR / "siconfi_dca_ie_2025.csv", dtype={"cod_ibge": str}, low_memory=False)
sau25 = d[d.conta.str.startswith("10 - Sa") & (d.coluna == "Despesas Empenhadas")].groupby("cod_ibge").valor.first().rename("saude")
base = mun[["cod_ibge", "ente", "grupo", "regiao8", "populacao", "saude", "receita"]].rename(columns={"populacao": "pop24", "saude": "saude24", "receita": "receita24"})
t = base.set_index("cod_ibge").join(pre.set_index("cod_ibge")[["pop2025", "dca_data"]]).join(r25).join(sau25.rename("saude")).reset_index()
t["populacao"] = pd.to_numeric(t.pop2025, errors="coerce")
excl = t[~((t.periodo == 6) & t.saude.notna() & t.populacao.notna() & (t.total > 0))]
print(f"Recorte de 2025: {len(t) - len(excl)} cidades; excluídas ({len(excl)}): {[(r.ente, int(r.periodo) if pd.notna(r.periodo) else None, bool(pd.notna(r.saude))) for r in excl.itertuples()]}")
t = t.drop(excl.index).copy()
t["receita"] = t.total
t["recente"] = t.dca_data.fillna("") > "2026-08-31"
print(f"DCA entregue depois de 31/08/2026 ('recente'): {int(t.recente.sum())}: {t[t.recente].ente.tolist()}")
t["y"] = np.log(t.saude / t.populacao)
t["x"] = np.log(t.receita / t.populacao)
t["Baixada"] = (t.grupo == c.BAIXADA).astype(float)
t["Resto"] = (t.grupo == c.RESTO).astype(float)
print("Cidades por grupo:", t.grupo.value_counts().to_dict())

r24 = receitas("siconfi_rreo_2024.csv")
res24 = pd.read_csv(TR / "improve_r1_triagem.csv", dtype={"cod_ibge": str}).set_index("cod_ibge")
oc = json.load(open(BR / "ibge_domicilios_uso_ocasional_9866.json", encoding="utf-8"))[0]["resultados"][0]["series"]
oc = {s["localidade"]["id"]: float(s["serie"]["2022"]) if s["serie"]["2022"] not in ("-", "...", "X") else 0.0 for s in oc}
t["oc_dom"] = t.cod_ibge.map(oc)


def deixa_uma_fora(t):
    sem = t[t.grupo != c.CAPITAL]
    out = []
    for i, r in t.iterrows():
        b = sem.drop(i, errors="ignore")
        m = sm.OLS(b.y, sm.add_constant(b[COLS])).fit()
        resto = 1.0 if r.grupo == c.CAPITAL else r.Resto
        pr = m.get_prediction(np.array([[1, r.x, r.Baixada, resto]])).summary_frame(alpha=0.05).iloc[0]
        out.append({"cod_ibge": r.cod_ibge, "res_pct": pct(r.y - pr["mean"]), "fora": bool(r.y < pr["obs_ci_lower"])})
    return pd.DataFrame(out).set_index("cod_ibge")


def mad_sem_si(t, g):
    dev = pd.Series(np.nan, index=t.index)
    for i in t.index:
        o = t[(t[g] == t.loc[i, g]) & (t.index != i)]
        if len(o) >= 2:
            dev[i] = t.loc[i, "y"] - o.y.median()
    return dev


def analisa(t, rotulo):
    t = t.copy()
    sem = t[t.grupo != c.CAPITAL]
    cap = t[t.grupo == c.CAPITAL]
    out = {}
    print(f"\n################ {rotulo}: {len(t)} cidades ({len(sem)} sem a capital) ################")
    m3 = sm.OLS(sem.y, sm.add_constant(sem[COLS])).fit(cov_type="HC3")
    ci = m3.conf_int(0.05)
    # K1
    b, lo, hi = m3.params["x"], ci.loc["x", 0], ci.loc["x", 1]
    out["K1"] = "sustenta" if hi < 1 else ("cai" if lo > 1 else "enfraquece")
    print(f"K1 elasticidade da receita {b:.3f} [{lo:.3f}; {hi:.3f}] -> {out['K1']}")
    # K2
    p, plo, phi = pct(m3.params["Resto"]), pct(ci.loc["Resto", 0]), pct(ci.loc["Resto", 1])
    out["K2"] = "cai" if (plo > 0 or phi < 0) else ("sustenta" if -10 <= p <= 5 else "enfraquece")
    print(f"K2 Resto da Metropolitana {p:+.1f}% [{plo:+.1f}%; {phi:+.1f}%] -> {out['K2']}   (Baixada {pct(m3.params['Baixada']):+.1f}% [{pct(ci.loc['Baixada',0]):+.1f}%; {pct(ci.loc['Baixada',1]):+.1f}%])")
    # K3
    if len(cap):
        cp = cap.iloc[0]
        m = sm.OLS(sem.y, sm.add_constant(sem[COLS])).fit()
        pr = m.get_prediction(np.array([[1, cp.x, 0, 1]])).summary_frame(alpha=0.05).iloc[0]
        dif = pct(cp.y - pr["mean"])
        out["K3"] = "sustenta" if dif <= -25 else ("enfraquece" if dif < 0 else "cai")
        print(f"K3 capital: real R$ {np.exp(cp.y):.0f}; previsto R$ {np.exp(pr['mean']):.0f} [R$ {np.exp(pr['obs_ci_lower']):.0f}; R$ {np.exp(pr['obs_ci_upper']):.0f}]; {dif:+.1f}%; fora do intervalo: {cp.y < pr['obs_ci_lower']} -> {out['K3']}")
    else:
        out["K3"] = "cai"
        print("K3 capital fora do recorte")
    # K4
    s2 = sem.assign(xp=np.log(sem.propria / sem.populacao), xt=np.log(sem.transf / sem.populacao), xtot=sem.x)
    mc = sm.OLS(s2.y, sm.add_constant(s2[["xp", "xt"]])).fit(cov_type="HC3")
    r2_p = sm.OLS(s2.y, sm.add_constant(s2[["xp"]])).fit().rsquared
    r2_t = sm.OLS(s2.y, sm.add_constant(s2[["xtot"]])).fit().rsquared
    ok1, ok2 = mc.params["xt"] > mc.params["xp"], r2_p < r2_t
    out["K4"] = "sustenta" if (ok1 and ok2) else ("enfraquece" if (ok1 or ok2) else "cai")
    print(f"K4 repasses {mc.params['xt']:.3f}, própria {mc.params['xp']:.3f}; R2 própria sozinha {r2_p:.3f}, total {r2_t:.3f} -> {out['K4']}")
    # K5
    l25 = deixa_uma_fora(t)
    t["res_pct"], t["fora"] = t.cod_ibge.map(l25.res_pct), t.cod_ibge.map(l25.fora)
    reps = [(cod, bool(t.set_index('cod_ibge').fora.get(cod, False)) if cod in set(t.cod_ibge) else None) for cod in (NITEROI, SPA, CAPITAL)]
    n_rep = sum(1 for _, v in reps if v)
    comum = t.set_index("cod_ibge").res_pct.to_frame("r25").join(res24.res_pct_24).dropna()
    rho = stats.spearmanr(comum.res_pct_24, comum.r25)[0]
    out["K5"] = "sustenta" if (n_rep >= 2 and rho >= 0.60) else ("cai" if (n_rep == 0 or rho < 0.40) else "enfraquece")
    print(f"K5 Niterói/São Pedro da Aldeia/capital fora do intervalo em 2025: {reps}; repetem {n_rep} de 3; Spearman dos resíduos 2024 x 2025 {rho:+.2f} (n={len(comum)}) -> {out['K5']}")
    print("   fora do intervalo em 2025:", t[t.fora][["ente", "res_pct"]].round(1).values.tolist())
    # K6
    tt = t.reset_index(drop=True)
    tt["rh"] = tt.receita / tt.populacao
    tt["faixa"] = pd.qcut(tt.rh, 5, labels=False)
    dr, dp = mad_sem_si(tt, "regiao8"), mad_sem_si(tt, "faixa")
    ok = dr.notna() & dp.notna()
    red = 1 - dp[ok].abs().mean() / dr[ok].abs().mean()
    out["K6"] = "sustenta" if red >= 0.20 else ("enfraquece" if red > 0 else "cai")
    print(f"K6 dispersão região {dr[ok].abs().mean():.3f}; pares {dp[ok].abs().mean():.3f}; redução {red:.0%} -> {out['K6']}")
    # K7
    a = sem.set_index("cod_ibge").join(r24[["transf", "propria", "periodo"]].add_suffix("_24"))
    a = a[(a.periodo_24 == 6) & (a.propria_24 > 0) & (a.propria > 0)]
    a["dy"] = a.y - np.log(a.saude24 / a.pop24)
    a["dt"] = np.log(a.transf / a.populacao) - np.log(a.transf_24 / a.pop24)
    a["dp"] = np.log(a.propria / a.populacao) - np.log(a.propria_24 / a.pop24)
    mf = sm.OLS(a.dy, sm.add_constant(a[["dt", "dp"]])).fit(cov_type="HC3")
    cf = mf.conf_int(0.05)
    pt, lo7 = mf.params["dt"], cf.loc["dt", 0]
    out["K7"] = "sustenta" if lo7 > 0 else ("enfraquece" if pt > 0 else "cai")
    bt = sm.OLS(s2.y, sm.add_constant(s2[["xp", "xt"]])).fit(cov_type="HC3")
    print(f"K7 ano a ano (n={int(mf.nobs)}) repasses {pt:.3f} [{lo7:.3f}; {cf.loc['dt', 1]:.3f}], própria {mf.params['dp']:.3f}; entre cidades {bt.params['xt']:.3f} [{bt.conf_int().loc['xt',0]:.3f}; {bt.conf_int().loc['xt',1]:.3f}] -> {out['K7']}")
    # K8
    rs = pd.Series(pct(m3.resid.values), index=sem.index)
    r8 = rs[sem.grupo == LIT].median()
    out["K8"] = "sustenta" if r8 <= -8 else ("enfraquece" if r8 <= -5 else "cai")
    print(f"K8 resíduo mediano das Baixadas Litorâneas {r8:+.1f}% (n={int((sem.grupo == LIT).sum())}) -> {out['K8']}")
    # K9
    meds = {}
    for k in (0, 1, 2, 3):
        pop = sem.populacao + k * sem.oc_dom
        dd = sem.assign(y=np.log(sem.saude / pop), x=np.log(sem.receita / pop))
        mm = sm.OLS(dd.y, sm.add_constant(dd[COLS])).fit()
        meds[k] = pd.Series(pct(mm.resid.values), index=dd.index)[dd.grupo == LIT].median()
    piora = [meds[k] < meds[0] for k in (1, 2, 3)]
    out["K9"] = "sustenta" if all(piora) else ("enfraquece" if any(piora) else "cai")
    print(f"K9 resíduo mediano das Baixadas Litorâneas com 0/1/2/3 visitantes: {[round(meds[k], 1) for k in (0, 1, 2, 3)]} -> {out['K9']}")
    return out, t


tudo, t_res = analisa(t, "TODAS as cidades do recorte")
sem_rec, _ = analisa(t[~t.recente], "SEM as DCAs 'recentes'")
linhas = []
print("\n================ CLASSIFICAÇÃO FINAL (a pior das duas leituras) ================")
for k in sorted(tudo):
    final = min(tudo[k], sem_rec[k], key=lambda v: ORDEM[v])
    linhas.append({"K": k, "todas": tudo[k], "sem_recentes": sem_rec[k], "final": final, "divergem": tudo[k] != sem_rec[k]})
    print(f"{k}: todas = {tudo[k]:10s} | sem recentes = {sem_rec[k]:10s} | FINAL = {final}" + ("   (divergem)" if tudo[k] != sem_rec[k] else ""))
pd.DataFrame(linhas).to_csv(TR / "control_2025_resultados.csv", index=False, encoding="utf-8-sig")
t_res[["cod_ibge", "ente", "grupo", "populacao", "saude", "receita", "recente", "res_pct", "fora"]].to_csv(TR / "control_2025_residuos.csv", index=False, encoding="utf-8-sig")
