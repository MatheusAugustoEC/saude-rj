# A página de entrega está pronta: seis partes, 92 cidades, um comando para refazer

**Fase 6 · Entrega, Saúde fiscal do Rio de Janeiro · Siconfi 2023 a 2025 · 26/10/2026**

> [!NOTE]
> Os dados são declarados pelas prefeituras e pelo estado, e não foram auditados. Gasto em saúde por habitante não mede qualidade nem necessidade. Cidade sinalizada é cidade para olhar, não cidade com problema.

<div class="numero"><b>6 partes</b><span>numa só página estática (pagina/index.html), com 28 itens para baixar, 12 slides e 21 testes que passam</span></div>

<div class="resumo" markdown="1">

**Em três linhas.** Construí a página que você aprovou nos rascunhos: Início, Cidade, Gestor, Controle e auditoria, Como cheguei aqui e Biblioteca. Todo número vem de um arquivo do pipeline (`dados_tratados/pagina_dados.json`, gerado pelo script 35). Conferi a página rodando, em duas rodadas, e corrigi oito defeitos; o que não consegui conferir está listado abaixo.

</div>

## 1. O que foi entregue

| Parte | O que a pessoa faz |
|---|---|
| Início | Vê a posição do estado (27º de 27), a variação entre cidades (7,2×), o mapa do Brasil com seletor de indicador e ranking dos 27 estados, curiosidades e o botão de mais itens |
| Cidade | Digita ou escolhe a cidade, ou clica no mapa; compara com cidades parecidas, cidades escolhidas, estado ou mediana; troca para a visão por Região, com mapa dos 10 grupos |
| Gestor | Cidades parecidas, relação receita × gasto, simulador de repasses e receita própria, folga sobre o mínimo de 15%, repasses por região, limites da LRF, planilha .xlsx |
| Controle e auditoria | Triagem de 2023 a 2025, chegada do balanço de 2025, conferência SIOPS × Siconfi, pergunta aberta das Baixadas Litorâneas, limites fiscais |
| Como cheguei aqui | Uma tela por etapa (Definir a Kaizen), com SIPOC, mapa do processo, diagrama das causas e vereditos |
| Biblioteca | 28 itens com busca e filtros (para quem, tipo, etapa, ano), .zip com tudo, apresentação .pptx de 12 slides e citação para copiar |

**Como refazer.** `python -X utf8 scripts/35_dados_pagina.py` e depois `scripts/36_gerar_pagina.py`. Os dois entram no `run_all.py`, e o `tests/test_pagina.py` confere que os números da página são os do pipeline, que os arquivos existem e que o .zip e a planilha abrem.

## 2. O que acrescentei além do combinado

Você aprovou todas as sugestões; a lista abaixo é para ficar registrada, e você decide se alguma sai.

- Busca de cidade nas primeiras telas, e o clique no mapa que atualiza tudo.
- Cartões "Você sabia?" e o botão de curiosidades, insights e alertas em cada parte, com fonte e janela de tempo em cada item.
- O simulador de repasses e receita própria, com faixa de −50% a +50%, faixa coberta de −30% a +30% e dois modos de leitura (entre cidades e de um ano para o outro).
- Uma tela por etapa em "Como cheguei aqui", com o diagrama das causas montado a partir dos resultados (e dito assim na página).
- A visão por Região, com os mapas do Brasil e do estado do Rio desenhados a partir das malhas do IBGE (guardadas em `dados_brutos/malha_ibge_api/`, com SHA-256).

## 3. Auditoria da página rodando

Abri a página no Edge, passei por todas as seis partes, em tela larga (1280 px) e de celular (390 px), nos temas claro e escuro, e cliquei nos controles, filtros, tags removíveis e downloads.

| Rodada | O que encontrei | O que fiz |
|---|---|---|
| 1 | Erro de console: a capital se chama "Rio de Janeiro (capital)" no dado, e a busca pelo nome falhava | Busca pelo código do IBGE |
| 1 | Rótulo do Acre cortado no mapa do Brasil | Margem maior no mapa |
| 1 | Gráfico de barras gigante em tela larga | Largura máxima dos gráficos |
| 1 | Sensibilidade de 0,81 (ajuste na página) contra 0,80 no resto do projeto | O texto usa o número do pipeline; a reta é só o desenho |
| 1 | Frase "gasta −31% da mediana" | "gasta 31% abaixo da mediana" |
| 2 | Grupo "Baixada" na cor vermelha, a mesma da seleção | Trocado por âmbar; outras duas cores ajustadas |
| 2 | Menu do cabeçalho ocupava meia tela no celular | Menu em linha, com rolagem |
| 2 | Linha selecionada com contraste baixo no tema escuro | Cor do texto própria para o vermelho do tema |

A segunda rodada terminou sem achado bloqueante. Verifiquei: console sem erro, sem rolagem horizontal em 390 px, .xlsx abre (4 abas), .pptx tem 12 slides, .zip tem 27 arquivos sem nome repetido.

**O que a auditoria não cobriu (limites):**

- Não abri o .pptx no PowerPoint nem o .xlsx no Excel: só conferi a estrutura dos arquivos.
- Não testei num celular de verdade, só numa janela de 390 px.
- A paleta foi conferida com cálculo próprio de daltonismo (simulação de Machado e distância no OKLab), não com o validador oficial da skill, que precisa de Node. As 10 cores dos grupos da região têm número no mapa como segundo código, porque algumas ficam abaixo da distância ideal.
- O mapa só funciona por clique ou toque; a lista ao lado é a alternativa por teclado.
- Páginas e arquivos ainda **não foram publicados**: o GitHub Pages só entra depois do seu aval, e o teste automático do GitHub ainda não rodou lá.

## Adendo de 27/10/2026: segunda rodada de ajustes e auditoria

Depois de usar a página, o responsável pediu correções e uma auditoria completa (olhar de gestor, controlador, auditor, especialista e recrutador). Tudo foi feito e reauditado; a seção 3 acima descreve a primeira auditoria e este adendo a substitui onde houver diferença.

**Ajustes:** Início só com estados e Brasil; Cidade em modo Região com clique que escolhe a região inteira, ranking das cidades da região em cima e ranking das 8 regiões embaixo; escolha de várias cidades dentro de "Comparar com"; Gestor com filtros em cascata (Região, depois Cidade, com "Todas"), faixas de receita em reais e planilha .xlsx que segue os filtros; simulador sem a linha sobreposta, com cartões titulados e o cartão "Folga estimada no cenário"; Controle e auditoria com fonte sob cada tabela e gráfico, balanço (DCA) dito, SIOPS em "R$ 37 para cada R$ 100" (mediana 0,37) e ficha de controle por cidade ou região; Biblioteca com descrições em forma de história; tema com ícone de sol e lua, sempre abrindo no claro.

**Acrescentado além do combinado:** glossário com 15 termos, link compartilhável (estado da tela no endereço) e a troca de "base de impostos" por "base de cálculo (impostos e transferências constitucionais)". A despesa em saúde é a **empenhada** (RREO Anexo 02 e DCA I-E), e a página não a chama de liquidada.

**Auditoria automática (Edge, 1280 e 390 px, claro e escuro):** 0 achados em 60 verificações, entre elas: downloads .xlsx por região, por região mais faixa e por cidade; 27 links da Biblioteca existentes; imagens carregando; campos com rótulo; nenhum "undefined" ou "NaN" nas seis partes; console sem erro. Testes do projeto: 21 passam.

**Limites que continuam:** nada testado em celular real; .pptx e .xlsx não abertos no Office; validador oficial de paleta não rodado (precisa de Node); página ainda não publicada.

## 4. Textos que você precisa conferir

- A apresentação .pptx é simples (título, um número, uma frase e, no primeiro slide, um gráfico). Os 12 títulos são os que você aprovou.
- O diagrama das causas e a tabela do Improve foram **montados a partir dos resultados** das fases; a página diz isso. Não há 5 porquês, Pareto nem Ishikawa feitos antes.
- A citação sugerida usa o nome do usuário do GitHub (MatheusAugustoEC). Se preferir o seu nome completo, é uma linha no script 36.

## 5. Para o tollgate

1. A página está como você imaginou? Algo a tirar da lista da seção 2?
2. Posso seguir para a **Banca** (revisão independente, skill banca-dmaic) antes de qualquer publicação?
3. Quando quiser publicar, me avise: eu listo os arquivos, e você dá o aval do primeiro push.

**Marco 3.** A página é um marco: posso preparar um rascunho de post para o LinkedIn quando você quiser.
