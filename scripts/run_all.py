"""Refaz as contas do projeto do dado bruto até os resultados, e roda os testes.

Uso (a partir da raiz do repositório):
    python -X utf8 scripts/run_all.py              # só as contas, com os dados brutos que já estão no repositório
    python -X utf8 scripts/run_all.py --coleta     # antes, baixa de novo 2023 e 2025 no Siconfi (demora e depende do site)
Não baixa nada sem --coleta. Os scripts de coleta de 2024 (04) e de verificação de acesso (08, 29, 31) ficam de fora:
os dados de 2024 estão congelados no repositório, e os testes de acesso são datados e se repetem só quando se quer testar a fonte de novo.
A ordem abaixo é a das fases. Cada passo para o programa se o script falhar.
"""
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
COLETA = ["22_coleta_2023_replicacao.py", "32_coleta_2025_confirmacao.py"]
CONTAS = [
    "19_analyze_a1_decomposicao.py", "20_analyze_a2_modelo.py", "21_analyze_a2_sensibilidade.py", "23_analyze_a5_replicacao_2023.py",
    "24_analyze_rodada2_propria_ocasional_siops.py", "28_analyze_modulo_ibge.py", "30_improve_recomendacoes.py", "33_control_confirmacao_2025.py", "35_dados_pagina.py", "36_gerar_pagina.py",
]


def roda(*cmd):
    inicio = time.time()
    r = subprocess.run([sys.executable, "-X", "utf8", *cmd], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8")
    ok = r.returncode == 0
    print(f"{'OK  ' if ok else 'FALHA'} {' '.join(cmd)} ({time.time() - inicio:.0f}s)", flush=True)
    if not ok:
        print(r.stdout[-1500:], r.stderr[-1500:])
        sys.exit(1)


if __name__ == "__main__":
    passos = (COLETA if "--coleta" in sys.argv else []) + CONTAS
    for s in passos:
        roda(f"scripts/{s}")
    roda("-m", "pytest", "tests", "-q")
    print("Tudo certo.")
