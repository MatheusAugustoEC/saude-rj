"""Analyze A2b: sensibilidade do modelo às cidades de maior influência (distância de Cook) e conferência RREO x DCA delas.

Uso: python -X utf8 scripts/21_analyze_a2_sensibilidade.py
Critério fixado antes de rodar: remover as cidades com distância de Cook acima de 4/n no modelo M3 do A2 (sem a capital) e reajustar.
"""
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
import _mapa_comum as c

warnings.filterwarnings("ignore")
mun, _, _ = c.carrega_dados()
d = mun[["cod_ibge", "ente", "grupo", "populacao", "saude", "receita"]].copy()
d["y"] = np.log(d.saude / d.populacao)
d["x"] = np.log(d.receita / d.populacao)
d["Baixada"] = (d.grupo == c.BAIXADA).astype(float)
d["Resto"] = (d.grupo == c.RESTO).astype(float)
sem = d[d.grupo != c.CAPITAL].reset_index(drop=True)
cols = ["x", "Baixada", "Resto"]
pct = lambda b: (np.exp(b) - 1) * 100


def ajusta(df):
    return sm.OLS(df.y, sm.add_constant(df[cols])).fit(cov_type="HC3")


infl = sm.OLS(sem.y, sm.add_constant(sem[cols])).fit().get_influence()
sem["cook"] = infl.cooks_distance[0]
sem["alavanca"] = infl.hat_matrix_diag
corte = 4 / len(sem)
alvo = sem[sem.cook > corte].sort_values("cook", ascending=False)
print(f"corte 4/n = {corte:.3f}; cidades acima: {len(alvo)}")
print(alvo[["ente", "grupo", "cook", "alavanca"]].round(3).to_string(index=False))


def mostra(nome, df):
    m = ajusta(df)
    ci = m.conf_int(0.05)
    print(f"\n{nome} (n={len(df)})  elasticidade {m.params['x']:.3f} [{ci.loc['x',0]:.3f}; {ci.loc['x',1]:.3f}]")
    for k in ("Baixada", "Resto"):
        print(f"  {k:8s} {pct(m.params[k]):+6.1f}%  [{pct(ci.loc[k,0]):+6.1f}%; {pct(ci.loc[k,1]):+6.1f}%]")


mostra("todas as 91", sem)
mostra("sem as de Cook alto", sem[~sem.ente.isin(alvo.ente)])
mostra("sem Niterói, Maricá, Saquarema", sem[~sem.ente.isin(["Niterói", "Maricá", "Saquarema"])])

conf = pd.read_csv(c.RAIZ / "dados_tratados" / "conferencia_saude_rreo_vs_dca.csv", dtype={"cod_ibge": str})
print("\nConferência RREO x DCA das cidades de Cook alto e de Baixadas Litorâneas:")
print(conf[conf.cod_ibge.isin(set(alvo.cod_ibge) | set(d[d.grupo == "Baixadas Litorâneas"].cod_ibge))].to_string(index=False))
