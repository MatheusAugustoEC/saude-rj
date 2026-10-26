# Control, passo 2: previsões para o recorte de confirmação (2025), escritas antes de abrir

Registrado em 25/10/2026, **antes de baixar qualquer valor de 2025**. Regra C5: o recorte de confirmação é aberto **uma única vez**; cada conclusão é registrada como **sustenta**, **enfraquece** ou **cai**, qualquer que seja o resultado, antes de olhar de novo. A especificação dos modelos não muda: só o ano.

**Situação dos dados (script 31, 24/10/2026):** RREO com 6º bimestre em 89 de 92 municípios; DCA em 87 de 92; população 2025 do IBGE em 92 de 92. Faltam DCA em Carmo, Magé, Mendes, Miracema e São Francisco de Itabapoana. As entregas da DCA vão de 30/01/2026 a 16/10/2026: o dado **ainda não está maduro** (C6).

## Como o recorte será montado
- **Municípios:** os que têm RREO do 6º bimestre **e** DCA de 2025 (esperados: 86 ou 87). As exclusões são listadas pelo nome.
- **Variáveis, como em 2024:** receita = Receitas (exceto intra), "Até o Bimestre", 6º bimestre; saúde = DCA Anexo I-E, função 10, "Despesas Empenhadas"; população = estimativa 2025 do IBGE (não interpolada, ao contrário de 2023).
- **Modelo:** log do gasto por habitante contra log da receita por habitante e os grupos Baixada e Resto da Metropolitana; capital fora do ajuste e prevista de fora; erros HC3; os mesmos grupos de 2024.
- **Maturidade (C6):** DCA entregue depois de 31/08/2026 fica marcada como "recente". Todo resultado sai **com e sem** as marcadas.
- **Abertura única:** a coleta e a análise rodam em uma passada, com a saída guardada. Se houver erro de código, corrijo o código e registro; **não reespecifico o modelo** nem troco critérios depois de ver o resultado.

## Conclusões, previsões e critérios

| Id | Conclusão que vem de antes | Previsão (palpite, fixado agora) | Sustenta | Enfraquece | Cai |
|---|---|---|---|---|---|
| K1 | Elasticidade da receita abaixo de 1 (H5; 0,81 em 2024, 0,80 em 2023) | Entre 0,70 e 0,92 | IC 95% inteiro abaixo de 1 | IC inclui 1 | IC inteiro acima de 1 |
| K2 | Resto da Metropolitana, com a mesma receita, sem conclusão (H1; −4,4% e −6,8%) | Ponto entre −10% e 0%, IC inclui zero | Ponto entre −10% e +5% e IC inclui zero | Ponto fora de ±10%, mas IC inclui zero | IC exclui zero |
| K3 | Capital abaixo do previsto pela receita (H3; −35% a −37%) | Entre −25% e −45% | Abaixo do previsto em 25% ou mais | Abaixo, mas menos de 25% | Acima do previsto |
| K4 | Gasto segue repasses mais que receita própria (H6) | Coeficiente dos repasses maior que o da própria; R² da própria sozinha menor que o da total | Os dois valem | Só um vale | Nenhum vale |
| K5 | Triagem R1: Niterói, São Pedro da Aldeia e a capital (São Francisco de Itabapoana fica fora por falta de DCA) | Pelo menos 2 das 3 saem de novo do intervalo sem a própria cidade; correlação de postos dos resíduos 2024 × 2025 de +0,60 ou mais | 2 ou 3 repetem **e** correlação ≥ +0,60 | 1 repete, ou correlação entre +0,40 e +0,60 | Nenhuma repete, ou correlação abaixo de +0,40 |
| K6 | Pares por receita leem melhor que a região (R2; 46%) | Redução de dispersão entre 30% e 55% | Redução de 20% ou mais | Entre 0% e 20% | Sem redução |
| K7 | Repasses movem o gasto dentro da cidade (R4; 0,28; IC 0,004 a 0,565) em 2024→2025 | Ponto entre 0,10 e 0,45; elasticidade entre cidades entre 0,55 e 0,80 | IC de ano a ano acima de zero | IC inclui zero, ponto positivo | Ponto zero ou negativo |
| K8 | Baixadas Litorâneas abaixo do previsto, achado para auditoria (resíduo mediano −15%) | Entre −8% e −22% | Resíduo mediano entre −8% e −22% | Entre −5% e −8% | Dentro de ±5% ou acima |
| K9 | Somar visitantes à população **piora** o resíduo das Baixadas Litorâneas (R3 não sustentada) | Piora com 1 a 3 visitantes por domicílio | Piora em todos os cenários | Piora em alguns | Melhora em todos |

**Não entram no recorte de 2025:** H8 (SIOPS 2025 não foi coletado nem verificado; fica como extensão), R5 e R7 (são fotos de um ano, descritivas, sem hipótese a confirmar) e R6 (conceitos de fontes diferentes).

## Regras de leitura
- **2025 não é amostra independente** do ponto de vista das cidades: são as mesmas 92. Confirma estabilidade no tempo, não generalização para outros lugares.
- **2025 é o primeiro ano de novos mandatos municipais** (eleições de 2024). Se algo mudar, a explicação pode ser de regime e não de modelo; isso entra em C9.
- **Resultado contrário vale.** "Cai" é resultado, e entra no relatório com o mesmo destaque que "sustenta".
- **Dado maduro:** o resultado é lido primeiro com todas as cidades do recorte e depois sem as DCAs "recentes". Se as duas leituras divergirem na classificação, vale a pior e a divergência é registrada.

## Desempates e definições operacionais (fixados antes de abrir, 25/10/2026)
Alguns casos ficaram fora das células da tabela. Para não decidir depois de ver o resultado:
- **K1:** sustenta se o limite superior do IC fica abaixo de 1; cai se o limite inferior fica acima de 1; qualquer outro caso, enfraquece.
- **K2:** se o IC exclui zero, cai; senão, se o ponto está entre −10% e +5%, sustenta; senão, enfraquece (inclui o ponto entre +5% e +10% com IC cruzando zero).
- **K5:** sustenta com 2 ou 3 repetições **e** correlação ≥ +0,60; cai com nenhuma repetição **ou** correlação < +0,40; senão, enfraquece. "Repetir" é ficar abaixo do limite inferior do intervalo de previsão de 95% calculado sem a própria cidade. A correlação é a de postos (Spearman) entre os resíduos deixa-uma-fora de 2024 e de 2025.
- **K6:** mesma medida do Improve (desvio absoluto médio do log do gasto por habitante contra a mediana do grupo sem a própria cidade), cinco faixas de receita por quantis de 2025, contra as 8 regiões.
- **K7:** sustenta se o limite inferior do IC de ano a ano (2024→2025, sem a capital, mesmo bimestre nos dois anos, HC3) fica acima de zero; enfraquece se o ponto é positivo e o IC inclui zero; cai se o ponto é zero ou negativo.
- **K8:** resíduo mediano das Baixadas Litorâneas (modelo M3 de 2025): sustenta se ≤ −8%; enfraquece se entre −8% e −5%; cai se acima de −5%.
- **K9:** o resíduo mediano das Baixadas Litorâneas é calculado com 0, 1, 2 e 3 visitantes por domicílio de uso ocasional (Censo 2022). Sustenta se piora (fica mais negativo) nos três cenários contra 0; enfraquece se piora em alguns; cai se não piora em nenhum.
- **Classificação final de cada K:** a pior entre a leitura com todas as cidades do recorte e a leitura sem as DCAs "recentes" (entregues depois de 31/08/2026). Ordem: sustenta > enfraquece > cai.

---

## Resultado do recorte de 2025 (aberto uma vez em 25/10/2026; script 32 coletou, script 33 analisou)

Saída completa: `dados_tratados/control_2025_saida.txt`. **86 cidades** no recorte (85 sem a capital). Excluídas, 6: Carmo, Magé, Mendes, Miracema, São Francisco de Itabapoana e **Volta Redonda** (esta tem DCA no extrato de entregas, mas o Anexo I-E voltou vazio; o script 31 contava 87 DCAs e o script 32 achou 86 com dado; fica registrado como divergência entre extrato e anexo). DCA "recente" (depois de 31/08/2026): Mesquita, Seropédica, Campos dos Goytacazes e Angra dos Reis. A leitura sem essas quatro não muda nenhuma classificação.

| Id | Resultado em 2025 | Previsão | Classificação |
|---|---|---|---|
| K1 | Elasticidade da receita 0,741 (IC 0,628 a 0,855) | 0,70 a 0,92 | **Sustenta** |
| K2 | Resto da Metropolitana −7,2% (IC −20,7% a +8,6%); Baixada −15,1% (IC −33,0% a +7,6%) | −10% a 0%, IC inclui zero | **Sustenta** |
| K3 | Capital: real R$ 1.152, previsto R$ 1.732 (R$ 1.135 a R$ 2.643), −33,5%; dentro do intervalo | −25% a −45% | **Sustenta** |
| K4 | Repasses 0,667, própria 0,113; R² da própria sozinha 0,397, da total 0,816 | Os dois valem | **Sustenta** |
| K5 | Das 3 sinalizadas, só **Niterói** fica de novo fora do intervalo (−43,8%); São Pedro da Aldeia e a capital ficam dentro. Correlação de postos dos resíduos 2024 × 2025 de +0,83. Fora do intervalo em 2025: Niterói e Araruama (−33,3%, nova) | 2 de 3 e correlação ≥ +0,60 | **Enfraquece** (1 de 3 repete; a correlação, que foi alta, não compensa) |
| K6 | Dispersão cai de 0,390 (região) para 0,211 (pares): 46% | 30% a 55% | **Sustenta** |
| K7 | Ano a ano (2024→2025, n = 85): repasses 0,591 (IC 0,268 a 0,915); entre cidades 0,667 | 0,10 a 0,45; 0,55 a 0,80 | **Sustenta** (mas o ponto ficou **acima** da previsão) |
| K8 | Baixadas Litorâneas: resíduo mediano −15,6% | −8% a −22% | **Sustenta** |
| K9 | Resíduo mediano das Baixadas Litorâneas com 0, 1, 2 e 3 visitantes: −15,6%, −17,5%, −18,6%, −18,8% | Piora nos três cenários | **Sustenta** |

**Placar: 8 sustentam, 1 enfraquece, nenhuma cai.**

**O que o resultado ensina (para o relatório):**
- A triagem da R1 é estável como **ordem** das cidades (correlação +0,83) mas instável como **lista de sinalizadas**: só Niterói persiste nos três anos (−49%, −48%, −44%). A capital, que em 2024 ficou pouco fora do intervalo, em 2025 fica dentro, como em 2023. Isso confirma o que o Improve já dizia: poucas cidades, intervalo largo.
- A elasticidade dos repasses dentro da cidade foi 0,28 (2023→2024) e 0,59 (2024→2025): o valor depende do par de anos. O teste de estresse da R4 precisa mostrar as duas faixas, e a elasticidade entre cidades (0,67, estável em três anos) continua o ponto de referência.
- Palpite errado: K7 (0,10 a 0,45; deu 0,59). Palpites certos: K1, K2, K3, K6, K8, K9.
- Araruama entrou na lista (−33,3%), sem explicação nos dados: achado para auditoria, com a ressalva de sempre.
