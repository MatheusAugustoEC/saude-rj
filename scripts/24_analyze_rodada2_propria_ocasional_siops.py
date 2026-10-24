"""Analyze, segunda rodada: receita própria (H6), domicílios de uso ocasional (H7) e SIOPS (H8). Hipóteses em docs/09-analyze-hipoteses.md.

Uso: python -X utf8 scripts/24_analyze_rodada2_propria_ocasional_siops.py
Saída: dados_tratados/analyze_rodada2_tabela_2024.csv e analyze_rodada2_coeficientes.csv.
Receita própria = RREO Anexo 01 "Receitas (exceto intra)" menos Transferências Correntes menos Transferências de Capital (até o bimestre).
Modelos sem a capital (91 cidades em 2024; 90 em 2023 com Carmo fora), como no A2; a capital é prevista de fora.
"""
import json
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

import _mapa_comum as c

warnings.filterwarnings("ignore")
BR = c.RAIZ / "dados_brutos"
TR = c.RAIZ / "dados_tratados"
pct = lambda b: (np.exp(b) - 1) * 100


def receitas(arquivo):
    r = pd.read_csv(BR / arquivo, dtype={"cod_ibge": str}, low_memory=False)
    r = r[(r.anexo == "RREO-Anexo 01") & (r.coluna == "Até o Bimestre (c)")]
    p = r.pivot_table(index="cod_ibge", columns="cod_conta", values="valor", aggfunc="first")
    out = pd.DataFrame({"total": p["ReceitasExcetoIntraOrcamentarias"], "transf_corr": p["TransferenciasCorrentes"], "transf_cap": p["TransferenciasDeCapital"].fillna(0)})
    out["transf"] = out.transf_corr + out.transf_cap
    out["propria"] = out.total - out.transf
    out["periodo"] = r.groupby("cod_ibge").periodo.first()
    return out


# ------------------------------------------------------------------------------------------- bases
mun, _, _ = c.carrega_dados()
t24 = mun[["cod_ibge", "ente", "grupo", "regiao8", "populacao", "saude", "receita"]].copy()
r24 = receitas("siconfi_rreo_2024.csv")
t24 = t24.join(r24[["transf", "propria"]], on="cod_ibge")
t24["periodo"] = t24.cod_ibge.map(r24.periodo)
print("2024: períodos do RREO:", t24.periodo.value_counts().to_dict(), "| diferença entre 'receita' do projeto e RREO total:",
      float((t24.receita / t24.cod_ibge.map(r24.total) - 1).abs().max()))
t23 = pd.read_csv(TR / "indicadores_2023_replicacao.csv", dtype={"cod_ibge": str})[["cod_ibge", "ente", "grupo", "regiao8", "pop2023", "saude", "receita"]].rename(columns={"pop2023": "populacao"})
r23 = receitas("siconfi_rreo_anexo01_2023.csv")
t23 = t23.join(r23[["transf", "propria"]], on="cod_ibge")


def prepara(t):
    t = t.copy()
    t["y"] = np.log(t.saude / t.populacao)
    t["x_total"] = np.log(t.receita / t.populacao)
    t["x_propria"] = np.log(t.propria / t.populacao)
    t["x_transf"] = np.log(t.transf / t.populacao)
    t["Baixada"] = (t.grupo == c.BAIXADA).astype(float)
    t["Resto"] = (t.grupo == c.RESTO).astype(float)
    return t


t24, t23 = prepara(t24), prepara(t23)
assert (t24.propria > 0).all() and (t24.transf > 0).all(), t24[(t24.propria <= 0) | (t24.transf <= 0)][["ente", "propria", "transf"]]
linhas = []


def ajusta(df, cols):
    return sm.OLS(df.y, sm.add_constant(df[cols])).fit(cov_type="HC3")


def relata(ano, t):
    sem = t[t.grupo != c.CAPITAL]
    print(f"\n=== H6, {ano}: receita própria x total (n={len(sem)}, sem a capital) ===")
    for nome, cols in (("A total", ["x_total"]), ("B própria", ["x_propria"]), ("C própria + transferências", ["x_propria", "x_transf"]),
                       ("D própria + grupos", ["x_propria", "Baixada", "Resto"]), ("E total + grupos (referência do A2)", ["x_total", "Baixada", "Resto"])):
        m = ajusta(sem, cols)
        ci = m.conf_int(0.05)
        txt = "; ".join(f"{k} {m.params[k]:.3f} [{ci.loc[k,0]:.3f}; {ci.loc[k,1]:.3f}]" if k.startswith("x_") else f"{k} {pct(m.params[k]):+.1f}% [{pct(ci.loc[k,0]):+.1f}%; {pct(ci.loc[k,1]):+.1f}%]" for k in cols)
        print(f"  {nome:36s} R2={m.rsquared:.3f}  {txt}")
        for k in cols:
            linhas.append({"ano": ano, "modelo": nome, "termo": k, "coef": m.params[k], "ic_baixo": ci.loc[k, 0], "ic_alto": ci.loc[k, 1], "r2": m.rsquared, "n": len(sem)})
    cap = t[t.grupo == c.CAPITAL].iloc[0]
    mb = sm.OLS(sem.y, sm.add_constant(sem[["x_propria"]])).fit()
    pr = mb.get_prediction(np.array([[1, cap.x_propria]])).summary_frame(alpha=0.05).iloc[0]
    print(f"  Capital: própria/hab R$ {np.exp(cap.x_propria):.0f} (total R$ {np.exp(cap.x_total):.0f}); gasto/hab real R$ {np.exp(cap.y):.0f}; previsto pelo modelo B R$ {np.exp(pr['mean']):.0f} "
          f"[R$ {np.exp(pr['obs_ci_lower']):.0f}; R$ {np.exp(pr['obs_ci_upper']):.0f}]; real em relação ao previsto {pct(cap.y - pr['mean']):+.1f}%")
    t["parte_propria"] = t.propria / t.receita
    print("  Parte da receita que é própria, mediana por grupo (%):", (t.groupby("grupo").parte_propria.median() * 100).round(0).sort_values().to_dict())


relata(2024, t24)
relata(2023, t23)

# ------------------------------------------------------------------------------------------- H7: uso ocasional
oc = json.load(open(BR / "ibge_domicilios_uso_ocasional_9866.json", encoding="utf-8"))[0]["resultados"][0]["series"]
oc = {s["localidade"]["id"]: float(s["serie"]["2022"]) if s["serie"]["2022"] not in ("-", "...", "X") else 0.0 for s in oc}
censo = json.load(open(BR / "ibge_populacao_censo2022_4714.json", encoding="utf-8"))["censo2022_mun"]
censo = {l["D1C"]: float(l["V"]) for l in censo[1:] if l["V"] not in ("-", "...", "X")}
t24["ocasional"] = t24.cod_ibge.map(oc)
t24["ocas_100"] = t24.ocasional / t24.cod_ibge.map(censo) * 100
assert t24.ocas_100.notna().all()
t24["fatia"] = t24.saude / t24.receita
t24["receita_hab"] = t24.receita / t24.populacao
t24["gasto_hab"] = t24.saude / t24.populacao
print("\n=== H7, uso ocasional (Censo 2022): domicílios de uso ocasional por 100 moradores ===")
print("  mediana por grupo:", t24.groupby("grupo").ocas_100.median().round(1).sort_values(ascending=False).to_dict())
sem = t24[t24.grupo != c.CAPITAL].copy()
for var in ("receita_hab", "fatia", "gasto_hab"):
    rho, p = stats.spearmanr(sem.ocas_100, sem[var])
    print(f"  Spearman uso ocasional x {var}: {rho:+.2f} (p={p:.3f})")
sem["x_oc"] = np.log1p(sem.ocas_100)
m_sem = ajusta(sem, ["x_total", "Baixada", "Resto"])
m_com = ajusta(sem, ["x_total", "x_oc", "Baixada", "Resto"])
sem["res_sem"], sem["res_com"] = pct(m_sem.resid), pct(m_com.resid)
ci = m_com.conf_int(0.05)
print(f"  modelo com uso ocasional: coef(ln(1+oc/100 hab)) {m_com.params['x_oc']:.3f} [{ci.loc['x_oc',0]:.3f}; {ci.loc['x_oc',1]:.3f}]; elasticidade da receita {m_com.params['x_total']:.3f}; R2 {m_com.rsquared:.3f} (sem: {m_sem.rsquared:.3f})")
print("  resíduo mediano por grupo (%), sem -> com uso ocasional:")
g = sem.groupby("grupo")[["res_sem", "res_com"]].median().round(0)
print(g.assign(n=sem.groupby("grupo").size()).sort_values("res_sem").to_string())
linhas.append({"ano": 2024, "modelo": "uso ocasional", "termo": "x_oc", "coef": m_com.params["x_oc"], "ic_baixo": ci.loc["x_oc", 0], "ic_alto": ci.loc["x_oc", 1], "r2": m_com.rsquared, "n": len(sem)})
print("  maiores participações de uso ocasional:", t24.sort_values("ocas_100", ascending=False).head(8)[["ente", "ocas_100"]].round(1).values.tolist())

# ------------------------------------------------------------------------------------------- H8: SIOPS
s = pd.read_excel(BR / "LCL141.xlsx")
s = s[s.UF == "RJ"].copy()
pc = lambda v: float(str(v).replace("%", "").replace(",", ".").strip())
s["aplicado_pct"] = s["Aplicado em ASPS"].map(pc)
s["chave"] = s.Ente.map(c.norma)
t24["chave"] = t24.ente.map(c.norma)
j = t24.merge(s[["chave", "aplicado_pct", "Valor Aplicado", "Valor Mínimo"]], on="chave", how="left")
print(f"\n=== H8, SIOPS 2024 ===\n  cidades casadas por nome: {int(j.aplicado_pct.notna().sum())} de {len(j)}; sem par: {j[j.aplicado_pct.isna()].ente.tolist()}")
j = j[j.aplicado_pct.notna()].copy()
print(f"  aplicado em ASPS: mediana {j.aplicado_pct.median():.1f}%; mínimo {j.aplicado_pct.min():.1f}% ({j.loc[j.aplicado_pct.idxmin(), 'ente']}); acima de 15%: {int((j.aplicado_pct >= 15).sum())} de {len(j)}")
print("  abaixo de 15%:", j[j.aplicado_pct < 15][["ente", "aplicado_pct"]].values.tolist())
menos = j.sort_values("gasto_hab").head(10)
print(f"  as 10 que menos gastam: aplicado mediano {menos.aplicado_pct.median():.1f}% (mín {menos.aplicado_pct.min():.1f}%): ", menos[["ente", "aplicado_pct"]].round(1).values.tolist())
rho, p = stats.spearmanr(j.aplicado_pct, j.gasto_hab)
print(f"  Spearman aplicado % x gasto por habitante: {rho:+.2f} (p={p:.3f})")
rho, p = stats.spearmanr(j.aplicado_pct, j.receita_hab)
print(f"  Spearman aplicado % x receita por habitante: {rho:+.2f} (p={p:.3f})")
j["parte_aplicada"] = j["Valor Aplicado"] / j.saude * 100
j["base_impostos_hab"] = j["Valor Mínimo"] / 0.15 / j.populacao
print("  parte do gasto em saúde (Siconfi) que cabe nos recursos próprios do SIOPS (valor aplicado ÷ saúde, %), mediana por grupo:",
      j.groupby("grupo").parte_aplicada.median().round(0).sort_values().to_dict())
print(f"  parte aplicada: mediana {j.parte_aplicada.median():.0f}%; acima de 100% em {int((j.parte_aplicada > 100).sum())} cidades: {j[j.parte_aplicada > 100].ente.tolist()}")
print("  aplicado % mediano por grupo:", j.groupby("grupo").aplicado_pct.median().round(1).sort_values().to_dict())
cap = j[j.grupo == c.CAPITAL].iloc[0]
print(f"  Capital: aplicado {cap.aplicado_pct:.1f}%; parte aplicada {cap.parte_aplicada:.0f}% do gasto em saúde do Siconfi")
j[["cod_ibge", "ente", "grupo", "aplicado_pct", "parte_aplicada", "base_impostos_hab"]].to_csv(TR / "analyze_rodada2_siops_2024.csv", index=False, encoding="utf-8-sig")
t24[["cod_ibge", "ente", "grupo", "propria", "transf", "ocas_100"]].to_csv(TR / "analyze_rodada2_tabela_2024.csv", index=False, encoding="utf-8-sig")
pd.DataFrame(linhas).to_csv(TR / "analyze_rodada2_coeficientes.csv", index=False, encoding="utf-8-sig")
