# Manifesto, fase 5 (Control)

Gerado em 25/10/2026. O conteúdo de `artefatos/` é uma **cópia congelada**; correção é adendo datado, nunca edição.

## Produzidos (cópia em `artefatos/`)

| Arquivo | O que é | Gerado por | Usado em | SHA-256 |
|---|---|---|---|---|
| `artefatos/31_teste_acesso_2025.py` | verifica a disponibilidade de 2025 sem ler valores | à mão (script) | relatório 2.1 | `0ade5974c417559e…` |
| `artefatos/32_coleta_2025_confirmacao.py` | coleta de 2025 no Siconfi (RREO Anexo 01 e DCA I-E) | à mão (script) | relatório 2.1 | `257ae4e458616ac2…` |
| `artefatos/33_control_confirmacao_2025.py` | recorte de confirmação K1 a K9, aberto uma vez | à mão (script) | relatório 2.1 | `6b1c6845db284b23…` |
| `artefatos/run_all.py` | refaz todas as contas e roda os testes | à mão (script) | relatório 2.3 | `4f94a459f04c7741…` |
| `artefatos/test_dados.py` | 13 testes automáticos do dado | à mão (script) | relatório 2.3 | `44c2d9406156a0db…` |
| `artefatos/parametros.json` | parâmetros fixados do projeto | à mão | testes, relatório 2.3 | `6710ff88256ccb2c…` |
| `artefatos/requirements.txt` | ambiente com versões fixadas | à mão | relatório 2.3 | `9004f8c59cde4883…` |
| `artefatos/testes.yml` | teste automático no GitHub (ainda não rodou lá) | à mão | relatório 2.3 | `2ce902e57a6f4214…` |
| `artefatos/control_2025_saida.txt` | saída completa da análise de 2025 | scripts/33 | relatório 2.1 | `d70872f52d905c6c…` |
| `artefatos/control_2025_resultados.csv` | classificação de K1 a K9, com e sem DCAs recentes | scripts/33 | relatório 2.1 | `5de1b2d65706d1de…` |
| `artefatos/control_2025_residuos.csv` | resíduo de cada cidade em 2025 | scripts/33 | relatório 2.1 | `58baffd5c18d33c6…` |
| `artefatos/14-control-previsoes-2025.md` | previsões, critérios, desempates e resultado de 2025 | à mão | relatório | `51d8505894060619…` |
| `artefatos/15-plano-de-controle.md` | plano de acompanhamento, o que invalida, padrões reutilizáveis | à mão | relatório 2.2 | `85de8252280d74a8…` |
| `artefatos/16-kaizen-do-projeto.md` | Kaizen do projeto, em linguagem universal | à mão | relatório 2.4 | `d282b0961046306a…` |

A coluna SHA-256 mostra os 16 primeiros caracteres; o código completo de cada artefato pode ser recalculado com `Get-FileHash` (PowerShell) ou `sha256sum`.

## Dados brutos usados (não copiados; caminho original e SHA-256 completo)

| Arquivo | SHA-256 |
|---|---|
| `dados_brutos/siconfi_rreo_anexo01_2025.csv` | `b787b896a8f6ea3a4053bffc97f8441b1169dd4b10228bdd52dcb23cbe158f75` |
| `dados_brutos/siconfi_dca_ie_2025.csv` | `e0f8ab7d002ab86e71e7009182d75957997cca081b76267805a2751fac7c1ff6` |
| `dados_brutos/siconfi_chamadas_2025.csv` | `c82f5d1c8efe9a8c6611e79a60e7d84da6cced3cf08fcc3da27adf8c1598cbb9` |
| `dados_brutos/teste_acesso_2025.csv` | `d9531cc50ab39e386b35f3b203e3946806f1c3012fa99c1006761b15ef3f8d48` |
| `dados_brutos/siconfi_rreo_2024.csv` | `4328e57f571f02a0866e33d7d48794eee80b8adf983cb0acee570be4b0568ef8` |

## Dados tratados usados (congelados em fases anteriores)

| Arquivo | SHA-256 |
|---|---|
| `dados_tratados/indicadores_2024.csv` | `3b2de3197587bec5093eaccbdc6eb4e7202f3f73387b4d1857cc5b343fba9b15` |
| `dados_tratados/improve_r1_triagem.csv` | `a09517b81c0ae8d7863319296736ede0aa6da2eaa8397575420b684449a42fe0` |
