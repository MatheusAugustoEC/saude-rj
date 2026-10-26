# Plano de controle: como acompanhar sem perder o rumo

Escrito em 25/10/2026, na fase Control. Serve a quem trabalha com controle, auditoria, finanças e gestão, e também a qualquer pessoa que queira acompanhar as contas da saúde da sua cidade. Nada aqui foi implementado em órgão nenhum: é uma especificação.

**Ressalvas em todas as linhas:** os dados são declarados pelas prefeituras e pelo estado, e não foram auditados. Gasto em saúde não mede qualidade do atendimento. Uma cidade que dispara um alerta é uma cidade para olhar, não uma cidade errada.

## 1. O que acompanhar, com que limite e o que fazer (C1)

| Id | O que se acompanha | De onde vem o dado | Com que frequência | Quando soa o alerta | Quem olha (papel) | O que fazer |
|---|---|---|---|---|---|---|
| R1 | Cidades cujo gasto em saúde por habitante fica abaixo do que a receita prevê | Siconfi (balanço anual e relatório bimestral) e população do IBGE | Uma vez por ano, quando o balanço anual estiver maduro | Gasto abaixo do intervalo de previsão de 95%, calculado sem a própria cidade, e resíduo negativo no ano anterior | Controladoria interna, tribunal de contas | Pedir a explicação à secretaria antes de abrir auditoria. Comparar com o balanço anual |
| R2 | Comparação de cada cidade com outras de receita parecida | Os mesmos | Anual | Não é alerta: é a régua de leitura. Cinco faixas fixas por receita por habitante | Gestão, conselho de saúde | Ler cada cidade contra os pares da faixa, e não contra a região |
| R4 | Dependência de repasses | Relatório bimestral (receitas) | Bimestral, lido uma vez por ano | Mais de 90% da receita vindo de repasses | Gestão, finanças | Rodar o cenário de queda de 10%, 20% e 30% dos repasses, com as duas elasticidades |
| R5 | Folga sobre o mínimo de 15% da saúde | SIOPS (Ministério da Saúde) | Anual, conforme a publicação do ano | Folga menor que 3 pontos percentuais (atenção); menor que 1 ponto (alta) | Controladoria, finanças | Acompanhar o ano seguinte; checar se a folga é estrutural ou de um ano |
| R6 | Razão entre o que o SIOPS diz aplicar e o gasto do Siconfi | SIOPS e Siconfi | Anual | Razão fora de mediana ± 2 desvios absolutos | Auditoria | Tratar como pergunta de conciliação; nunca como alarme sozinho |
| R7 | Pessoal, dívida e restos a pagar contra os limites da Lei de Responsabilidade Fiscal | Relatório de gestão fiscal e relatório bimestral | Quadrimestral e bimestral, lido por ano | Pessoal acima do limite prudencial; dívida a partir de 80% do limite; restos a pagar no quartil superior | Controladoria, finanças | Conferir se o dado é atípico antes de concluir. Marcar entes com dado atípico |

A R3 (ajuste de veraneio) não entra: o teste de 2025 confirmou que a conta não funciona.

## 2. Quando o dado fica pronto, e o que fazer se atrasar (C13)

| Dado | Quando fica completo, na prática | O que o acompanhamento faz |
|---|---|---|
| Balanço anual (DCA) | De 30/01 a 16/10 do ano seguinte (2025). Quatro das 86 cidades do recorte entregaram depois de 31/08/2026 | Marcar o ano como **em atualização** se menos de 95% das cidades entregaram, ou se uma cidade em alerta ainda não entregou. Não interpretar o resultado desse ano |
| Relatório bimestral (RREO) | 89 de 92 cidades chegaram ao 6º bimestre de 2025; três ficaram no 5º ou no 2º | Usar só as cidades com 6º bimestre. Listar as outras pelo nome |
| SIOPS | Segue a publicação do Ministério da Saúde | Declarar o ano de referência junto de cada número |
| População do IBGE | A estimativa de 2023 não foi publicada | Declarar quando houver interpolação |

**Regra de ouro:** período ainda incompleto aparece **marcado**, não interpretado. Cidade sem dado é uma informação (aparece como "sem dado"), e não é tratada como zero.

## 3. Quando recalcular os limites (C3)

Os limites desta tabela só mudam se o processo mudar de fato (por exemplo, nova regra de repasse do SUS ou nova lei), e nunca para "limpar" um alerta incômodo. Cada mudança entra neste arquivo com data e motivo.

## 4. O que invalidaria esta análise (C9)

| Evento | O que muda | Quando revisar |
|---|---|---|
| Nova regra de repasses do SUS (piso, forma de transferência) | A relação entre repasses e gasto (R4) | Ao ser publicada |
| Mudança na Lei Complementar 141 (os 15%) ou nos limites da Lei de Responsabilidade Fiscal | R5 e R7 | Ao ser publicada |
| Mudança nos anexos ou no plano de contas do Siconfi | Os testes automáticos falham | No mesmo dia, pelo teste |
| Novo Censo ou nova estimativa de população | O denominador de tudo | Ao ser divulgado |
| Troca de mandatos (2025 e 2029) e anos de eleição | Prioridades de gasto mudam. Em 2025 as mudanças já podem estar nos dados | Todo ano de início de mandato |
| Queda forte de royalties ou receitas do petróleo | Receita por habitante das cidades que dependem delas | Quando o preço do petróleo variar muito |
| Retificação de relatório já publicado | Resultados de anos fechados | Anual (hoje, B4 aberto: não sei qual versão a API devolve) |
| Mudança de quem atende a população (hospital federal ou estadual na cidade) | O gasto municipal por habitante, em especial na capital | Ao saber da mudança |

**Revisão regular:** uma vez por ano, quando o balanço anual estiver maduro (por volta de outubro).

## 5. Gatilho de revisão da triagem (C10, versão simples)

Não existe aqui um modelo de previsão em produção, mas a triagem usa uma regressão. Ela deve ser refeita se:
- a elasticidade da receita sair da faixa de **0,60 a 0,95** (valores de 2023, 2024 e 2025: 0,80, 0,81 e 0,74); ou
- o poder de explicação do modelo com a receita total cair abaixo de **0,70** (hoje, cerca de 0,80); ou
- mudar a lista de cidades (fusão, criação de município) ou o ano-base da população.

## 6. O que vira padrão reutilizável (C11)

| Padrão | Para que serve | Onde aplicar depois |
|---|---|---|
| Decomposição do gasto por habitante em receita por habitante e fatia | Separar "tem pouco" de "dedica pouco" | Outros estados e outras funções (educação) |
| Triagem com previsão sem a própria cidade | Achar quem destoa sem que a cidade puxe a régua | Regiões metropolitanas de outros estados |
| Comparação por faixas de receita (pares) | Ler cada cidade contra quem se parece | Qualquer indicador por habitante |
| Registro das previsões antes de abrir o dado novo | Evitar ajustar a história depois | Todo recorte de confirmação |
| Teste de acesso datado a cada fonte, com plano B | Não depender de fonte que cai | Todo projeto com dado público |
| Marcar o período ainda incompleto | Evitar alarme falso | Qualquer série com atraso de registro |

## 7. O que este plano não faz

Não substitui auditoria nem decide se um gasto está certo. Não mede resultado de saúde. Não foi testado em órgão nenhum: é uma proposta, com os limites vindos dos dados de 2023 a 2025 do Rio de Janeiro.
