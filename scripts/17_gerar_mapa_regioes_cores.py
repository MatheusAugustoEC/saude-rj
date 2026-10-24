"""Gera o mapa do Marco 2, versão B: uma família de cor por grupo de região, com o tom indicando o gasto.

Uso: python -X utf8 -u scripts/17_gerar_mapa_regioes_cores.py
Grava em imagens/: marco2_mapa_B_cores.png e .svg (horizontal, 1920 x 1080 px).

Regras de cor (visualização): 4 famílias (capital, Baixada núcleo, resto da Metropolitana, interior em tom neutro), 5 degraus em cada,
com a MESMA luminosidade nos degraus de todas as famílias (o mesmo tom quer dizer o mesmo valor em qualquer região);
mais escuro = gasta mais. Contorno preto grosso em volta de cada grupo de região. Os 10 que menos gastam: só o número em círculo.
"""
import _mapa_comum as c
from _mapa_comum import (BAIXADA, CAPITAL, FUNDO, GRUPOS, H, INTERIOR, LINHA, RESTO, ROTULOS_CLASSE, TEXTO, TEXTO_2, W, br, caixa, classe,
                         contornos, eixo, limites, numeros_do_zoom, pinta, rampa, texto)
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from shapely.ops import unary_union
import matplotlib.patheffects as pe

mun, menores, maiores = c.carrega_dados()
mediana = mun.v.median()
n_metro10 = int((menores.regiao8 == "Metropolitana").sum())
n_metro = int((mun.regiao8 == "Metropolitana").sum())

BASES = {"capital": "#1baf7a", "baixada": "#eb6834", "resto": "#2a78d6"}
RAMPAS = {"capital": rampa(BASES["capital"]), "baixada": rampa(BASES["baixada"]), "resto": rampa(BASES["resto"]), "interior": rampa("#9aa5b1", neutro=True)}
NOME_FAM = {"capital": "Capital", "baixada": "Baixada (núcleo de 6)", "resto": "Resto da Metropolitana (15)", "interior": "Interior (7 regiões)"}
FAM_DE = {CAPITAL: "capital", BAIXADA: "baixada", RESTO: "resto"}
mun["fam"] = mun.grupo.map(lambda g: FAM_DE.get(g, "interior"))
mun["cor"] = [RAMPAS[f][classe(v)] for f, v in zip(mun.fam, mun.v)]
menores["fam"] = menores.grupo.map(lambda g: FAM_DE.get(g, "interior"))

fig, fundo = c.tela()
texto(fundo, 50, 55, f"{n_metro10} dos 10 municípios que menos gastam em saúde", px=56, peso="bold", cor="#1f2933")
texto(fundo, 50, 120, "por habitante estão na Região Metropolitana", px=56, peso="bold", cor="#1f2933")
texto(fundo, 50, 178, f"Os {n_metro} municípios da Metropolitana (a capital incluída) são {n_metro / len(mun) * 100:.0f}% dos 92 do RJ, mas "
      f"{n_metro10 / 10 * 100:.0f}% dos dez que menos gastam. Gasto em saúde por habitante, 2024.", px=26, cor=TEXTO_2)

# ---------------------------------------------------------------------------- mapa principal
ax = eixo(fig, 40, 205, 1010, 745)
pinta(ax, mun, lambda r: r.cor)
contornos(ax, mun, lw=3.0)
limites(ax, mun)
ax.apply_aspect()
fig.canvas.draw()
DESLOCA = {"Serrana": (0.00, 0.10), "Costa Verde": (-0.03, -0.12), "Noroeste Fluminense": (0.0, 0.0), "Norte Fluminense": (0.0, 0.0),
           "Centro-Sul Fluminense": (-0.02, 0.0), "Médio Paraíba": (-0.02, 0.0)}
HALO = [pe.withStroke(linewidth=4.5, foreground="#ffffff")]
for nome in [n for n in INTERIOR if n != "Baixadas Litorâneas"]:
    g = unary_union(list(mun[mun.grupo == nome].geom))
    p = g.representative_point()
    dx, dy = DESLOCA.get(nome, (0, 0))
    quebra = nome.replace(" Fluminense", "\nFluminense").replace("Baixadas ", "Baixadas\n").replace("Médio ", "Médio\n")
    ax.text(p.x + dx, p.y + dy, quebra, fontsize=21 * c.PT, fontweight="bold", color="#1f2933", ha="center", va="center", zorder=12,
            path_effects=HALO, linespacing=1.05)
metro = mun[mun.regiao8 == "Metropolitana"]
mb = unary_union(list(metro.geom)).bounds
m_ = 0.03
ax.add_patch(Rectangle((mb[0] - m_, mb[1] - m_), mb[2] - mb[0] + 2 * m_, mb[3] - mb[1] + 2 * m_, fc="none", ec="#1f2933", lw=2.2, ls=(0, (5, 3)), zorder=15))
for r in menores.itertuples():
    if r.regiao8 != "Metropolitana":
        p = r.geom.representative_point()
        ax.add_patch(plt.Circle((p.x, p.y), 0.045, fc="#ffffff", ec="#000000", lw=2.2, zorder=20))
        ax.text(p.x, p.y, str(r.rank), fontsize=17 * c.PT, color="#000000", ha="center", va="center", fontweight="bold", zorder=21)
# a Metropolitana é ampliada ao lado: o nome vai para o mar, com linha-guia
pm = unary_union(list(metro.geom)).representative_point()
ex, ey = ax.transData.transform((pm.x, pm.y))
fundo.plot([470, ex], [895, H - ey], color="#1f2933", lw=1.6, zorder=11)
fundo.add_patch(plt.Circle((ex, H - ey), 5, fc="#1f2933", ec="#ffffff", lw=1.2, zorder=12))
texto(fundo, 470, 905, "Metropolitana\n(ver zoom)", px=21, peso="bold", cor="#1f2933", ha="center", halo=True, z=13)
pb = unary_union(list(mun[mun.grupo == "Baixadas Litorâneas"].geom)).representative_point()
bx_, by_ = ax.transData.transform((pb.x, pb.y))
fundo.plot([905, bx_], [825, H - by_], color="#1f2933", lw=1.6, zorder=11)
fundo.add_patch(plt.Circle((bx_, H - by_), 5, fc="#1f2933", ec="#ffffff", lw=1.2, zorder=12))
texto(fundo, 905, 825, "Baixadas\nLitorâneas", px=21, peso="bold", cor="#1f2933", ha="center", halo=True, z=13)

# ---------------------------------------------------------------------------- legenda (4 famílias x 5 degraus)
lx, ly = 66, 250
caixa(fundo, lx - 12, ly - 38, 500, 312, "#ffffff", LINHA, lw=1.6, z=3)
texto(fundo, lx, ly - 14, "Gasto em saúde por habitante", px=22, peso="bold")
texto(fundo, lx, ly + 12, "mais escuro = gasta mais (R$ por habitante)", px=18, cor=TEXTO_2)
for j, rot in enumerate(ROTULOS_CLASSE):
    cx_ = lx + 210 + j * 54
    texto(fundo, cx_ + 25, ly + 50, rot.replace(" a ", "\na ").replace("até ", "até\n").replace("mais de ", "mais de\n"), px=14, cor=TEXTO_2, ha="center", espaco=1.0)
for i, fam in enumerate(["capital", "baixada", "resto", "interior"]):
    yy = ly + 108 + i * 38
    texto(fundo, lx, yy, NOME_FAM[fam].replace(" (15)", "").replace(" (7 regiões)", ""), px=19, cor=TEXTO)
    for j, cor in enumerate(RAMPAS[fam]):
        fundo.add_patch(Rectangle((lx + 210 + j * 54, yy - 14), 50, 28, fc=cor, ec="#ffffff", lw=1.5, zorder=4))
texto(fundo, lx, ly + 252, f"mediana dos 92 municípios: R$ {br(mediana)}", px=17, cor=TEXTO_2)

# ---------------------------------------------------------------------------- zoom na Metropolitana
zx, zy, zw, zh = 1075, 205, 805, 345
caixa(fundo, zx, zy, zw, zh, "#ffffff", "#1f2933", lw=2.4, raio=14, tracejado=True)
az = eixo(fig, zx + 8, zy + 34, zw - 16, zh - 40)
pinta(az, metro, lambda r: r.cor, lw_mun=1.0)
contornos(az, metro, lw=3.0)
az.set_xlim(mb[0] - 0.005, mb[2] + 0.005)
az.set_ylim(mb[1] - 0.005, mb[3] + 0.005)
az.set_aspect("equal")
az.axis("off")
az.apply_aspect()
fig.canvas.draw()
texto(fundo, zx + 16, zy + 20, "Zoom: Região Metropolitana", px=22, peso="bold", cor="#1f2933")
numeros_do_zoom(az, menores)
# nomes dos três grupos da Metropolitana, no próprio zoom
cap = mun[mun.grupo == CAPITAL].iloc[0].geom.representative_point()
az.text(cap.x - 0.005, cap.y - 0.062, "Capital", fontsize=22 * c.PT, fontweight="bold", color="#0b0b0b", ha="center", va="center", zorder=31, path_effects=HALO)
resto = mun[mun.grupo == RESTO]
rx_, ry_ = az.transData.inverted().transform((zx + zw - 175, H - (zy + 235)))
az.text(rx_, ry_, "Resto da\nMetropolitana", fontsize=20 * c.PT, fontweight="bold", color="#0b0b0b", ha="center", va="center", zorder=31, path_effects=HALO, linespacing=1.0)
caxias = mun[mun.cod_ibge == mun[mun.ente == "Duque de Caxias"].cod_ibge.iloc[0]].iloc[0].geom.representative_point()
inv = az.transData.inverted()
bx, by = inv.transform((zx + zw - 135, H - (zy + 95)))
az.plot([caxias.x, bx], [caxias.y, by], color="#0b0b0b", lw=1.6, zorder=25)
az.text(bx, by, "Baixada\n(núcleo de 6)", fontsize=20 * c.PT, fontweight="bold", color="#0b0b0b", ha="center", va="center", zorder=31, path_effects=HALO, linespacing=1.0)

# ---------------------------------------------------------------------------- lista dos 10 que menos gastam
lx0, ly0 = 1075, 568
texto(fundo, lx0, ly0, "Os 10 que menos gastam (R$ por habitante)", px=24, peso="bold")
vmax = menores.v.max()
CURTO = {CAPITAL: "Capital", BAIXADA: "Baixada", RESTO: "Metropolitana"}
for i, r in enumerate(menores.itertuples()):
    yy = ly0 + 36 + i * 30
    c.bolha  # noqa
    fundo.add_patch(plt.Circle((lx0 + 14, yy), 13, fc="#ffffff", ec="#000000", lw=2.2, zorder=20))
    fundo.text(lx0 + 14, yy, str(r.rank), fontsize=13 * 1.15 * c.PT, color="#000000", ha="center", va="center", fontweight="bold", zorder=21)
    texto(fundo, lx0 + 38, yy, r.ente.replace(" (capital)", ""), px=21)
    cor = RAMPAS[r.fam][3]
    largura = 170 * r.v / vmax
    fundo.add_patch(Rectangle((lx0 + 360, yy - 9), largura, 18, fc=cor, ec="#1f2933", lw=1.0, zorder=4))
    texto(fundo, lx0 + 360 + largura + 8, yy, f"R$ {br(r.v)}", px=21)
    texto(fundo, lx0 + 668, yy, CURTO.get(r.grupo, r.grupo.replace(" Fluminense", "").replace("Baixadas Litorâneas", "B. Litorâneas")), px=18, cor=TEXTO_2)
mais = " · ".join(f"{r.ente} R$ {br(r.v)}" for r in maiores.itertuples())
texto(fundo, lx0, ly0 + 36 + 10 * 30 + 4, f"Os 3 que mais gastam: {mais}", px=19, cor=TEXTO_2, largura=72)

# ---------------------------------------------------------------------------- faixa inferior
caixa(fundo, 40, 962, 1840, 76, "#f6f5fb", "#1f2933", lw=1.8, z=1)
texto(fundo, 60, 984, "Como ler: cada polígono é um município. A cor mostra o grupo (capital, Baixada, resto da Metropolitana ou interior) e o tom mostra o gasto: quanto mais escuro, mais gasta.", px=20, cor=TEXTO)
texto(fundo, 60, 1014, "Contorno preto separa as regiões do CEPERJ. O número marca os 10 que menos gastam. Quadro tracejado: a Metropolitana ampliada. Baixada: escolha analítica, não é região oficial.", px=20, cor=TEXTO)
texto(fundo, 50, 1062, "Dados declarados pelos entes (Siconfi), 2024, população IBGE, sem auditoria. Gasto em saúde não é qualidade. Projeto aberto no GitHub: MatheusAugustoEC/saude-rj", px=19, cor=TEXTO_2)

fig.savefig(c.SAIDA / "marco2_mapa_B_cores.png", dpi=100, facecolor=FUNDO)
fig.savefig(c.SAIDA / "marco2_mapa_B_cores.svg", facecolor=FUNDO)
print("Gravado marco2_mapa_B_cores.png")
for fam, r_ in RAMPAS.items():
    print(fam, r_, [round(c.hex_oklch(x)[0], 2) for x in r_])
