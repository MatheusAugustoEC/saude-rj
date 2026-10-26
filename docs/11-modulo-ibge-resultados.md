# Módulo IBGE (D2): idade e saneamento no modelo do Analyze

Rodado em 24/10/2026, depois da aprovação das hipóteses M1 a M5 (docs/09). Código: `scripts/28_analyze_modulo_ibge.py`. Dados: Censo 2022 (IBGE, SIDRA), tabela 10157 (população por idade) e tabela 6805 (esgotamento sanitário), em `dados_brutos/`. Saídas: `dados_tratados/analyze_ibge_*.csv`.

**Conferência dos dados:** a população total da tabela por idade é idêntica (diferença 0,0) à população do Censo usada no projeto, nos 92 municípios; os domicílios com esgoto ligado à rede variam de 3,2% a 98,8% entre as cidades, dentro do esperado.

**Variáveis:** percentual de 65 anos ou mais e percentual de domicílios com esgoto ligado à rede (rede geral, pluvial ou fossa ligada à rede), cada um dividido por 10 para o coeficiente ser o efeito de +10 pontos percentuais.

## Resultados (dado declarado, não auditado; gasto não é qualidade; associação entre cidades não é causa)

| Id | Hipótese | Resultado | Veredito |
|---|---|---|---|
| M1 | Mais idosos, mais gasto (com a mesma receita) | −3,0% por +10 pp, IC −26% a +26% (2024); −0,2% em 2023. O intervalo é larguíssimo: +10 pp é quase toda a faixa observada (8% a 17,6%) | **Não se sustenta** (sinal oposto, sem poder para decidir) |
| M2 | Saneamento pior, mais gasto (hipótese do responsável) | Sem controle, a correlação é como previsto (Spearman −0,27 em 2024, −0,33 em 2023). Descontada a receita, o sinal **inverte**: +3,4% por +10 pp de esgoto, IC +0,3% a +6,5% (2024); +2,5%, IC −0,9% a +5,9% (2023) | **Não se sustenta depois de descontar a receita**: o padrão bruto vem de as cidades com pouco esgoto serem as de receita alta (correlação receita × esgoto −0,42) |
| M3 | O efeito da Metropolitana muda pouco | −4,4% passa a −6,4% (mudança de 2,0 pp; 2023: 1,1 pp), abaixo do limite de 5 pp | **Confirmada** |
| M4 | A capital segue abaixo do previsto | Real R$ 1.136, previsto R$ 1.853 (R$ 1.225 a R$ 2.804): 38,7% abaixo, fora do intervalo em 2024; em 2023, 35,8% abaixo, dentro do intervalo por R$ 5 | **Confirmada em 2024; limítrofe em 2023** (igual ao Analyze) |
| M5 | Repete em 2023 | M3 e M4 sim; M2 enfraquece (intervalo inclui zero); M1 sem efeito | **Parcial** |

**Diagnóstico:** VIF máximo de 1,54 (nada preocupante); idade quase não se correlaciona com receita (0,12) nem com esgoto (−0,03). O R² sobe de 0,802 para 0,820 com as duas variáveis.

**Descrição (mediana por grupo, 2022):** esgoto ligado à rede de 36% na Costa Verde e 54% na Serrana a 93% na Baixada (núcleo de 6) e 95% na capital; idosos de 9,9% na Costa Verde a 14,5% na capital e no Noroeste. Menores esgotos: São Francisco de Itabapoana (3,2%), Paraty (17,7%). Mais idosos: Italva, Niterói e Miguel Pereira (17,3% a 17,6%).

## O que fica

- Idade e saneamento **não explicam** o gasto baixo da Metropolitana nem o da capital: os resultados de H1 a H4 do Analyze se mantêm.
- A Baixada (6 cidades) vai de −3,5% para −10,2% (IC −25% a +8%) quando se desconta o saneamento alto dela: continua sem conclusão.
- As Baixadas Litorâneas seguem gastando menos que o previsto (resíduo mediano −10%, antes −15%): idade e saneamento explicam um pouco; o uso ocasional também; sobra uma parte sem explicação, que segue como achado para auditoria.
- **Pergunta aberta que o saneamento deixa:** saneamento pior aumenta as doenças ligadas a ele (internações por doenças relacionadas ao saneamento inadequado); testar a hipótese do responsável de forma mais direta pede dados do SUS (internações), que é o módulo seguinte.
