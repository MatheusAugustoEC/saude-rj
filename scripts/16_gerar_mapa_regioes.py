"""Gera o mapa do Marco 2: gasto em saúde por habitante, por município, com as 8 regiões do CEPERJ.

Uso: python -X utf8 -u scripts/16_gerar_mapa_regioes.py
Grava em imagens/: marco2_mapa_regioes.png e .svg (horizontal, 1920 x 1080 px).

Mensagem: 8 dos 10 municípios que menos gastam em saúde por habitante estão na Região Metropolitana (a capital incluída).
Fontes (nada digitado à mão): dados_tratados/indicadores_measure_2024.csv e a malha municipal do IBGE (dados_brutos/malha_rj).
Cores (regra de visualização): escala divergente, duas famílias (azul = abaixo da mediana, laranja = acima), cinza neutro no meio,
dois degraus por lado. A mediana (R$ 2.319) fica dentro da classe neutra. Contorno preto = os 10 que menos gastam.
"""
import struct
import textwrap
import unicodedata
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch, PathPatch, Rectangle
from matplotlib.path import Path as MPath
from shapely.geometry import Polygon
from shapely.ops import unary_union

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "imagens"
SAIDA.mkdir(exist_ok=True)

FUNDO, TEXTO, TEXTO_2, CINZA, LINHA = "#fcfcfb", "#0b0b0b", "#52514e", "#9aa5b1", "#c9ccd1"
AZUL_ESC, AZUL_CLA, NEUTRO, LAR_CLA, LAR_ESC = "#184f95", "#86b6ef", "#f0efec", "#f1a285", "#b04e27"
VIOLETA = "#6250d6"
plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
W, H = 1920, 1080
PT = 0.72

# ------------------------------------------------------------------------------------------ dados
ind = pd.read_csv(RAIZ / "dados_tratados" / "indicadores_measure_2024.csv", dtype={"cod_ibge": str})
mun = ind[ind.esfera == "M"].copy()
mun["regiao8"] = mun.regiao_ceperj.replace({"Capital (Rio de Janeiro)": "Metropolitana", "Metropolitana (sem a capital)": "Metropolitana"})
mun["v"] = mun.saude / mun.populacao
mediana = mun.v.median()
mun = mun.sort_values("v").reset_index(drop=True)
menores = mun.head(10).copy()
menores["rank"] = range(1, 11)
maiores = mun.tail(3).iloc[::-1]
n_metro10 = int((menores.regiao8 == "Metropolitana").sum())
n_metro = int((mun.regiao8 == "Metropolitana").sum())

CLASSES = [(0, 1400, AZUL_ESC, "até R$ 1.400"), (1400, 2000, AZUL_CLA, "R$ 1.400 a 2.000"),
           (2000, 2700, NEUTRO, "R$ 2.000 a 2.700"), (2700, 4000, LAR_CLA, "R$ 2.700 a 4.000"), (4000, 1e9, LAR_ESC, "mais de R$ 4.000")]


def cor_de(v):
    for lo, hi, cor, _ in CLASSES:
        if lo <= v < hi:
            return cor


mun["cor"] = mun.v.map(cor_de)


def br(x, casas=0):
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ------------------------------------------------------------------------------------------ malha (shapefile sem biblioteca extra)
def le_malha():
    base = RAIZ / "dados_brutos" / "malha_rj" / "RJ_Municipios_2024"
    dbf = (base.with_suffix(".dbf")).read_bytes()
    n_reg, tam_cab, tam_reg = struct.unpack("<IHH", dbf[4:12])
    campos, o = [], 32
    while dbf[o] != 0x0D:
        campos.append((dbf[o:o + 11].split(b"\0")[0].decode(), dbf[o + 16]))
        o += 32
    codigos, pos = [], tam_cab
    for _ in range(n_reg):
        r = dbf[pos:pos + tam_reg]
        pos += tam_reg
        k = 1
        for nome, tam in campos:
            if nome == "CD_MUN":
                codigos.append(r[k:k + tam].decode("cp1252").strip())
            k += tam
    shp = base.with_suffix(".shp").read_bytes()
    pos, geoms = 100, []
    while pos < len(shp):
        _, tam = struct.unpack(">ii", shp[pos:pos + 8])
        c = shp[pos + 8:pos + 8 + tam * 2]
        pos += 8 + tam * 2
        tipo = struct.unpack("<i", c[:4])[0]
        assert tipo == 5, "esperava polígonos"
        n_partes, n_pontos = struct.unpack("<ii", c[36:44])
        partes = list(struct.unpack(f"<{n_partes}i", c[44:44 + 4 * n_partes])) + [n_pontos]
        pts = np.frombuffer(c[44 + 4 * n_partes:44 + 4 * n_partes + 16 * n_pontos], dtype="<f8").reshape(-1, 2)
        exteriores, buracos = [], []
        for a, b in zip(partes[:-1], partes[1:]):
            anel = pts[a:b]
            area = 0.5 * np.sum(anel[:-1, 0] * anel[1:, 1] - anel[1:, 0] * anel[:-1, 1])
            (exteriores if area < 0 else buracos).append(anel)
        g = unary_union([Polygon(a).buffer(0) for a in exteriores])
        if buracos:
            g = g.difference(unary_union([Polygon(a).buffer(0) for a in buracos]))
        geoms.append(g)
    assert len(codigos) == len(geoms) == 92
    return dict(zip(codigos, geoms))


FATOR = np.cos(np.radians(22.0))     # corrige a largura da longitude na latitude do estado


def projeta(g):
    from shapely import affinity
    return affinity.scale(g, xfact=FATOR, yfact=1.0, origin=(0, 0))


malha = {c: projeta(g.simplify(0.0008)) for c, g in le_malha().items()}
mun["geom"] = mun.cod_ibge.map(malha)
menores["geom"] = menores.cod_ibge.map(malha)
assert mun.geom.notna().all()


def para_path(g):
    polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
    verts, codes = [], []
    for p in polys:
        for anel in [p.exterior] + list(p.interiors):
            xy = np.asarray(anel.coords)
            verts.extend(xy)
            codes.extend([MPath.MOVETO] + [MPath.LINETO] * (len(xy) - 2) + [MPath.CLOSEPOLY])
    return MPath(verts, codes)


def desenha(ax, dados, regioes=True, mostrar_nomes_regiao=True, contorno_menores=True, numeros=None, lw_mun=0.6):
    for r in dados.itertuples():
        ax.add_patch(PathPatch(para_path(r.geom), fc=r.cor, ec="#ffffff", lw=lw_mun, zorder=2))
    if regioes:
        for nome, g in dados.groupby("regiao8"):
            u = unary_union(list(g.geom))
            for linha in ([u.boundary] if u.geom_type == "Polygon" else [p.boundary for p in u.geoms]):
                geos = [linha] if linha.geom_type in ("LineString", "LinearRing") else list(linha.geoms)
                for ls in geos:
                    xs, ys = ls.xy
                    ax.plot(xs, ys, color="#1f2933", lw=2.4, zorder=4, solid_joinstyle="round")
    if contorno_menores:
        for r in dados[dados.cod_ibge.isin(menores.cod_ibge)].itertuples():
            ax.add_patch(PathPatch(para_path(r.geom), fc="none", ec="#000000", lw=3.2, zorder=5))
    ax.set_aspect("equal")
    ax.axis("off")


def texto(ax, x, y, s, px=24, cor=TEXTO, peso="normal", ha="left", va="center", largura=None, espaco=1.22, halo=False, z=10):
    if largura:
        s = "\n".join(textwrap.fill(p, largura) for p in s.split("\n"))
    s = s.replace("$", r"\$")
    t = ax.text(x, y, s, fontsize=px * PT, color=cor, fontweight=peso, ha=ha, va=va, linespacing=espaco, zorder=z)
    if halo:
        t.set_path_effects([pe.withStroke(linewidth=4, foreground="#ffffff")])
    return t


def bolinha(ax, x, y, n, r=14):
    ax.add_patch(plt.Circle((x, y), r, fc="#ffffff", ec="#000000", lw=2.2, zorder=20))
    ax.text(x, y, str(n), fontsize=r * 1.15 * PT, color="#000000", ha="center", va="center", fontweight="bold", zorder=21)


# ------------------------------------------------------------------------------------------ figura
fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=FUNDO)
fundo = fig.add_axes([0, 0, 1, 1])
fundo.set_xlim(0, W)
fundo.set_ylim(H, 0)
fundo.axis("off")


def eixo(x, y, w, h):
    # Cria um eixo na posição em pixels (x, y do canto superior esquerdo)
    return fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H])


texto(fundo, 50, 55, f"{n_metro10} dos 10 municípios que menos gastam em saúde", px=56, peso="bold")
texto(fundo, 50, 120, "por habitante estão na Região Metropolitana", px=56, peso="bold", cor=VIOLETA)
texto(fundo, 50, 178, f"Os {n_metro} municípios da Metropolitana (a capital incluída) são {n_metro / len(mun) * 100:.0f}% dos 92 do RJ, mas "
      f"{n_metro10 / 10 * 100:.0f}% dos dez que menos gastam. Gasto em saúde por habitante, 2024.", px=26, cor=TEXTO_2)

# --- Mapa principal
ax = eixo(40, 205, 1010, 745)
desenha(ax, mun)
xmin = min(g.bounds[0] for g in mun.geom)
xmax = max(g.bounds[2] for g in mun.geom)
ymin = min(g.bounds[1] for g in mun.geom)
ymax = max(g.bounds[3] for g in mun.geom)
ax.set_xlim(xmin - 0.02, xmax + 0.02)
ax.set_ylim(ymin - 0.02, ymax + 0.02)
# nomes das regiões
ax.apply_aspect()
fig.canvas.draw()
reg_g = {nome: unary_union(list(g.geom)) for nome, g in mun.groupby("regiao8")}
DESLOCA = {"Serrana": (0.00, 0.10), "Costa Verde": (-0.03, -0.12), "Noroeste Fluminense": (0.0, 0.0),
           "Norte Fluminense": (0.0, 0.0), "Centro-Sul Fluminense": (-0.02, 0.0), "Médio Paraíba": (-0.02, 0.0)}
HALO = [pe.withStroke(linewidth=4.5, foreground="#ffffff")]
for nome, g in reg_g.items():
    p = g.representative_point()
    quebra = nome.replace(" Fluminense", "\nFluminense").replace("Baixadas ", "Baixadas\n").replace("Médio ", "Médio\n")
    if nome in DESLOCA:
        dx, dy = DESLOCA[nome]
        ax.text(p.x + dx, p.y + dy, quebra, fontsize=21 * PT, fontweight="bold", color="#1f2933", ha="center", va="center", zorder=12,
                path_effects=HALO, linespacing=1.05)
# Metropolitana e Baixadas Litorâneas: o miolo é apertado, então o nome vai para o mar, com linha-guia
for nome, (lx_, ly_) in {"Metropolitana": (470, 905), "Baixadas Litorâneas": (905, 825)}.items():
    p = reg_g[nome].representative_point()
    ex, ey = ax.transData.transform((p.x, p.y))
    fundo.plot([lx_, ex], [ly_, H - ey], color="#1f2933", lw=1.6, zorder=11)
    fundo.add_patch(plt.Circle((ex, H - ey), 5, fc="#1f2933", ec="#ffffff", lw=1.2, zorder=12))
    texto(fundo, lx_, ly_, nome.replace("Baixadas ", "Baixadas\n"), px=21, peso="bold", cor="#1f2933", ha="center", halo=True, z=13)
# números dos 10 que menos gastam, só fora da Metropolitana (dentro dela os números ficam no zoom)
for r in menores.itertuples():
    if r.regiao8 != "Metropolitana":
        p = r.geom.representative_point()
        ax.add_patch(plt.Circle((p.x, p.y), 0.045, fc="#ffffff", ec="#000000", lw=2.2, zorder=20))
        ax.text(p.x, p.y, str(r.rank), fontsize=17 * PT, color="#000000", ha="center", va="center", fontweight="bold", zorder=21)
# caixa do zoom: contorno tracejado na Metropolitana
metro = mun[mun.regiao8 == "Metropolitana"]
mb = unary_union(list(metro.geom)).bounds
margem = 0.03
ax.add_patch(Rectangle((mb[0] - margem, mb[1] - margem), mb[2] - mb[0] + 2 * margem, mb[3] - mb[1] + 2 * margem, fc="none", ec=VIOLETA, lw=2.4, ls=(0, (5, 3)), zorder=15))

# legenda das cores, no mar (canto inferior direito do mapa)
lx, ly = 70, 262
fundo.add_patch(FancyBboxPatch((lx - 10, ly - 30), 410, 232, boxstyle="round,pad=0,rounding_size=12", fc="#ffffff", ec=LINHA, lw=1.6, zorder=3))
texto(fundo, lx + 8, ly - 10, "Gasto em saúde por habitante", px=22, peso="bold", cor=TEXTO)
for i, (lo, hi, cor, rot) in enumerate(CLASSES):
    n = int(((mun.v >= lo) & (mun.v < hi)).sum())
    yy = ly + 28 + i * 30
    fundo.add_patch(Rectangle((lx + 8, yy - 10), 36, 20, fc=cor, ec="#9aa5b1", lw=1.2, zorder=4))
    texto(fundo, lx + 56, yy, f"{rot}  ({n})", px=21, cor=TEXTO)
texto(fundo, lx + 8, ly + 182, f"mediana: R$ {br(mediana)}  ·  azul = gasta menos", px=19, cor=TEXTO_2)

# --- Zoom na Metropolitana
zx, zy, zw, zh = 1075, 205, 805, 345
fundo.add_patch(FancyBboxPatch((zx, zy), zw, zh, boxstyle="round,pad=0,rounding_size=14", fc="#ffffff", ec=VIOLETA, lw=2.6, ls=(0, (5, 3)), zorder=1))
az = eixo(zx + 8, zy + 34, zw - 16, zh - 40)
desenha(az, mun[mun.regiao8 == "Metropolitana"], regioes=False, contorno_menores=True, lw_mun=1.0)
az.set_xlim(mb[0] - 0.005, mb[2] + 0.005)
az.set_ylim(mb[1] - 0.005, mb[3] + 0.005)
az.apply_aspect()
fig.canvas.draw()
texto(fundo, zx + 16, zy + 20, "Zoom: Região Metropolitana", px=22, peso="bold", cor=VIOLETA)
# Números no zoom. As cidades do núcleo da Baixada são minúsculas e os números se sobrepõem:
# elas ganham os números em fila, acima do conjunto, ligados à cidade por uma linha fina.
NUCLEO = {"Belford Roxo", "Duque de Caxias", "Mesquita", "Nilópolis", "Nova Iguaçu", "São João de Meriti", "Queimados"}


def norma(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def bolha(x, y, n):
    az.text(x, y, str(n), fontsize=17 * PT, color="#000000", ha="center", va="center", fontweight="bold", zorder=30,
            bbox=dict(boxstyle="circle,pad=0.28", fc="#ffffff", ec="#000000", lw=2.2))


da_metro = [r for r in menores.itertuples() if r.regiao8 == "Metropolitana"]
cluster = sorted([r for r in da_metro if norma(r.ente) in {norma(x) for x in NUCLEO}], key=lambda r: r.geom.representative_point().x)
isolados = [r for r in da_metro if r not in cluster]
for r in isolados:
    q = r.geom.representative_point()
    bolha(q.x, q.y, r.rank)
inv = az.transData.inverted()
cx = np.mean([az.transData.transform((r.geom.representative_point().x, r.geom.representative_point().y))[0] for r in cluster])
topo = min(az.transData.transform(r.geom.bounds[2:4])[1] for r in cluster)    # (pixel, origem embaixo) borda de cima do conjunto
topo = max(az.transData.transform((r.geom.bounds[0], r.geom.bounds[3]))[1] for r in cluster)
for i, r in enumerate(cluster):
    q = r.geom.representative_point()
    px_x = cx - 44 * (len(cluster) - 1) / 2 - 70 + i * 44
    px_y = topo + 62
    bx, by = inv.transform((px_x, px_y))
    az.plot([q.x, bx], [q.y, by], color="#000000", lw=1.6, zorder=25)
    bolha(bx, by, r.rank)

# --- Lista dos 10 que menos gastam (também é a "tabela" do gráfico)
lx0, ly0 = 1075, 568
texto(fundo, lx0, ly0, "Os 10 que menos gastam (R$ por habitante)", px=24, peso="bold")
vmax = menores.v.max() * 1.0
for i, r in enumerate(menores.itertuples()):
    yy = ly0 + 36 + i * 30
    bolinha(fundo, lx0 + 14, yy, r.rank, r=13)
    texto(fundo, lx0 + 38, yy, r.ente.replace(" (capital)", ""), px=21, cor=TEXTO)
    cor = VIOLETA if r.regiao8 == "Metropolitana" else CINZA
    largura = 190 * r.v / vmax
    fundo.add_patch(Rectangle((lx0 + 380, yy - 9), largura, 18, fc=cor, ec="none", zorder=4))
    texto(fundo, lx0 + 380 + largura + 8, yy, f"R$ {br(r.v)}", px=21, cor=TEXTO)
    if r.regiao8 != "Metropolitana":
        texto(fundo, lx0 + 700, yy, r.regiao_ceperj.replace(" Fluminense", "").replace("Baixadas Litorâneas", "B. Litorâneas"), px=18, cor=TEXTO_2)
fundo.add_patch(Rectangle((lx0 + 540, ly0 - 8), 16, 16, fc=VIOLETA, ec="none"))
texto(fundo, lx0 + 562, ly0, "Metropolitana", px=19, cor=TEXTO_2)
fundo.add_patch(Rectangle((lx0 + 705, ly0 - 8), 16, 16, fc=CINZA, ec="none"))
texto(fundo, lx0 + 727, ly0, "outras", px=19, cor=TEXTO_2)
mais = " · ".join(f"{r.ente} R$ {br(r.v)}" for r in maiores.itertuples())
texto(fundo, lx0, ly0 + 36 + 10 * 30 + 4, f"Os 3 que mais gastam: {mais}", px=19, cor=TEXTO_2, largura=72)

# --- Faixa inferior: como ler
fundo.add_patch(FancyBboxPatch((40, 962), 1840, 76, boxstyle="round,pad=0,rounding_size=12", fc="#f6f5fb", ec=VIOLETA, lw=2.0, zorder=1))
texto(fundo, 60, 984, "Como ler: cada polígono é um município e a cor mostra quanto ele gasta em saúde por habitante (azul, menos que a mediana; laranja, mais).", px=21, cor=TEXTO)
texto(fundo, 60, 1014, "Linhas grossas separam as 8 regiões do CEPERJ. Contorno preto e número marcam os 10 que menos gastam. Quadro tracejado: a região ampliada.", px=21, cor=TEXTO)
texto(fundo, 50, 1062, "Dados declarados pelos entes (Siconfi), 2024, população IBGE, sem auditoria. Gasto em saúde não é qualidade. Projeto aberto no GitHub: MatheusAugustoEC/saude-rj",
      px=19, cor=TEXTO_2)

fig.savefig(SAIDA / "marco2_mapa_regioes.png", dpi=100, facecolor=FUNDO)
fig.savefig(SAIDA / "marco2_mapa_regioes.svg", facecolor=FUNDO)
print("Gravado:", SAIDA / "marco2_mapa_regioes.png", "| classes:", [int(((mun.v >= lo) & (mun.v < hi)).sum()) for lo, hi, _, _ in CLASSES])
