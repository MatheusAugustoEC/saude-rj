# Manifesto, fase 4 (Improve)

Gerado em 24/10/2026. O conteúdo de `artefatos/` é uma **cópia congelada**; correção é adendo datado, nunca edição.

## Produzidos (cópia em `artefatos/`)

| Arquivo | O que é | Gerado por | Usado em | SHA-256 |
|---|---|---|---|---|
| `artefatos/30_improve_recomendacoes.py` | contas das recomendações R1 a R7 | à mão (script) | relatório 2 | `281803e1e116c3da…` |
| `artefatos/improve_saida.txt` | saída completa do script, linha a linha | scripts/30 | relatório, conferência | `4d60d4cac152befe…` |
| `artefatos/improve_r1_triagem.csv` | triagem por cidade: resíduo em 2023 e 2024, intervalo, sinalização | scripts/30 | relatório 2.1 | `a09517b81c0ae8d7…` |
| `artefatos/improve_r2_pares.csv` | pares por receita: desvio contra a região e contra os pares | scripts/30 | relatório 2.2 | `e6396ecd013c1ea1…` |
| `artefatos/improve_r3_veraneio.csv` | resíduo por grupo conforme visitantes por domicílio ocasional | scripts/30 | relatório 2.3 | `b88c33ceceb53e63…` |
| `artefatos/improve_r4_estresse.csv` | cenários do teste de estresse dos repasses | scripts/30 | relatório 2.4 | `8fd2be567fbba90c…` |
| `artefatos/improve_r4_dependencia.csv` | parte da receita que vem de repasses, por cidade | scripts/30 | relatório 2.4 | `bb6b25310eeaa1e6…` |
| `artefatos/improve_r5_r6_siops.csv` | folga sobre o mínimo e razão Siconfi x SIOPS, por cidade | scripts/30 | relatório 2.5 | `157a9f27cc0c5433…` |
| `artefatos/improve_r7_limites.csv` | pessoal, dívida e restos a pagar contra limites, por município | scripts/30 | relatório 2.5 | `3610428a4999bdf3…` |
| `artefatos/13-improve-criterios.md` | recomendações, hipóteses e critérios escritos antes de rodar | à mão | relatório | `da34a15c8ce0d1d8…` |

A coluna SHA-256 mostra os 16 primeiros caracteres; o código completo de cada artefato pode ser recalculado com `Get-FileHash` (PowerShell) ou `sha256sum`.

## Dados brutos usados (não copiados; caminho original e SHA-256 completo)

| Arquivo | SHA-256 |
|---|---|
| `dados_brutos/siconfi_rreo_2024.csv` | `4328e57f571f02a0866e33d7d48794eee80b8adf983cb0acee570be4b0568ef8` |
| `dados_brutos/siconfi_rreo_anexo01_2023.csv` | `b441d14ef1dc5785688786ae4776a5d247fdf620b17a7e19525ffc3affd1df27` |
| `dados_brutos/ibge_domicilios_uso_ocasional_9866.json` | `fbaabdf613395fb4a2119e9542f3e22a9baaebfe5428e3ec5be3d9b4f27fa178` |
| `dados_brutos/LCL141.xlsx` | `621c4cf9c770d71bc2666ad66de1360d0361d21ad88267280e5f425e4220a948` |
| `dados_brutos/municipios_rj_ceperj.csv` | `140c54ec8bff459dbc22810c1cde68b4a222ddcfcb6491b40f301df04a21e040` |

## Dados tratados usados (congelados em fases anteriores)

| Arquivo | SHA-256 |
|---|---|
| `dados_tratados/indicadores_2024.csv` | `3b2de3197587bec5093eaccbdc6eb4e7202f3f73387b4d1857cc5b343fba9b15` |
| `dados_tratados/indicadores_measure_2024.csv` | `1e7f28a744823365a5d7ce026061cd7e9b8176c7a90696acd0c673c765208061` |
| `dados_tratados/indicadores_2023_replicacao.csv` | `73f01a4801aef8fc1c28d5e0c8510fd56825c2662fa527a9e288f6f83a441939` |
