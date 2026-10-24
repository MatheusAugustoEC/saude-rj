"""Partes comuns dos mapas do Marco 2 (dados, malha do IBGE, grupos de região, cores e desenho).

Usado por 17_gerar_mapa_regioes_cores.py e 18_gerar_mapa_regioes_tabela.py. Não gera imagem sozinho.
Nada digitado à mão: dados de dados_tratados/indicadores_measure_2024.csv e malha de dados_brutos/malha_rj.
"""
import colorsys
import math
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
from shapely import affinity
from shapely.geometry import Polygon
from shapely.ops import unary_union

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "imagens"
SAIDA.mkdir(exist_ok=True)

FUNDO, TEXTO, TEXTO_2, CINZA, LINHA = "#fcfcfb", "#0b0b0b", "#52514e", "#9aa5b1", "#c9ccd1"
VIOLETA = "#6250d6"
W, H, PT = 1920, 1080, 0.72
plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]

NUCLEO = ["Belford Roxo", "Duque de Caxias", "Mesquita", "Nilópolis", "Nova Iguaçu", "São João de Meriti"]
CAPITAL, BAIXADA, RESTO = "Capital", "Baixada (núcleo de 6)", "Metropolitana (resto, 15)"
INTERIOR = ["Costa Verde", "Baixadas Litorâneas", "Médio Paraíba", "Centro-Sul Fluminense", "Serrana", "Noroeste Fluminense", "Norte Fluminense"]
GRUPOS = [CAPITAL, BAIXADA, RESTO] + INTERIOR
CLASSES_VALOR = [(0, 1400), (1400, 2000), (2000, 2700), (2700, 4000), (4000, 1e9)]
ROTULOS_CLASSE = ["até 1.400", "1.400 a 2.000", "2.000 a 2.700", "2.700 a 4.000", "mais de 4.000"]


def br(x, casas=0):
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def norma(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().strip()


def classe(v):
    for i, (lo, hi) in enumerate(CLASSES_VALOR):
        if lo <= v < hi:
            return i


# ----------------------------------------------------------------------------------- cores (OKLCH, degraus de mesma luminosidade)
def _srgb_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lin_srgb(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def hex_oklch(h):
    r, g, b = (_srgb_lin(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3), m ** (1 / 3), s ** (1 / 3)
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def oklch_hex(L, C, h):
    # Reduz a croma até a cor caber no sRGB
    for _ in range(60):
        a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
        l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
        m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
        s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
        r = 4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
        g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
        bl = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
        if all(-0.001 <= c <= 1.001 for c in (r, g, bl)):
            break
        C *= 0.96
    return "#%02x%02x%02x" % tuple(round(_lin_srgb(c) * 255) for c in (r, g, bl))


NIVEIS_L = [0.92, 0.82, 0.70, 0.57, 0.43]       # claro = gasta menos, escuro = gasta mais; iguais para todas as famílias
FATOR_C = [0.45, 0.70, 0.90, 1.0, 1.0]


def rampa(base_hex, neutro=False):
    _, c, h = hex_oklch(base_hex)
    if neutro:
        c, h = 0.022, 250.0
    return [oklch_hex(L, c * f, h) for L, f in zip(NIVEIS_L, FATOR_C)]


def mistura(cor, t):
    r, g, b = (int(cor[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(round(c + (255 - c) * t) for c in (r, g, b))


# ----------------------------------------------------------------------------------- dados
def carrega_dados():
    ind = pd.read_csv(RAIZ / "dados_tratados" / "indicadores_measure_2024.csv", dtype={"cod_ibge": str})
    mun = ind[ind.esfera == "M"].copy()
    nuc = {norma(x) for x in NUCLEO}

    def grupo(r):
        if r.regiao_ceperj == "Capital (Rio de Janeiro)":
            return CAPITAL
        if norma(r.ente) in nuc:
            return BAIXADA
        if r.regiao_ceperj == "Metropolitana (sem a capital)":
            return RESTO
        return r.regiao_ceperj

    mun["grupo"] = mun.apply(grupo, axis=1)
    mun["regiao8"] = mun.regiao_ceperj.replace({"Capital (Rio de Janeiro)": "Metropolitana", "Metropolitana (sem a capital)": "Metropolitana"})
    mun["v"] = mun.saude / mun.populacao
    mun = mun.sort_values("v").reset_index(drop=True)
    malha = le_malha()
    mun["geom"] = mun.cod_ibge.map(malha)
    assert mun.geom.notna().all()
    menores = mun.head(10).copy()
    menores["rank"] = range(1, 11)
    maiores = mun.tail(3).iloc[::-1]
    return mun, menores, maiores


# ----------------------------------------------------------------------------------- malha (shapefile sem biblioteca extra)
FATOR = math.cos(math.radians(22.0))


def le_malha():
    base = RAIZ / "dados_brutos" / "malha_rj" / "RJ_Municipios_2024"
    dbf = base.with_suffix(".dbf").read_bytes()
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
        assert struct.unpack("<i", c[:4])[0] == 5, "esperava polígonos"
        n_partes, n_pontos = struct.unpack("<ii", c[36:44])
        partes = list(struct.unpack(f"<{n_partes}i", c[44:44 + 4 * n_partes])) + [n_pontos]
        pts = np.frombuffer(c[44 + 4 * n_partes:44 + 4 * n_partes + 16 * n_pontos], dtype="<f8").reshape(-1, 2)
        ext, bur = [], []
        for a, b in zip(partes[:-1], partes[1:]):
            anel = pts[a:b]
            area = 0.5 * np.sum(anel[:-1, 0] * anel[1:, 1] - anel[1:, 0] * anel[:-1, 1])
            (ext if area < 0 else bur).append(anel)
        g = unary_union([Polygon(a).buffer(0) for a in ext])
        if bur:
            g = g.difference(unary_union([Polygon(a).buffer(0) for a in bur]))
        geoms.append(affinity.scale(g.simplify(0.0008), xfact=FATOR, yfact=1.0, origin=(0, 0)))
    assert len(codigos) == len(geoms) == 92
    return dict(zip(codigos, geoms))


def para_path(g):
    polys = [g] if g.geom_type == "Polygon" else list(g.geoms)
    verts, codes = [], []
    for p in polys:
        for anel in [p.exterior] + list(p.interiors):
            xy = np.asarray(anel.coords)
            verts.extend(xy)
            codes.extend([MPath.MOVETO] + [MPath.LINETO] * (len(xy) - 2) + [MPath.CLOSEPOLY])
    return MPath(verts, codes)


# ----------------------------------------------------------------------------------- desenho
def tela():
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=FUNDO)
    fundo = fig.add_axes([0, 0, 1, 1])
    fundo.set_xlim(0, W)
    fundo.set_ylim(H, 0)
    fundo.axis("off")
    return fig, fundo


def eixo(fig, x, y, w, h):
    return fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H])


def texto(ax, x, y, s, px=24, cor=TEXTO, peso="normal", ha="left", va="center", largura=None, espaco=1.22, halo=False, z=10):
    if largura:
        s = "\n".join(textwrap.fill(p, largura) for p in s.split("\n"))
    s = s.replace("$", r"\$")
    t = ax.text(x, y, s, fontsize=px * PT, color=cor, fontweight=peso, ha=ha, va=va, linespacing=espaco, zorder=z)
    if halo:
        t.set_path_effects([pe.withStroke(linewidth=4, foreground="#ffffff")])
    return t


def pinta(ax, dados, cor_de, lw_mun=0.7):
    for r in dados.itertuples():
        ax.add_patch(PathPatch(para_path(r.geom), fc=cor_de(r), ec="#ffffff", lw=lw_mun, zorder=2))


def contornos(ax, dados, lw=3.0):
    # Contorno preto grosso em volta de cada grupo de região
    for nome, g in dados.groupby("grupo"):
        u = unary_union(list(g.geom))
        pol = [u] if u.geom_type == "Polygon" else list(u.geoms)
        for p in pol:
            for anel in [p.exterior] + list(p.interiors):
                xs, ys = anel.xy
                ax.plot(xs, ys, color="#000000", lw=lw, zorder=6, solid_joinstyle="round")


def bolha(ax, x, y, n, tam=17):
    ax.text(x, y, str(n), fontsize=tam * PT, color="#000000", ha="center", va="center", fontweight="bold", zorder=30,
            bbox=dict(boxstyle="circle,pad=0.28", fc="#ffffff", ec="#000000", lw=2.2))


def caixa(ax, x, y, w, h, fc, ec, lw=2.0, raio=12, tracejado=False, z=1):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={raio}", fc=fc, ec=ec, lw=lw,
                                ls=(0, (5, 3)) if tracejado else "-", zorder=z))


def limites(ax, dados, folga=0.02):
    xmin = min(g.bounds[0] for g in dados.geom)
    xmax = max(g.bounds[2] for g in dados.geom)
    ymin = min(g.bounds[1] for g in dados.geom)
    ymax = max(g.bounds[3] for g in dados.geom)
    ax.set_xlim(xmin - folga, xmax + folga)
    ax.set_ylim(ymin - folga, ymax + folga)
    ax.set_aspect("equal")
    ax.axis("off")


def numeros_do_zoom(az, menores):
    # Os números do núcleo da Baixada se sobrepõem: ficam em fila, acima do conjunto, ligados à cidade por uma linha fina
    nuc = {norma(x) for x in NUCLEO} | {norma("Queimados")}
    da_metro = [r for r in menores.itertuples() if r.regiao8 == "Metropolitana"]
    cluster = sorted([r for r in da_metro if norma(r.ente) in nuc], key=lambda r: r.geom.representative_point().x)
    for r in da_metro:
        if r not in cluster:
            q = r.geom.representative_point()
            bolha(az, q.x, q.y, r.rank)
    inv = az.transData.inverted()
    cx = np.mean([az.transData.transform((r.geom.representative_point().x, r.geom.representative_point().y))[0] for r in cluster])
    topo = max(az.transData.transform((r.geom.bounds[0], r.geom.bounds[3]))[1] for r in cluster)
    for i, r in enumerate(cluster):
        q = r.geom.representative_point()
        px_x = cx - 44 * (len(cluster) - 1) / 2 - 70 + i * 44
        bx, by = inv.transform((px_x, topo + 62))
        az.plot([q.x, bx], [q.y, by], color="#000000", lw=1.6, zorder=25)
        bolha(az, bx, by, r.rank)


def poder_mde(mun, grupo):
    # Efeito mínimo detectável (nível 5%, poder 80%, escala de log) de um grupo contra o resto dos municípios sem a capital
    fora = mun[mun.grupo != CAPITAL]
    s = np.log(fora.saude_por_hab).std()
    n1 = int((fora.grupo == grupo).sum())
    if n1 < 2:
        return None
    n2 = len(fora) - n1
    return (math.exp((1.96 + 0.8416) * s * math.sqrt(1 / n1 + 1 / n2)) - 1) * 100
