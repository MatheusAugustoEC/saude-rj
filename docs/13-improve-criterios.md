# Improve, etapa I0: recomendações, hipóteses e critérios (antes de rodar)

Escrito em 24/10/2026, **antes** de qualquer conta do Improve. Palpites e limiares abaixo são fixados agora para não serem ajustados depois. Regras da fase: I1–I14 da skill metodo-dmaic. Projeto de diagnóstico, sem modelo preditivo: `modelagem.md` não se aplica. Nada é implementado.

**Público:** controle, auditoria, gestão e, no que os dados sustentam, financeiro (risco fiscal, não caixa).

**Ressalvas (vão no relatório da fase e junto de cada recomendação):** dado declarado e não auditado; gasto em saúde por habitante não mede qualidade nem necessidade; cidade sinalizada é cidade para olhar, não cidade errada; associação entre cidades não é efeito dentro de uma cidade; os dois anos usam as mesmas 92 cidades; nada é implementado, os ganhos são estimativas.

**Não se aplicam (declarado em uma linha):** I5 (não mexemos em preço, prazo ou conveniência do cliente) e I7 (sem horizonte acima de um ano nem ganho em dinheiro de longo prazo).

## Contramedidas

| Id | Contramedida | Causa que ataca (Analyze) | Classe (I1) | Para quem |
|---|---|---|---|---|
| R1 | Triagem de auditoria: cidades cujo gasto fica abaixo da faixa que a receita prevê | Desvio sem explicação (Baixadas Litorâneas, 13% a 15% abaixo nos dois anos) | Detecta | Controle, auditoria |
| R2 | Painel de pares por receita, com receita própria separada de repasses e a fatia aplicada | A diferença da Metropolitana quase some ao comparar cidades com a mesma receita; o gasto segue repasses (H6) | Reduz a variação de leitura | Gestão |
| R3 | Ajuste da base nas cidades de veraneio | Uso ocasional infla a receita por habitante (H7) | Reduz a variação de leitura | Gestão, controle |
| R4 | Teste de estresse dos repasses | Gasto segue repasses (0,68 contra 0,12 da própria) | Protege contra o efeito | Gestão, financeiro |
| R5 | Folga em reais sobre o mínimo de 15% | Mínimo cumprido por todos, mas com margens muito diferentes (H8) | Detecta | Controle, financeiro |
| R6 | Reconciliação Siconfi × SIOPS | Duas fontes, conceitos diferentes; recursos próprios do SIOPS ≈ 37% do gasto do Siconfi | Detecta | Auditoria |
| R7 | Painel de folga sobre os limites da LRF (pessoal, dívida) e restos a pagar | **Nenhuma causa validada**: o Analyze não testou pessoal, dívida nem restos a pagar. Painel descritivo de risco fiscal | Detecta | Controle, financeiro |

## Hipóteses, contrafactual, conta e critérios

Para todas: contrafactual escrito por extenso (I2), três cenários com a premissa de cada um (I3), ponto de indiferença acima do ganho bruto onde a premissa decisiva não é estimável (I4), pior caso de contorno da regra (I11) e FMEA (I12), parágrafo do cético com resposta (I14).

**R1 Triagem.** Regra: cidade é sinalizada se o gasto observado fica abaixo do intervalo de previsão de 95% calculado **sem ela** (deixa-uma-fora, para a cidade não puxar o modelo) **e** o resíduo é negativo também em 2023.
- Contrafactual: "se a cidade sinalizada gastasse o que a receita prevê, o gasto seria R$ X por habitante, ou R$ Y no total".
- Palpite: no máximo 8 das 92 sinalizadas, e as Baixadas Litorâneas sobrerrepresentadas.
- Critério de utilidade (retroteste): das cidades que ficariam sinalizadas só com 2023, a parcela que se repete em 2024, comparada com a que se repetiria ao acaso. Repetição acima do acaso, com a ressalva dos dois anos não independentes, sustenta o uso.
- Ponto de indiferença: parcela mínima p* de sinalizadas **sem explicação legítima** para a triagem valer o custo, p* = 1/v, onde v é quantas vezes um achado vale o custo de olhar uma cidade. Tabela com v = 2, 5 e 10.
- Teste proposto (I8–I10): unidade = município; piloto em que a controladoria olha sinalizadas e uma amostra de não sinalizadas; métrica = parcela com achado relevante; tamanho de amostra e efeito mínimo detectável **calculados**. Palpite: com cerca de 8 sinalizadas, só se detecta diferença grande; o desenho exige ampliar para outros estados (o Siconfi cobre todos). Ameaças: contaminação (um achado muda o comportamento de vizinhos), efeito novidade, parar cedo.

**R2 Pares.** Hipótese: comparar cada cidade com as de faixa de receita parecida (cinco faixas por quantis de receita por habitante) reduz a dispersão do gasto por habitante mais do que comparar com a região (as 8 regiões CEPERJ).
- Medida: desvio absoluto médio do log do gasto por habitante em relação à mediana do grupo, **excluindo a própria cidade** da mediana.
- Critério (fixado agora): redução de pelo menos 20% frente à região é relevante; entre 0% e 20%, é pequena; sem redução, a hipótese cai.
- Contrafactual: "se o gestor de Maricá comparasse com cidades de receita parecida, e não com a Metropolitana, a leitura de 'gasta menos' ficaria assim".
- Indiferença: a redução mínima de dispersão abaixo da qual o painel novo não acrescenta nada sobre o da região.

**R3 Veraneio.** Hipótese: contar parte dos domicílios de uso ocasional como população adicional aproxima de zero o resíduo das Baixadas Litorâneas.
- Cenários de pessoas não residentes por domicílio ocasional: 0 (hoje), 1, 2 e 3 (premissa, sem fonte oficial: é variável de sensibilidade).
- Ponto de indiferença (I4, o número principal): quantas pessoas por domicílio ocasional zerariam o resíduo mediano. Se for um valor implausível (acima do tamanho médio de uma família), o uso ocasional não explica sozinho e o achado para auditoria permanece.
- Critério: resíduo mediano de −15% (hoje) se aproximar de zero (dentro de ±5%) em algum cenário plausível.

**R4 Estresse dos repasses.** Hipótese: a elasticidade do gasto em relação aos repasses (0,68) vale também para variações de um ano para o outro dentro da mesma cidade (primeiras diferenças 2023→2024), o que autoriza usá-la no teste.
- Verificação antes de usar: coeficiente de Δln(repasses por habitante) sobre Δln(gasto por habitante), com IC 95% e HC3. Positivo com intervalo sem zero: o teste de estresse vale. Se o intervalo incluir zero: o teste vira apenas ilustração e é declarado assim (associação entre cidades não é efeito dentro de uma cidade).
- Cenários: repasses caem 10%, 20% e 30%; pessimista com o limite superior do IC do coeficiente, provável com o ponto, otimista com o limite inferior.
- Ponto de indiferença: queda de repasses que reduz o gasto por habitante em 10% (a margem de relevância do projeto).
- Dependência de regra (I13): parte dos repasses é carimbada do SUS e depende de regras federais; se mudarem, a conta muda. Declarado.

**R5 Folga sobre o mínimo.** Folga em reais = valor aplicado − 15% × base de impostos (SIOPS 2024).
- Sinalização (julgamento meu, fixado agora): folga abaixo de 3 pontos percentuais.
- Palpite: poucas cidades (até 6), entre elas Paracambi e Mesquita.
- Ponto de indiferença: queda percentual do gasto que zeraria a folga de cada cidade.
- Limite: um só ano (2024) no SIOPS; a folga não diz se foi folga estrutural ou de um ano.

**R6 Reconciliação (opcional).** Razão entre recursos próprios do SIOPS e gasto em saúde do Siconfi, por cidade.
- Hipótese: a razão varia muito entre cidades (conceitos diferentes), então serve como pergunta, não como alarme.
- Critério: se a faixa entre o 25º e o 75º percentil for larga (mais de 0,30 em razão), conclusão = "baixa especificidade, usar só como pergunta". Cidades fora de mediana ± 2 desvios absolutos da mediana são listadas e cruzadas com a R1.

**R7 Painel de limites (descritivo).** Dados do Measure (`indicadores_2024.csv`), sem coleta nova.
- Pessoal: gasto do Executivo sobre a RCL contra o limite prudencial e o máximo (54% nos municípios; 49% no estado). Dívida: DCL sobre a RCL contra o limite do Senado (120% nos municípios; 200% no estado). Restos a pagar sobre a receita: só descrição, sem limite legal.
- Sinalização (fixada agora): pessoal acima do limite prudencial; dívida a partir de 80% do limite (96% da RCL nos municípios); restos a pagar no quartil superior (descritivo).
- Palpite: no máximo 10 municípios acima do prudencial e no máximo 5 com dívida a partir de 80% do limite.
- Limite honesto: **não ataca causa validada** (o Analyze não testou estas variáveis). A relação entre folga fiscal e gasto em saúde fica para as extensões, depois do núcleo ([docs/12](12-extensoes-depois-do-nucleo.md)). Entes com sinalizador especial no Measure são marcados, não retirados.

## Decisões do responsável (24/10/2026)
- R7 aprovada como painel **descritivo**.
- Limiares como propostos: R2 em 20%, R5 em 3 pontos percentuais, R1 com palpite de no máximo 8 sinalizadas.
- R6 entra. (Interpretação do "Aprovo. Prossiga" sobre as três perguntas; declarada ao responsável na entrega.)
