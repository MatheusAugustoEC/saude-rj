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
