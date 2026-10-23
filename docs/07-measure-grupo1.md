# Measure, grupo 1: A2 (Búzios), A5 (sete municípios) e B1 (população)

Data: 22/10/2026. Regras do método usadas: M2 (acurácia, com segunda fonte), M3 e M5 (atípico só com regra escrita, "com e sem"), M4 (procedência do dado). **Nenhum indicador do notebook, da planilha ou dos posts foi alterado.** As mudanças abaixo são propostas para aprovação.

## A2. Armação dos Búzios: corrigido com fonte

| Fonte | Despesa total | Saúde |
|---|---|---|
| RREO Anexo 01 (empenhada até o 6º bimestre) | R$ 542,7 mi | não traz função |
| RREO Anexo 02 (o que o notebook usava) | R$ 269,3 mi | R$ 33,9 mi (coluna "no bimestre": R$ 159,2 mi) |
| **DCA Anexo I-E (prestação de contas anual)** | **R$ 530,7 mi** | **R$ 156,2 mi** |
| SIOPS (só recursos próprios em saúde) | | R$ 72,9 mi |

- O Anexo 02 de Búzios é incoerente por dentro: o valor "no bimestre" (saúde R$ 159,2 mi; total R$ 383,8 mi) é maior que o acumulado "até o bimestre" (R$ 33,9 mi; R$ 290,8 mi), o que não acontece nos outros municípios.
- A DCA concorda com o Anexo 01 (diferença de 2%) e com o SIOPS (recursos próprios não podem passar do total).
- **Validação nos 119 entes** (`scripts/13_coleta_dca_funcao_saude.py`, 119 chamadas, 0 falhas): a saúde do RREO bate com a DCA em até 0,1% em 117 entes; Porciúncula difere 0,7%; **Búzios é o único fora**. Resultado em `dados_tratados/conferencia_saude_rreo_vs_dca.csv`.
- **Proposta:** usar a saúde da DCA para Búzios (R$ 156,2 mi, R$ 4.003 por habitante com a população do Siconfi) e tirar a marca de "totais inconsistentes" da saúde por habitante dele. Ele entra no meio da distribuição, não é mais o menor (R$ 867). O intervalo do post (R$ 1.026 a R$ 6.853) não muda por causa disso.

## A5. Sete municípios com despesa acima de 115% da receita: parcialmente confirmado

| Município | Despesa ÷ receita | Despesa ÷ (receita + saldos de anos anteriores usados) | DCA x RREO (despesa) |
|---|---|---|---|
| Cambuci | 1,215 | **0,854** (explicado) | 0,978 |
| Itaboraí | 1,153 | **0,960** (explicado) | 1,000 |
| Eng. Paulo de Frontin | 1,174 | 1,026 (perto) | 1,025 |
| Carapebus | 1,123 | 1,046 (perto) | 1,000 |
| Porciúncula | 1,278 | 1,172 | 0,998 |
| Barra do Piraí | 1,245 | 1,193 | 1,000 |
| Rio Bonito | 1,224 | 1,198 | 1,000 |

- A **despesa é real** (a DCA confirma). O que varia é a explicação.
- **Sem explicação nos dados que temos:** Porciúncula, Barra do Piraí e Rio Bonito (gastaram 17% a 20% acima da receita mais os saldos). A receita de Porciúncula no RREO (R$ 152,3 mi) é 26% **maior** que a da DCA (R$ 120,8 mi), diferença não explicada. Para os outros seis, o RREO fica 6% a 10% abaixo da DCA bruta, coerente com deduções, mas não reconciliado.
- 2024 é ano final de mandato municipal; **isso é só uma hipótese de contexto, não verificada**, e não vai para texto público.
- **Efeito no projeto:** a saúde por habitante desses sete não é afetada (bate com a DCA). A receita por habitante de Porciúncula fica em dúvida (afeta o X "receita por habitante" dele).
- Carapebus, o "maior" do ranking, tem a saúde **confirmada pela DCA**.

## B1. População: origem não confirmada, e ela muda os extremos

- O Siconfi traz um valor único de população por município, sem dizer o ano. Comparado ao IBGE (SIDRA, tabela 6579, estimativas de 2018 a 2025, e tabela 4714, Censo 2022): **nenhum ano bate** (0 de 92 iguais; 1 de 92 com o Censo). Mais próximo: Censo 2022 (diferença mediana de 1,9%). Estimativa 2024: diferença mediana de 5,4%.
- Efeito na saúde por habitante dos municípios (com Búzios corrigido):

| População usada | Menor | Maior | Razão |
|---|---|---|---|
| Siconfi | São Pedro da Aldeia, R$ 1.026 | Carapebus, R$ 6.853 | 6,7 |
| Estimativa IBGE 2024 | São João de Meriti, R$ 900 | São João da Barra, R$ 6.465 | 7,2 |
| Censo 2022 | São João de Meriti, R$ 952 | São João da Barra, R$ 6.842 | 7,2 |

- A ordem geral quase não muda (Spearman 0,99; maior mudança de posição: 17), mas **o menor e o maior trocam de município**. Com a população do Siconfi, Carapebus e São João da Barra empatam no topo (diferença de 22 centavos).
- **Decisão pendente do Matheus:** qual população usar. Recomendação do assistente: a **estimativa 2024 do IBGE** (oficial, do mesmo ano da despesa, reproduzível, igual para estados e municípios), com a população do Siconfi como análise de sensibilidade. Se for adotada, os números do post publicado (R$ 1.026 a R$ 6.853; 6,7 vezes) passam a ser R$ 900 a R$ 6.465 (7,2 vezes), e vale decidir se uma nota de correção é necessária.

## Arquivos criados ou atualizados

- `scripts/13_coleta_dca_funcao_saude.py`; `dados_brutos/siconfi_dca_ie_2024.csv` e `siconfi_dca_ie_chamadas_2024.csv`.
- `dados_brutos/ibge_populacao_6579.json` e `ibge_populacao_censo2022_4714.json`.
- `dados_tratados/conferencia_saude_rreo_vs_dca.csv`.
- `docs/04` (status de A2, A5 e B1) e `docs/05` (I8 e I9).

## Decisões do Matheus e etapa 1 aplicada (23/10/2026)

- **A2:** seguir a recomendação (saúde de Búzios pela DCA). **B1:** usar a estimativa 2024 do IBGE. **A5:** os três municípios sem explicação são tratados como **achado** (ponto de atenção que pede apuração, com a ressalva), e não como defeito de dado (insight I10 em `docs/05`).
- **Aplicado:** `scripts` do notebook (população do IBGE em `populacao`, a do Siconfi em `populacao_siconfi`; saúde de Búzios pela DCA em `saude`, original em `saude_rreo`; denominador da fatia da saúde em `despesa_base_saude`), notebook regerado (59 células, 0 erros), `dados_tratados/indicadores_2024.csv` regerado e planilha regerada e recalculada pelo Excel (3.081 fórmulas, **0 diferenças** contra o CSV). Cópias do estado anterior: `notebooks/arquivo/..._antes_do_measure.ipynb`, `dados_tratados/arquivo/` e `planilhas/arquivo/`.

### O que mudou nos números (antes → depois)

| Indicador | Antes | Depois |
|---|---|---|
| Municípios, menor gasto em saúde por habitante | Búzios R$ 867 (caso especial); sem especiais, São Pedro da Aldeia R$ 1.026 | São João de Meriti **R$ 900** |
| Municípios, maior | Carapebus R$ 6.853 | São João da Barra **R$ 6.465** (Carapebus: R$ 6.391) |
| Municípios, mediana | R$ 2.379 | **R$ 2.319** |
| Estados, menor / maior / mediana | RJ R$ 628 / Amapá R$ 2.765 / R$ 975 | RJ **R$ 606** / Amapá **R$ 2.666** / **R$ 946** |
| Capital, saúde por habitante (posição entre 92) | R$ 1.153 (85ª maior) | **R$ 1.136** (85ª maior) |
| Correlação receita x saúde por habitante (Spearman) | 0,80 estados, 0,82 municípios | 0,80 estados, **0,87** municípios |
| Correlação receita x fatia da saúde, municípios | −0,33 | **−0,31** |
| Maior variação das medianas sem os casos especiais | 3,2% | **4,7%** |

**O post publicado** (R$ 1.026 a R$ 6.853, 6,7 vezes; correlação de 0,82) usou a população do Siconfi. Com o critério adotado, os mesmos números ficam: **R$ 900 a R$ 6.465 (7,2 vezes) e correlação de 0,87.** A conclusão do post (gasto acompanha receita; gasto não é qualidade) se mantém e até se reforça. Se o Matheus quiser registrar o ajuste, o rascunho de uma nota está em `docs/06`.


# Etapa 2: auditoria do dado (23/10/2026)

Regras usadas: M2 (acurácia com segunda fonte e integridade entre relatórios), M3 (nulo legítimo), M4 (procedência), M5 (atípico só com regra escrita). Nenhum item foi resolvido por suposição.

## Resultado das 17 pendências restantes

| Item | Resultado |
|---|---|
| A1 | Corrigido com fonte: limite legal de dívida é 2x/1,2x a RCL (Resolução do Senado 40/2001); os 3 entes fora do padrão têm dívida muito abaixo de qualquer limite |
| A3 | Areal e Miracema: RCL subestimada porque o RREO Anexo 03 deles traz só 4 e 2 dos 12 meses de receita. **Itaperuna: o RCL do RGF é 3 vezes menor que o do RREO do mesmo ente, sem causa identificada (achado)** |
| A4 | Confirmado: faltava a 4ª dedução (R$ 244.779,28) |
| A6 | Sem confirmação: Itatiaia não declarou a inscrição de restos a pagar do exercício; Saquarema e Vassouras não declararam o limite do Senado |
| B1 | O cadastro do Siconfi traz a população do IBGE 2025 (92 de 92 municípios); o campo dos relatórios que usávamos não bate com nenhum ano. Decisão: IBGE 2024 |
| B2 a B7 | B2 e B3 confirmados em fonte oficial; B4 sem confirmação; B5, B6 e B7 confirmados só em parte, por fonte secundária |
| C1 a C4 | C1, C3 e C4 confirmados no texto oficial; C2 em parte |

## Achados que pedem apuração (ressalva: dado declarado pelos entes, sem auditoria nossa, causa não confirmada)

1. **Barra do Piraí, Rio Bonito e Porciúncula**: despesa de 17% a 20% acima da receita mais saldos de anos anteriores (A5).
2. **Itaperuna**: RCL do RGF (R$ 192,8 mi) contra R$ 583,8 mi no RREO do mesmo ente (A3). Com o RCL do Anexo 03, o pessoal total (soma dos Poderes) seria 47,5% da RCL ajustada, em vez dos 141,7% que o RGF mostra (sensibilidade, não correção).
3. **Limites de pessoal declarados que diferem da LRF (C1)**: Maricá (Executivo 60% contra 54%), Mesquita (Legislativo 54% contra 6%), Nilópolis (Legislativo 6,23%), Valença (Legislativo 1%), e Pará, Bahia e Goiás (Executivo 48,6% contra 49%). O limite que o ente declara afeta a folga que calculamos.
4. **Porciúncula**: a receita no RREO (R$ 152,3 mi) é 26% maior que na DCA (R$ 120,8 mi).

## O que será aplicado na regeneração final (depois da etapa 3)

Limite legal de dívida (2x/1,2x) em todos os entes; limite legal de pessoal do Executivo (49% estados e DF, 54% municípios) como coluna ao lado do declarado; a 4ª dedução da RCL; regiões do CEPERJ (`dados_brutos/municipios_rj_ceperj.csv`).


# Fechamento das pendências (23/10/2026)

Fechadas em fonte oficial: **B5, B6, B7, C2**, com reforço em B2. Origem do CEPERJ e da malha registrada pela instituição, sem link (E1 e E3).

- **Defensoria (B5).** A Defensoria entrega o próprio RGF, mas ele não traz a despesa total com pessoal nem o limite (a LRF não fixa limite para ela). Por isso a soma de pessoal dos Poderes **não a inclui**. A despesa líquida dela é de 0,5% a 2,5% da do Executivo, e incluí-la subiria o pessoal total dos estados em 0,18 a 1,17 ponto da RCL (RJ: de 54,3% para 55,4%, mesma posição). Tratamento: manter a soma atual, com a ressalva dita.
- **Anexos 8 e 12 (B6).** A Portaria STN 642/2019 manda esses anexos ao SIOPE e ao SIOPS, e não ao Siconfi. Voltar vazio na API é o comportamento esperado.
- **Função Saúde (B7).** A função 10 e suas seis subfunções são definidas por portaria federal, válida para todos os entes. Continua sem prova que cada ente classifica o mesmo conteúdo nela.

**Ainda abertas:** B4 (qual versão a API devolve numa retificação; o documento de metadados do Tesouro recusou o acesso, tentar de novo), D1 (DF no SIOPS) e D2 (módulos IBGE e SUS), as duas depois do núcleo.

**E2 decidido (23/10/2026):** recorte "núcleo da Baixada" com 6 municípios, rotulado como escolha analítica (fonte secundária, sem definição oficial). Descrição prévia, 2024: população de 3,03 milhões; saúde por habitante de R$ 1.366 (soma ÷ soma; mediana de R$ 1.106) contra R$ 1.764 no resto da Metropolitana sem a capital (15 municípios); fatia da saúde de 34,5%. Com n = 6, o efeito mínimo detectável é de 71%: **descreve, não testa**.
