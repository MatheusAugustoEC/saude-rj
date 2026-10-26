# Saúde fiscal do Rio de Janeiro

**Quem gasta mais em saúde, por habitante e como parte do orçamento, entre os estados e os municípios do RJ, e o que explica a diferença?**

Projeto de análise de dados públicos reais (Siconfi, Tesouro Nacional), conduzido em **Lean Six Sigma (DMAIC)**, fase a fase, com o trabalho aberto para quem quiser acompanhar, conferir e questionar. O público pensado é quem trabalha com controles, auditoria, compliance e gestão pública.

> **Leia isto antes de qualquer número.** Os dados são **declarados pelos próprios entes** ao Tesouro Nacional, de 2024. Conferi o que foi possível contra uma segunda fonte, mas **não auditei**. Gasto em saúde **não é qualidade** da saúde: o gasto por habitante acompanha a receita por habitante.

## Onde o projeto está

| Fase | Status | Relatório |
|---|---|---|
| Reconhecimento (fontes e coleta) | feita | [docs/02](docs/02-fontes-de-dados.md), [docs/03](docs/03-relatorio-coleta.md) |
| Define (pergunta, Y e X, SIPOC, mapa do processo) | concluída | [docs/01](docs/01-define-relatorio.md) |
| Measure 2A (o dado é confiável?) | concluída, aprovada com ressalva | [fases/fase-2a-measure-qualidade](fases/fase-2a-measure-qualidade/relatorio.pdf) |
| Measure 2B (o que o processo entrega hoje?) | concluída, aprovada com ressalva | [fases/fase-2b-measure-baseline](fases/fase-2b-measure-baseline/relatorio.pdf) |
| Analyze (o que explica o gasto por habitante?) | concluída, aprovada | [fases/fase-3-analyze](fases/fase-3-analyze/relatorio.pdf) |
| Improve (o que controle, auditoria e gestão podem fazer com isso?) | concluída, aprovada | [fases/fase-4-improve](fases/fase-4-improve/relatorio.pdf) |
| Control (como acompanhar sem perder o rumo) | em andamento: confirmação com dados de 2025 feita | [docs/14](docs/14-control-previsoes-2025.md), [docs/15](docs/15-plano-de-controle.md) |

O mapa completo, com as decisões que atravessam o projeto, está em [fases/indice.md](fases/indice.md).

## O que já se sabe (baseline do Measure, 2024)

- Entre os **92 municípios do RJ**, o gasto em saúde por habitante vai de **R$ 900 a R$ 6.465** (7,2 vezes), com mediana de **R$ 2.319**.
- O **estado do RJ** gasta **R$ 606** por habitante, o menor entre os 27 estados e o DF (mediana R$ 946).
- A fatia da despesa que vai para saúde tem mediana de **29,0%** nos municípios e **16,2%** nos estados.
- Só 3 das 8 Regiões de Governo do CEPERJ têm municípios suficientes para sustentar uma comparação estatística.

O baseline está congelado em [fases/fase-2b-measure-baseline/artefatos](fases/fase-2b-measure-baseline/artefatos/baseline_measure_2024.csv), com SHA-256.

## Pontos de atenção que pedem apuração

Ao conferir os dados apareceram casos que os dados públicos **não explicam** (despesa acima da receita mais os saldos de anos anteriores, relatórios do mesmo ente que se contradizem, limites de pessoal declarados diferentes da LRF). **Não afirmo irregularidade**: a causa de cada um não está confirmada, e a lista com a ressalva de cada item está em [docs/05](docs/05-insights-do-projeto.md) e [docs/07](docs/07-measure-grupo1.md).

## Como o projeto está organizado

| Pasta | Conteúdo |
|---|---|
| `docs/` | Define, fontes de dados, relatório da coleta, pendências e resultados do Measure, insights com ressalva |
| `fases/` | Checkpoint de cada fase: relatório (`.md` e `.pdf`), manifesto com SHA-256 e artefatos congelados |
| `notebooks/` | `01_eda_siconfi_2024` (exploração) e `02_measure_qualidade_e_baseline` (qualidade e baseline) |
| `scripts/` | Coleta, conferência, planilha e imagens, numerados na ordem de uso; `fonte_dos_notebooks/` gera os notebooks |
| `dados_brutos/` | O que as fontes devolveram, sem tratamento |
| `dados_tratados/` | Indicadores calculados e conferências |
| `planilhas/` | Planilha em Excel com fórmulas visíveis e conferida contra o código |
| `imagens/` | SIPOC e mapa do processo |
| `tests/` e `config/` | Testes automáticos do dado e parâmetros fixados do projeto |

## Fontes de dados

| Fonte | Instituição |
|---|---|
| RREO, RGF e DCA (API de dados abertos) | Secretaria do Tesouro Nacional (Siconfi) |
| População (estimativa 2024) e malha municipal | Instituto Brasileiro de Geografia e Estatística (IBGE) |
| Regiões de Governo | Centro de Estatísticas, Estudos e Pesquisas (CEEP), Fundação CEPERJ |
| Mínimo legal de saúde (LC 141/2012) | Ministério da Saúde (SIOPS) |
| Leis e normas | Planalto, Câmara dos Deputados, Tesouro Nacional e Secretaria de Orçamento Federal |

Credibilidade e limitações de cada fonte: [docs/02-fontes-de-dados.md](docs/02-fontes-de-dados.md).

## Como reproduzir

**O caminho curto (Analyze, Improve e Control).** Os dados brutos já estão no repositório. Com Python 3.11:

```
pip install -r requirements.txt
python -X utf8 scripts/run_all.py
```

Em cerca de dois minutos o comando refaz todas as contas e roda os testes. Na última conferência, os arquivos de resultado saíram idênticos aos gravados. Para baixar de novo 2023 e 2025 do Siconfi, use `--coleta` (demora e depende do site do Tesouro). Os parâmetros fixados estão em [config/parametros.json](config/parametros.json). Os testes automáticos do dado (`python -m pytest tests -q`) também rodam no GitHub a cada mudança.

**O caminho longo (Define e Measure).** A coleta usa a API pública do Siconfi e do IBGE, sem chave.

1. Coleta: `scripts/04_coleta_valores.py`, `06_pessoal_por_poder.py`, `07_viabilidade_divida_restos.py`, `13_coleta_dca_funcao_saude.py`, `14_coleta_rreo_anexo03_rcl.py`.
2. Indicadores: `cd scripts/fonte_dos_notebooks && python build_nb2.py` (gera `dados_tratados/indicadores_2024.csv`).
3. Measure: `python build_measure.py` na mesma pasta. **Atenção:** ele regrava o baseline, que deve ser imutável (veja o `LEIA-ME.md` da pasta).
4. Planilha: `scripts/09_gerar_planilha.py`, depois `11_recalcular_planilha.ps1` (usa o Excel) e `10_conferir_planilha.py`.

## Licença

Código sob **MIT** ([LICENSE](LICENSE)). Textos, relatórios, análises e tabelas do autor sob **CC BY 4.0** ([LICENSE-TEXTOS.md](LICENSE-TEXTOS.md)). Os dados brutos são públicos e pertencem às instituições de origem.

## Autor

Matheus ([@MatheusAugustoEC](https://github.com/MatheusAugustoEC)), economista, com cinco anos como analista de compliance e controles.
