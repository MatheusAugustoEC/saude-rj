# Métodos estatísticos e matemáticos: fase Analyze

Cada fase tem o seu arquivo de métodos; só na Entrega eles são juntados (decisão do responsável, 24/10/2026, para não embolar e facilitar extrair um assunto por vez). Documento vivo. Para cada método: **o que é**, **por que foi escolhido**, **como foi feito** (com um exemplo do projeto) e **onde o código está**. Cada etapa nova acrescenta os seus. Este texto alimenta o relatório do Analyze e a seção "Como fizemos" da página final.

---

## A1. Decomposição exata do gasto por habitante (Analyze, 24/10/2026)

Código: `scripts/19_analyze_a1_decomposicao.py`. Saída: `dados_tratados/analyze_a1_decomposicao.csv`.

### 1. Identidade contábil

- **O que é:** gasto por habitante = receita por habitante × fatia, com fatia = gasto em saúde ÷ receita.
- **Por quê:** responde se uma cidade gasta pouco porque arrecada pouco ou porque dedica pouco do que arrecada. É aritmética, sem estimativa e sem suposição estatística.
- **Como:** para cada uma das 92 cidades, calculamos `gasto_hab = saude / populacao`, `receita_hab = receita / populacao` e `fatia = saude / receita`.
- **Exemplo (capital):** R$ 5.789 de receita por habitante × 19,6% = R$ 1.136 de gasto por habitante.

### 2. Logaritmo natural

- **O que é:** o log transforma multiplicação em soma: ln(a × b) = ln(a) + ln(b).
- **Por quê:** a identidade acima é um produto, e queremos dizer quanto de cada fator explica a distância. Em log vira soma e dá para repartir sem sobra. O log também trata as distâncias em proporção: estar 50% abaixo e 100% acima ficam simétricos. Gasto e receita são assimétricos (poucas cidades muito acima), e o log reduz o peso desses extremos.
- **Como:** `np.log` de cada medida das 92 cidades.
- **Exemplo:** ln(1.136) = 7,04; ln(5.789) = 8,66; ln(0,196) = −1,63; e 8,66 + (−1,63) = 7,03, que é o ln do gasto, a menos de arredondamento.

### 3. Média geométrica como referência

- **O que é:** média feita nos logs e depois desfeita com a exponencial. Dá R$ 2.322 (gasto), R$ 7.983 (receita) e 29,1% (fatia).
- **Por quê:** a mediana não se decompõe em produto, a média geométrica sim. Ela fica perto da mediana e não é puxada pelos extremos. A referência não é meta nem norma, só o centro das 92.
- **Como:** `média dos ln` de cada medida, e `exp` dessa média. Cada cidade pesa 1 (sem ponderar por população).

### 4. Desvio em relação à média dos logs

- **O que é:** distância de cada cidade até a referência, em log: `desvio = ln(valor da cidade) − média dos ln`.
- **Por quê:** a conta fecha exatamente: desvio do gasto = desvio da receita + desvio da fatia.
- **Como:** o script confere a igualdade nas 92 cidades com `assert` (passou).

### 5. Conversão do desvio em porcentagem

- **Como:** `exp(desvio) − 1`. Exemplo: capital, gasto 1.136 ÷ 2.322 = 0,49, ou 51% abaixo.

### 6. Mediana do desvio por grupo

- **Por quê:** resumir o grupo sem se deixar levar por uma cidade extrema.
- **Limite:** a mediana de uma soma não é a soma das medianas, então por grupo os três números só fecham de forma aproximada. Por cidade fecham exatamente.

### 7. Correlação de Pearson entre os logs

- **O que é:** mede o quanto duas variáveis andam juntas, de −1 a 1.
- **Por quê:** resumo rápido de quanto do gasto acompanha a receita e quanto acompanha a fatia.
- **Como:** `np.corrcoef` entre `ln(gasto_hab)` e `ln(receita_hab)` (0,89), e entre `ln(gasto_hab)` e `ln(fatia)` (0,04).
- **Limite:** correlação não é causa, e parte do 0,89 é mecânica, porque repasses do SUS entram no gasto e na receita.

**O que o A1 não usa:** teste de hipótese, valor-p, intervalo de confiança, regressão ou peso por população.

---

## A2. Modelo em log nas 92 cidades (Analyze, 24/10/2026)

Código: `scripts/20_analyze_a2_modelo.py`. Saídas: `dados_tratados/analyze_a2_coeficientes.csv` e `analyze_a2_residuos.csv`. Hipóteses: `docs/09-analyze-hipoteses.md` (H1, H2, H3, H5).

### 1. Regressão linear em log (log-log)

- **O que é:** ln(gasto por habitante) = a + b × ln(receita por habitante) + efeito do grupo + erro.
- **Por quê:** responde se, com a mesma receita, a Metropolitana ainda gasta menos. Em log-log o coeficiente b é uma *elasticidade*: se a receita sobe 10%, o gasto sobe b × 10%. Se b < 1, a fatia da receita dedicada à saúde cai quando a receita sobe (H5). Os efeitos de grupo viram diferenças percentuais com `exp(coef) − 1`.
- **Como:** `statsmodels` (`OLS`), grupos como variáveis 0/1 (Baixada, Resto da Metropolitana), referência = interior.
- **Exemplo:** coeficiente do Resto da Metropolitana = −0,045; `exp(−0,045) − 1` = −4,4%.

### 2. A capital fica fora do modelo como variável

- **Por quê:** uma variável 0/1 para uma só cidade "decora" a cidade: o resíduo dela vira zero e o coeficiente não testa nada. Na primeira execução isso gerou um intervalo sem sentido, e eu corrigi o desenho (não foi problema nos dados).
- **Como:** ajusta-se o modelo nas outras 91 cidades e *prevê-se* a capital, com intervalo de previsão de 95%. Se o gasto real cai fora do intervalo, a capital gasta menos do que a receita dela sugere.

### 3. Erros-padrão robustos HC3

- **Por quê:** a variância dos erros pode diferir entre cidades; o HC3 não supõe variância igual e funciona bem com amostra pequena. Erros agrupados por região seriam instáveis com só 8 regiões.
- **Como:** `cov_type="HC3"`.

### 4. Bootstrap das cidades (conferência)

- **O que é:** sorteia-se 5.000 vezes um conjunto de cidades com reposição, reajusta-se o modelo, e o intervalo vem dos percentis 2,5% e 97,5% dos coeficientes.
- **Por quê:** não depende de fórmula. Se concorda com o HC3, o intervalo é confiável. (Sorteio de cidades, não de regiões: com poucas regiões, sortear regiões seria pior.)

### 5. Ponderação por população (WLS)

- **Por quê:** o modelo simples dá o mesmo peso a Cardoso Moreira e a São Gonçalo (visão da cidade típica). Ponderar dá a visão do morador típico. Mostramos as duas.

### 6. Intervalo de 95% e margem de relevância de ±10%

- **95%:** nível de 5%, o usual. **±10%:** margem de relevância prática escolhida por mim. Para dizer "sem diferença relevante", o intervalo inteiro precisa estar dentro de ±10%. Se o intervalo é largo e passa da margem, a conclusão é "sem conclusão".

### 7. Diagnóstico dos resíduos

- **Shapiro-Wilk** (normalidade dos resíduos) e **Breusch-Pagan** (variância constante): valores p altos significam que não há evidência contra o modelo. **Distância de Cook:** mede quanto uma cidade sozinha mexe no modelo; referência de alerta 4/n.
- **Limite:** teste com p alto não prova que o modelo está certo, só que não achamos problema.

### Resultados em uma linha

H5 (pergunta aberta sobre receita e fatia): elasticidade 0,81 (IC 0,72 a 0,90), ou seja, abaixo de 1: quanto maior a receita, menor a fatia, o contrário da expectativa inicial. H1 e H2: sem conclusão (intervalos de −18% a +14%). H3: a capital gasta 35 a 37% menos que o previsto pela receita e fica pouco abaixo do limite inferior do intervalo de previsão.

---

## A2b. Sensibilidade às cidades de maior influência (Analyze, 24/10/2026)

Código: `scripts/21_analyze_a2_sensibilidade.py`.

- **O que é:** refazer o modelo sem as cidades que mais o puxam, para ver se a conclusão depende delas. Não é "tirar outlier para melhorar o resultado": as cidades não têm erro de dado (a conferência RREO × DCA fecha em 1,000 para elas) e a pergunta é só se a conclusão resiste.
- **Distância de Cook:** mede quanto os coeficientes mudariam se a cidade saísse (combina o quão fora do padrão ela está, o resíduo, com o quão extremo é o valor dela na variável explicativa, a alavanca). Regra fixada antes de rodar: remover as cidades com Cook acima de 4/n (6 cidades no M3: Niterói, Maricá, Saquarema, Rio Bonito, São Pedro da Aldeia, Duque de Caxias). Rodei também a versão só com as três de receita mais extrema (Niterói, Maricá, Saquarema), escolhidas por terem os maiores valores no primeiro diagnóstico.
- **Resultado:** a elasticidade sobe de 0,79 para 0,86 (sem as seis) e 0,89 (sem as três, intervalo 0,79 a 0,996). O efeito do Resto da Metropolitana vai de −4,4% para +1,2% e +6,6%. Ou seja: a lacuna da Metropolitana some e H5 continua valendo, porém mais fraca.

---

## A5. Replicação com 2023 (Analyze, 24/10/2026)

Código: `scripts/22_coleta_2023_replicacao.py` (coleta) e `scripts/23_analyze_a5_replicacao_2023.py` (análise). Saídas: `dados_tratados/indicadores_2023_replicacao.csv` e `analyze_a5_coeficientes.csv`. Previsão registrada antes em `docs/09`.

- **O que é:** refazer o A1 e o A2 com os dados de 2023, com as mesmas definições, e comparar com a previsão escrita antes de olhar. Replicar em outro ano mostra que o padrão não é um acidente de um ano nem um erro de declaração daquele ano.
- **Limite:** são as mesmas 92 cidades, com estruturas de receita parecidas de um ano para o outro. Os dois anos não são amostras independentes, então a replicação reforça a consistência e não vira "segunda prova" no sentido forte.
- **População de 2023:** o IBGE não publicou estimativa municipal para 2023 (a tabela 6579 vai 2021, 2022, 2024, 2025). Usei a média geométrica entre o Censo 2022 e a estimativa de 2024, que equivale a crescimento constante entre os dois anos. Exemplo: Censo 100.000 e estimativa 2024 de 104.000 dá 101.980.
- **Carmo fora:** entregou o RREO só até o 5º bimestre; receita de ano incompleto não é comparável (91 cidades; 90 sem a capital nos modelos de grupo).

---

## Segunda rodada: receita própria, uso ocasional e SIOPS (Analyze, 24/10/2026)

Código: `scripts/24_analyze_rodada2_propria_ocasional_siops.py`. Hipóteses H6, H7 e H8 em `docs/09`, escritas antes de rodar.

### 1. Receita própria e transferências a partir do RREO Anexo 01

- **Como:** receita própria = receitas (exceto intra-orçamentárias) menos transferências correntes menos transferências de capital, "até o bimestre", do mesmo relatório que já usamos (sem coleta nova). Conferência: a receita total do RREO é igual, centavo a centavo, à `receita` do projeto.
- **Limite:** os royalties e as compensações financeiras entram em "transferências"; os repasses do SUS também, sem separar saúde de outras áreas. A "receita própria" aqui é o que sobra, e inclui rendimentos financeiros (receita patrimonial).

### 2. Cinco modelos lado a lado (mesma estrutura log-log do A2, sem a capital)

A (receita total), B (só própria), C (própria e transferências juntas), D (própria + grupos), E (total + grupos, o do A2). **Por quê:** comparar o quanto cada receita explica do gasto (R²) e o peso de cada uma quando entram juntas. **Como:** `OLS` com erros HC3, como no A2.

### 3. Correlação de postos de Spearman (H7 e H8)

- **O que é:** mede se duas variáveis crescem juntas sem supor linha reta (usa as posições, não os valores).
- **Por quê:** o uso ocasional e o percentual aplicado são assimétricos e têm valores extremos; os postos não são puxados por eles.
- **Como:** `scipy.stats.spearmanr`. **Limite:** correlação não é causa.

### 4. Uso ocasional como variável do modelo

- Domicílios de uso ocasional (Censo 2022, IBGE) por 100 moradores, em `ln(1 + x)` para não zerar a cidade sem nenhum. É acrescentado ao modelo E para ver se o resíduo das Baixadas Litorâneas diminui.
- **Limite:** o Censo é de 2022, o gasto de 2024; o indicador muda devagar, mas não é do mesmo ano.

### 5. SIOPS: percentual aplicado e parte do gasto

- **Percentual aplicado em ASPS:** vem pronto do SIOPS (arquivo LCL141). **Parte do gasto coberta pelos recursos próprios:** valor aplicado (SIOPS) dividido pelo gasto em saúde do Siconfi. **Limite:** são bases diferentes (o SIOPS conta só recursos próprios dentro das regras da LC 141); a razão é uma ordem de grandeza e não uma identidade.
