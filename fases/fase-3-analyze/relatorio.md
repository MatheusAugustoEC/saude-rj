# Analyze: o que explica o gasto baixo em saúde por habitante

**Saúde fiscal do Rio de Janeiro · Siconfi 2024 (com replicação em 2023) · 24/10/2026**

> [!NOTE]
> Dados públicos e declarados pelos entes, não auditados. Gasto em saúde por habitante não mede qualidade nem resultado em saúde. Toda conclusão abaixo vem com a sua ressalva.

<div class="resumo" markdown="1">

**Pergunta central.** O gasto baixo em saúde por habitante da Região Metropolitana se explica pela receita por habitante?

**Resposta curta.** Em boa parte sim: a receita por habitante sozinha explica cerca de 80% da variação do gasto entre as 92 cidades, e quando se compara cidades com a mesma receita a diferença da Metropolitana cai de 16% para 4%. Mas **a amostra não permite concluir** se sobra alguma diferença real (o intervalo vai de −18% a +11%), e o resultado depende de poucas cidades de receita muito alta. A capital é o caso que mais destoa: gasta bem menos do que a receita dela indica, principalmente por dedicar uma fatia menor da receita à saúde.

</div>

## 1. O que foi feito

| Etapa | O que fez | Script |
|---|---|---|
| A0 | Hipóteses e critérios de decisão, escritos antes dos modelos ([docs/09](../../docs/09-analyze-hipoteses.md)) | — |
| A1 | Decomposição exata: gasto por habitante = receita por habitante × fatia da receita dedicada à saúde | `scripts/19` |
| A2 | Modelo em log nas 92 cidades (91 nos modelos de grupo), erros robustos HC3, bootstrap, ponderação por população, diagnóstico | `scripts/20` |
| A2b | Sensibilidade às cidades de maior influência (distância de Cook) | `scripts/21` |
| A5 | Replicação com 2023 (coleta nova no Siconfi: 92 de 92 municípios) | `scripts/22`, `scripts/23` |
| Rodada 2 | Receita própria contra transferências (H6), domicílios de uso ocasional do Censo 2022 (H7), SIOPS (H8) | `scripts/24` |
| Conferência | Notebook de reprodução com conferência dos números do relatório; planilha em Excel (A1, regressão, modelo M3 e previsão da capital) | `notebooks/03`, `scripts/25` a `27` |

Cada método (o que é, por que foi escolhido, como foi feito, com exemplo) está em [docs/10](../../docs/10-metodos-estatisticos.md).

> [!WARNING]
> **Falha de ordem, declarada.** O A1 foi rodado antes de eu mostrar o A0 ao responsável, e as hipóteses H3 e H5 foram escritas depois de eu ver o padrão do A1. O A0 diz isso no topo. A replicação em 2023 passou a ser o teste "cego", e a previsão para 2023 foi registrada antes de coletar. A H5 também foi reformulada: a primeira redação ("a fatia cai") era minha, não do responsável; a atual é neutra.

## 2. Resultados por hipótese

| Id | Hipótese | Resultado | Veredito |
|---|---|---|---|
| H1 | Com a mesma receita por habitante, a Metropolitana (sem a capital) não gasta diferente de forma relevante | −4,4% (IC 95%: −18% a +12%) em 2024; −6,8% (−22% a +11%) em 2023. O intervalo passa da margem de ±10% | **Sem conclusão** |
| H2 | A Baixada (6 cidades) gasta menos que a receita prevê | −3,5% (−18% a +14%); ponderado por população −8,2% (−33% a +25%); 2023: −7,9% (−28% a +17%) | **Sem conclusão** |
| H3 | A capital gasta menos por dedicar fatia menor da receita à saúde | Gasto 35% a 37% abaixo do previsto pela receita total; fatia de 19,6%, contra mediana de 29,2%; contra a receita própria, 67% abaixo, fora do intervalo de previsão nos dois anos | **Sustentada**; com a receita total é limítrofe (2024 pouco fora do intervalo, 2023 dentro) |
| H4 | O padrão de 2024 se repete em 2023 | Elasticidade 0,80; efeito da Metropolitana pequeno e incerto; capital abaixo do previsto; 9 dos 10 que menos gastam na Metropolitana (8 em 2024) | **Confirmada**, com a ressalva de que os dois anos não são amostras independentes |
| H5 | Como se comportam as cidades de maior receita? (pergunta aberta; expectativa: fatia maior) | Elasticidade 0,81 (0,72 a 0,90), abaixo de 1: **quanto maior a receita por habitante, menor a fatia dedicada à saúde**. Contra a expectativa inicial | **Fatia menor**; sensível a 3 cidades (0,89 sem elas) |
| H6 | Receita própria acompanha menos o gasto que a receita total | Própria sozinha: R² 0,35 e elasticidade 0,45; total: R² 0,80. Com as duas juntas: transferências 0,68, própria 0,12. 2023 igual | **Confirmada** |
| H7 | Uso ocasional infla a receita por habitante e explica parte do resíduo das Baixadas Litorâneas | Correlação de postos com a receita por habitante +0,51 e com a fatia −0,44; resíduo mediano das Baixadas Litorâneas de −15% para −9% | **Parcial**: coeficiente com intervalo que encosta no zero |
| H8 | A maioria cumpre o mínimo de 15% e o gasto baixo não vem de aplicar pouco | 92 de 92 acima de 15% (mediana 23,3%); as 10 que menos gastam aplicam mediana de 20,9% | **Confirmada** |

### 2.1 Decomposição (A1)

A referência é a média geométrica das 92 cidades: R$ 2.322 de gasto por habitante, R$ 7.983 de receita por habitante e fatia de 29,1%. Em log, o desvio do gasto é a soma do desvio da receita e do desvio da fatia (conferido nas 92 cidades).

| Grupo (mediana do desvio, %) | n | Gasto | Receita | Fatia |
|---|---|---|---|---|
| Baixada (núcleo de 6) | 6 | −52 | −58 | +18 |
| Capital | 1 | −51 | −27 | −33 |
| Metropolitana (resto) | 15 | −16 | −21 | +8 |
| Baixadas Litorâneas | 10 | +23 | +56 | −20 |
| Costa Verde | 3 | +47 | +61 | −1 |

Leitura: Baixada e Metropolitana gastam pouco principalmente por receita baixa. A capital é diferente: a receita dela fica 27% abaixo da referência, mas a fatia fica 33% abaixo. Por grupo as medianas não fecham exatamente (a mediana de uma soma não é a soma das medianas); por cidade a conta é exata.

### 2.2 Sensibilidade (A2b)

Seis cidades têm distância de Cook acima de 4/n: Niterói, Maricá, Saquarema, Rio Bonito, São Pedro da Aldeia e Duque de Caxias. A conferência da DCA contra o RREO fecha para elas (não são erros de dado). Isso mostra que a conclusão sobre a Metropolitana é sensível a três cidades de receita muito alta, e não que a região seja pequena demais.

| Versão | Elasticidade | Resto da Metropolitana |
|---|---|---|
| Todas (91) | 0,79 | −4,4% (−18% a +12%) |
| Sem as 6 (85) | 0,86 (0,76 a 0,96) | +1,2% (−8% a +12%) |
| Sem Niterói, Maricá e Saquarema (88) | 0,89 (0,79 a 0,996) | +6,6% (−5% a +19%) |

A "lacuna da Metropolitana" desaparece sem essas cidades, e a elasticidade sobe para perto de 1.

### 2.3 Receita própria e transferências (H6)

Receita própria = receita total menos transferências correntes e de capital (RREO Anexo 01).

- Quase todas as regiões têm 17% a 25% da receita como própria; a capital, 66%.
- No modelo com as duas juntas, o gasto em saúde por habitante acompanha as **transferências** (0,68) e muito pouco a receita própria (0,12).
- Mesmo contra a receita própria, a capital gasta 67% abaixo do previsto (2024) e 66% (2023).
- **Ressalva:** as transferências incluem os repasses do SUS (carimbados para a saúde), então parte dessa relação é automática. Royalties e compensações financeiras entram em transferências e não se separam nos dados.

### 2.4 Uso ocasional (H7)

Domicílios de uso ocasional por 100 moradores (Censo 2022): Baixadas Litorâneas 20 (mediana), Costa Verde 16,5, Baixada núcleo 0,2. Mangaratiba 58, Arraial do Cabo 41, São João da Barra 38. A hipótese de que cidades de veraneio têm receita inflada por uma base que não mora lá é plausível e explica parte do desvio, mas não o fecha. O Censo é de 2022 e o gasto de 2024.

### 2.5 SIOPS (H8)

Todas as 92 cidades declaram aplicar mais que o mínimo de 15% (menor valor: Paracambi, 15,1%; Mesquita, 15,2%). Correlação entre o percentual aplicado e o gasto por habitante: +0,15, sem evidência. Os recursos próprios do SIOPS cobrem cerca de 37% (mediana) do gasto em saúde do Siconfi, 21% na Baixada (núcleo de 6) e 50% na capital (bases diferentes; é ordem de grandeza).

## 3. Achado para auditoria

> [!IMPORTANT]
> **Baixadas Litorâneas gastam 13% a 15% menos do que a receita prevê, nos dois anos (2023 e 2024).** Os dados não explicam. O uso ocasional reduz o desvio para −9% mas não o elimina. Pode haver explicação legítima (por exemplo, gasto em saúde registrado em outro ente ou fundo, ou escolha de prioridade). Fica na lista para quem tem acesso aos livros: controladoria ou tribunal de contas.

## 4. Limites e ressalvas

- Dados declarados, não auditados; o gasto é empenhado, não pago.
- Gasto em saúde por habitante residente não mede qualidade nem necessidade; a capital e as cidades-polo atendem quem mora em outro município.
- A população de 2023 é aproximada (média geométrica entre o Censo 2022 e a estimativa de 2024, porque o IBGE não publicou estimativa municipal de 2023).
- Carmo ficou fora da replicação de 2023 (entregou o RREO só até o 5º bimestre).
- Os dois anos usam as mesmas 92 cidades, então não são amostras independentes.
- Regiões pequenas (capital, n=1; Baixada, n=6) só se descrevem; o intervalo largo significa "sem conclusão", e não "sem diferença".
- Pendências herdadas: B4 (versão que a API devolve para relatório retificado) e módulos IBGE/SUS e DF no SIOPS (D1, D2).
- **Reprodução e conferência:** o notebook `notebooks/03_analyze_gasto_saude.ipynb` refaz todos os cálculos e confere 47 números deste relatório contra a execução (0 divergências). A planilha `planilhas/saude_fiscal_rj_analyze.xlsx` refaz em fórmulas de Excel a decomposição, a regressão simples, o modelo M3 (com a Baixada e o resto da Metropolitana) e a previsão da capital com o intervalo de previsão (1.778 fórmulas, 0 erros, 0 diferenças contra o Python; o intervalo da capital sai igual: R$ 1.144 a R$ 2.668). Ficam só no notebook os erros robustos HC3, o bootstrap, a ponderação por população e os modelos de receita própria.
- **Não foi feito:** gráficos finais (ficam para a página de entrega); royalties por município (ANP) e atividade econômica (extensão futura).

## 5. Decisões tomadas na fase

| Decisão | Por quê |
|---|---|
| Testar as 92 cidades juntas, com a região como variável | Região é agregado de cidades; um modelo único aproveita todos os dados |
| Capital fora do modelo como variável própria; prevista de fora | Uma variável para uma cidade só "decora" a cidade e não testa nada |
| Margem de relevância de ±10% e intervalo de 95% | Escolha de julgamento, fixada antes de ver os resultados |
| HC3 e bootstrap das cidades em vez de erros agrupados por região | Com 8 regiões, o agrupamento fica instável |
| H5 reformulada como pergunta neutra | A primeira redação foi minha e não pedida |

## 6. Tollgate

**Proposta: APROVADO.** O critério do tollgate é a qualidade do processo, e não se as hipóteses deram a resposta esperada. Aqui: hipóteses e critérios escritos antes; replicação em outro ano; sensibilidade; diagnóstico dos modelos; notebook que confere os números do relatório; planilha independente; falhas de ordem declaradas. Resultado "sem conclusão" e hipótese não confirmada são resultados válidos e entram como tal; viram perguntas para a fase seguinte e para trabalhos futuros.

**Pendências herdadas (não são da fase):** B4 (qual versão a API devolve para relatório retificado) e os módulos IBGE/SUS e DF no SIOPS (D1, D2).

**Perguntas abertas que o Analyze deixa:**
- O que explica o gasto 13% a 15% abaixo da receita nas Baixadas Litorâneas, além do uso ocasional? Pergunta para quem acessa os livros.
- Sobra alguma diferença real da Metropolitana depois de descontar a receita? Com 15 cidades o intervalo é largo (−18% a +11%); repetir a pergunta nas regiões metropolitanas de outros estados (o Siconfi cobre todos) aumentaria o número de cidades.
- O quanto da receita alta de Maricá, Saquarema e outras vem de royalties? Exige o dado por município da ANP.

A decisão é do responsável.

**Insumos para a página de entrega:** [docs/08](../../docs/08-banco-de-curiosidades.md) (curiosidades por uso) e [docs/05](../../docs/05-insights-do-projeto.md) (insights com ressalva). A seleção do que entra na página e no relatório final fica para a montagem.
