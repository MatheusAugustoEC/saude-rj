# Insights do projeto (para levar até a entrega)

**Regra:** cada insight **só pode aparecer na entrega, nos posts e na página final junto com a sua ressalva**. Se a ressalva não couber, o insight não entra. Cada número aqui vem do notebook `notebooks/01_eda_siconfi_2024.ipynb` (dados de 2024, declarados pelos entes, não auditados).

Atualizado em 22/10/2026.

## Insights confirmados na EDA

| # | Insight | Ressalva obrigatória | Onde está no notebook |
|---|---|---|---|
| I1 | **A capital gasta R$ 1.136 por habitante em saúde (população do IBGE 2024), o 85º maior entre os 92 municípios (um dos 8 menores).** | **Isso, sozinho, não diz que a saúde da capital é pior.** Saúde por habitante acompanha a receita por habitante (correlação de 0,87 nos municípios), e a receita por habitante da capital é a 71ª maior. O Siconfi mostra gasto, não qualidade. | Seção 8 e seção 11 |
| I2 | **O RJ (estado) tem o menor gasto em saúde por habitante entre os 27 estados (R$ 606) e a menor fatia da despesa em saúde (10,4%).** | A mesma ressalva de I1 (correlação de 0,80 nos estados). Cada estado classifica seus gastos por função de um jeito, e não conferimos se "Saúde" tem o mesmo conteúdo em todos. O DF acumula funções de estado e de município. | Seções 7 e 11 |
| I3 | **Saúde por habitante acompanha de perto a receita por habitante** (0,80 nos estados, 0,87 nos municípios). Já a fatia da despesa em saúde é **negativa** em relação à receita nos municípios (−0,31). | Correlação mede se as coisas andam juntas, não a causa. Para medir prioridade, a fatia da despesa é melhor que o gasto por habitante. | Seção 8 |
| I4 | **A capital destina 19,3% da despesa à saúde, a 88ª maior fatia entre os 92.** O padrão dos municípios (quem tem mais receita por habitante destina fatia menor) **não explica** a fatia baixa dela, porque a capital não tem receita alta por habitante. | É uma **observação para o Analyze, não uma conclusão**. Os dados não dizem por quê. | Seção 11 |
| I5 | **O pessoal compromete 54,3% da RCL do RJ (soma dos Poderes), a 5ª maior entre os 26 estados completos.** O Executivo sozinho mostra 46,8%. | Os limites de pessoal são os que o estado declarou, não conferidos com a lei. O DF fica de fora por ter Poderes faltando. | Seções 5.6 e 6 |
| I6 | **A dívida líquida do RJ equivale a 211,3% da RCL, a maior entre os 27 estados e acima do limite do Senado que o próprio estado declara (200%).** | Valores declarados, não conferidos com a lei. Esta é uma descrição, não o teste da hipótese da dívida (isso é do Analyze). | Seção 10 |
| I7 | **Tirar os casos especiais muda pouco as medianas dos municípios** (variação máxima de 4,7%, em saúde por habitante, sem os atípicos e sem os simplificados). | Vale para a mediana; as médias e os extremos mudam mais. | Seção 9 |
| I8 | **A população usada como denominador muda os extremos dos municípios.** Com a população do Siconfi, o menor e o maior gasto em saúde por habitante são R$ 1.026 e R$ 6.853 (6,7 vezes). Com a estimativa 2024 do IBGE, são R$ 900 (São João de Meriti) e R$ 6.465 (São João da Barra), 7,2 vezes. A ordem dos 92 quase não muda (Spearman 0,99), mas o maior e o menor trocam de município. | O Siconfi não diz de onde vem a população dele, e nenhum ano do IBGE (2018 a 2025, Censo 2022) bate com ela. Carapebus e São João da Barra empatam no topo com a população do Siconfi (diferença de 22 centavos). Isso é efeito de medida, não conclusão sobre os municípios. | docs/07, B1 |
| I9 | **O Anexo 02 do RREO bate com a DCA (prestação de contas anual) em 117 dos 119 entes, em até 0,1% na despesa com saúde.** A exceção grande é Armação dos Búzios (R$ 33,9 mi no RREO contra R$ 156,2 mi na DCA). | Vale para a despesa empenhada em saúde de 2024. Não prova que a classificação por função é igual entre entes. | docs/07, A2 |
| I10 | **Três municípios (Barra do Piraí, Rio Bonito e Porciúncula) empenharam em 2024 de 17% a 20% acima da receita realizada somada aos saldos de exercícios anteriores usados, e os dados públicos que temos não explicam a diferença.** A despesa existe (a DCA confirma). Em Porciúncula, a receita do RREO é 26% maior que a da DCA. | **Ponto de atenção que pede apuração, não conclusão de irregularidade.** Pode haver fonte de recurso que o relatório não mostra, déficit real ou erro de declaração. Dado declarado pelos entes, sem auditoria nossa. Em público, não chamar de "errado" nem de "atípico". É o tipo de achado que o público de controles e auditoria aprofunda. | docs/07, A5 |

## Como usar cada insight

- **Nos posts:** nunca nomear município como "atípico" ou "errado" em público (Areal, Itaperuna, Miracema, Armação dos Búzios): a causa não está confirmada.
- **Na página final:** a ressalva fica **ao lado** do insight, na mesma tela, e não só no rodapé.
- **No Analyze:** I4 e a relação receita × gasto (I3) entram como pontos a investigar, não como achados.
