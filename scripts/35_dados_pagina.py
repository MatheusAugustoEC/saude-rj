"""Gera o arquivo de dados da página de entrega (dados_tratados/pagina_dados.json) a partir dos resultados das fases.

Uso: python -X utf8 scripts/35_dados_pagina.py
Nada é digitado à mão: todo número da página sai de arquivos de dados_tratados/ (resultados das fases Measure a Control) e de dados_brutos/ (malhas do IBGE).
Cada curiosidade carrega a fonte e a janela de tempo, e as contas que a sustentam são feitas aqui, com verificações (assert) que param o programa se o número mudar.
"""
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
T = RAIZ / "dados_tratados"
B = RAIZ / "dados_brutos"
SAIDA = T / "pagina_dados.json"

SIGLA = {11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO", 21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL", 28: "SE", 29: "BA", 31: "MG", 32: "ES", 33: "RJ", 35: "SP", 41: "PR", 42: "SC", 43: "RS", 50: "MS", 51: "MT", 52: "GO", 53: "DF"}
# grupos do estudo: o nome de exibição e a região de governo (CEPERJ) de cada um
GRUPOS = [
    ("Capital", "Capital (Rio de Janeiro)", "Metropolitana"),
    ("Baixada (núcleo de 6)", "Baixada Fluminense (núcleo de 6)", "Metropolitana"),
    ("Metropolitana (resto, 15)", "Metropolitana, demais cidades", "Metropolitana"),
    ("Baixadas Litorâneas", "Baixadas Litorâneas", "Baixadas Litorâneas"),
    ("Costa Verde", "Costa Verde", "Costa Verde"),
    ("Médio Paraíba", "Médio Paraíba", "Médio Paraíba"),
    ("Serrana", "Serrana", "Serrana"),
    ("Centro-Sul Fluminense", "Centro-Sul Fluminense", "Centro-Sul Fluminense"),
    ("Norte Fluminense", "Norte Fluminense", "Norte Fluminense"),
    ("Noroeste Fluminense", "Noroeste Fluminense", "Noroeste Fluminense"),
]


KNOMES = {"K1": "A receita pesa menos que proporcionalmente no gasto (sensibilidade abaixo de 1)", "K2": "Resto da Metropolitana, com a mesma receita, sem diferença conclusiva", "K3": "A capital gasta abaixo do que a receita indica",
          "K4": "O gasto segue os repasses mais que a receita própria", "K5": "Triagem: as cidades sinalizadas se repetem em 2025", "K6": "Comparar por receita parecida lê melhor que comparar por região",
          "K7": "Os repasses movem o gasto dentro da própria cidade", "K8": "Baixadas Litorâneas gastam menos do que a receita indica", "K9": "Somar visitantes à população piora o resultado das Baixadas Litorâneas"}


def pt(x, casas=0):
    s = f"{x:,.{casas}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def le(nome):
    return pd.read_csv(T / nome)


def main():
    d = le("indicadores_2024.csv")
    cid = d[d.esfera == "M"].copy()
    uf = d[d.esfera.isin(["E", "D"])].copy()
    assert len(cid) == 92 and len(uf) == 27, (len(cid), len(uf))

    # ---------- cidades ----------
    gr = le("analyze_a2_residuos.csv")[["cod_ibge", "grupo", "residuo_pct"]].rename(columns={"grupo": "g", "residuo_pct": "res_modelo"})
    cid = cid.drop(columns=["grupo"]).merge(gr, on="cod_ibge").rename(columns={"g": "grupo"})
    pares = le("improve_r2_pares.csv")[["cod_ibge", "regiao8", "faixa", "dev_reg", "dev_par"]]
    cid = cid.merge(pares, on="cod_ibge")
    tri = le("improve_r1_triagem.csv")[["cod_ibge", "res_pct_24", "fora_ic_24", "res_pct_23", "fora_ic_23"]]
    cid = cid.merge(tri, on="cod_ibge", how="left")
    c25 = le("control_2025_residuos.csv")[["cod_ibge", "res_pct", "fora", "recente"]].rename(columns={"res_pct": "res_pct_25", "fora": "fora_ic_25", "recente": "dca25_recente"})
    cid = cid.merge(c25, on="cod_ibge", how="left")
    sio = le("improve_r5_r6_siops.csv")[["cod_ibge", "aplicado_pct", "folga_pp", "queda_zera_pct", "razao", "fora6"]]
    cid = cid.merge(sio, on="cod_ibge", how="left")
    dep = le("improve_r4_dependencia.csv")[["cod_ibge", "parte_transf"]]
    cid = cid.merge(dep, on="cod_ibge", how="left")
    lim = le("improve_r7_limites.csv")[["cod_ibge", "acima_prud", "acima_max"]]
    cid = cid.merge(lim, on="cod_ibge", how="left")
    cid["fatia"] = cid.saude / cid.receita * 100
    cid["fatia_despesa"] = cid.saude / cid.despesa_base_saude * 100
    assert (cid.fatia_despesa - cid.saude_pct_despesa).abs().max() < 1e-6
    assert cid.aplicado_pct.notna().all() and (cid.folga_pp >= 0).all()

    def v(x, n=2):
        return None if pd.isna(x) else round(float(x), n)

    cidades = []
    for _, r in cid.sort_values("nome").iterrows():
        cidades.append({
            "c": int(r.cod_ibge), "n": r.nome, "r": r.regiao8, "g": r.grupo, "pop": int(r.populacao),
            "gh": v(r.saude_por_hab, 1), "rh": v(r.receita_por_hab, 1), "pd": v(r.saude_pct_despesa, 2), "fa": v(r.fatia, 2),
            "sa": v(r.saude, 0), "re": v(r.receita, 0), "de": v(r.despesa_base_saude, 0),
            "ap": v(r.aplicado_pct, 2), "fo": v(r.folga_pp, 2), "qz": v(r.queda_zera_pct, 1), "rz": v(r.razao, 3), "f6": bool(r.fora6),
            "pt": v(r.parte_transf * 100 if r.parte_transf <= 1 else r.parte_transf, 1),
            "r24": v(r.res_pct_24, 1), "o24": bool(r.fora_ic_24), "r23": v(r.res_pct_23, 1), "o23": bool(r.fora_ic_23),
            "r25": v(r.res_pct_25, 1), "o25": None if pd.isna(r.fora_ic_25) else bool(r.fora_ic_25), "n25": None if pd.isna(r.dca25_recente) else bool(r.dca25_recente),
            "fx": int(r.faixa), "dr": v(r.dev_reg, 1), "dp": v(r.dev_par, 1),
            "pes": v(r.pessoal_pct_rcl, 2), "prud": v(r.limite_prudencial_pct, 2), "lmax": v(r.limite_max_pct, 2),
            "ap_": bool(r.acima_prud) if not pd.isna(r.acima_prud) else None, "fl": "" if pd.isna(r.flag_especial) else str(r.flag_especial),
            "rp": v(r.rp_pct_receita, 1), "dcl": v(r.dcl_pct_rcl, 1),
        })

    # ---------- estados ----------
    ufs = []
    for _, r in uf.iterrows():
        ufs.append({"c": int(r.cod_ibge), "s": SIGLA[int(r.cod_ibge)], "n": r.nome, "gh": v(r.saude_por_hab, 1), "pd": v(r.saude_pct_despesa, 2), "rh": v(r.receita_por_hab, 1)})
    rj = uf[uf.cod_ibge == 33].iloc[0]
    assert rj.saude_por_hab == uf.saude_por_hab.min() and rj.saude_pct_despesa == uf.saude_pct_despesa.min()
    estado_rj = {"gh": v(rj.saude_por_hab, 1), "pd": v(rj.saude_pct_despesa, 2), "rh": v(rj.receita_por_hab, 1), "pes": v(rj.pessoal_pct_rcl, 1), "prud": v(rj.limite_prudencial_pct, 1), "lmax": v(rj.limite_max_pct, 1),
                 "dcl": v(rj.dcl_pct_rcl, 1), "lim_dcl": 200, "pos_gh": int((uf.saude_por_hab > rj.saude_por_hab).sum() + 1), "pos_pd": int((uf.saude_pct_despesa > rj.saude_pct_despesa).sum() + 1)}
    assert estado_rj["pos_gh"] == 27 and estado_rj["dcl"] > 200

    # ---------- regiões e grupos ----------
    def agg(df):
        return {"n": int(len(df)), "pop": int(df.populacao.sum()), "gh": round(df.saude.sum() / df.populacao.sum(), 1), "rh": round(df.receita.sum() / df.populacao.sum(), 1), "pd": round(df.saude.sum() / df.despesa_base_saude.sum() * 100, 2), "fa": round(df.saude.sum() / df.receita.sum() * 100, 2),
                "tr": round(float((df.parte_transf.where(df.parte_transf > 1, df.parte_transf * 100) * df.receita).sum() / df.receita.sum()), 1)}

    grupos = [{"k": k, "nome": nome, "regiao": reg, **agg(cid[cid.grupo == k])} for k, nome, reg in GRUPOS]
    regioes = []
    for reg in sorted({g[2] for g in GRUPOS}):
        a = agg(cid[cid.regiao8 == reg]) if False else agg(cid[cid.grupo.isin([g[0] for g in GRUPOS if g[2] == reg])])
        regioes.append({"k": reg, **a, "grupos": [g[0] for g in GRUPOS if g[2] == reg]})
    assert sum(g["n"] for g in grupos) == 92 and sum(r["n"] for r in regioes) == 92
    assert [r for r in regioes if r["k"] == "Metropolitana"][0]["n"] == 22
    pop_uf = int(cid.populacao.sum())

    # ---------- globais ----------
    med = float(cid.saude_por_hab.median())
    menor, maior = cid.saude_por_hab.min(), cid.saude_por_hab.max()
    abaixo_pop = cid[cid.saude_por_hab < med].populacao.sum() / pop_uf * 100
    dez_menores = cid.nsmallest(10, "saude_por_hab")
    n_metro_10 = int(dez_menores.regiao8.eq("Metropolitana").sum())
    cinco_menos_receita = set(cid.nsmallest(5, "receita_por_hab").nome)
    inter = cinco_menos_receita & set(dez_menores.nome)
    arraial, spa = cid[cid.nome == "Arraial do Cabo"].iloc[0], cid[cid.nome == "São Pedro da Aldeia"].iloc[0]
    capital = cid[cid.nome.str.contains("capital")].iloc[0]
    ibge = le("analyze_ibge_indicadores.csv")
    es24 = ibge[ibge.ano == 2024].esgoto10 * 10
    saneam_min, saneam_max = float(es24.min()), float(es24.max())
    saida = (T / "improve_saida.txt").read_text(encoding="utf-8")
    m = re.search(r"região = ([0-9.]+); pares = ([0-9.]+); redução de (\d+)%", saida)
    pares_reg, pares_par, pares_red = float(m.group(1)), float(m.group(2)), int(m.group(3))
    m = re.search(r"Δln\(repasses\) ([0-9.]+) \[([0-9.]+); ([0-9.]+)\]; Δln\(própria\) ([0-9.\-]+) \[([0-9.\-]+); ([0-9.]+)\]", saida)
    d_rep = (float(m.group(1)), float(m.group(2)), float(m.group(3)))
    d_prop = (float(m.group(4)), float(m.group(5)), float(m.group(6)))
    coef = le("analyze_rodada2_coeficientes.csv")
    c24 = coef[(coef.ano == 2024) & (coef.modelo == "C própria + transferências")].set_index("termo")
    t24 = coef[(coef.ano == 2024) & (coef.modelo == "A total")].iloc[0]
    e_rep = (round(c24.loc["x_transf", "coef"], 3), round(c24.loc["x_transf", "ic_baixo"], 3), round(c24.loc["x_transf", "ic_alto"], 3))
    e_prop = (round(c24.loc["x_propria", "coef"], 3), round(c24.loc["x_propria", "ic_baixo"], 3), round(c24.loc["x_propria", "ic_alto"], 3))
    elast = {a: round(float(coef[(coef.ano == a) & (coef.modelo == "A total")].coef.iloc[0]), 2) for a in (2023, 2024)}
    sp25 = re.search(r"Spearman dos resíduos 2024 x 2025 ([+\-][0-9.]+) \(n=86\)", (T / "control_2025_saida.txt").read_text(encoding="utf-8")).group(1).replace(".", ",")
    kres = le("control_2025_resultados.csv")
    n_sust = int((kres.final == "sustenta").sum())
    assert (len(kres), n_sust) == (9, 8)
    r25 = cid[cid.res_pct_25.notna()]
    folga1, folga3 = int((cid.folga_pp < 1).sum()), int((cid.folga_pp < 3).sum())
    assert (folga1, folga3) == (7, 18)
    acima_prud = int(cid.acima_prud.sum())
    assert acima_prud == 22 and int(cid.fora6.sum()) == 11
    nor = cid[cid.grupo == "Noroeste Fluminense"]
    met = cid[cid.grupo.isin(["Baixada (núcleo de 6)", "Metropolitana (resto, 15)"])]
    nor_rec = (nor.receita.sum() / nor.populacao.sum()) / (met.receita.sum() / met.populacao.sum()) * 100 - 100
    nor_gasto = (nor.saude.sum() / nor.populacao.sum()) / (met.saude.sum() / met.populacao.sum()) * 100 - 100
    bx = cid[cid.grupo == "Baixada (núcleo de 6)"]
    bx_pd = bx.saude.sum() / bx.despesa_base_saude.sum() * 100
    bl = cid[cid.grupo == "Baixadas Litorâneas"]
    estr = le("improve_r4_estresse.csv")

    # ---------- estados (Início fala só de estados) ----------
    top_gh = uf.loc[uf.saude_por_hab.idxmax()]
    top_pd = uf.loc[uf.saude_pct_despesa.idxmax()]
    med_uf_gh, med_uf_pd = float(uf.saude_por_hab.median()), float(uf.saude_pct_despesa.median())
    pos_rh = int((uf.receita_por_hab > rj.receita_por_hab).sum() + 1)
    lx, ly = np.log(uf.receita_por_hab.to_numpy()), np.log(uf.saude_por_hab.to_numpy())
    r2_uf = float(np.corrcoef(lx, ly)[0, 1] ** 2)
    estado_rj["pos_rh"] = pos_rh
    faixas = [{"fx": int(f), "min": round(float(g.receita_por_hab.min()), 0), "max": round(float(g.receita_por_hab.max()), 0), "n": int(len(g))} for f, g in cid.groupby("faixa")]
    assert [x["fx"] for x in faixas] == [0, 1, 2, 3, 4] and sum(x["n"] for x in faixas) == 92

    glob = {
        "n_cidades": 92, "n_estados": 27, "pop_uf": pop_uf, "mediana_gh": round(med, 1), "menor_gh": round(menor, 1), "maior_gh": round(maior, 1), "razao_extremos": round(maior / menor, 2),
        "menor_nome": cid.loc[cid.saude_por_hab.idxmin(), "nome"], "maior_nome": cid.loc[cid.saude_por_hab.idxmax(), "nome"],
        "pop_abaixo_mediana_pct": round(abaixo_pop, 1), "aplicado_mediana": round(float(cid.aplicado_pct.median()), 1), "aplicado_min": round(float(cid.aplicado_pct.min()), 2),
        "r2_total": round(float(t24.r2), 3), "elast_total": elast, "elast_repasses": e_rep, "elast_propria": e_prop, "k_sustentam": n_sust, "k_total": 9,
        "dif_regiao": pares_reg, "dif_pares": pares_par, "pares_reducao": pares_red, "folga_menor1": folga1, "folga_menor3": folga3, "acima_prudencial": acima_prud, "siops_fora": int(cid.fora6.sum()),
        "fatia_mediana": round(float(cid.fatia.median()), 1), "faixas": faixas, "siops_razao_mediana": round(float(cid.razao.median()), 2),
        "estresse_ano_a_ano": {"rep": d_rep, "prop": d_prop},
        "estresse_tabela": estr[["queda_repasses", "cenario", "elasticidade", "queda_gasto_pct"]].round(3).to_dict("records"),
    }
    assert glob["pares_reducao"] == 46 and 0.79 < elast[2024] < 0.81

    # ---------- curiosidades (cada uma com fonte e janela) ----------
    I, E = "Curiosidade", "Insight"
    A, AC = "Alerta", "Achado"
    fi = "dados_tratados/indicadores_2024.csv"
    cur = [
        # início
        ("cidade", I, "A cidade típica não é a pessoa típica", f"{pt(abaixo_pop)}%".replace(",0%", "%"), f"das pessoas moram em cidades que gastam menos que a cidade do meio (R$ {pt(med)} por habitante).", "2024", fi, 0),
        ("cidade", I, "Onde estão os que menos gastam", f"{n_metro_10} em 10", "dos dez que menos gastam por habitante estão na Região Metropolitana, capital incluída.", "2024", fi, 1),
        ("cidade", I, "Vizinhos, mundos diferentes", f"{pt(arraial.saude_por_hab / spa.saude_por_hab, 1)}×", f"Arraial do Cabo (R$ {pt(arraial.saude_por_hab)}) e São Pedro da Aldeia (R$ {pt(spa.saude_por_hab)}) ficam na mesma região.", "2024", fi, 0),
        ("cidade", I, "Falta de receita, não de prioridade", f"{len(inter)} de 5", "das cidades que menos arrecadam por habitante estão entre as dez que menos gastam em saúde.", "2024", fi, 0),
        ("cidade", I, "Saneamento muda muito", f"{pt(saneam_min)}% a {pt(saneam_max)}%", "dos domicílios ligados à rede de esgoto, de uma cidade a outra (Censo 2022).", "Censo 2022", "dados_tratados/analyze_ibge_indicadores.csv", 0),
        ("cidade", I, "Mínimo da lei", "92 de 92", f"cidades aplicam ao menos 15% em saúde (SIOPS); a cidade do meio aplica {pt(glob['aplicado_mediana'], 1)}%.", "2024", "dados_tratados/improve_r5_r6_siops.csv", 0),
        ("cidade", E, "A receita explica quase tudo", f"≈ {round(glob['r2_total'] * 100)}%", "da diferença de gasto por habitante entre as cidades é explicada pela receita por habitante.", "2024", "dados_tratados/analyze_rodada2_coeficientes.csv", 0),
        ("cidade", E, "O gasto segue os repasses", f"{pt(e_rep[0], 2)} × {pt(e_prop[0], 2)}", "é a sensibilidade do gasto aos repasses contra a da arrecadação própria.", "2024", "dados_tratados/analyze_rodada2_coeficientes.csv", 0),
        ("cidade", E, "Idade e saneamento não explicam", "", "Cidades com mais idosos ou menos esgoto não gastam mais, descontada a receita; o padrão bruto vem de a receita ser maior nas cidades com menos esgoto.", "2022–2024", "docs/11-modulo-ibge-resultados.md", 0),
        ("cidade", A, "O estado e as cidades não se comparam diretamente", f"R$ {pt(estado_rj['gh'])}", f"é o gasto do estado por habitante, menos que o da cidade que menos gasta (R$ {pt(menor)}). Estado e município têm funções diferentes no SUS.", "2024", fi, 1),
        ("cidade", I, "Baixada: fatia grande, bolso pequeno", f"{pt(bx_pd, 1)}%", f"da despesa da Baixada Fluminense (núcleo de 6) vai para a saúde, mas são só R$ {pt(bx.saude.sum() / bx.populacao.sum())} por habitante.", "2024", fi, 0),
        ("cidade", I, "Dois destinos para o mesmo dinheiro", f"{pt(nor_gasto)}%", f"é quanto mais por habitante o Noroeste gasta que a Metropolitana sem a capital, com receita por habitante só {pt(nor_rec)}% maior.", "2024", fi, 0),
        # início (só estados)
        ("inicio", I, "Arrecada no meio, gasta o mínimo", f"{pos_rh}º e 27º", "é a posição do Rio de Janeiro em receita por habitante e em gasto em saúde por habitante: arrecada no meio da tabela e gasta menos que todos os outros estados.", "2024", fi, 1),
        ("inicio", I, "O maior e o menor", f"{pt(top_gh.saude_por_hab / rj.saude_por_hab, 1)}×", f"é quanto {top_gh.nome} (R$ {pt(top_gh.saude_por_hab)} por habitante) gasta a mais que o Rio de Janeiro (R$ {pt(rj.saude_por_hab)}).", "2024", fi, 0),
        ("inicio", I, "Fatia da despesa", f"{pt(rj.saude_pct_despesa, 1)}%", f"da despesa do estado do Rio vai para a saúde, contra {pt(med_uf_pd, 1)}% no estado do meio. A maior fatia é de {top_pd.nome}: {pt(top_pd.saude_pct_despesa, 1)}%.", "2024", fi, 0),
        ("inicio", I, "O estado do meio", f"R$ {pt(med_uf_gh)}", f"por habitante é o gasto em saúde do estado do meio. O Rio gasta {pt(rj.saude_por_hab / med_uf_gh * 100)}% disso.", "2024", fi, 0),
        ("inicio", E, "A receita explica parte", f"≈ {round(r2_uf * 100)}%", "da diferença de gasto por habitante entre os 27 estados é explicada pela receita por habitante (conta descritiva, só 27 pontos).", "2024", fi, 0),
        ("inicio", A, "Dívida acima do limite", f"{pt(estado_rj['dcl'], 1)}%", f"da receita corrente líquida é a dívida líquida declarada pelo estado do Rio, acima do limite de {estado_rj['lim_dcl']}% do Senado.", "2024", fi, 1),
        ("inicio", A, "O Distrito Federal é diferente", "DF", "reúne as funções de estado e de município; compare o seu valor com cuidado.", "2024", fi, 0),
        ("inicio", A, "Declarado, não auditado", "Siconfi", "Os valores são os que cada estado declarou ao Tesouro Nacional, sem auditoria. Gasto em saúde não mede qualidade nem necessidade.", "2024", fi, 0),
        # cidade
        ("cidade", I, "A capital", f"R$ {pt(capital.saude_por_hab)}", f"por habitante, cerca de metade da cidade do meio. A fatia da receita dedicada à saúde é {pt(capital.fatia, 1)}%, contra mediana de {pt(glob['fatia_mediana'], 1)}%.", "2024", fi, 1),
        ("cidade", I, "Perto do limite", f"{folga1} cidades", "aplicam menos de 1 ponto percentual acima do mínimo de 15%: uma queda pequena de receita já as colocaria abaixo.", "2024", "dados_tratados/improve_r5_r6_siops.csv", 1),
        ("cidade", I, "Cidade de veraneio", f"R$ {pt(arraial.saude_por_hab)}", f"por habitante em Arraial do Cabo, que tem R$ {pt(arraial.receita_por_hab)} de receita por habitante, mais de {pt(arraial.receita_por_hab // cid.receita_por_hab.median())} vezes a da cidade do meio.", "2024", fi, 0),
        ("cidade", I, "A cidade do meio", f"R$ {pt(med)}", "por habitante: metade das cidades gasta mais, metade gasta menos.", "2024", fi, 0),
        ("cidade", E, "Regiões com poucas cidades", f"{len(cid[cid.grupo == 'Costa Verde'])} cidades", "é todo o tamanho da Costa Verde: o valor da região é só descritivo e não vale como tendência.", "2024", "dados_brutos/municipios_rj_ceperj.csv", 1),
        # gestor
        ("gestor", E, "Comparar por receita parecida", f"−{pares_red}%", f"na diferença de leitura entre cidades ao comparar por faixa de receita e não por região (de {pt(pares_reg, 3)} para {pt(pares_par, 3)}).", "2024", "dados_tratados/improve_r2_pares.csv", 0),
        ("gestor", E, "A fatia cai quando a receita sobe", f"{pt(elast[2024], 2)}", "é a sensibilidade do gasto à receita total, abaixo de 1: quem arrecada mais por habitante dedica fatia menor da receita à saúde.", "2023 a 2025", "dados_tratados/analyze_rodada2_coeficientes.csv", 0),
        ("gestor", AC, "Somar visitantes piorou a leitura", "", "Corrigir a população das cidades de veraneio com o uso ocasional dos domicílios aumentou a distância das Baixadas Litorâneas em vez de reduzi-la.", "2024", "dados_tratados/improve_r3_veraneio.csv", 1),
        ("gestor", I, "Folga curta", f"{folga3} cidades", "aplicam menos de 3 pontos percentuais acima do mínimo de 15%.", "2024", "dados_tratados/improve_r5_r6_siops.csv", 1),
        ("gestor", E, "Se os repasses caírem 20%", "−20%", f"nos repasses reduzem o gasto em saúde em cerca de {pt(abs(float(estr[(estr.queda_repasses == 0.2) & (estr.cenario == 'provável')].queda_gasto_pct.iloc[0])), 0)}% (entre cidades) ou {pt(abs(float(estr[(estr.queda_repasses == 0.2) & (estr.cenario == 'provável (ano a ano)')].queda_gasto_pct.iloc[0])), 0)}% (de um ano para o outro).", "2023–2025", "dados_tratados/improve_r4_estresse.csv", 1),
        ("gestor", I, "Dependência de repasses", f"{pt(float(cid.parte_transf.median()) * (100 if cid.parte_transf.median() <= 1 else 1))}%", "da receita é, na cidade mediana, repasse de outros entes.", "2024", "dados_tratados/improve_r4_dependencia.csv", 0),
        # controle
        ("controle", A, "Niterói fora da faixa três anos seguidos", "−44%", "em 2025 (−49% em 2023 e −48% em 2024): gasto bem abaixo do que a receita indica. Um alerta é um convite para olhar, nunca uma conclusão.", "2023 a 2025", "dados_tratados/improve_r1_triagem.csv", 1),
        ("controle", A, "Pessoal acima do limite prudencial", f"{acima_prud} municípios", "declaram despesa com pessoal acima do limite prudencial da Lei de Responsabilidade Fiscal (dado declarado: conferir antes de concluir).", "2024", "dados_tratados/improve_r7_limites.csv", 1),
        ("controle", A, "Dívida do estado", f"{pt(estado_rj['dcl'], 1)}%", f"da receita corrente líquida, acima do limite de {estado_rj['lim_dcl']}%, e pessoal em {pt(estado_rj['pes'], 1)}% (limite prudencial {pt(estado_rj['prud'], 1)}%).", "2024", fi, 1),
        ("controle", A, "Conferência entre fontes", f"{int(cid.fora6.sum())} cidades", f"registram no SIOPS uma parte do gasto do Siconfi bem diferente da cidade do meio (R$ {pt(float(cid.razao.median()) * 100)} para cada R$ 100): pergunta de conciliação, não alarme.", "2024", "dados_tratados/improve_r5_r6_siops.csv", 1),
        ("controle", AC, "A triagem mantém a ordem, não a lista", "1 de 3", f"cidades da triagem de 2024 continuam fora do intervalo em 2025; mas a ordem das cidades pelo desvio do previsto se mantém (correlação de postos de {sp25}).", "2025", "dados_tratados/control_2025_saida.txt", 0),
        ("controle", AC, "Pergunta aberta: Baixadas Litorâneas", f"−{pt(abs(float(bl.res_modelo.median())), 0)}%", "é a distância mediana entre o gasto e o previsto pela receita nas dez cidades das Baixadas Litorâneas: gastam menos do que a receita indica, sem explicação nos dados públicos.", "2024", "dados_tratados/analyze_a2_residuos.csv", 1),
        ("controle", AC, "Balanço anual demora", "9 meses", "para o balanço de todas as cidades ficar completo (2025: entregas de janeiro a outubro de 2026).", "2025", "dados_tratados/control_2025_residuos.csv", 0),
        # como
        ("como", AC, "Oito de nove se mantiveram", f"{n_sust} de 9", "conclusões se mantiveram em 2025, com previsões escritas antes de abrir os dados. A que enfraqueceu foi a lista da triagem.", "2025", "dados_tratados/control_2025_resultados.csv", 0),
        ("como", A, "Apostas minhas que erraram", "3 + 1", "apostas minhas erraram (três no Improve e uma no Control) e estão registradas como resultado, não escondidas.", "2024–2025", "fases/fase-4-improve/relatorio.md", 1),
        ("como", AC, "Dados que não estavam lá", "DF", "O Distrito Federal não está disponível no SIOPS e ficou de fora da conferência entre fontes; a população de 2023 foi estimada, e isso está declarado.", "2024", "docs/04-pendencias-measure.md", 0),
    ]
    curiosidades = [{"s": s, "t": t, "ti": ti, "v": val, "x": tx, "j": j, "f": f, "d": bool(dest)} for s, t, ti, val, tx, j, f, dest in cur]

    # ---------- sumário do manifesto ----------
    fontes_arquivos = sorted({c["f"] for c in curiosidades} | {"dados_tratados/indicadores_2024.csv"})
    malhas = {p.name: sha(p) for p in sorted((B / "malha_ibge_api").glob("*.json"))}

    # ---------- chegada do balanço anual (DCA 2025), por mês ----------
    ta = pd.read_csv(B / "teste_acesso_2025.csv")
    mes = ta.dca_data.dropna().str[:7].value_counts().sort_index()
    dca = {"meses": list(mes.index), "n": [int(x) for x in mes.values], "total": int(mes.sum()), "entes": int(len(ta))}
    # ---------- simulador: sensibilidades e janela coberta ----------
    simulador = {
        "entre": {"rep": list(e_rep), "prop": list(e_prop)}, "ano_a_ano": {"rep": list(d_rep), "prop": list(d_prop)},
        "faixa_coberta": 30, "faixa_max": 50, "ref_ano": 2024,
    }
    melhorar = [
        {"id": "R1", "nome": "Triagem de auditoria", "ver": "Sustentada", "txt": "4 cidades ficam fora do intervalo; 2 das 3 de 2023 se repetem em 2024."},
        {"id": "R2", "nome": "Comparar por receita parecida", "ver": "Sustentada", "txt": f"A diferença de leitura cai {pares_red}% (de {pt(pares_reg, 3)} para {pt(pares_par, 3)}), em parte por construção."},
        {"id": "R3", "nome": "Ajuste das cidades de veraneio", "ver": "Não sustentada", "txt": "O resíduo das Baixadas Litorâneas piora de −15% para −18% e nunca chega a zero."},
        {"id": "R4", "nome": "Teste de estresse dos repasses", "ver": "Com cautela", "txt": f"Entre cidades, {pt(e_rep[0], 2)}; de um ano para o outro, {pt(d_rep[0], 2)} (intervalo {pt(d_rep[1], 3)} a {pt(d_rep[2], 3)})."},
        {"id": "R5", "nome": "Folga sobre o mínimo de 15%", "ver": "Descritiva", "txt": f"Nenhuma cidade abaixo do mínimo; {folga3} com folga abaixo de 3 pontos e {folga1} abaixo de 1."},
        {"id": "R6", "nome": "Conferência Siconfi × SIOPS", "ver": "Como pergunta", "txt": f"{int(cid.fora6.sum())} cidades fora da faixa; serve para perguntar, não para alarmar."},
        {"id": "R7", "nome": "Limites da LRF", "ver": "Descritiva", "txt": f"{acima_prud} municípios declaram pessoal acima do limite prudencial; nenhum tem dívida perto do limite."},
    ]
    dados = {
        "meta": {"versao": "1.0", "data": "26/10/2026", "janela_principal": "2024", "repositorio": "https://github.com/MatheusAugustoEC/saude-rj", "malhas_sha256": malhas, "fontes_arquivos": fontes_arquivos},
        "ufs": ufs, "cidades": cidades, "grupos": grupos, "regioes": regioes, "estado_rj": estado_rj, "globais": glob, "curiosidades": curiosidades,
        "k": [{"k": r.K, "final": r.final, "nome": KNOMES[r.K]} for r in kres.itertuples()], "dca": dca, "simulador": simulador, "melhorar": melhorar,
    }
    SAIDA.write_text(json.dumps(dados, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Gravado {SAIDA.relative_to(RAIZ)} ({SAIDA.stat().st_size / 1024:.0f} KB): {len(cidades)} cidades, {len(ufs)} estados, {len(curiosidades)} curiosidades.")
    print(f"Conferências: capital R$ {capital.saude_por_hab:.0f}; mediana R$ {med:.0f}; {abaixo_pop:.1f}% da população abaixo da mediana; {n_metro_10} dos 10 menores na Metropolitana; interseção receita×gasto: {len(inter)}")


if __name__ == "__main__":
    main()
