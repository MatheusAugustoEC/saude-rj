# Banco de curiosidades e insights para relatório, post e painel

Guardado em 23/10/2026, a pedido do Matheus. Cada item tem o número-chave, a **ressalva obrigatória** (nada vai a público sem ela) e a melhor forma de usar. A tabela completa, com a ressalva por extenso, está em [docs/05](05-insights-do-projeto.md). Os números saem de `dados_tratados/indicadores_measure_2024.csv`, do baseline do Measure e dos notebooks 01 e 02.

**Regras de uso.** (1) Toda curiosidade vai com a ressalva: dado declarado pelos entes, sem auditoria, e gasto não é qualidade. (2) Em texto público, nenhum município é chamado de "errado" ou "atípico": usar "os dados públicos não explicam". (3) Regiões só se descrevem; apenas Noroeste, Serrana e Metropolitana (sem a capital) sustentam comparação estatística; a Baixada (6 municípios) e a capital só se descrevem.

## 1. As que dão post (curiosidade e susto)

| ID | Curiosidade | Número-chave | Gancho |
|---|---|---|---|
| I11 | A população antiga subestimava as cidades da Baixada | São João de Meriti −15,6%, Belford Roxo −13,8% | "O número de habitantes estava errado, e mudou quem é o campeão" |
| I17 | Dois municípios empatados em 22 centavos | R$ 6.852,71 e R$ 6.852,49 | "O primeiro e o segundo lugar eram o mesmo número" |
| I19 | O município típico e o morador típico não são o mesmo | R$ 2.319 contra R$ 1.136 | "A cidade do meio gasta R$ 2.319, mas 88% das pessoas moram em cidades que gastam menos" |
| I21 | **Oito dos dez que menos gastam estão na Metropolitana** (a capital incluída) | 8 de 10; 24% dos municípios, 80% dos dez menores | "Onde estão os dez que menos gastam" (usada no Marco 2) |
| I27 | As cinco cidades que menos arrecadam estão entre as dez que menos gastam | São Gonçalo R$ 2.632 de receita por habitante, São João de Meriti R$ 2.656 | "Não é falta de prioridade, é falta de bolo" |
| I28 | Noroeste arrecada 23% mais e gasta 75% mais que a Metropolitana (sem a capital) | 39% da receita em saúde contra 27% | "Dois destinos para o mesmo dinheiro" |
| I22 | Vizinhos de região, abismo de gasto | Arraial do Cabo R$ 5.525 e São Pedro da Aldeia R$ 949 | "Mesma região, quase seis vezes de diferença" |
| I15 | Baixada: fatia grande, bolso pequeno | 34,5% da despesa, R$ 1.366 por habitante | "Gastam uma parte enorme do que têm, e mesmo assim é pouco" |

## 2. As que dão relatório (para quem audita e controla)

| ID | Curiosidade | Número-chave | Fonte do número |
|---|---|---|---|
| I9 | Relatório que contradiz a prestação de contas | R$ 34 mi contra R$ 156 mi | docs/07, A2 |
| I10 | Despesa acima da receita sem explicação | 3 municípios, 17% a 20% | docs/07, A5 |
| (docs/07) | RCL três vezes diferente entre dois relatórios do mesmo ente | R$ 192,8 mi contra R$ 583,8 mi | docs/07, A3 |
| (docs/04) | Limites de pessoal declarados diferentes da LRF | 7 entes | docs/04, C1 |
| I12 | Quanto da saúde é recurso próprio | mediana de 37%, de 13% a 74% | notebook 02, seção 4 |
| I13 | Quem está perto do mínimo legal | 7 a menos de 1 ponto, 12 a menos de 2 | notebook 02, seção 7 |
| I18 | Retificar é rotina | 63% dos municípios | docs/04, B4 |
| (docs/04) | Anexos 8 e 12 não estão no Siconfi | Portaria STN 642/2019 | docs/04, B6 |
| (docs/04) | A Defensoria fica fora da soma de pessoal | 0,5% a 2,5% do Executivo | docs/04, B5 |

## 3. As que dão painel (gráfico sugerido)

| ID | Curiosidade | Gráfico sugerido no painel |
|---|---|---|
| I19 | Município típico contra morador típico | Duas barras, ou curva de distribuição acumulada pela população |
| I20 | Capital e Metropolitana contra o resto | Barras de gasto por habitante com a participação na população |
| I21, I22 | Extremos e dispersão por região | Faixa mínimo-máximo por região (gráfico de "haltere"), com os nomes dos extremos |
| I23 | Receita por habitante contra gasto por habitante, por região | Dispersão com uma cor por região e a capital destacada |
| I24 | Quanto da receita vai para a saúde, por região | Barras ordenadas, com a mediana marcada |
| I25 | Proporção acima do limite prudencial de pessoal, por região | Barras de proporção com o intervalo de Wilson e o n escrito |
| I26 | Onde estão as despesas acima da receita | Mapa de pontos sobre a malha municipal do IBGE |
| I14, I16 | Mínimo legal e gasto por habitante; capital | Dispersão e cartão da capital |
| I1 a I7 (EDA) | Capital, estado do RJ, receita e gasto | Cartões e mapa colorido pela região do CEPERJ |

**Vindos do desenho do Analyze (planejados, ainda sem resultado; entram na página final quando houver número):**

| ID | Ideia | Gráfico sugerido na página final |
|---|---|---|
| P1 | Decomposição exata do gasto por habitante: receita por habitante × fatia da receita dedicada à saúde, por cidade | Barras empilhadas ou haltere por cidade, com o fator que mais explica a distância da mediana |
| P2 | Modelo nas 92 cidades juntas (gasto contra receita por habitante e região): com a mesma receita, a Metropolitana ainda gasta menos? | Dispersão com reta, uma cor por região, intervalo de confiança escrito; versão com e sem a capital |
| P3 | Capital comparada com a receita, e não só com o gasto: gasta pouco por ter pouca receita ou por dedicar menos dela à saúde? | Cartão da capital com a posição na decomposição e no modelo |
| P4 | Análise por região, como agregado das cidades (soma ÷ soma) | Painel por região, com o n e o intervalo ao lado |

| P5 | Receita própria contra transferências: quanto do gasto em saúde de cada cidade se apoia em repasses | Barras empilhadas por região (própria × transferências) ao lado do gasto por habitante; depende da etapa opcional de coleta |
| P6 | O padrão se repete em 2023? (replicação da pergunta central em outro ano) | Dois painéis lado a lado, 2023 e 2024, com a mesma escala |
| P7 | Segunda medida de resultado: % da receita própria aplicado em saúde contra o mínimo legal de 15% (SIOPS) | Dispersão contra o gasto por habitante; divergência entre as duas medidas vai para a lista de auditoria |

Ressalvas a levar junto: receita mede capacidade financeira, não saúde financeira (essa é outra leitura: dívida e limites da LRF); parte do gasto em saúde vem de repasses do SUS, que também contam como receita, então a relação tem um pedaço mecânico; grupo pequeno entra no modelo, mas o intervalo largo significa "sem conclusão", não "sem diferença".

**Para o mapa:** a malha municipal do IBGE (`dados_brutos/malha_rj`) e a coluna `regiao_ceperj` (em `indicadores_measure_2024.csv`) já estão prontas; falta desenhar. Cada gráfico leva ao lado a ressalva, na mesma tela.

## 4. Onde usar primeiro

- **Marco 2 (Measure): usado** I21 (mapa das regiões) com I27 e I28 como pista.
- **Post do Marco 3 (Analyze):** I22 (vizinhos de região, abismo de gasto) e I19 (município típico e morador típico), com a pergunta "por que?" como fio.
- **Relatório do Analyze:** I19, I20, I23 e I24 como pano de fundo das regiões.
- **Página final do projeto (Entrega):** todas, organizadas como acima, com a ressalva ao lado.

## 5. Ideias de gráfico para a página final (a criticar; não é compromisso de usar)

| Gráfico | Para quê | Crítica |
|---|---|---|
| **Dispersão log-log** receita por habitante × gasto por habitante, reta do modelo, cor por grupo, capital destacada | O gráfico central do Analyze: mostra quem fica abaixo da reta | Eixos em log precisam estar bem rotulados (R$ e não ln) |
| **Histograma** do gasto por habitante (em escala log) e da receita por habitante | Mostrar a assimetria e a mediana, e por que o log | Poucos cortes escondem o formato, muitos criam ruído; com 92 cidades, 12 a 15 faixas |
| **Histograma dos resíduos** | Diagnóstico do modelo | Só para o relatório técnico, não para o público |
| **Pontos por região** (um ponto por cidade sobre uma faixa, com mediana) | Comparar regiões sem esconder o n | Melhor que histograma por região: com 3 a 15 cidades o histograma engana |
| **Barras do desvio** (decomposição A1: receita × fatia) | Ver por que cada cidade está longe da referência | Ordenar por gasto e marcar o n e a capital |

## 6. Resultados do A2 (24/10/2026; com ressalva: dado declarado, não auditado; gasto não é qualidade)

- A receita por habitante sozinha explica cerca de 80% da variação do gasto por habitante (em log) entre as 92 cidades.
- Com a mesma receita, a diferença da Metropolitana (sem a capital) cai de −16% (bruto) para −4%, com intervalo de −18% a +11%: não dá para afirmar nem negar diferença relevante.
- A elasticidade é 0,81 (abaixo de 1): nas 92 cidades, quanto maior a receita por habitante, menor a fatia dedicada à saúde (H5; contraria a expectativa de que mais receita levaria a fatia maior).
- A capital gasta cerca de 36% abaixo do que a receita prevê, no limite do intervalo de previsão.
- Baixadas Litorâneas: mediana dos resíduos −15% (gastam menos que a receita sugere); sem explicação nos dados, vai para a lista de auditoria com ressalva.
- Sensibilidade (A2b): sem as cidades de maior influência, a diferença da Metropolitana desaparece (−4% vira +1% a +7%, intervalos largos) e a elasticidade sobe de 0,79 para 0,86 a 0,89 (ainda abaixo de 1, no limite com as três de receita mais extrema). a conclusão de H5 (fatia menor com mais receita) depende dessas cidades para ter a força que tem.

## 7. Replicação em 2023 (A5, 24/10/2026; mesmas 92 cidades, Carmo fora; população de 2023 interpolada)

- Elasticidade da receita em 2023: 0,80 (M1) e 0,77 (M3), intervalo de 0,64 a 0,89: o padrão "mais receita, fatia menor" se repete. Sem Niterói, Maricá e Saquarema: 0,87 (0,76 a 0,985), a mesma fragilidade de 2024.
- Metropolitana (sem a capital) com a mesma receita: −6,8% (−22% a +11%), de novo sem conclusão. Baixada: −7,9% (−28% a +17%).
- Capital: gasto 33% abaixo do previsto pela receita, dentro do intervalo de previsão em 2023 (em 2024 ficou pouco abaixo do limite): direção igual, força limítrofe.
- Baixadas Litorâneas: resíduo mediano −13% (em 2024, −15%): repete, ainda sem explicação.
- 9 dos 10 que menos gastam estão na Metropolitana em 2023 (8 em 2024).
- A previsão escrita antes (elasticidade perto de 0,8; Metropolitana pequena e com intervalo largo; capital abaixo) se confirmou nos três itens. Ressalva: os dois anos não são amostras independentes.

## 8. Segunda rodada (24/10/2026): receita própria, uso ocasional e SIOPS (dado declarado, não auditado; gasto não é qualidade)

- **Receita própria × total.** O gasto em saúde por habitante acompanha as transferências, não a arrecadação própria: com as duas no modelo, a elasticidade das transferências é 0,68 e a da própria é 0,12; a própria sozinha explica 35% da variação, a total 80% (2024; 2023 igual). Ressalva: transferências incluem repasses do SUS, então parte é mecânica. Para a página final: mostrar receita própria, transferências e total lado a lado, por região.
- **Capital arrecada por conta própria:** 66% da receita dela é própria, contra 17% a 31% nas demais regiões. Mesmo contra a receita própria, gasta 67% abaixo do previsto (intervalo de previsão não inclui o valor real), em 2024 e em 2023.
- **Uso ocasional (Censo 2022).** Baixadas Litorâneas: 20 domicílios de uso ocasional por 100 moradores (mediana); Baixada núcleo de 6: 0,2. Mangaratiba 58, Arraial do Cabo 41, São João da Barra 38. Cidades com mais uso ocasional têm mais receita por habitante (Spearman +0,51) e menor fatia da receita na saúde (−0,44). Incluir o indicador aproxima o resíduo das Baixadas Litorâneas de zero (de −15% para −9%), mas não o elimina, e o coeficiente tem intervalo que encosta no zero. Hipótese plausível, não explicação fechada.
- **SIOPS 2024.** Todas as 92 cidades declaram aplicar mais que o mínimo de 15% (mediana 23,3%; menor valor Paracambi, 15,1%; Mesquita, 15,2%). As 10 que menos gastam aplicam mediana de 20,9% (capital 17,8%): o gasto baixo por habitante não vem de aplicar pouco sobre a base de impostos, e sim de a base ser pequena. Correlação entre o percentual aplicado e o gasto por habitante: +0,15 (sem evidência). Os recursos próprios do SIOPS correspondem a cerca de 37% (mediana) do gasto em saúde do Siconfi; 21% na Baixada (núcleo de 6) e 50% na capital.

## 9. Módulo IBGE (24/10/2026): idade e saneamento (dado declarado, não auditado; associação entre cidades não é causa)

- **Quem tem pouco esgoto não gasta mais com saúde por isso: gasta mais por ter receita alta.** Sem controle, cidades com menos esgoto ligado à rede gastam mais (Spearman −0,27); descontada a receita, o sinal inverte (+3,4% por +10 pp de esgoto, no limite do significativo em 2024 e sem significância em 2023). Cidades de pouco esgoto são as de receita alta (Costa Verde 36% de esgoto, Serrana 54%). Uso: post (contraria o que se espera) e página (dispersão com e sem controle).
- **A Baixada e a capital têm esgoto quase universal (93% e 95%) e as menores receitas e gastos por habitante;** a Costa Verde tem 36% e a maior receita. Descritivo.
- **Idade não ajuda a explicar o gasto:** +10 pp de idosos muda o gasto em −3% (IC −26% a +26%): sem poder para decidir, porque a faixa observada (8% a 17,6%) é curta.
- **A capital é uma das cidades mais envelhecidas (14,5% de 65+, igual ao Noroeste e acima de quase todas) e mesmo assim gasta 39% abaixo do previsto com idade e saneamento no modelo.** Ressalva: a capital atende quem mora em outros municípios.
- **Pergunta aberta para o módulo SUS:** internações por doenças ligadas ao saneamento inadequado testariam a hipótese de forma mais direta.


---

## 10. Curiosidades do Improve (24/10/2026)

Todas valem com a ressalva de sempre: dado declarado e não auditado; gasto não é qualidade; cidade sinalizada é cidade para olhar.

- **Niterói gasta 48% menos do que a receita prevê, nos dois anos** (−47,7% em 2024, −49,0% em 2023), fora do intervalo de previsão sem ela no ajuste. É o desvio mais forte da lista e não tinha aparecido antes, porque no Analyze estava dentro do grupo Resto da Metropolitana. Sem explicação nos dados; achado para auditoria.
- **São Francisco de Itabapoana também (−42,6% e −41,7%).** Mais uma cidade que persiste nos dois anos.
- **O desvio das Baixadas Litorâneas é do grupo, não de uma cidade.** Só 1 das 10 fica fora do intervalo sozinha (São Pedro da Aldeia).
- **Comparar por receita parecida reduz 46% da dispersão** e muda a leitura de 34 das 92 cidades. A Baixada deixa de parecer 33% abaixo e passa a 15%.
- **Somar visitantes à população piora o resíduo das Baixadas Litorâneas** (de −15% para −18%), porque a elasticidade é menor que 1. A ideia de "corrigir a base" não funciona; usar o uso ocasional como controle (H7) funciona em parte.
- **A elasticidade dos repasses dentro da cidade (0,28) é menos da metade da de entre cidades (0,68).** Um teste de estresse com 0,68 exagera.
- **22 municípios declaram pessoal acima do limite prudencial** (11 acima do máximo); 3 estão marcados como "RCL atípica". O estado declara 46,8%, pouco acima do prudencial (46,5%).
- **Nenhum município chega a 80% do limite de dívida; 53 têm dívida líquida negativa.** O estado declara 211,3% da RCL.
- **A folga sobre os 15% da saúde vai de 0,1 ponto (Paracambi, Engenheiro Paulo de Frontin) até uma mediana de 8,3 pontos.** A capital aplica 17,8%, folga de R$ 596 milhões.
- **Três palpites meus erraram** (Baixadas Litorâneas sobrerrepresentadas, folga em até 6 cidades, pessoal acima do prudencial em até 10). Vale mostrar: registrar o palpite antes é o que dá valor ao erro.
