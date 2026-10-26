"""Gera o mapa do Marco 2, versão C (segunda imagem): uma cor chapada por região, contorno preto e tabela por região.

Uso: python -X utf8 -u scripts/18_gerar_mapa_regioes_tabela.py
Grava em imagens/: marco2_mapa_C_regioes.png e .svg (horizontal, 1920 x 1080 px).

A cor aqui só IDENTIFICA a região (10 grupos: a capital, o núcleo da Baixada, o resto da Metropolitana e as outras 7 regiões do CEPERJ).
Como são mais de 3 cores num mapa, a identificação não depende só da cor: cada região tem o nome escrito e contorno preto grosso.
O valor (gasto por habitante) está na tabela, calculado somando o gasto e dividindo pela soma da população de cada região.
"""
import _mapa_comum as c
from _mapa_comum import (BAIXADA, CAPITAL, FUNDO, GRUPOS, H, INTERIOR, LINHA, RESTO, TEXTO, TEXTO_2, br, caixa, contornos, eixo, limites,
                         mistura, pinta, poder_mde, texto)
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from shapely.ops import unary_union

mun, menores, maiores = c.carrega_dados()
CORES = {CAPITAL: "#6250d6", BAIXADA: "#eb6834", RESTO: mistura("#e87ba4", 0.12), "Costa Verde": mistura("#1baf7a", 0.25),
         "Baixadas Litorâneas": mistura("#eda100", 0.30), "Médio Paraíba": mistura("#008300", 0.50), "Centro-Sul Fluminense": mistura("#2a78d6", 0.38),
         "Serrana": mistura("#e34948", 0.40), "Noroeste Fluminense": "#d2b48c", "Norte Fluminense": mistura("#9aa5b1", 0.10)}
mun["cor"] = mun.grupo.map(CORES)

# ---------------------------------------------------------------------------- números por grupo (soma ÷ soma)
tab = []
for g in GRUPOS:
    d = mun[mun.grupo == g]
    mde = poder_mde(mun, g)
    tab.append({"grupo": g, "n": len(d), "pop": d.populacao.sum() / 1e6, "gasto": d.saude.sum() / d.populacao.sum(),
                "receita": d.receita.sum() / d.populacao.sum(), "so_descreve": (mde is None) or (mde >= 50)})
tab = sorted(tab, key=lambda r: -r["gasto"])

fig, fundo = c.tela()
texto(fundo, 50, 55, "O estado do Rio em regiões", px=56, peso="bold", cor="#1f2933")
texto(fundo, 50, 120, "e quanto cada uma gasta em saúde por habitante", px=56, peso="bold", cor="#1f2933")
texto(fundo, 50, 178, "Capital e Baixada (núcleo de 6 municípios) separadas da Metropolitana; as outras sete são as regiões de governo do CEPERJ. 2024.", px=26, cor=TEXTO_2)

# ---------------------------------------------------------------------------- mapa
ax = eixo(fig, 40, 205, 1010, 745)
pinta(ax, mun, lambda r: r.cor, lw_mun=0.6)
contornos(ax, mun, lw=3.2)
limites(ax, mun)
ax.apply_aspect()
fig.canvas.draw()
HALO = [pe.withStroke(linewidth=4.5, foreground="#ffffff")]
DESLOCA = {"Serrana": (0.00, 0.10), "Costa Verde": (-0.03, -0.12), "Noroeste Fluminense": (0.0, 0.0), "Norte Fluminense": (0.0, 0.0),
           "Centro-Sul Fluminense": (-0.02, 0.0), "Médio Paraíba": (-0.02, 0.0)}
for nome in [n for n in INTERIOR if n != "Baixadas Litorâneas"]:
    p = unary_union(list(mun[mun.grupo == nome].geom)).representative_point()
    dx, dy = DESLOCA.get(nome, (0, 0))
    ax.text(p.x + dx, p.y + dy, nome.replace(" Fluminense", "\nFluminense").replace("Médio ", "Médio\n"), fontsize=21 * c.PT, fontweight="bold",
            color="#0b0b0b", ha="center", va="center", zorder=12, path_effects=HALO, linespacing=1.05)
metro = mun[mun.regiao8 == "Metropolitana"]
mb = unary_union(list(metro.geom)).bounds
m_ = 0.03
ax.add_patch(Rectangle((mb[0] - m_, mb[1] - m_), mb[2] - mb[0] + 2 * m_, mb[3] - mb[1] + 2 * m_, fc="none", ec="#1f2933", lw=2.2, ls=(0, (5, 3)), zorder=15))
for nome, (lx_, ly_), rot in (("Metropolitana", (470, 905), "Metropolitana\n(ver zoom)"), ("Baixadas Litorâneas", (905, 825), "Baixadas\nLitorâneas")):
    g = unary_union(list(mun[mun.regiao8 == nome].geom if nome == "Metropolitana" else list(mun[mun.grupo == nome].geom))).representative_point()
    ex, ey = ax.transData.transform((g.x, g.y))
    fundo.plot([lx_, ex], [ly_ - 10, H - ey], color="#1f2933", lw=1.6, zorder=11)
    fundo.add_patch(plt.Circle((ex, H - ey), 5, fc="#1f2933", ec="#ffffff", lw=1.2, zorder=12))
    texto(fundo, lx_, ly_, rot, px=21, peso="bold", cor="#1f2933", ha="center", halo=True, z=13)

# ---------------------------------------------------------------------------- zoom
zx, zy, zw, zh = 1075, 205, 805, 345
caixa(fundo, zx, zy, zw, zh, "#ffffff", "#1f2933", lw=2.4, raio=14, tracejado=True)
az = eixo(fig, zx + 8, zy + 34, zw - 16, zh - 40)
pinta(az, metro, lambda r: r.cor, lw_mun=1.0)
contornos(az, metro, lw=3.2)
az.set_xlim(mb[0] - 0.005, mb[2] + 0.005)
az.set_ylim(mb[1] - 0.005, mb[3] + 0.005)
az.set_aspect("equal")
az.axis("off")
az.apply_aspect()
fig.canvas.draw()
texto(fundo, zx + 16, zy + 20, "Zoom: Região Metropolitana", px=22, peso="bold", cor="#1f2933")
inv = az.transData.inverted()
cap = mun[mun.grupo == CAPITAL].iloc[0].geom.representative_point()
az.text(cap.x, cap.y - 0.01, "Capital", fontsize=22 * c.PT, fontweight="bold", color="#ffffff", ha="center", va="center", zorder=31,
        path_effects=[pe.withStroke(linewidth=4, foreground="#000000")])
nuc_pts = unary_union(list(mun[mun.grupo == BAIXADA].geom)).representative_point()
bx, by = inv.transform((zx + 215, H - (zy + 88)))
az.plot([nuc_pts.x, bx], [nuc_pts.y, by], color="#0b0b0b", lw=1.6, zorder=25)
az.text(bx, by, "Baixada\n(núcleo de 6)", fontsize=21 * c.PT, fontweight="bold", color="#0b0b0b", ha="center", va="center", zorder=31, path_effects=HALO, linespacing=1.0)
rx, ry = inv.transform((zx + zw - 170, H - (zy + 235)))
az.text(rx, ry, "Resto da\nMetropolitana", fontsize=20 * c.PT, fontweight="bold", color="#0b0b0b", ha="center", va="center", zorder=31, path_effects=HALO, linespacing=1.0)

# ---------------------------------------------------------------------------- tabela por região
x0, y0 = 1075, 568
texto(fundo, x0, y0, "Quanto cada região gasta (soma do gasto ÷ soma da população)", px=22, peso="bold")
cab = y0 + 34
for x, s, ha in ((x0 + 295, "mun.", "right"), (x0 + 370, "hab. (mi)", "right"), (x0 + 390, "gasto por habitante (R$)", "left"), (x0 + 805, "receita (R$)", "right")):
    texto(fundo, x, cab, s, px=16, cor=TEXTO_2, ha=ha)
vmax = max(r["gasto"] for r in tab)
for i, r in enumerate(tab):
    yy = y0 + 62 + i * 30
    fundo.add_patch(Rectangle((x0, yy - 10), 20, 20, fc=CORES[r["grupo"]], ec="#000000", lw=1.8, zorder=4))
    texto(fundo, x0 + 30, yy, r["grupo"].replace("Metropolitana (resto, 15)", "Metropolitana (resto)").replace("Baixada (núcleo de 6)", "Baixada (núcleo de 6)"), px=19)
    texto(fundo, x0 + 295, yy, f"{r['n']}" + ("†" if r["so_descreve"] else ""), px=19, ha="right")
    texto(fundo, x0 + 370, yy, br(r["pop"], 1), px=19, ha="right")
    larg = 200 * r["gasto"] / vmax
    fundo.add_patch(Rectangle((x0 + 390, yy - 9), larg, 18, fc="#52514e", ec="none", zorder=4))
    marca = "  menor" if i == len(tab) - 1 else ("  maior" if i == 0 else "")
    texto(fundo, x0 + 390 + larg + 8, yy, f"{br(r['gasto'])}{marca}", px=19, peso="bold" if marca else "normal")
    texto(fundo, x0 + 805, yy, br(r["receita"]), px=19, ha="right", cor=TEXTO_2)
texto(fundo, x0, y0 + 62 + 10 * 30 + 2, "† só descreve: poucos municípios para testar diferença (regra de poder estatístico).", px=17, cor=TEXTO_2)

# ---------------------------------------------------------------------------- faixa inferior
caixa(fundo, 40, 962, 1840, 76, "#f6f5fb", "#1f2933", lw=1.8, z=1)
texto(fundo, 60, 984, "Como ler: cada cor é uma região e a cor só identifica o lugar; o valor está na tabela. Contorno preto separa as regiões, e os nomes estão no mapa.", px=20, cor=TEXTO)
texto(fundo, 60, 1014, "A capital faz parte da Metropolitana do CEPERJ, mas aparece separada. Baixada (núcleo de 6) é escolha analítica, não é região oficial. Gasto não é qualidade.", px=20, cor=TEXTO)
texto(fundo, 50, 1062, "Dados declarados pelos entes (Siconfi), 2024, população IBGE, sem auditoria. Projeto aberto no GitHub: MatheusAugustoEC/saude-rj", px=19, cor=TEXTO_2)

fig.savefig(c.SAIDA / "marco2_mapa_C_regioes.png", dpi=100, facecolor=FUNDO)
fig.savefig(c.SAIDA / "marco2_mapa_C_regioes.svg", facecolor=FUNDO)
print("Gravado marco2_mapa_C_regioes.png")
for r in tab:
    print(f"{r['grupo']:28s} n={r['n']:2d} pop={r['pop']:.2f} gasto={r['gasto']:.0f} receita={r['receita']:.0f} so_descreve={r['so_descreve']}")
