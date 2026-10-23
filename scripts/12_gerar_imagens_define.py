"""Gera as imagens do Marco 1: SIPOC e mapa do processo (PNG e SVG), em formato horizontal 1920 x 1080 px.

Uso: python -u -I scripts/12_gerar_imagens_define.py
Grava em imagens/: sipoc.png, sipoc.svg, mapa_processo.png, mapa_processo.svg.
Cores: cada coluna do SIPOC e cada etapa do mapa tem a sua cor (paleta de 6 matizes distintos).
Borda tracejada = etapa que depende de terceiros; borda cheia = etapa que depende de nós.
As seis etapas têm o MESMO texto no SIPOC e no mapa.
"""
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon

SAIDA = Path(__file__).resolve().parent.parent / "imagens"
SAIDA.mkdir(exist_ok=True)

FUNDO, TEXTO, TEXTO_2, ESCURO = "#fcfcfb", "#0b0b0b", "#52514e", "#1f2a37"
AZUL, LARANJA, VERDE, VIOLETA, MAGENTA, AMBAR = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6", "#e87ba4", "#eda100"
SIM, NAO = "#008300", "#e34948"
ETAPAS_COR = [AZUL, LARANJA, VERDE, VIOLETA, MAGENTA, AMBAR]
plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
W, H = 1920, 1080
PT = 0.72                       # pixels -> pontos (a figura tem 100 dpi)

# As seis etapas aprovadas (texto, depende de terceiros?)
ETAPAS = [("Declaração das contas pelos entes", True), ("Publicação dos dados na API do Siconfi", True),
          ("Coleta por script, com cópia bruta e data", False), ("Conferência e exploração dos dados", False),
          ("Cálculo e comparação dos indicadores", False), ("Publicação do resultado", False)]


def mistura(cor, t):
    # Clareia a cor misturando com branco (t = 0 mantém a cor, t = 1 vira branco)
    r, g, b = (int(cor[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(round(c + (255 - c) * t) for c in (r, g, b))


def luminancia(cor):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(int(cor[i:i + 2], 16)) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def cor_texto(fundo):
    # Branco ou preto, o que tiver mais contraste sobre o fundo
    lf = luminancia(fundo)
    return "#ffffff" if (1.05 / (lf + 0.05)) > ((lf + 0.05) / 0.0533) else TEXTO


def tela(altura=H):
    fig = plt.figure(figsize=(W / 100, altura / 100), dpi=100, facecolor=FUNDO)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(altura, 0)
    ax.axis("off")
    return fig, ax


def caixa(ax, x, y, w, h, fc, ec, lw=3, raio=18, tracejado=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={raio}", fc=fc, ec=ec, lw=lw,
                                ls=(0, (5, 3)) if tracejado else "-"))


def texto(ax, x, y, s, px=24, cor=TEXTO, peso="normal", ha="left", va="center", largura=None, espaco=1.25, rot=0):
    if largura:
        s = "\n".join(textwrap.fill(p, largura) for p in s.split("\n"))
    ax.text(x, y, s, fontsize=px * PT, color=cor, fontweight=peso, ha=ha, va=va, linespacing=espaco, rotation=rot)


def seta(ax, x1, y1, x2, y2, cor=ESCURO, lw=3.2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=cor, lw=lw, shrinkA=0, shrinkB=0, mutation_scale=24))


def rodape(ax, y=1052, px=20):
    texto(ax, 60, y, "Dados públicos do Siconfi (Tesouro Nacional), exercício 2024. Os números são o que cada ente declarou.", px=px, cor=TEXTO_2)


def cabecalho(ax, titulo, subtitulo):
    texto(ax, 60, 56, titulo, px=54, peso="bold")
    texto(ax, 60, 112, subtitulo, px=27, cor=TEXTO_2)


def lista(ax, x, y_ini, y_fim, itens, largura, px=26, passo=36, entre=24):
    # Lista com marcador e recuo nas linhas quebradas, centralizada na vertical entre y_ini e y_fim
    quebrados = [textwrap.wrap(it, largura) for it in itens]
    total = sum(len(q) for q in quebrados) * passo + (len(itens) - 1) * entre
    yy = y_ini + (y_fim - y_ini - total) / 2 + passo / 2
    for linhas in quebrados:
        for k, ln in enumerate(linhas):
            texto(ax, x + (0 if k == 0 else 28), yy, ("•  " if k == 0 else "") + ln, px=px)
            yy += passo
        yy += entre


# ===================================================================================================== SIPOC
fig, ax = tela()
cabecalho(ax, "SIPOC", "Do dado público ao painel: as contas da saúde no RJ")

COLUNAS = [
    ("S", "Fornecedores", AZUL, 60, 310, ["Estados e municípios, que declaram as contas", "Tesouro Nacional, que publica os dados no Siconfi"]),
    ("I", "Entradas", LARANJA, 398, 310, ["Relatórios RREO e RGF dos 27 estados e dos 92 municípios do RJ", "População de cada ente"]),
    ("P", "Processo", VERDE, 736, 500, None),
    ("O", "Saídas", VIOLETA, 1264, 310, ["Painel de página única", "Planilha para baixar e conferir", "Relatório do método e dos limites"]),
    ("C", "Clientes", MAGENTA, 1602, 258, ["Cidadão curioso, do RJ ou de fora"]),
]
TOPO, BASE = 160, 940
for letra, nome, cor, x, w, itens in COLUNAS:
    caixa(ax, x, TOPO, w, BASE - TOPO, mistura(cor, 0.88), cor, lw=3.5)
    caixa(ax, x, TOPO, w, 22, cor, cor, lw=0, raio=11)
    texto(ax, x + w / 2, TOPO + 90, letra, px=72, cor=cor, peso="bold", ha="center")
    texto(ax, x + w / 2, TOPO + 160, nome, px=28, peso="bold", ha="center")
    ax.plot([x + 24, x + w - 24], [TOPO + 200, TOPO + 200], color=cor, lw=2)
    if itens:
        lista(ax, x + 26, TOPO + 215, BASE - 20, itens, int((w - 52) / 13.8), px=26)

# P: as seis etapas (tracejado = terceiros)
xp, wp = 736, 500
yy = TOPO + 212
for n, (nome, terceiros) in enumerate(ETAPAS, start=1):
    caixa(ax, xp + 20, yy, wp - 40, 80, "#ffffff", VERDE, lw=3, raio=14, tracejado=terceiros)
    ax.add_patch(Circle((xp + 64, yy + 40), 23, fc=VERDE, ec="none"))
    texto(ax, xp + 64, yy + 40, str(n), px=25, cor=TEXTO, peso="bold", ha="center")
    texto(ax, xp + 104, yy + 40, nome, px=24, largura=26, espaco=1.15)
    yy += 94
# setas entre as colunas
for xa in (370, 708, 1236, 1574):
    ax.add_patch(Polygon([(xa + 2, 538), (xa + 26, 550), (xa + 2, 562)], closed=True, fc=ESCURO, ec="none"))

# legenda
caixa(ax, 60, 972, 52, 34, "#ffffff", VERDE, lw=3, raio=8, tracejado=True)
texto(ax, 126, 989, "etapa que depende de terceiros (entes e Tesouro)", px=22, cor=TEXTO_2)
caixa(ax, 700, 972, 52, 34, "#ffffff", VERDE, lw=3, raio=8)
texto(ax, 766, 989, "etapa que depende de nós", px=22, cor=TEXTO_2)
rodape(ax, 1050)
fig.savefig(SAIDA / "sipoc.png", dpi=100, facecolor=FUNDO)
fig.savefig(SAIDA / "sipoc.svg", facecolor=FUNDO)
plt.close(fig)

# ============================================================================================ MAPA DO PROCESSO
fig, ax = tela()
cabecalho(ax, "Mapa do processo", "Do dado público ao painel, com os pontos de controle")

BW, BH = 240, 140                         # tamanho das caixas das etapas


def etapa(x, y, num):
    nome, terceiros = ETAPAS[num - 1]
    cor = ETAPAS_COR[num - 1]
    caixa(ax, x, y, BW, BH, mistura(cor, 0.86), cor, lw=4, tracejado=terceiros)
    ax.add_patch(Circle((x + 34, y + 34), 24, fc=cor, ec="none"))
    texto(ax, x + 34, y + 34, str(num), px=26, cor=cor_texto(cor), peso="bold", ha="center")
    texto(ax, x + BW / 2, y + BH / 2 + 24, nome, px=23, ha="center", largura=19, espaco=1.12)


def controle(x, y, rotulo):
    caixa(ax, x + BW - 70, y - 20, 70, 38, ESCURO, ESCURO, lw=0, raio=19)
    texto(ax, x + BW - 35, y - 1, rotulo, px=22, cor="#ffffff", peso="bold", ha="center")


# raias
caixa(ax, 40, 140, 1840, 190, "#f3f2ee", "#d9d8d1", lw=1.5)
texto(ax, 76, 235, "TERCEIROS", px=22, cor=TEXTO_2, peso="bold", ha="center", rot=90)
caixa(ax, 40, 350, 1840, 450, "#f4f8fd", "#d4e3f6", lw=1.5)
texto(ax, 76, 575, "NÓS", px=24, cor=AZUL, peso="bold", ha="center", rot=90)

# raia dos terceiros
x1, x2 = 140, 435
y_l1 = 165
etapa(x1, y_l1, 1)
etapa(x2, y_l1, 2)
seta(ax, x1 + BW, y_l1 + BH / 2, x2, y_l1 + BH / 2)

# raia "nós"
y_l2 = 420
x3, x4, xd, x5, x6 = 435, 725, 1015, 1315, 1605
etapa(x3, y_l2, 3)
etapa(x4, y_l2, 4)
controle(x4, y_l2, "C1")
etapa(x5, y_l2, 5)
controle(x5, y_l2, "C2")
etapa(x6, y_l2, 6)
controle(x6, y_l2, "C3")
seta(ax, x2 + BW / 2, y_l1 + BH, x3 + BW / 2, y_l2)
seta(ax, x3 + BW, y_l2 + BH / 2, x4, y_l2 + BH / 2)
yc = y_l2 + BH / 2
# decisão (losango) depois da etapa 4
cxd, hw, hh = xd + 115, 115, 105
seta(ax, x4 + BW, yc, cxd - hw, yc)
ax.add_patch(Polygon([(cxd, yc - hh), (cxd + hw, yc), (cxd, yc + hh), (cxd - hw, yc)], closed=True, fc="#ffffff", ec=ESCURO, lw=3.5))
texto(ax, cxd, yc, "Dado completo\ne coerente?", px=23, peso="bold", ha="center", espaco=1.15)
# sim
seta(ax, cxd + hw, yc, x5, yc, cor=SIM)
texto(ax, (cxd + hw + x5) / 2, yc - 24, "sim", px=24, cor=SIM, peso="bold", ha="center")
seta(ax, x5 + BW, yc, x6, yc)
# não: ramo de baixo e volta à coleta
yb = 655
seta(ax, cxd, yc + hh, cxd, yb, cor=NAO)
texto(ax, cxd + 14, (yc + hh + yb) / 2, "não", px=24, cor=NAO, peso="bold")
caixa(ax, cxd - 195, yb, 390, 110, mistura(NAO, 0.9), NAO, lw=3.5)
texto(ax, cxd, yb + 55, "Registrar a falha, corrigir a leitura ou marcar o ente como caso especial", px=22, ha="center", largura=30, espaco=1.15)
xv = x3 + BW / 2
ax.plot([cxd - 195, xv], [yb + 55, yb + 55], color=NAO, lw=3.2, ls=(0, (5, 3)), solid_capstyle="butt")
seta(ax, xv, yb + 55, xv, y_l2 + BH, cor=NAO)
texto(ax, (cxd - 195 + xv) / 2, yb + 28, "volta à coleta", px=22, cor=NAO, ha="center")
# fim
seta(ax, x6 + BW / 2, y_l2 + BH, x6 + BW / 2, 655)
caixa(ax, x6 - 5, 655, BW + 10, 84, ESCURO, ESCURO, lw=0, raio=42)
texto(ax, x6 + BW / 2, 697, "Painel, planilha\ne relatório", px=22, cor="#ffffff", peso="bold", ha="center", espaco=1.15)

# legenda dentro da raia "nós"
texto(ax, 130, 440, "Como ler", px=24, peso="bold")
caixa(ax, 130, 475, 52, 32, "#ffffff", ESCURO, lw=3, raio=8, tracejado=True)
texto(ax, 196, 491, "depende de terceiros", px=21, cor=TEXTO_2)
caixa(ax, 130, 525, 52, 32, "#ffffff", ESCURO, lw=3, raio=8)
texto(ax, 196, 541, "depende de nós", px=21, cor=TEXTO_2)
caixa(ax, 130, 575, 52, 32, ESCURO, ESCURO, lw=0, raio=16)
texto(ax, 156, 591, "C1", px=17, cor="#ffffff", peso="bold", ha="center")
texto(ax, 196, 591, "ponto de controle", px=21, cor=TEXTO_2)
ax.plot([130, 182], [637, 637], color=SIM, lw=4)
texto(ax, 196, 637, "sim", px=21, cor=SIM)
ax.plot([130, 182], [677, 677], color=NAO, lw=4)
texto(ax, 196, 677, "não", px=21, cor=NAO)

# cartões dos pontos de controle (a cor lateral é a da etapa onde o controle atua)
CARTOES = [("C1", "Conferência e exploração (etapa 4)",
            "O DF veio vazio na 1ª coleta (esfera diferente da aceita pela API). Limite de dívida declarado como “120” em vez de reais. Dois totais de despesa no mesmo relatório.", ETAPAS_COR[3]),
           ("C2", "Cálculo e comparação (etapa 5)",
            "Cada indicador é uma fórmula explícita. A planilha e o notebook foram conferidos: 0 diferenças nos 119 entes.", ETAPAS_COR[4]),
           ("C3", "Publicação com ressalva (etapa 6)",
            "Cada número tem origem registrada, e toda comparação lembra que gasto não é qualidade.", ETAPAS_COR[5])]
for k, (tag, titulo, corpo, cor) in enumerate(CARTOES):
    x = 60 + k * 600
    caixa(ax, x, 825, 570, 185, "#ffffff", "#d9d8d1", lw=1.5, raio=16)
    caixa(ax, x, 825, 14, 185, cor, cor, lw=0, raio=7)
    caixa(ax, x + 34, 842, 64, 36, ESCURO, ESCURO, lw=0, raio=18)
    texto(ax, x + 66, 860, tag, px=22, cor="#ffffff", peso="bold", ha="center")
    texto(ax, x + 112, 860, titulo, px=24, peso="bold")
    texto(ax, x + 34, 940, corpo, px=22, cor=TEXTO_2, largura=44, espaco=1.2)
texto(ax, 60, 1034, "Cartões: o que cada ponto de controle já pegou ou garante neste projeto.", px=19, cor=TEXTO_2)
rodape(ax, 1060, px=19)
fig.savefig(SAIDA / "mapa_processo.png", dpi=100, facecolor=FUNDO)
fig.savefig(SAIDA / "mapa_processo.svg", facecolor=FUNDO)
plt.close(fig)

# ======================================================================== SIPOC + MAPA JUNTOS (horizontal, 1920 x 1300)
H2 = 1300
fig, ax = tela(H2)
texto(ax, 48, 46, "SIPOC e mapa do processo", px=46, peso="bold")
texto(ax, 48, 90, "Do dado público ao painel: as contas da saúde no RJ", px=24, cor=TEXTO_2)
texto(ax, 48, 130, "1  SIPOC", px=26, peso="bold", cor=ESCURO)

COL2 = [
    ("S", "Fornecedores", AZUL, 48, 270, ["Estados e municípios, que declaram as contas", "Tesouro Nacional, que publica os dados no Siconfi"]),
    ("I", "Entradas", LARANJA, 330, 290, ["Relatórios RREO e RGF dos 27 estados e dos 92 municípios do RJ", "População de cada ente"]),
    ("P", "Processo", VERDE, 632, 640, None),
    ("O", "Saídas", VIOLETA, 1284, 290, ["Painel de página única", "Planilha para baixar e conferir", "Relatório do método e dos limites"]),
    ("C", "Clientes", MAGENTA, 1586, 286, ["Cidadão curioso, do RJ ou de fora"]),
]
T2, B2 = 152, 530
for letra, nome, cor, x, w, itens in COL2:
    caixa(ax, x, T2, w, B2 - T2, mistura(cor, 0.88), cor, lw=3)
    caixa(ax, x, T2, w, 16, cor, cor, lw=0, raio=8)
    texto(ax, x + w / 2, T2 + 58, letra, px=54, cor=cor, peso="bold", ha="center")
    texto(ax, x + w / 2, T2 + 106, nome, px=24, peso="bold", ha="center")
    ax.plot([x + 20, x + w - 20], [T2 + 132, T2 + 132], color=cor, lw=2)
    if itens:
        lista(ax, x + 22, T2 + 140, B2 - 12, itens, int((w - 74) / 10.2), px=21, passo=28, entre=14)
# P: as seis etapas em grade de 2 colunas (a linha de cima é a dos terceiros, tracejada)
cw = (640 - 32 - 12) / 2
for i, (nome, terceiros) in enumerate(ETAPAS):
    r, c = divmod(i, 2)
    x, y = 632 + 16 + c * (cw + 12), T2 + 142 + r * 78
    caixa(ax, x, y, cw, 68, "#ffffff", VERDE, lw=2.5, raio=12, tracejado=terceiros)
    ax.add_patch(Circle((x + 32, y + 34), 18, fc=VERDE, ec="none"))
    texto(ax, x + 32, y + 34, str(i + 1), px=21, cor=TEXTO, peso="bold", ha="center")
    texto(ax, x + 62, y + 34, nome, px=20, largura=int((cw - 78) / 10), espaco=1.1)
for xa in (318, 620, 1272, 1574):
    ax.add_patch(Polygon([(xa, (T2 + B2) / 2 - 9), (xa + 12, (T2 + B2) / 2), (xa, (T2 + B2) / 2 + 9)], closed=True, fc=ESCURO, ec="none"))
caixa(ax, 48, 552, 44, 26, "#ffffff", VERDE, lw=2.5, raio=7, tracejado=True)
texto(ax, 102, 565, "etapa que depende de terceiros (entes e Tesouro)", px=20, cor=TEXTO_2)
caixa(ax, 640, 552, 44, 26, "#ffffff", VERDE, lw=2.5, raio=7)
texto(ax, 694, 565, "etapa que depende de nós", px=20, cor=TEXTO_2)

texto(ax, 48, 612, "2  Mapa do processo", px=26, peso="bold", cor=ESCURO)
BW2, BH2 = 240, 130


def etapa2(x, y, num):
    nome, terceiros = ETAPAS[num - 1]
    cor = ETAPAS_COR[num - 1]
    caixa(ax, x, y, BW2, BH2, mistura(cor, 0.86), cor, lw=3.5, tracejado=terceiros)
    ax.add_patch(Circle((x + 32, y + 32), 21, fc=cor, ec="none"))
    texto(ax, x + 32, y + 32, str(num), px=23, cor=cor_texto(cor), peso="bold", ha="center")
    texto(ax, x + BW2 / 2, y + BH2 / 2 + 22, nome, px=20, ha="center", largura=21, espaco=1.12)


def controle2(x, y, rotulo):
    caixa(ax, x + BW2 - 66, y - 19, 66, 36, ESCURO, ESCURO, lw=0, raio=18)
    texto(ax, x + BW2 - 33, y - 1, rotulo, px=20, cor="#ffffff", peso="bold", ha="center")


caixa(ax, 40, 634, 1840, 156, "#f3f2ee", "#d9d8d1", lw=1.5)
texto(ax, 72, 712, "TERCEIROS", px=20, cor=TEXTO_2, peso="bold", ha="center", rot=90)
caixa(ax, 40, 805, 1840, 295, "#f4f8fd", "#d4e3f6", lw=1.5)
texto(ax, 72, 952, "NÓS", px=22, cor=AZUL, peso="bold", ha="center", rot=90)
yl1, yl2 = 650, 850
x1, x2, x3, x4, xd, x5, x6 = 140, 435, 435, 725, 1015, 1315, 1605
etapa2(x1, yl1, 1)
etapa2(x2, yl1, 2)
seta(ax, x1 + BW2, yl1 + BH2 / 2, x2, yl1 + BH2 / 2)
etapa2(x3, yl2, 3)
etapa2(x4, yl2, 4)
controle2(x4, yl2, "C1")
etapa2(x5, yl2, 5)
controle2(x5, yl2, "C2")
etapa2(x6, yl2, 6)
controle2(x6, yl2, "C3")
seta(ax, x2 + BW2 / 2, yl1 + BH2, x3 + BW2 / 2, yl2)
seta(ax, x3 + BW2, yl2 + BH2 / 2, x4, yl2 + BH2 / 2)
yc = yl2 + BH2 / 2
cxd, hw, hh = xd + 115, 115, 88
seta(ax, x4 + BW2, yc, cxd - hw, yc)
ax.add_patch(Polygon([(cxd, yc - hh), (cxd + hw, yc), (cxd, yc + hh), (cxd - hw, yc)], closed=True, fc="#ffffff", ec=ESCURO, lw=3))
texto(ax, cxd, yc, "Dado completo\ne coerente?", px=21, peso="bold", ha="center", espaco=1.15)
seta(ax, cxd + hw, yc, x5, yc, cor=SIM)
texto(ax, (cxd + hw + x5) / 2, yc - 22, "sim", px=22, cor=SIM, peso="bold", ha="center")
seta(ax, x5 + BW2, yc, x6, yc)
yb, hb = 1044, 50
seta(ax, cxd, yc + hh, cxd, yb, cor=NAO)
texto(ax, cxd + 16, (yc + hh + yb) / 2 - 2, "não", px=22, cor=NAO, peso="bold")
caixa(ax, cxd - 200, yb, 400, hb, mistura(NAO, 0.9), NAO, lw=3)
texto(ax, cxd, yb + hb / 2, "Registrar a falha, corrigir a leitura ou marcar o ente como caso especial", px=19, ha="center", largura=46, espaco=1.1)
xv = x3 + BW2 / 2
ax.plot([cxd - 200, xv], [yb + hb / 2, yb + hb / 2], color=NAO, lw=3, ls=(0, (5, 3)), solid_capstyle="butt")
seta(ax, xv, yb + hb / 2, xv, yl2 + BH2, cor=NAO)
texto(ax, (cxd - 200 + xv) / 2, yb + hb / 2 - 20, "volta à coleta", px=20, cor=NAO, ha="center")
seta(ax, x6 + BW2 / 2, yl2 + BH2, x6 + BW2 / 2, yb)
caixa(ax, x6 - 5, yb, BW2 + 10, hb, ESCURO, ESCURO, lw=0, raio=hb / 2)
texto(ax, x6 + BW2 / 2, yb + hb / 2, "Painel, planilha e relatório", px=19, cor="#ffffff", peso="bold", ha="center", largura=22, espaco=1.1)
# legenda na raia "nós"
texto(ax, 110, 840, "Como ler", px=22, peso="bold")
for k, (rot, desc) in enumerate([("tracejado", "depende de terceiros"), ("cheio", "depende de nós"), ("ctrl", "ponto de controle"), ("sim", "sim"), ("nao", "não")]):
    yy = 878 + k * 38
    if rot == "tracejado":
        caixa(ax, 110, yy - 14, 46, 28, "#ffffff", ESCURO, lw=2.5, raio=7, tracejado=True)
    elif rot == "cheio":
        caixa(ax, 110, yy - 14, 46, 28, "#ffffff", ESCURO, lw=2.5, raio=7)
    elif rot == "ctrl":
        caixa(ax, 110, yy - 14, 46, 28, ESCURO, ESCURO, lw=0, raio=14)
        texto(ax, 133, yy, "C1", px=14, cor="#ffffff", peso="bold", ha="center")
    else:
        ax.plot([110, 156], [yy, yy], color=SIM if rot == "sim" else NAO, lw=4)
    texto(ax, 170, yy, desc, px=19, cor=SIM if rot == "sim" else NAO if rot == "nao" else TEXTO_2)

CART2 = [("C1", "Conferência e exploração (etapa 4)",
          "O DF veio vazio na 1ª coleta (esfera diferente da aceita pela API). Limite de dívida declarado como “120” em vez de reais. Dois totais de despesa no mesmo relatório.", ETAPAS_COR[3]),
         ("C2", "Cálculo e comparação (etapa 5)",
          "Cada indicador é uma fórmula explícita. A planilha e o notebook foram conferidos: 0 diferenças nos 119 entes.", ETAPAS_COR[4]),
         ("C3", "Publicação com ressalva (etapa 6)",
          "Cada número tem origem registrada, e toda comparação lembra que gasto não é qualidade.", ETAPAS_COR[5])]
for k, (tag, titulo, corpo, cor) in enumerate(CART2):
    x = 48 + k * 617
    caixa(ax, x, 1120, 590, 130, "#ffffff", "#d9d8d1", lw=1.5, raio=14)
    caixa(ax, x, 1120, 12, 130, cor, cor, lw=0, raio=6)
    caixa(ax, x + 28, 1132, 60, 32, ESCURO, ESCURO, lw=0, raio=16)
    texto(ax, x + 58, 1148, tag, px=20, cor="#ffffff", peso="bold", ha="center")
    texto(ax, x + 102, 1148, titulo, px=22, peso="bold")
    texto(ax, x + 28, 1204, corpo, px=19, cor=TEXTO_2, largura=62, espaco=1.18)
texto(ax, 48, 1270, "Cartões: o que cada ponto de controle já pegou ou garante neste projeto.  Dados públicos do Siconfi (Tesouro Nacional), 2024; os números são o que cada ente declarou.", px=17, cor=TEXTO_2)
fig.savefig(SAIDA / "sipoc_e_mapa.png", dpi=100, facecolor=FUNDO)
fig.savefig(SAIDA / "sipoc_e_mapa.svg", facecolor=FUNDO)
plt.close(fig)
print("Imagens gravadas em", SAIDA)
