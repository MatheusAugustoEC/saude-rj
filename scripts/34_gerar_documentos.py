"""Gera os documentos de leitura em PDF (pasta documentos/) a partir das edições escritas para leitura (documentos/fonte/*.md) e dos gráficos.

Uso: python -X utf8 scripts/34_gerar_documentos.py
Os .md de docs/ são os documentos de trabalho (versionados, usados pelas fases). Os de documentos/fonte/ são a mesma matéria escrita para quem lê: linguagem universal, cores e gráficos.
Os PDFs saem em documentos/. Os gráficos usam os dados do projeto (dados_brutos/teste_acesso_2025.csv e dados_tratados/control_2025_resultados.csv).
Precisa do Microsoft Edge (gera o PDF sem abrir janela), como os relatórios de fase.
"""
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker
import pandas as pd
from matplotlib.patches import FancyBboxPatch

RAIZ = Path(__file__).resolve().parent.parent
FONTE, IMG = RAIZ / "documentos" / "fonte", RAIZ / "documentos" / "fonte" / "img"
IMG.mkdir(parents=True, exist_ok=True)

# cores do estilo dos relatórios (scripts/pdf/relatorio.css): azul = achado, verde = confirmado, laranja = cuidado, vermelho = falha, cinza = detalhe
AZUL, VERDE, LARANJA, VERMELHO, CINZA, TINTA, SUAVE, LINHA = "#2F5D8A", "#2E7D5B", "#B26B00", "#B3261E", "#8A94A0", "#1B2430", "#6B7785", "#DCE2E8"
plt.rcParams.update({"font.family": ["Segoe UI", "DejaVu Sans"], "axes.edgecolor": LINHA, "axes.labelcolor": SUAVE, "xtick.color": SUAVE, "ytick.color": SUAVE})


def fig_chegada_dca():
    d = pd.read_csv(RAIZ / "dados_brutos" / "teste_acesso_2025.csv")
    datas = pd.to_datetime(d.dca_data.dropna().str[:10]).sort_values().reset_index(drop=True)
    y = range(1, len(datas) + 1)
    fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=200)
    ax.step(datas, list(y), where="post", color=AZUL, lw=2.2)
    ax.axvline(pd.Timestamp("2026-04-30"), color=SUAVE, lw=1, ls=(0, (4, 3)))
    ax.text(pd.Timestamp("2026-04-30") - pd.Timedelta(days=3), 90, "30/04: prazo usual", color=SUAVE, fontsize=8, ha="right", va="center")
    ax.axvline(pd.Timestamp("2026-08-31"), ymax=0.62, color=LARANJA, lw=1, ls=(0, (4, 3)))
    ax.text(pd.Timestamp("2026-08-31") + pd.Timedelta(days=3), 40, "31/08: a partir daqui,\no balanço é tratado\ncomo \"dado recente\"", color=LARANJA, fontsize=8, ha="left", va="center", linespacing=1.3)
    ate_abril = int((datas <= pd.Timestamp("2026-04-30")).sum())
    ax.annotate(f"{ate_abril} cidades até o prazo", (pd.Timestamp("2026-04-30"), ate_abril), xytext=(-14, 6), textcoords="offset points", ha="right", fontsize=9, color=TINTA, fontweight="bold")
    ax.annotate(f"{len(datas)} de 92 cidades até {datas.iloc[-1]:%d/%m}", (datas.iloc[-1], len(datas)), xytext=(0, 9), textcoords="offset points", ha="right", fontsize=9, color=TINTA, fontweight="bold")
    ax.set_ylim(0, 95)
    ax.set_ylabel("cidades com balanço anual (DCA) entregue", fontsize=8)
    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: meses[mdates.num2date(v).month - 1]))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.grid(axis="y", color=LINHA, lw=0.6)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    fig.savefig(IMG / "chegada_dca_2025.png")
    plt.close(fig)


def fig_veredictos():
    k = pd.read_csv(RAIZ / "dados_tratados" / "control_2025_resultados.csv")
    blocos = {
        "Analyze (H1 a H8)": {"Sustentada": 5, "Parcial ou com cautela": 1, "Sem conclusão": 2},
        "Improve (R1 a R7)": {"Sustentada": 2, "Parcial ou com cautela": 2, "Não sustentada": 1, "Descritiva": 2},
        "Confirmação em 2025 (K1 a K9)": {"Sustentada": int((k.final == "sustenta").sum()), "Parcial ou com cautela": int((k.final == "enfraquece").sum()), "Não sustentada": int((k.final == "cai").sum())},
    }
    cores = {"Sustentada": VERDE, "Parcial ou com cautela": LARANJA, "Sem conclusão": CINZA, "Não sustentada": VERMELHO, "Descritiva": AZUL}
    marca = {"Sustentada": "✓", "Parcial ou com cautela": "▲", "Sem conclusão": "○", "Não sustentada": "✕", "Descritiva": "–"}
    fig, ax = plt.subplots(figsize=(7.2, 2.6), dpi=200)
    for i, (nome, cats) in enumerate(blocos.items()):
        x = 0
        for cat, n in cats.items():
            if n == 0:
                continue
            ax.barh(i, n, left=x, height=0.55, color=cores[cat], edgecolor="white", lw=2)
            ax.text(x + n / 2, i, f"{marca[cat]} {n}", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
            x += n
    ax.set_yticks(range(len(blocos)))
    ax.set_yticklabels(list(blocos), fontsize=8.5, color=TINTA)
    ax.invert_yaxis()
    ax.set_xlim(0, 9)
    ax.set_xticks([])
    for lado in ("top", "right", "bottom", "left"):
        ax.spines[lado].set_visible(False)
    ax.tick_params(length=0)
    legenda = [plt.Rectangle((0, 0), 1, 1, color=cores[c]) for c in cores]
    ax.legend(legenda, [f"{marca[c]} {c}" for c in cores], loc="upper center", bbox_to_anchor=(0.4, -0.02), ncol=5, frameon=False, fontsize=7.2, handlelength=1, columnspacing=1.2)
    fig.tight_layout()
    fig.savefig(IMG / "veredictos.png")
    plt.close(fig)


def gerar_pdfs():
    gerador = RAIZ / "scripts" / "pdf" / "gerar_pdf.py"
    for md in sorted(FONTE.glob("*.md")):
        saida = RAIZ / "documentos" / (md.stem + ".pdf")
        r = subprocess.run([sys.executable, "-X", "utf8", str(gerador), str(md), "--projeto", "Saúde fiscal do Rio de Janeiro", "--saida", str(saida)], capture_output=True, text=True, encoding="utf-8")
        print(("OK   " if r.returncode == 0 else "FALHA"), saida.name, r.stdout.strip().splitlines()[-1:] if r.returncode == 0 else r.stderr[-400:])


if __name__ == "__main__":
    fig_chegada_dca()
    fig_veredictos()
    gerar_pdfs()
