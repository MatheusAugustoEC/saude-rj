# Saúde fiscal do Rio de Janeiro

| Fase | Status | Tollgate | Relatório | Data |
|---|---|---|---|---|
| 0 · Reconhecimento | feita antes do método (viabilidade e coleta) | — | [docs/02](../docs/02-fontes-de-dados.md), [docs/03](../docs/03-relatorio-coleta.md) | 21/10/2026 |
| 1 · Define | concluída | declaração do problema aprovada | [docs/01](../docs/01-define-relatorio.md) | 22/10/2026 |
| 2A · Measure, o instrumento | concluída | APROVADO COM RESSALVA | [relatório](fase-2a-measure-qualidade/relatorio.pdf) | 23/10/2026 |
| 2B · Measure, o processo | concluída | APROVADO COM RESSALVA | [relatório](fase-2b-measure-baseline/relatorio.pdf) | 23/10/2026 |
| 3 · Analyze | concluída | APROVADO | [relatório](fase-3-analyze/relatorio.pdf) | 24/10/2026 |
| 4 · Improve | concluída | APROVADO | [relatório](fase-4-improve/relatorio.pdf) | 24/10/2026 |
| 5 · Control | concluída | APROVADO | [relatório](fase-5-control/relatorio.pdf) | 25/10/2026 |
| 6 · Entrega | página construída e auditada (2 rodadas); aguardando tollgate | pendente | [relatório](fase-6-entrega/relatorio.pdf) | 27/10/2026 |

Marco 1 (Define) publicado no LinkedIn pelo Matheus em 22/10/2026.

## Fluxo

```mermaid
flowchart LR
  F0[Reconhecimento: fontes e coleta] --> F1[Define: pergunta, Y e X, SIPOC, mapa]
  F1 --> F2A[Measure 2A: dado conferido contra DCA e leis]
  F2A --> F2B[Measure 2B: baseline congelado]
  F2B --> F3[Analyze: testar os X contra os Y]
  F3 --> F4[Improve: contramedidas de controle e seus testes]
  F4 --> F5[Control: confirmação com 2025, plano de acompanhamento, testes]
```

## Decisões que atravessam o projeto

| Decisão | Fase de origem |
|---|---|
| Pergunta central e Y: gasto em saúde por habitante (Y1) e fatia da despesa (Y2); usar "gasta", não "investe" | Define |
| Escopo: Siconfi como núcleo; IBGE, SUS e SIOPS como módulos | Define |
| Regiões: 8 Regiões de Governo do CEPERJ, capital à parte, só descrição onde o n não sustenta | Define, Measure 2B |
| Atípicos e relatórios simplificados: manter, marcar e mostrar com e sem | Define |
| População: estimativa 2024 do IBGE | Measure 2A |
| Saúde de Búzios pela DCA | Measure 2A |
| Limites legais (LRF, Resolução do Senado 40/2001, LC 141) ao lado dos declarados | Measure 2A |
| O que fica sem explicação é achado de auditoria, com ressalva | Measure 2A |
| Todo insight vai com a ressalva (gasto não é qualidade) | Define |
| DF fora do SIOPS por enquanto; retomar ao terminar o núcleo | Measure 2A |
| Recorte "núcleo da Baixada": 6 municípios, rotulado como escolha analítica; só descrição (n = 6) | Measure 2A, decisão de 23/10/2026 |
| Improve: sete contramedidas de controle e gestão, sem recomendar gastar mais; ajuste de veraneio (R3) não sustentado; R7 só descritiva | Improve, decisão de 24/10/2026 |
| Dados do IBGE e do SUS entram depois do núcleo, como extensões ([docs/12](../docs/12-extensoes-depois-do-nucleo.md)) | decisão de 24/10/2026 |
| Página de entrega estática, atualizada por um comando; teste automático no GitHub; sem atualização agendada completa | Control, decisão de 25/10/2026 |
| Texto público em linguagem universal (nunca "para leigos") | Control, decisão de 25/10/2026 |
| Repositório público no GitHub, com todos os dados brutos; licença MIT (código) e CC BY 4.0 (textos e análises); rótulos de dado em dúvida mantidos | decisão de 23/10/2026 |
