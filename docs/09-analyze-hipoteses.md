# Analyze, etapa A0: hipóteses e critérios de decisão

Escritas em 24/10/2026, **depois** de rodar a decomposição descritiva (A1) e **antes** do modelo (A2) e da replicação em 2023 (A5). A1 não testa nada, mas já mostrou o padrão; por isso A2 é tratada como confirmação parcial, e a prova mais forte é A5.

**Pergunta central:** o gasto baixo da Metropolitana se explica pela receita por habitante?

| Id | Hipótese | Critério de decisão |
|---|---|---|
| H1 | Com a mesma receita por habitante, estar na Metropolitana (sem a capital) não muda o gasto por habitante de forma relevante | Intervalo de confiança do efeito da região, em escala log, contido em ±10%. Se o intervalo for largo demais para decidir, o resultado é "sem conclusão" |
| H2 | A Baixada (núcleo de 6) gasta menos que o previsto pela receita | Descrita município a município; o grupo entra no modelo, mas o intervalo largo é reportado como "sem conclusão" |
| H3 | A capital gasta menos por dedicar fatia menor da receita à saúde, e não só por receita menor | Decomposição (A1) e resíduo do modelo com e sem a capital |
| H4 | O padrão de 2024 se repete em 2023 | Mesma decomposição e mesmo modelo em 2023; se o sinal e a ordem de grandeza se mantêm, ganha força |

| H5 | **Pergunta do responsável:** como as cidades de maior receita por habitante se comportam em relação ao gasto em saúde? A expectativa dele é que mais receita leve a fatia maior para a saúde. (Reformulada em 24/10/2026: a primeira redação, "a fatia cai", foi minha, tirada do que eu já tinha visto no A1, e não foi pedida.) Hipótese neutra: a elasticidade da receita é diferente de 1 | Regressão em log: elasticidade com intervalo de 95%. Acima de 1: fatia sobe com a receita (expectativa do responsável). Igual a 1 (intervalo contém 1): fatia constante. Abaixo de 1: fatia cai. Descrição complementar: as 23 cidades do quartil de maior receita por habitante, com fatia e posição de cada uma |

Dois números diferentes nos critérios: o **intervalo de confiança é de 95%** (nível de 5%, o usual). O **±10% da H1 é uma margem de relevância prática**, escolhida por mim: abaixo disso, a diferença é pequena demais para importar (cerca de R$ 230 sobre R$ 2.322). Para dizer "sem diferença relevante", o intervalo inteiro precisa caber dentro da margem.

Regras: dado declarado e não auditado; gasto não é qualidade; resultado sem explicação vai para a lista de auditoria; receita mede capacidade financeira, não saúde financeira; parte do gasto em saúde vem de repasses do SUS que contam como receita.

**Previsão registrada antes da coleta de 2023 (H4):** pelo que vimos em 2024, espero em 2023 elasticidade abaixo de 1 (perto de 0,8), efeito do Resto da Metropolitana pequeno e dentro de ±10% ou com intervalo largo, e capital abaixo do previsto pela receita. Se 2023 contrariar, registro como achado.

---

## Segunda rodada: receita própria, domicílios de uso ocasional e SIOPS

Escritas em 24/10/2026 **antes** de rodar os scripts 24 (e dos dados de uso ocasional, já baixados mas não olhados) e depois de A2 e A5. Previsões são palpites registrados para não serem ajustados depois.

| Id | Hipótese e previsão | Critério |
|---|---|---|
| H6 | **Receita própria** (total sem transferências correntes e de capital): o gasto em saúde acompanha menos a receita própria do que a total, porque parte do gasto é paga por repasses. Previsão: elasticidade da receita própria abaixo de 1 e R² menor que o de 0,79 do modelo com a receita total; no modelo com as duas juntas (própria e transferências por habitante), o coeficiente das transferências é maior que o da própria | Elasticidades com IC de 95% e R² dos modelos, em 2024 e 2023 |
| H7 | **Uso ocasional** (Censo 2022, domicílios de uso ocasional por 100 moradores): as cidades de veraneio têm receita por habitante inflada por base de não moradores, o que cria a aparência de "fatia menor". Previsão: o indicador correlaciona positivamente com a receita por habitante e negativamente com a fatia da receita; incluí-lo no modelo aproxima de zero o resíduo mediano das Baixadas Litorâneas (hoje −15%) | Correlação de Spearman; resíduo mediano das Baixadas Litorâneas antes e depois |
| H8 | **SIOPS** (percentual da receita de impostos aplicado em saúde contra o mínimo de 15%, 2024): a maioria das cidades aplica bem mais que o mínimo, inclusive as 10 que menos gastam por habitante, porque a diferença de gasto por habitante vem da base de receita e não do esforço sobre ela. Previsão: pelo menos 90% das cidades acima de 15% e as 10 que menos gastam com mediana acima de 20% | Contagens e medianas; correlação entre o percentual aplicado e o gasto por habitante |

---

## Módulo IBGE (D2), plano proposto em 24/10/2026, APROVADO pelo responsável em 24/10/2026, com a M2 reformulada por ele (rodado depois da aprovação)

**Pergunta:** depois de descontar a receita, a idade da população e o saneamento explicam parte do gasto em saúde por habitante e das diferenças que ficaram sem conclusão?

**Dados (Censo 2022, IBGE, verificados para os 92 municípios):** população por sexo e grupos de idade (tabela 10157), percentual de 65 anos ou mais; esgotamento sanitário (tabela 6805), percentual de domicílios com esgoto ligado à rede. Só essas duas variáveis, escolhidas antes, para não ajustar o acaso com 91 cidades.

| Id | Hipótese (antes de rodar) | Critério |
|---|---|---|
| M1 | Com a mesma receita, cidades com mais idosos gastam mais em saúde por habitante | Coeficiente positivo com IC 95% que não inclui zero |
| M2 | **Hipótese do responsável:** cidades com saneamento pior (menor percentual de domicílios com esgoto ligado à rede) tendem a gastar mais em saúde por habitante; cidades com saneamento melhor, menos | Coeficiente do percentual de esgoto adequado negativo, com IC 95% que não inclui zero. Positivo ou com intervalo que inclui zero: a hipótese não se sustenta |
| M3 | O efeito da Metropolitana (−4,4%) muda pouco ao controlar idade e saneamento | Mudança maior que 5 pontos percentuais é relevante |
| M4 | A capital continua gastando menos do que o previsto, com idade e saneamento | Valor real fora do intervalo de previsão de 95% |
| M5 | Os resultados se repetem com 2023 (mesmo Censo, outro ano de gasto) | Mesmos critérios de M1 a M4 |

**Método:** o mesmo modelo log-log do Analyze, erros HC3, margem de ±10%, intervalo de 95%; métodos novos explicados no docs/10.
**Ressalvas previstas:** Censo de 2022 e não de 2024; idade e saneamento não medem necessidade; poder limitado com 91 cidades.
**SUS (outra metade do D2):** primeiro verificar se a base de leitos (CNES) é acessível e cobre os 92 municípios; só segue se valer o esforço.

**Diagnóstico acrescentado (sem nova variável):** correlações entre receita, idade, saneamento e grupos, e fator de inflação da variância (VIF), porque saneamento e receita costumam andar juntos e a Baixada tem saneamento baixo; coeficiente com VIF acima de 5 é lido com reserva. **Cuidado de leitura:** associação entre cidades não diz que as famílias sem saneamento causam o gasto (falácia ecológica).
