# O dado do Siconfi serve ao projeto, depois de uma correção em Armação dos Búzios e com cinco ressalvas

Fase 2A · Measure, o instrumento — Saúde fiscal do Rio de Janeiro · 23/10/2026 · exercício de 2024 · versão 1

<div class="numero"><b>119 de 119</b><span>entes com a despesa em saúde do RREO igual à da DCA, a segunda fonte, depois de corrigir Búzios (antes da correção: 118 de 119)</span></div>

<div class="resumo" markdown="1">
**Em três linhas.** Conferi o dado do Siconfi contra uma segunda fonte (a DCA, a prestação de contas anual do ente) e contra o texto das leis. Corrigi um município, troquei a população pela do IBGE e achei pontos que pedem apuração de quem entende de controle. A fase passou no tollgate, com ressalva.
</div>

## 1. A pergunta desta fase

**Será que posso confiar nos números que vou comparar?** O projeto compara o gasto em saúde de 27 estados e 92 municípios. Se a régua estiver torta, toda comparação depois dela também fica. Por isso esta fase confere o dado antes de medir qualquer coisa.

## 2. O que eu encontrei

### O Anexo 02 de Búzios estava errado, e a DCA mostrou onde

O relatório de Búzios traz a despesa em saúde de R$ 33,9 mi, mas a DCA, que é a prestação de contas do mesmo ano, mostra **R$ 156,2 mi**. O relatório dele é incoerente por dentro: o valor "no bimestre" (R$ 159,2 mi) é maior que o acumulado "até o bimestre" (R$ 33,9 mi), o que não acontece em nenhum outro município.

| Fonte | Despesa total | Saúde |
|---|---|---|
| RREO Anexo 01 | R$ 542,7 mi | não traz função |
| RREO Anexo 02 (o que eu usava) | R$ 269,3 mi | R$ 33,9 mi |
| **DCA (prestação de contas anual)** | **R$ 530,7 mi** | **R$ 156,2 mi** |
| SIOPS (só recursos próprios em saúde) | | R$ 72,9 mi |

A DCA concorda com o Anexo 01 (diferença de 2%) e com o SIOPS (recursos próprios não podem passar do total). Nos outros 118 entes, a saúde do RREO bate com a DCA em até 1%.

> [!NOTE]
> **Detalhe técnico (M2, acurácia).** Segunda fonte: DCA Anexo I-E, função 10, despesa empenhada, coletada pelo script 13 (119 chamadas, 0 falhas). O resultado por ente está em `conferencia_saude_rreo_vs_dca.csv`. Decisão: usar a DCA só para Búzios; para os demais, o RREO bate, e manter uma única fonte evita misturar critérios.

### A população do Siconfi não bate com nenhum ano do IBGE

O cadastro de entes do Siconfi traz a população de **2025** do IBGE nos 92 municípios. Já o campo de população dos relatórios, que eu usava, não bate com nenhum ano do IBGE (2018 a 2025, nem o Censo 2022). Troquei pela **estimativa de 2024 do IBGE**, que é oficial e do mesmo ano da despesa.

Isso muda quem é o maior e o menor: o menor gasto por habitante passou de R$ 1.026 (São Pedro da Aldeia) para **R$ 900 (São João de Meriti)**, e o maior de R$ 6.853 (Carapebus) para **R$ 6.465 (São João da Barra)**. A ordem geral quase não muda (correlação de Spearman de 0,99).

### Seis pontos pedem apuração, e eu não sei explicá-los

> [!IMPORTANT]
> **Achados para quem trabalha com controle.** Todos são dado declarado pelos próprios entes, sem auditoria minha, e a causa de cada um não está confirmada. Não afirmo irregularidade.

| # | O que o dado mostra | O que falta para explicar |
|---|---|---|
| 1 | **Barra do Piraí, Rio Bonito e Porciúncula** empenharam de 17% a 20% acima da receita realizada somada aos saldos de anos anteriores. A despesa existe (a DCA confirma) | Fonte de recurso que o relatório não mostra, déficit real ou erro de declaração |
| 2 | **Itaperuna**: a RCL do RGF é R$ 192,8 mi, e a do RREO do mesmo ente é R$ 583,8 mi (3,0 vezes). Com a segunda, o pessoal total seria 47,5% da RCL, e não 141,7% | Qual dos dois relatórios está certo |
| 3 | **Areal e Miracema** preencheram só 4 e 2 dos 12 meses de receita no demonstrativo da RCL; a RCL deles está subestimada por isso | Por que os meses ficaram em branco |
| 4 | **Maricá** declara limite de pessoal do Executivo de 60% (a lei diz 54%). **Mesquita** declara 54% para o Legislativo (a lei diz 6%). **Nilópolis** (6,23%) e **Valença** (1%) também diferem. **Pará, Bahia e Goiás** declaram 48,6% para o Executivo (a lei diz 49%) | Troca de campo na declaração, ou regra local que não li |
| 5 | **Porciúncula**: a receita no RREO (R$ 152,3 mi) é 26% maior que a da DCA (R$ 120,8 mi) | A origem da diferença |
| 6 | **Roraima, Carmo e Paracambi** declaram limites de dívida fora do padrão (90,3%, 21,3% e 126,7%), mas a dívida deles está muito abaixo de qualquer limite, então não afeta o resultado | Mesmo item de troca de campo |

### Todas as fontes casam, com duas exceções explicadas

As nove junções que o projeto faz (Siconfi, DCA, IBGE, CEPERJ, malha, SIOPS) casam em 100% dos entes, **exceto**: o Anexo 03 do RREO (12 ausências, os municípios de relatório simplificado, que a lei dispensa) e o SIOPS dos estados (sem o Distrito Federal).

### Os limites da lei foram lidos no texto oficial

Conferi no texto oficial os limites de pessoal (LRF, arts. 19, 20 e 22), de dívida (Resolução do Senado 40/2001: 2 vezes a RCL para estados e DF, 1,2 vez para municípios) e de saúde (LC 141/2012: 12% estados, 15% municípios). **Os 92 municípios e os 26 estados do SIOPS estão acima do mínimo de saúde.** Só o estado do RJ está acima do limite legal de dívida (211,3% da RCL contra 200%).

## 3. O que eu decidi

> [!TIP]
> **Decisões**, cada uma com a alternativa descartada.

| Escolha | O que usei | O que mais considerei | Por que esta | Evidência | Regra |
|---|---|---|---|---|---|
| Saúde de Búzios | Valor da DCA | Valor do RREO Anexo 02 | O Anexo 02 é incoerente por dentro; a DCA concorda com o Anexo 01 e com o SIOPS | docs/07, A2 | M2 |
| População | Estimativa 2024 do IBGE | Campo do Siconfi (o que o projeto usava) | O campo não bate com nenhum ano; o IBGE é oficial e do ano da despesa | docs/07, B1 | M4 |
| Limite de dívida | Limite legal (2x e 1,2x a RCL) | Limite declarado pelo ente | Três entes declaram valores fora do padrão e dois não declaram | docs/07, A1 | M2 |
| Limite de pessoal | Limite legal ao lado do declarado | Só o declarado | Sete entes declaram valores que diferem da LRF | docs/04, C1 | M2 |
| Atípicos | Marcar e mostrar com e sem | Remover | Sem prova de erro, remover é garimpo | notebook 02, seção 5 | M5 |
| Pendência sem explicação | Registrar como achado, com ressalva | Esconder ou tratar como erro de dado | O público do projeto (controles e auditoria) aprofunda o que não se explica | decisão do Matheus, 23/10/2026 | M5 |

## 4. Para você explicar esta fase

**A fase em 30 segundos.** Antes de comparar estados e municípios, conferi se os números são confiáveis. Comparei o relatório de cada ente com a prestação de contas anual dele e com o texto da lei. O dado de saúde bate em todos os 119 entes depois de corrigir um município. No caminho achei casos que um auditor gostaria de investigar, como três municípios que gastaram bem acima do que arrecadaram.

**As perguntas que vão te fazer**

- **Por que você não só confiou no Siconfi?** Porque são dados declarados pelos próprios entes. Um deles tinha um relatório incoerente por dentro, e só uma segunda fonte mostrou isso.
- **Por que trocou a população?** A que eu usava não batia com nenhum ano do IBGE. Usei a estimativa de 2024, do mesmo ano da despesa. O custo é que o maior e o menor município mudaram.
- **Isso quer dizer que esses municípios fizeram algo errado?** Não. Quer dizer que os dados públicos não explicam a diferença. Cabe a quem audita apurar.
- **Por que a DCA como segunda fonte?** É a prestação de contas anual do mesmo ente, entregue em outro relatório e com outra finalidade.

**Os números para saber de cor.** 119 de 119 entes batem com a DCA; R$ 156,2 mi (e não R$ 33,9 mi) é a saúde de Búzios; 92 de 92 municípios acima do mínimo de saúde.

## 5. O que ainda não sei

- **A origem da população do campo dos relatórios.** Sei que não é do IBGE em nenhum ano.
- **Qual versão a API devolve quando há retificação.** 58 dos 92 municípios têm algum RREO ou RGF retificado em 2024. Tratei os dados como a versão vigente, por inferência.
- **O Distrito Federal no SIOPS.** O arquivo que consegui era do indicador errado.
- **Parte das regras só tem fonte secundária:** a Defensoria no limite do Executivo, o Anexo 12 vindo do SIOPS e a padronização das funções (Portaria 42/1999). O art. 166, § 16, da Constituição, como o RGF o cita, não achei no texto vigente.
- **Atraso de entrega** dos relatórios, que não auditei.

## 6. O veredito

| Critério | Veredito | Motivo |
|---|---|---|
| Instrumento auditado nas seis dimensões | <span class="ok">OK</span> | 12 testes, 7 sem ressalva |
| Dado conferido contra segunda fonte | <span class="ok">OK</span> | 119 de 119 depois de corrigir Búzios |
| Pendências de dado resolvidas | <span class="ok">OK</span> | Todas fechadas como confirmadas, corrigidas ou sem confirmação |
| Fundamento legal conferido em fonte oficial | <span class="ressalva">RESSALVA</span> | LRF, LC 141 e Resolução do Senado no texto oficial; Defensoria, Anexo 12 e funções só em fonte secundária |
| Cobertura das fontes | <span class="ressalva">RESSALVA</span> | Distrito Federal fora do SIOPS |
| Qual versão da retificação a API devolve | <span class="ressalva">RESSALVA</span> | Inferência não confirmada |

**Tollgate: aprovado com ressalva.** Nenhuma ressalva impede o baseline.

## 7. O próximo capítulo

A fase 2B fixa o ponto de partida: a distribuição do gasto por habitante e da fatia da saúde, por grupo e por região, e o baseline congelado. **O que muda no plano:** a população do IBGE passa a ser a base, e os limites legais entram ao lado dos declarados.

## Bastidores

1. Segunda fonte da saúde: `scripts/13_coleta_dca_funcao_saude.py`.
2. Demonstrativo da RCL para conferir o RGF: `scripts/14_coleta_rreo_anexo03_rcl.py`.
3. População: SIDRA do IBGE, tabelas 6579 e 4714 (`dados_brutos/ibge_populacao_*.json`).
4. Leis lidas no texto oficial: ver `docs/02`, seção 6.
5. Aplicação das decisões e regeneração: notebook 01 (indicadores), planilha (scripts 09, 11 e 10) e notebook 02 (`notebooks/02_measure_qualidade_e_baseline.ipynb`).
6. Registro de cada pendência: `docs/04` e `docs/07`.


## Adendo de 23/10/2026: pendências de regra fechadas

Depois do relatório, fechei em texto oficial quatro regras que estavam só em fonte secundária.

| Item | Resultado | Veredito atualizado |
|---|---|---|
| Defensoria no limite de pessoal (B5) | A Defensoria entrega o próprio RGF, sem as linhas de despesa total e de limite. Fica fora da minha soma de pessoal (0,5% a 2,5% do Executivo; no RJ, 55,4% da RCL em vez de 54,3%, mesma posição) | <span class="ok">OK</span> |
| Anexos 8 e 12 vazios (B6) | A Portaria STN 642/2019 manda esses anexos ao SIOPE e ao SIOPS, e não ao Siconfi | <span class="ok">OK</span> |
| Função Saúde igual entre entes (B7) | A função 10 e as subfunções 301 a 306 são definidas pela Portaria SOF 42/1999, para todos os entes. Não prova que cada ente classifica o mesmo conteúdo | <span class="ok">OK</span> |
| Art. 166, § 16, da Constituição (C2) | Achei o texto da EC 100/2019: a transferência das emendas de bancada fica fora da base da RCL para os limites de pessoal | <span class="ok">OK</span> |

**Tollgate atualizado:** o critério "fundamento legal conferido em fonte oficial" passa de ressalva para <span class="ok">OK</span>. Seguem como ressalva a cobertura (DF fora do SIOPS) e a versão da retificação (B4, ainda sem fonte oficial lida). A origem do CEPERJ e da malha está registrada pela instituição.
