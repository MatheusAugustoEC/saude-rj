# Define — Saúde fiscal do Estado do Rio de Janeiro

Status: **em andamento** (5 Porquês e checagem de viabilidade concluídos; SIPOC, mapa do processo e declaração do problema pendentes).
Data do registro: 20/10/2026.

## Visão geral do projeto (versão simples)

### O ponto central

> **Como o Rio de Janeiro e os seus municípios estão gerindo o dinheiro da saúde, e onde as contas públicas estão apertadas?**

A pergunta nasce dos 5 Porquês: a suspeita de contas apertadas, vinda do noticiário, será testada com dados públicos.

**Status: provisório.** Esta pergunta, os três indicadores sugeridos (gasto em saúde por habitante, percentual da receita em saúde, peso de pessoal na receita) e o desenho do painel vieram dos 5 Porquês e de uma checagem de viabilidade (o dado existe e chega), **não de uma exploração dos dados**. Nenhum valor das contas foi examinado ainda. A análise exploratória (EDA) vai confirmar, ajustar ou descartar esses itens antes de o Define ser fechado.

### O papel de cada fonte

| Fonte | Papel | Quando entra |
|---|---|---|
| Tesouro Nacional (Siconfi) | **É o núcleo do projeto.** Fornece as contas: receita, gasto com pessoal, gasto com saúde | Agora |
| IBGE | Contexto: população por idade e saneamento, para não comparar cidades desiguais como se fossem iguais | Módulo futuro, opcional |
| SUS | Indicadores de oferta, como leitos. Ainda não verificado | Módulo futuro, talvez |

O projeto está completo só com o Siconfi. IBGE e SUS são extensões opcionais, que se encaixam depois pelo código do estado ou do município.

### Como será apresentado

Uma página única (painel) com três partes:
1. O RJ comparado com os outros estados (todos visíveis, o RJ em destaque).
2. Os 92 municípios do RJ, nos mesmos indicadores.
3. Método e limites: de onde vêm os números e o que eles **não** dizem (por exemplo, a qualidade do atendimento).

Também haverá uma planilha para baixar e um post no LinkedIn a cada marco.

### Onde os dados ficam guardados

- A API é a fonte. Os arquivos em `dados_brutos/` são a nossa cópia, gravada por script, com a data da coleta.
- Hoje estão salvos só os catálogos (quem entregou o quê no Siconfi; quais tabelas do IBGE existem).
- **Os valores das contas ainda não foram baixados.** A coleta acontece no Measure, depois que a pergunta estiver fechada. Haverá dois arquivos: os dados brutos, como vieram, e uma tabela limpa em CSV.
- A origem de cada dado é registrada em `docs/02-fontes-de-dados.md`.

### Limites declarados

- O Siconfi mostra **quanto se gasta**, não a **qualidade do atendimento**. O painel não classifica "melhor saúde".
- O piso de gasto em saúde e o limite de pessoal da LRF **não estão confirmados** na lei. Não serão usados antes disso.

## 1. 5 Porquês

Respostas do Matheus, registradas como ele as deu. São hipóteses, não fatos.

| # | Pergunta | Resposta registrada |
|---|---|---|
| 1 | Por que o projeto é sobre o RJ? | É o estado onde ele reside e quer entender as condições financeiras e fiscais do seu estado como cidadão. |
| 2 | Por que isso importa ao cidadão? | A condição fiscal e financeira reflete na entrega de serviços e infraestrutura de saúde, o que impacta a população fluminense. |
| 3 | Por que as contas podem não estar saudáveis? | Notícias recorrentes de falta de insumos, medicamentos, profissionais e infraestrutura nas unidades de saúde. Quer testar a suspeita com dados em vez de aceitá-la pela mídia. |
| 4 | Qual a causa mais provável da falta de recursos? | Receita comprometida, que levaria a atraso de pagamentos e execução lenta. Receita insuficiente é considerada improvável, porque o estado é "rico". |
| 5 | Por que a receita estaria comprometida? | Pelo serviço da dívida, ligado à recuperação fiscal. O que mais ocupa a receita é desconhecido e será investigado. |

### Hipóteses a testar

| Nível | Hipótese | Situação |
|---|---|---|
| Sintoma | Falta de insumos, profissionais e infraestrutura na saúde (fonte: mídia) | Fora do alcance do Siconfi |
| Causa provável | Receita comprometida por despesas obrigatórias, em especial dívida | A testar |
| Desdobramento | Atraso de pagamentos e execução lenta | A testar |
| Descartada pelo Matheus | Receita insuficiente | A verificar |
| Desconhecido | O que mais consome a receita | A investigar |

### Ressalvas levantadas ao longo dos Porquês

- **Fiscal e financeiro são coisas diferentes.** Fiscal é o equilíbrio das contas no tempo (receita, despesa, dívida, limites da LRF). Financeiro é caixa e liquidez. É preciso escolher qual será medido.
- **"Estado rico" não é receita suficiente.** PIB da economia não é o mesmo que folga na receita do governo estadual.
- **O elo entre contas e qualidade do serviço de saúde é hipótese.** O Siconfi mostra quanto foi gasto, não a qualidade nem a falta de insumos.
- **Os caminhos 3 e 4 (execução lenta, atraso de pagamento) podem ser consequência da receita comprometida, mas também podem existir sozinhos** (falha de processo).

## 2. Checagem de viabilidade na API do Siconfi

Consulta feita em 20/10/2026 na API oficial (`apidatalake.tesouro.gov.br/ords/siconfi/tt/`). **As consultas foram feitas de forma avulsa e ainda não estão num script reexecutável. O script e os dados brutos serão salvos em `scripts/` e `dados_brutos/`.**

### Confirmado

- A API responde sem chave. O catálogo OpenAPI oficial existe em `/ords/siconfi/open-api-catalog/tt/`.
- Paginação: 5.000 linhas por chamada (`limit`), com `hasMore` indicando mais páginas.
- Os parâmetros que a especificação chama de "path" funcionam como query string.
- O governo estadual do RJ entregou em 2024: RREO (6 bimestres), RGF (3 quadrimestres), DCA e MSC mensal.
- Retornaram valores para o estado em 2024: RREO Anexo 02 (2.021 linhas), RGF Anexo 01 (214 linhas), DCA Anexo I-E (577 linhas).
- A lista de entes tem 92 municípios do RJ.

### Armadilhas

1. Em `/entes`, o estado é o ente `33`, com `uf = 'BR'` e esfera `E`. Filtrar `uf == 'RJ'` traz só os municípios. Dentro de `/rreo`, `/rgf` e `/dca` o mesmo ente vem com `uf = 'RJ'`.
2. ~~Os textos vêm com a acentuação quebrada.~~ **Corrigido em 20/10/2026:** as 92 respostas de `/extrato_entregas` decodificaram em UTF-8 sem erro. A acentuação quebrada que apareceu antes veio do terminal do Windows, não da API. Ao imprimir no terminal, a tela pode mostrar "�"; gravar em arquivo UTF-8 resolve.
3. O endpoint `/anexos-relatorios` é lento e deu timeout em duas tentativas. A lista oficial completa de anexos não foi obtida.

### O que os dados permitem responder

| Pergunta | Fonte provável | Situação |
|---|---|---|
| Gasto com pessoal | RGF Anexo 01 | Dados confirmados |
| Orçado e empenhado por função, inclusive Saúde | RREO Anexo 02, DCA I-E | Dados confirmados; falta checar a linha "Saúde" e as demais colunas |
| Suficiência da receita | RREO Anexo 01 | Não testado |
| Peso da dívida | RGF Anexo 02 | Não testado |
| Restos a pagar e atrasos | RREO Anexo 07 | Não testado |
| Limites da LRF | Lei oficial | **Não confirmado** |
| Falta de medicamento ou profissional | — | O Siconfi não responde |

### Recuperação fiscal

Fontes consultadas indicam adesão em 2017, acordo em 2022 para permanecer no regime e, em abril de 2025, manifestação do Tesouro sobre excluir o RJ, com decisão do STF mantendo o estado e suspendendo sanções. **O status em outubro de 2026 não está confirmado.** Os valores de dívida citados nas matérias vêm de fonte secundária e não serão usados.

Fontes:
- https://forbes.com.br/forbes-money/2022/06/estado-do-rio-fecha-acordo-com-a-uniao-para-permanecer-no-regime-de-recuperacao-fiscal/
- https://www.poder360.com.br/poder-economia/rj-deve-ser-excluido-do-regime-de-recuperacao-fiscal-diz-ceron/

## 3. Unidade de análise

**Decisão revisada (21/10/2026): o núcleo passa a ser o estado do RJ comparado com os 26 outros estados, mais o detalhe dos 92 municípios.** A decisão inicial (20/10/2026) tinha sido C, só os municípios. O Matheus propôs ampliar para o estado e os demais estados, porque a comparação entre estados dá o referencial ("em relação a quê?") e retoma a hipótese dos 5 Porquês (dívida e recuperação fiscal, que são do estado). A recomendação do analista era A (só o estado). A decisão foi do Matheus.

Registro da decisão original (C): **Motivo dele:** poder comparar as cidades do estado entre si e ver como cada uma está.

Consequência: a hipótese dos 5 Porquês (dívida do estado e recuperação fiscal) é do governo estadual e **não se aplica diretamente aos municípios**. Ela precisa ser reformulada para o nível municipal. Isso está pendente.

### Viabilidade para os 92 municípios (script `scripts/01_viabilidade_municipios.py`)

Dados brutos: `dados_brutos/extrato_entregas_municipios_rj_2024.json`. Exercício 2024.

- 92 de 92 consultas com sucesso, 0 falhas.
- Os 92 municípios têm ao menos um RREO, um RGF e uma DCA listados em 2024. Nenhum município ficou sem entrega.
- Existem versões **"Simplificado"** do RREO e do RGF. Isso indica que alguns municípios entregam relatórios com outros anexos. **A regra de quem pode entregar a versão simplificada não está confirmada.**
- O campo `status_relatorio` traz os códigos `HO` e `RE`. **O significado dos códigos não está confirmado.**
- Isso mostra que os relatórios foram **entregues**. Não mostra que o **conteúdo** é completo e consistente. Isso é tarefa do Measure.

## 4. Hipótese reformulada para o nível municipal (superada em 22/10/2026: ver 4.1 a 4.3)

**Decisão do Matheus (20/10/2026): Opção 1, com a Opção 2 como etapa futura.**

- **Pergunta central (Opção 1):** quais municípios fluminenses cumprem o mínimo de saúde e como isso se compara ao peso de pessoal na receita?
- **Etapa futura (Opção 2):** quais municípios estão em alerta nos dois critérios ao mesmo tempo (cruzamento dos dois indicadores da Opção 1).

Ressalvas que seguem abertas:
- O piso de gasto em saúde dos municípios e o limite de pessoal da LRF **não estão confirmados** na fonte oficial. Não serão usados antes disso.
- Parte do gasto com pessoal é com profissionais de saúde, então os dois indicadores provavelmente se sobrepõem. A sobreposição precisa ser confirmada.
- O RREO pode ter um anexo específico de saúde ("Anexo 12", ainda não testado).
- A pergunta original "sobra pouco para a saúde?" foi abandonada, porque a saúde também é despesa com piso obrigatório.

## 4.1 Decisões de 22/10/2026

- **Cliente do SIPOC:** o cidadão curioso, do RJ ou de fora. Profissionais de compliance, controles e auditoria e recrutadores são o **público-alvo da divulgação**, mas **não** aparecem como clientes no SIPOC.
- **Mudança de foco:** o Matheus não considera interessante a hipótese de "receita comprometida" como pergunta central e prefere trabalhar **quem gasta mais em saúde**. A hipótese dos 5 Porquês passa a ser uma **possível explicação** (um X candidato) a investigar no Analyze, e não a pergunta do projeto.
- **A esclarecer:** "gasta" ou "investe"? Em contabilidade pública, **investimento** é a despesa de capital (obras e equipamentos), que **não foi coletada**. O Siconfi aqui traz o gasto total na função Saúde.
- **Post do Marco 1:** formato em aberto (um post com imagens ou dois). O Matheus quer o que der mais alcance.
- **Regiões:** entram na fase **Analyze**, e não no Marco 1.
- **SIPOC:** as seis etapas foram aprovadas (declaração, publicação, coleta, conferência e exploração, cálculo e comparação, publicação do resultado). Imagens em `imagens/sipoc.png` e `imagens/mapa_processo.png` (PNG e SVG), em formato **horizontal** (1920 x 1080) e **coloridas** (uma cor por coluna do SIPOC e uma por etapa do mapa), refeitas em 22/10/2026 a pedido do Matheus. O mapa usa as **mesmas seis etapas** do SIPOC, em duas raias ("terceiros" e "nós"), com a decisão "Dado completo e coerente?" e três pontos de controle: **C1** conferência e exploração (etapa 4), **C2** cálculo e comparação com fórmulas explícitas conferidas (etapa 5) e **C3** publicação com ressalva (etapa 6). Gerador: `scripts/12_gerar_imagens_define.py`.

## 4.2 Pergunta central, Y e X (aceitos pelo Matheus em 22/10/2026)

> **Quem gasta mais em saúde, por habitante e como parte do orçamento, entre os estados e os municípios do RJ, e o que explica a diferença?**

| Papel | Indicador | Observação |
|---|---|---|
| **Y principal** | Gasto em saúde por habitante (R$ por habitante) | É o que as pessoas perguntam. Acompanha de perto a receita por habitante (0,80 nos estados e 0,82 nos municípios) |
| **Y2** | Fatia da despesa total destinada à saúde (%) | Mede prioridade. Nos municípios anda no sentido contrário da receita (−0,33) |
| **X candidatos** (para o Analyze) | Receita por habitante, peso da folha de pessoal, dívida, restos a pagar, população, região | A hipótese dos 5 Porquês (receita comprometida) vira um X a investigar, não a pergunta do projeto |

O gasto absoluto (R$ totais) não serve para comparar, porque o ente maior sempre ganharia. Usamos "gasta", e não "investe": investimento em contabilidade pública é despesa de capital, que não foi coletada. Toda comparação vem com a ressalva de que **gasto não é qualidade**.

## 4.3 Declaração do problema (APROVADA pelo Matheus em 22/10/2026)

Em 2024, o gasto em saúde por habitante variou muito entre os municípios do RJ e entre os estados, e não existe hoje uma comparação pública simples, conferida e com a ressalva certa que permita a um cidadão ver quem gasta mais e entender a diferença.

| Elemento | Conteúdo |
|---|---|
| **O quê (Y)** | Gasto em saúde por habitante (despesa empenhada na função Saúde ÷ população). Y2: fatia da despesa total destinada à saúde |
| **Onde** | Os 27 estados (com o DF) e os 92 municípios do RJ |
| **Quando** | Exercício de 2024 |
| **Tamanho (linha de base da EDA)** | Entre os municípios do RJ: de R$ 1.026 a R$ 6.853 por habitante (6,7 vezes), sem contar 4 municípios com dado em checagem; mediana de R$ 2.379. Entre os estados: de R$ 628 (RJ) a R$ 2.765 (Amapá); mediana de R$ 975 |
| **Agravantes (fatos, sem causa)** | O estado do RJ aparece com UF "BR" no cadastro do Siconfi; entes declaram o mesmo dado de formas diferentes (limite de dívida como "120" em vez de reais); um relatório traz dois totais de despesa diferentes; e o gasto por habitante acompanha a receita por habitante, então sozinho não mostra prioridade nem qualidade |
| **Dentro do escopo** | Comparação do RJ com os outros 26 estados e dos 92 municípios entre si, com Siconfi 2024 |
| **Fora do escopo** | Qualidade do atendimento; mínimo legal de saúde (SIOPS, fora do ar em 21/10/2026); módulos IBGE e SUS; regiões (entram no Analyze) |
| **Objetivo** | Descrever quem gasta mais e menos, testar no Analyze o que explica a diferença e recomendar como acompanhar isso (Improve e Control), com cada número rastreável e a ressalva junto |

Observação: é um projeto de diagnóstico com dados públicos, então **não há meta numérica**. A meta é de qualidade da resposta: cada número com origem registrada e nenhuma conclusão além do que os dados sustentam.

## 5. Pendências do Define

- [x] Unidade de análise: estado do RJ comparado com os outros 26 estados, mais o detalhe dos 92 municípios (revisada em 21/10/2026).
- [x] Verificar o catálogo do IBGE (ver `docs/02-fontes-de-dados.md`).
- [x] Reformular a hipótese para o nível municipal (Opção 1).
- [x] Salvar o script de checagem e os dados brutos (municípios).
- [ ] Confirmar o significado dos códigos `HO`/`RE` e a regra do relatório "Simplificado".
- [ ] Testar RREO Anexo 01, RGF Anexo 02, RREO Anexo 07 e a linha "Saúde".
- [ ] Confirmar os limites da LRF na lei.
- [ ] Confirmar a situação atual do RJ na recuperação fiscal.
- [ ] SIPOC.
- [ ] Mapa do processo (com imagem).
- [ ] Declaração do problema.
