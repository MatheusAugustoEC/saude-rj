"""Gera a imagem do Marco 2 (Measure): imagens/marco2_measure.png e .svg, horizontal, 1920 x 1080 px.

Uso: python -u -I scripts/15_gerar_imagem_measure.py
Todos os números vêm dos arquivos do projeto (nada digitado à mão):
  - dados_tratados/conferencia_saude_rreo_vs_dca.csv  (conferência do RREO contra a DCA)
  - dados_tratados/indicadores_2024.csv                (população do IBGE e do Siconfi)
  - fases/fase-2b-measure-baseline/artefatos/baseline_measure_2024.csv  (baseline congelado)
Não nomeia nenhum município.
"""
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "imagens"
SAIDA.mkdir(exist_ok=True)

FUNDO, TEXTO, TEXTO_2, CINZA = "#fcfcfb", "#0b0b0b", "#52514e", "#9aa5b1"
AZUL, LARANJA, VERDE, VIOLETA = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
W, H = 1920, 1080
PT = 0.72  # pixels -> pontos (a figura tem 100 dpi)


def br(x, casas=0):
    return f"{x:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ----------------------------------------------------------------------------- números (todos de arquivos)
ind = pd.read_csv(RAIZ / "dados_tratados" / "indicadores_2024.csv", dtype={"cod_ibge": str})
ind["flag_especial"] = ind.flag_especial.fillna("")
conf = pd.read_csv(RAIZ / "dados_tratados" / "conferencia_saude_rreo_vs_dca.csv", dtype={"cod_ibge": str})
base = pd.read_csv(RAIZ / "fases" / "fase-2b-measure-baseline" / "artefatos" / "baseline_measure_2024.csv")

razao = conf.saude / conf.dca_saude
n_total = len(conf)
n_bate_antes = int(((razao - 1).abs() <= 0.01).sum())
fora = conf[(razao - 1).abs() > 0.01].iloc[0]
rreo_mi, dca_mi = fora.saude / 1e6, fora.dca_saude / 1e6

mun = ind[ind.esfera == "M"]
publicado = mun[mun.flag_especial == ""]            # o que o Marco 1 mostrou: sem os 4 marcados, população do Siconfi
velho = publicado.saude / publicado.populacao_siconfi
vmin, vmax = velho.min(), velho.max()


def pega(metrica, grupo, filtro):
    return base[(base.metrica.str.startswith(metrica)) & (base.grupo == grupo) & (base.filtro == filtro)].iloc[0]


y1 = pega("Y1", "Municípios do RJ", "todos os 92")
y1e = pega("Y1", "Estados e DF", "todos os 27 (com o DF)")


def tela():
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=FUNDO)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    return fig, ax


def caixa(ax, x, y, w, h, fc, ec, lw=3, raio=18):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={raio}", fc=fc, ec=ec, lw=lw))


def texto(ax, x, y, s, px=24, cor=TEXTO, peso="normal", ha="left", va="center", largura=None, espaco=1.22, riscado=False):
    if largura:
        s = "\n".join(textwrap.fill(p, largura) for p in s.split("\n"))
    s = s.replace("$", r"\$")   # dois "$" no mesmo texto viram fórmula no matplotlib
    t = ax.text(x, y, s, fontsize=px * PT, color=cor, fontweight=peso, ha=ha, va=va, linespacing=espaco)
    if riscado:
        fig = ax.figure
        fig.canvas.draw()
        bb = t.get_window_extent()
        inv = ax.transData.inverted()
        (x0, y0), (x1, y1_) = inv.transform((bb.x0, bb.y0)), inv.transform((bb.x1, bb.y1))
        ym = (y0 + y1_) / 2
        ax.plot([x0 - 4, x1 + 4], [ym, ym], color=cor, lw=3.4)
    return t


def card(ax, x, y, w, h, cor, rotulo, titulo):
    caixa(ax, x, y, w, h, "#ffffff", cor, lw=4, raio=22)
    caixa(ax, x, y, w, 96, cor, cor, lw=0, raio=22)
    ax.add_patch(plt.Rectangle((x, y + 60), w, 40, fc=cor, ec=cor, lw=0))   # canto reto embaixo da faixa
    texto(ax, x + 30, y + 30, rotulo, px=21, cor="#ffffff", peso="bold")
    texto(ax, x + 30, y + 68, titulo, px=34, cor="#ffffff", peso="bold")


fig, ax = tela()
texto(ax, 60, 52, "CAPÍTULO 2 · MEASURE", px=24, cor=VIOLETA, peso="bold")
texto(ax, 60, 112, "Antes de explicar o número, desconfie dele", px=62, peso="bold")
texto(ax, 60, 168, "O que mudou quando conferi o gasto em saúde dos municípios do RJ (2024)", px=29, cor=TEXTO_2)

TOPO, ALT, LARG, GAP, X0 = 215, 640, 572, 32, 60
xs = [X0 + i * (LARG + GAP) for i in range(3)]

# --- Card 1: a conferência
x, y = xs[0], TOPO
card(ax, x, y, LARG, ALT, AZUL, "1 · A CONFERÊNCIA", "Contra a prestação de contas")
texto(ax, x + 30, y + 190, f"{n_bate_antes} de {n_total}", px=104, cor=AZUL, peso="bold")
texto(ax, x + 30, y + 285, "entes tinham o gasto em saúde igual ao da prestação de contas anual.", px=27, largura=36)
texto(ax, x + 30, y + 372, "O que não batia, em um município:", px=25, cor=TEXTO_2, peso="bold")
caixa(ax, x + 30, y + 405, 250, 130, "#fdeee8", LARANJA, lw=3, raio=14)
texto(ax, x + 155, y + 436, "Relatório", px=22, cor=TEXTO_2, ha="center")
texto(ax, x + 155, y + 488, f"R$ {br(rreo_mi)} mi", px=44, cor=LARANJA, peso="bold", ha="center")
caixa(ax, x + 292, y + 405, 250, 130, "#e6f6ef", VERDE, lw=3, raio=14)
texto(ax, x + 417, y + 436, "Prestação de contas", px=22, cor=TEXTO_2, ha="center")
texto(ax, x + 417, y + 488, f"R$ {br(dca_mi)} mi", px=44, cor="#0b7a52", peso="bold", ha="center")
texto(ax, x + 30, y + 592, f"Corrigido: {n_total} de {n_total} batem.", px=27, peso="bold")

# --- Card 2: o denominador
x = xs[1]
card(ax, x, y, LARG, ALT, LARANJA, "2 · A CONTA POR HABITANTE", "Confira o denominador")
texto(ax, x + 30, y + 175, "A população do Siconfi não bate com nenhum ano do IBGE. Troquei pela estimativa oficial de 2024.", px=27, largura=38)
texto(ax, x + 30, y + 295, "Eu tinha publicado", px=24, cor=TEXTO_2)
texto(ax, x + 30, y + 350, f"R$ {br(vmin)} a R$ {br(vmax)}", px=46, cor=CINZA, peso="bold", riscado=True)
texto(ax, x + 30, y + 438, "Na verdade é", px=24, cor=TEXTO_2)
texto(ax, x + 30, y + 495, f"R$ {br(y1.minimo)} a R$ {br(y1.maximo)}", px=54, cor=LARANJA, peso="bold")
texto(ax, x + 30, y + 565, f"{br(y1.maximo / y1.minimo, 1)} vezes de diferença por habitante.", px=25)
texto(ax, x + 30, y + 603, "O maior e o menor trocaram de município.", px=25, peso="bold")

# --- Card 3: o ponto de partida
x = xs[2]
card(ax, x, y, LARG, ALT, VERDE, "3 · O PONTO DE PARTIDA", "Baseline congelado")
texto(ax, x + 30, y + 190, f"R$ {br(y1.mediana)}", px=100, cor="#0b7a52", peso="bold")
texto(ax, x + 30, y + 283, "mediana do gasto em saúde por habitante nos 92 municípios do RJ.", px=27, largura=36)
caixa(ax, x + 30, y + 372, LARG - 60, 3, CINZA, CINZA, lw=0, raio=1)
texto(ax, x + 30, y + 460, f"R$ {br(y1e.minimo)}", px=76, cor="#0b7a52", peso="bold")
texto(ax, x + 30, y + 545, "gasto por habitante do estado do RJ, o menor entre os 27 estados e o DF.", px=26, largura=38)

# --- Faixa inferior
caixa(ax, 60, 880, 1800, 118, "#efedfb", VIOLETA, lw=3, raio=18)
texto(ax, 90, 913, "No caminho achei casos que os dados públicos não explicam. Ficam registrados, com ressalva, para quem audita.", px=26, cor=TEXTO, peso="bold")
texto(ax, 90, 962, "Projeto aberto no GitHub e atualizado a cada fase: MatheusAugustoEC/saude-rj", px=26, cor=VIOLETA, peso="bold")
texto(ax, 60, 1042, "Dados declarados pelos próprios entes, 2024, sem auditoria. Gasto em saúde não é qualidade.", px=21, cor=TEXTO_2)

fig.savefig(SAIDA / "marco2_measure.png", dpi=100, facecolor=FUNDO)
fig.savefig(SAIDA / "marco2_measure.svg", facecolor=FUNDO)
print("Gravado:", SAIDA / "marco2_measure.png")
