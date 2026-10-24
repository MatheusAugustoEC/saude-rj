# Fonte dos notebooks

Os notebooks são gerados por código, para que cada número venha dos dados e nada seja digitado à mão.

| Notebook | Células (fonte) | Montagem e execução |
|---|---|---|
| `notebooks/01_eda_siconfi_2024.ipynb` | `cells_eda_v2.py` | `python build_nb2.py` |
| `notebooks/02_measure_qualidade_e_baseline.ipynb` | `cells_measure.py` | `python build_measure.py` |
| `notebooks/03_analyze_gasto_saude.ipynb` | `cells_analyze.py` | `python build_analyze.py` (depende de `scripts/_mapa_comum.py` e dos dados de `scripts/22`, `scripts/23`) |

Rode de dentro desta pasta. Cada `build_*.py` monta o notebook e o executa com `nbconvert`. **Não rode `build_measure.py` de novo depois de fechado o Measure sem antes ler `fases/fase-2b-measure-baseline/`:** ele regrava o baseline (que deve ser imutável).
