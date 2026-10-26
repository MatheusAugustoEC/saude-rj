# A triagem de auditoria se sustenta; o ajuste de veraneio não

**Fase 4 · Improve, Saúde fiscal do Rio de Janeiro · Siconfi 2024 (com 2023 para comparação) · 24/10/2026**

> [!NOTE]
> Dados públicos e declarados pelos entes, não auditados. Gasto em saúde por habitante não mede qualidade nem necessidade. Cidade sinalizada é cidade para olhar, não cidade errada. Nada foi implementado: os ganhos são estimativas.

<div class="numero"><b>46%</b><span>menos dispersão do gasto por habitante ao comparar cada cidade com cidades de receita parecida, e não com a própria região (92 cidades, 2024)</span></div>

<div class="resumo" markdown="1">

**Em três linhas.** Propus sete contramedidas de controle, com critérios escritos antes das contas ([docs/13](../../docs/13-improve-criterios.md)). Quatro se sustentaram, duas são descritivas e **uma caiu no próprio critério** (o ajuste do veraneio). Três dos meus palpites estavam errados, e isso está registrado como resultado.

</div>

## 1. A pergunta desta fase

O Analyze mostrou que o gasto em saúde segue a receita e os repasses, que todas as cidades cumprem o mínimo de 15% e que ficaram desvios sem explicação. O Improve pergunta o que um controle, uma auditoria ou uma gestão poderia **fazer** com isso, de modo que dê para provar errado. Como o projeto é de diagnóstico e nada se implementa, o rigor está em três coisas: a conta à vista, o ponto de indiferença e o desenho do teste (regras I2 a I4 e I8).

## 2. O que eu encontrei

| Id | Contramedida | Resultado | Veredito |
|---|---|---|---|
| R1 | Triagem de auditoria | 4 cidades sinalizadas: Niterói, São Francisco de Itabapoana, São Pedro da Aldeia e a capital. Das 3 fora do intervalo em 2023, 2 repetem em 2024 | **Sustentada**, mas o teste de campo não cabe só no RJ |
| R2 | Painel de pares por receita | Dispersão cai 46% (de 0,372 para 0,200), contra 20% exigido; 34 de 92 cidades mudam de leitura | **Sustentada**, com a ressalva de que é em parte por construção |
| R3 | Ajuste de veraneio | O resíduo das Baixadas Litorâneas **piora** de −15% para −18% e nunca chega a zero | **Não sustentada** |
| R4 | Teste de estresse dos repasses | Entre cidades, elasticidade 0,68; de um ano para o outro dentro da cidade, 0,28 (intervalo 0,004 a 0,565) | **Sustentada com cautela**: o critério passa, mas encostando no zero |
| R5 | Folga sobre o mínimo de 15% | Nenhuma abaixo do mínimo; 18 com folga abaixo de 3 pontos; 7 com menos de 1 ponto | **Descritiva**; meu palpite (até 6) errou |
| R6 | Reconciliação Siconfi × SIOPS | Razão mediana 0,37, quartis 0,26 a 0,48; 11 cidades fora da faixa; nenhuma é sinalizada na R1 | **Utilizável como pergunta** |
| R7 | Painel de limites da LRF | 22 municípios declaram pessoal acima do limite prudencial; nenhum tem dívida perto do limite | **Descritiva**; meu palpite (até 10) errou |

### 2.1 R1: a triagem separa poucas cidades, e elas persistem

**Quatro cidades ficam fora do intervalo de previsão sem a própria cidade no ajuste:**

| Cidade | Grupo | Gasto contra o previsto 2024 | 2023 |
|---|---|---|---|
| Niterói | Metropolitana (resto) | −47,7% | −49,0% (também fora do intervalo) |
| São Francisco de Itabapoana | Norte Fluminense | −42,6% | −41,7% (também fora) |
| São Pedro da Aldeia | Baixadas Litorâneas | −36,7% | −28,4% |
| Rio de Janeiro (capital) | Capital | −35,0% | −32,7% |

- **Retroteste:** das 3 cidades fora do intervalo em 2023, 2 repetem em 2024 (67%), contra 4% de taxa-base. O teste exato de Fisher dá p = 0,004. O resíduo de 2023 e o de 2024 têm correlação de postos de +0,77.
- **O palpite sobre as Baixadas Litorâneas errou.** Eu esperava essa região sobrerrepresentada; só uma das 10 cidades dela é sinalizada. O desvio de −13% a −15% do Analyze é de **grupo**: nenhuma cidade da região é extrema sozinha, o grupo todo fica um pouco abaixo.
- **Niterói e São Francisco de Itabapoana são novos para a lista de auditoria.** Não têm explicação nos dados. Entram como achado para auditoria, com a ressalva de que pode haver gasto registrado em outro ente ou fundo.
- **Conta à vista:** o desvio somado das 4 é de R$ 5,0 bilhões que a receita prevê a mais (isto **não é ganho**, é a magnitude do que ficou sem explicação). Com a parcela sem explicação legítima de 20%, 50% e 80%, esperam-se 0,8, 2,0 e 3,2 cidades com achado.
- **Ponto de indiferença:** a triagem vale o custo se a parcela sem explicação ficar acima de 1/v, onde v é quantas vezes um achado vale o custo de olhar uma cidade: 50% (v = 2), 20% (v = 5), 10% (v = 10).

> [!WARNING]
> **O teste de campo não cabe só no RJ.** Com 4 sinalizadas e 4 controles, poder de 80% e taxa-base de achado de 20%, só se detectaria diferença a partir de 99%. Para distinguir 20% de 50% seriam necessárias 38 cidades por grupo. Por isso o desenho propõe ampliar para outros estados, que o Siconfi cobre.

### 2.2 R2: comparar por receita parecida lê melhor do que comparar por região

**A dispersão cai de 0,372 para 0,200 (46%), com 92 cidades e a mediana do grupo calculada sem a própria cidade.** O limite que fixei era 20%.

- **Placebo:** cinco grupos sorteados com os mesmos tamanhos (2.000 vezes) dão 0,388; os pares ficam muito abaixo do 5º percentil (0,365).
- **A leitura muda:** 34 de 92 cidades trocam de lado (abaixo ou acima da mediana do grupo) ao trocar a região pelos pares. A Baixada (núcleo de 6) passa de −33% contra a região para −15% contra os pares; a Metropolitana (resto) passa de +27% para +2%.
- **Limite honesto:** agrupar por receita explica o gasto em boa parte por construção, porque gasto é receita vezes a fatia. O ganho é de **leitura** para quem gere, não de causa.

### 2.3 R3: contar visitantes no denominador não aproxima o resíduo de zero

**Quanto mais visitantes por domicílio de uso ocasional eu somo à população, mais negativo fica o resíduo das Baixadas Litorâneas.** Com 0, 1, 2 e 3 pessoas por domicílio, o resíduo mediano vai de −15,0% a −16,8%, −17,9% e −18,2%, e nem com 10 pessoas chega a zero.

- **Por quê:** a elasticidade da receita é abaixo de 1. Dividir gasto e receita por uma população maior reduz o gasto por habitante mais do que reduz o previsto, e o resíduo cai. É um efeito do denominador, e não uma refutação do uso ocasional.
- **O que ainda vale do Analyze (H7):** usar o uso ocasional como **variável de controle** reduziu o resíduo de −15% para −9%. Isso é outra operação, resultado parcial do Analyze, e não uma recomendação nova daqui.
- **Consequência:** a R3 como desenhada não entra na lista de recomendações. O achado para auditoria das Baixadas Litorâneas **permanece**.

### 2.4 R4: o teste de estresse vale, mas o efeito dentro da cidade é menor

**Se os repasses caíssem 20%, o gasto em saúde cairia entre 6% e 14%, conforme a elasticidade usada.** Como o gasto total das 92 cidades é de cerca de R$ 27,8 bilhões, isso é de R$ 1,7 a R$ 3,9 bilhões.

| Queda dos repasses | Ano a ano (0,28; IC 0,004 a 0,565) | Entre cidades (0,68; IC 0,57 a 0,78) |
|---|---|---|
| 10% | −3,0% (de 0,0% a −5,8%) | −6,9% (de −5,9% a −7,9%) |
| 20% | −6,1% (de −0,1% a −11,8%) | −14,0% (de −12,0% a −16,0%) |
| 30% | −9,6% (de −0,1% a −18,2%) | −21,5% (de −18,5% a −24,3%) |

- **Critério fixado antes:** o coeficiente de ano a ano ter intervalo sem zero. **Passou, mas por pouco**: 0,284 (0,004 a 0,565), R² de 0,035. Por isso mostro as duas colunas e não só a de 0,68, que supõe que o efeito entre cidades vale dentro de uma cidade.
- **Ponto de indiferença** (queda dos repasses que reduz o gasto em 10%): 14,4% com a elasticidade entre cidades; 31,0% com a de ano a ano; 17,0% no pior caso do ano a ano.
- **Quem está mais exposto:** cidades onde 90% a 92% da receita vem de repasses (Rio das Flores, Santa Maria Madalena, Engenheiro Paulo de Frontin e São Francisco de Itabapoana, entre outras). A capital tem 34%.
- **Dependência de regra (I13):** parte dos repasses é carimbada do SUS e depende de regra federal. Se a regra mudar, a conta muda.

### 2.5 R5, R6 e R7: três painéis descritivos

- **R5, folga sobre o mínimo de 15%:** nenhuma cidade abaixo do mínimo. Pelo critério (folga abaixo de 3 pontos), **18 cidades**, entre elas a capital (17,8%) e Niterói (16,9%), que têm folga grande em reais (R$ 596 milhões e R$ 47 milhões). Abaixo de 1 ponto são 7: Mesquita, Magé, Paracambi, Natividade, Miguel Pereira, São Sebastião do Alto e Engenheiro Paulo de Frontin. Para zerar a folga, o gasto próprio teria de cair 0,6% em Paracambi e 15,7% na capital. A folga mediana é de 8,3 pontos (R$ 328 por habitante).
- **R6, Siconfi × SIOPS:** razão mediana de 0,37 (quartis 0,26 a 0,48; amplitude 0,22, abaixo do 0,30 que eu tinha fixado). Onze cidades ficam fora de mediana ± 2 desvios absolutos (Magé, Rio das Ostras, Itaguaí, Macaé, Angra dos Reis, entre outras). **Nenhuma coincide com as sinalizadas na R1**: são sinais independentes. Os conceitos das duas fontes são diferentes, então a lista é uma pergunta para conciliação e não um alarme.
- **R7, limites da LRF:**
  - **Pessoal:** 22 municípios declaram pessoal acima do limite prudencial (11 acima do máximo). Três deles estão marcados no Measure como "RCL atípica" (Areal, Itaperuna e Miracema, com 122% a 154%); sem esses três, são 19 acima do prudencial e 8 acima do máximo. O **estado** declara 46,8% da RCL, um pouco acima do prudencial (46,5%) e abaixo do máximo (49,0%).
  - **Dívida:** nenhum município chega a 80% do limite; 53 têm dívida líquida negativa. O estado declara 211,3% da RCL, acima do limite de 200%.
  - **Restos a pagar:** 23 municípios no quartil superior (a partir de 4,5% da receita), com Rio Bonito (28,6%) e Barra do Piraí (20,4%) à frente.
  - **Cuidado de leitura:** é o valor declarado. Acima do limite não significa irregular; pode ser deduções, base de cálculo ou problema do dado. A R7 não ataca causa validada (o Analyze não testou pessoal, dívida nem restos a pagar).

## 3. O que eu decidi

| Escolha | O que usei | O que mais considerei | Por que esta | Evidência | Regra |
|---|---|---|---|---|---|
| Intervalo da triagem | Previsão de 95% **sem a própria cidade** (deixa-uma-fora) | Intervalo do ajuste com todas (convencional) | Com a cidade dentro, ela puxa o modelo para si e some do alvo | `improve_r1_triagem.csv` | I1, I2 |
| Teste da triagem | Persistência 2023→2024 por Fisher exato e correlação de postos | Só descrever os casos | Com 3 casos, o exato é o teste adequado; o aviso dos dois anos não independentes fica no texto | p = 0,004 | I8 |
| Comparação de pares | Cinco faixas por quantis de receita, mediana sem a própria cidade, com placebo | Regiões do CEPERJ (convencional) | O Analyze mostrou que a receita explica a maior parte; o placebo mostra que a queda não é acaso de agrupar | 0,372 contra 0,200 | I2 |
| Ajuste de veraneio | População somada de visitantes em quatro cenários, e o valor que zeraria | Variável de controle (já feita no H7) | Testa se a correção da base é viável; o ponto de indiferença é o número principal | `improve_r3_veraneio.csv` | I4 |
| Elasticidade do estresse | Duas: entre cidades e de ano a ano (primeiras diferenças) | Só a do corte transversal (convencional) | A segunda mede o que importa para um choque dentro de uma cidade | 0,68 e 0,28 | I3, I13 |
| Tamanho do teste | Poder de 80%, nível 5%, taxa-base de 20% como premissa | Não calcular | Sem calcular, não se sabe que o piloto não decide | 4 sinalizadas só detectam 99%; 38 por grupo | I8 |
| Limiares | R2 em 20%, R5 em 3 pontos, R1 palpite de 8 | Sem limiar | Fixados antes de ver resultado | docs/13 | I3 |

> [!TIP]
> **Decisão de enquadramento:** as sete contramedidas são de **controle e gestão**, não de política de saúde. Nenhuma diz que se deve gastar mais, porque gasto não mede qualidade.

### Como a regra seria contornada, e o FMEA (I11, I12)

| Contramedida | Como burlar (Goodhart) | Falha | Gravidade | Ocorrência | Detecção | Prioridade | Mitigação antes do piloto |
|---|---|---|---|---|---|---|---|
| R1 triagem | Registrar gasto em outro ente ou fundo para sair da faixa | Sinalizar cidade com explicação legítima | 6 | 6 | 5 | 180 | Pedir a explicação antes de auditar; comparar com a DCA |
| R2 pares | Usar faixas de receita que escondam a cidade | Ler a faixa como meta | 5 | 5 | 6 | 150 | Faixas fixas por quantis, publicadas antes |
| R4 estresse | Tratar o cenário como previsão | Gestor ancora no número de 0,68 | 7 | 5 | 6 | 210 | Mostrar sempre as duas elasticidades e o intervalo |
| R5 folga | Inflar o gasto próprio no fim do ano para passar do mínimo | Folga artificial | 6 | 4 | 6 | 144 | Ler a folga em dois anos |
| R6 reconciliação | Ajustar um lado da conta para fechar a razão | Alarme falso por diferença de conceito | 4 | 7 | 4 | 112 | Tratar como pergunta, nunca como alarme |
| R7 limites | Reclassificar despesa para sair do limite | Ler "acima" como irregular | 7 | 5 | 5 | 175 | Marcar entes com dado atípico, mostrar o valor declarado |

Notas de 1 a 10 são julgamento meu, não medida. Prioridade = gravidade × ocorrência × detecção.

### O parágrafo do cético, e a resposta (I14)

> **Contra:** "Você sinalizou quatro cidades com um modelo que explica só a receita. Niterói e a capital têm hospitais que atendem gente de fora, e o gasto por habitante residente fica para baixo por construção. A triagem só reencontra o que o modelo não conhece, e auditar essas cidades é gastar o tempo de quem controla."
>
> **Resposta:** o ponto é justo, e é por isso que a R1 é de triagem e não de acusação. A recomendação pede a explicação antes de auditar, e o ponto de indiferença diz a parcela sem explicação a partir da qual compensa olhar. O que eu não posso dizer é que a cidade gasta "pouco". Posso dizer que gasta menos do que a receita dela prevê, nos dois anos, sem explicação nos dados públicos.

**Não se aplicam (declarado):** I5, porque nenhuma contramedida mexe em preço, prazo ou conveniência de cliente; I7, porque não há horizonte acima de um ano nem ganho em dinheiro a trazer a valor presente. A `modelagem.md` não se aplica: o projeto é de diagnóstico.

### Desenho do teste (I8 a I10)

Piloto em que uma controladoria olha as cidades sinalizadas e uma amostra de não sinalizadas. **Unidade:** município. **Métrica:** parcela com achado relevante, definido antes. **Duração:** dois exercícios, para cobrir a sazonalidade orçamentária. **Guardas:** esforço por cidade e tempo de resposta. **Parada:** fixada em número de cidades, sem espiar o resultado. **Tamanho:** 38 por grupo para distinguir 20% de 50%, o que exige outros estados. **Ameaças:** contaminação (um achado muda o comportamento de vizinhos), efeito novidade e perda diferencial de cidades que não respondem. Sem aleatorizar (I10), a alternativa é comparar sinalizadas com não sinalizadas de resíduo parecido; a premissa é que o resíduo antes da triagem seja a única diferença, e ela se verifica com o histórico de 2023.

## 4. Para você explicar esta fase

**A fase em 30 segundos.** "Depois de entender que o gasto em saúde segue a receita, propus sete ferramentas de controle, com critérios escritos antes. Uma triagem separou quatro cidades que gastam bem menos do que a receita prevê, e duas delas repetem em 2023. Comparar por receita parecida lê melhor do que comparar por região. E uma ideia minha, a do ajuste de veraneio, não funcionou, e eu registrei isso."

| Pergunta que vão fazer | Resposta |
|---|---|
| Por que você não propõe gastar mais em saúde? | Gasto não mede qualidade, e o dado não mostra necessidade. As recomendações são de controle: onde olhar, como comparar e que risco vigiar. |
| Por que só 4 cidades sinalizadas? | O intervalo de previsão é de 95% e a cidade fica fora do ajuste. Quatro é pouco para decidir um piloto; por isso a proposta de ampliar para outros estados. |
| O que deu errado? | O ajuste do veraneio. Somar visitantes à população piorou o resíduo, porque a elasticidade é menor que 1. E três palpites meus erraram (Baixadas Litorâneas, folga e limite de pessoal). |
| O teste de estresse é previsão? | Não. A elasticidade entre cidades (0,68) é de cortes transversais; a de ano a ano (0,28) é a que mais se aproxima do que acontece em uma cidade. Mostro as duas. |
| Por que sem teste de campo? | Em portfólio nada se implementa. Eu desenho o teste e calculo o tamanho; o RJ sozinho não tem cidades suficientes. |

**Números para saber de cor:** 46% (menos dispersão por pares); 2 de 3 cidades se repetem de 2023 para 2024 na triagem; 0,28 contra 0,68 (elasticidade dos repasses, dentro e entre cidades); 38 cidades por grupo para o piloto.

## 5. O que ainda não sei

- Se Niterói e São Francisco de Itabapoana têm explicação legítima. Pergunta para quem acessa os livros.
- Se a elasticidade de ano a ano (0,28) é estável. Usei dois exercícios; mais anos ajudariam.
- Quanto pesa a folha de pessoal ou a dívida no gasto em saúde: o Analyze não testou. Fica para as extensões ([docs/12](../../docs/12-extensoes-depois-do-nucleo.md)).
- Se a razão entre SIOPS e Siconfi (R6) tem um valor esperado: os conceitos são diferentes.
- O que pode invalidar: dado declarado que seja retificado (B4 segue aberto); 2023 e 2024 usam as mesmas 92 cidades, então não são amostras independentes; Carmo ficou fora de 2023.

## 6. O veredito

**APROVADO pelo responsável em 24/10/2026.** O critério é a qualidade do processo, e não se as hipóteses se confirmaram.

| Critério | Veredito | Motivo |
|---|---|---|
| Critérios e palpites escritos antes | <span class="ok">OK</span> | docs/13, com data, antes da primeira conta |
| Contrafactual escrito e conta à vista, em faixas | <span class="ok">OK</span> | R1 e R4 com três cenários; R2 a R7 com a medida e o critério |
| Ponto de indiferença | <span class="ok">OK</span> | R1, R3, R4 e R5 |
| Desenho de teste com tamanho calculado | <span class="ok">OK</span> | 38 por grupo; limite do RJ declarado |
| Resultado contrário ao esperado registrado como resultado | <span class="ok">OK</span> | R3 e três palpites |
| FMEA, contorno da regra e cético | <span class="ok">OK</span> | seção 3 |
| Honestidade sobre causa | <span class="ok">OK</span> | R7 declarada descritiva; R2 declarada em parte por construção |

## 7. O próximo capítulo

**Control:** transformar as seis contramedidas que sobreviveram em plano de monitoramento: o que medir, com que limite de alerta, quem olha e o que fazer quando disparar. A R3 fica de fora. As extensões (SUS, idade em faixas, pessoal e dívida contra o gasto) só entram depois do núcleo.

## Bastidores

| Passo | Script |
|---|---|
| Critérios e palpites | `docs/13-improve-criterios.md` |
| R1 a R7: todas as contas | `scripts/30_improve_recomendacoes.py` |
| Saída completa, linha a linha | `dados_tratados/improve_saida.txt` |
| Tabelas por cidade | `dados_tratados/improve_r1_triagem.csv`, `improve_r2_pares.csv`, `improve_r3_veraneio.csv`, `improve_r4_estresse.csv`, `improve_r4_dependencia.csv`, `improve_r5_r6_siops.csv`, `improve_r7_limites.csv` |
