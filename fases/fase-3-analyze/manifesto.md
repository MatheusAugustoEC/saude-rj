# Manifesto, fase 3 (Analyze)

Gerado em 24/10/2026. O conteúdo de `artefatos/` é uma **cópia congelada**; correção é adendo datado, nunca edição.

## Produzidos (cópia em `artefatos/`)

| Arquivo | O que é | Gerado por | Usado em | SHA-256 |
|---|---|---|---|---|
| `artefatos/19_analyze_a1_decomposicao.py` | A1: decomposição exata do gasto por habitante | à mão (script) | relatório 2.1, notebook 03 | `7cc54cfd69ff297b…` |
| `artefatos/20_analyze_a2_modelo.py` | A2: modelo em log nas 92 cidades, capital prevista de fora | à mão (script) | relatório 2, notebook 03 | `0e8ce90a345a9829…` |
| `artefatos/21_analyze_a2_sensibilidade.py` | A2b: sensibilidade às cidades de maior influência | à mão (script) | relatório 2.2, notebook 03 | `4cb82b908fbf684b…` |
| `artefatos/22_coleta_2023_replicacao.py` | coleta de 2023 no Siconfi (RREO Anexo 01 e DCA I-E), 92 municípios | à mão (script) | A5 | `2d0c7de8cce02987…` |
| `artefatos/23_analyze_a5_replicacao_2023.py` | A5: replicação com 2023 | à mão (script) | relatório 2, notebook 03 | `7a5e1b4fb9427d1f…` |
| `artefatos/24_analyze_rodada2_propria_ocasional_siops.py` | H6, H7 e H8: receita própria, uso ocasional e SIOPS | à mão (script) | relatório 2.3 a 2.5, notebook 03 | `8a56a213f33a109a…` |
| `artefatos/25_gerar_planilha_analyze.py` | gera a planilha de conferência | à mão (script) | planilha | `0569fd662521499a…` |
| `artefatos/26_recalcular_planilha_analyze.ps1` | recalcula a planilha no Excel | à mão (script) | planilha | `6ca12cc821f376ca…` |
| `artefatos/27_conferir_planilha_analyze.py` | confere a planilha contra o Python | à mão (script) | planilha | `c62d3fa6f80f080b…` |
| `artefatos/03_analyze_gasto_saude.ipynb` | notebook de reprodução; confere 47 números do relatório | scripts/fonte_dos_notebooks/build_analyze.py | relatório, página de entrega | `84e49ea6ce9e10a3…` |
| `artefatos/saude_fiscal_rj_analyze.xlsx` | planilha com decomposição, regressão, modelo M3 e previsão da capital em fórmulas (1.778) | scripts/25 | conferência independente | `bbd268cf511610c0…` |
| `artefatos/indicadores_2023_replicacao.csv` | indicadores de 2023 (91 cidades; população interpolada) | scripts/23 | A5, notebook 03 | `73f01a4801aef8fc…` |
| `artefatos/analyze_a1_decomposicao.csv` | decomposição por cidade (desvios de gasto, receita e fatia) | scripts/19 | relatório 2.1 | `0dfb1f7b7fbeecac…` |
| `artefatos/analyze_a2_coeficientes.csv` | coeficientes e intervalos do A2 | scripts/20 | relatório 2 | `ce404e06d32a4420…` |
| `artefatos/analyze_a2_residuos.csv` | resíduo do modelo por cidade | scripts/20 | página de entrega | `fd78fe9baec5a815…` |
| `artefatos/analyze_a5_coeficientes.csv` | coeficientes da replicação em 2023 | scripts/23 | relatório 2 | `2ae6f064f37b0839…` |
| `artefatos/analyze_rodada2_coeficientes.csv` | coeficientes da receita própria e do uso ocasional | scripts/24 | relatório 2.3, 2.4 | `5349302fa2b071c7…` |
| `artefatos/analyze_rodada2_tabela_2024.csv` | receita própria, transferências e uso ocasional por cidade (2024) | scripts/24 | página de entrega | `ca00a285920e3be1…` |
| `artefatos/analyze_rodada2_siops_2024.csv` | SIOPS por cidade (percentual aplicado e parte do gasto) | scripts/24 | relatório 2.5 | `105e41ff82093118…` |
| `artefatos/09-analyze-hipoteses.md` | hipóteses e critérios (A0), com a previsão de 2023 e a segunda rodada | à mão | relatório | `b571d2be550cd2ec…` |
| `artefatos/10-metodos-estatisticos.md` | métodos: o que é, por que, como | à mão | relatório, página final | `a18a43d3924e9d84…` |

A coluna SHA-256 mostra os 16 primeiros caracteres; o código completo de cada artefato pode ser recalculado com `Get-FileHash` (PowerShell) ou `sha256sum`.

## Dados brutos usados (não copiados; caminho original e SHA-256 completo)

| Arquivo | SHA-256 |
|---|---|
| `dados_brutos/siconfi_rreo_2024.csv` | `4328e57f571f02a0866e33d7d48794eee80b8adf983cb0acee570be4b0568ef8` |
| `dados_brutos/siconfi_dca_ie_2024.csv` | `9bd897e985ace321c89b7c0b155d0e1ccc027bcf70cc20a5adc7c77120b86821` |
| `dados_brutos/siconfi_rreo_anexo01_2023.csv` | `b441d14ef1dc5785688786ae4776a5d247fdf620b17a7e19525ffc3affd1df27` |
| `dados_brutos/siconfi_dca_ie_2023.csv` | `a374e66533f50339265620ea60202351b2dbf5efc6640643311e0fc9391f0a26` |
| `dados_brutos/siconfi_chamadas_2023.csv` | `11e90b20eca688879fbb04a97a4a2c789216197a82bfddd4c96f41f23b137bda` |
| `dados_brutos/ibge_populacao_6579.json` | `f22706f1909681dadcf42a829c9ba36e6f5d8f1919ce82c380db8e61b47bd36e` |
| `dados_brutos/ibge_populacao_censo2022_4714.json` | `fd624f5e387265cc745263799f961dbe05b9e64d6f3b9e8b25eeedc843d504ea` |
| `dados_brutos/ibge_domicilios_uso_ocasional_9866.json` | `fbaabdf613395fb4a2119e9542f3e22a9baaebfe5428e3ec5be3d9b4f27fa178` |
| `dados_brutos/LCL141.xlsx` | `621c4cf9c770d71bc2666ad66de1360d0361d21ad88267280e5f425e4220a948` |
| `dados_brutos/municipios_rj_ceperj.csv` | `140c54ec8bff459dbc22810c1cde68b4a222ddcfcb6491b40f301df04a21e040` |

## Também usados (congelados na fase 2B)

| Arquivo | SHA-256 |
|---|---|
| `dados_tratados/indicadores_2024.csv` | `3b2de3197587bec5093eaccbdc6eb4e7202f3f73387b4d1857cc5b343fba9b15` |
| `dados_tratados/indicadores_measure_2024.csv` | `1e7f28a744823365a5d7ce026061cd7e9b8176c7a90696acd0c673c765208061` |
