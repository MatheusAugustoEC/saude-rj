# Registro de fontes de dados

Regra do projeto: toda coleta de dado entra neste registro, com origem, data, script e arquivo bruto, para que qualquer pessoa consiga conferir de onde veio cada número.

Última atualização: 20/10/2026.

## 1. Fontes oficiais usadas

### 1.1 Siconfi: API de dados abertos do Tesouro Nacional

| Item | Registro |
|---|---|
| Órgão | Secretaria do Tesouro Nacional (governo federal) |
| Endereço da API | https://apidatalake.tesouro.gov.br/ords/siconfi/tt/ |
| Documentação oficial | https://apidatalake.tesouro.gov.br/docs/siconfi/ (a página carrega por JavaScript); catálogo OpenAPI: https://apidatalake.tesouro.gov.br/ords/siconfi/open-api-catalog/tt/ |
| Acesso | Público, sem chave |
| Coletado em | 20/10/2026 |
| O que foi extraído | Lista de entes (`/entes`); extrato de entregas de 2024 dos 27 estados e dos 92 municípios do RJ (`/extrato_entregas`); **valores de 2024** do RREO (Anexos 01, 02 e 07) e do RGF (Anexo 01, por Poder, e Anexo 02, dívida) para os 27 estados e os 92 municípios do RJ (`/rreo`, `/rgf`) |
| Scripts | `scripts/01_viabilidade_municipios.py` (extrato dos 92 municípios); `scripts/04_coleta_valores.py` (valores); `scripts/05_conferencia_coleta.py` (conferência); `scripts/06_pessoal_por_poder.py` (pessoal por Poder); `scripts/07_viabilidade_divida_restos.py` (campos de dívida e restos a pagar) |
| Arquivos brutos | `dados_brutos/extrato_entregas_municipios_rj_2024.json`; `dados_brutos/siconfi_rreo_2024.csv`; `dados_brutos/siconfi_rgf_2024.csv`; `dados_brutos/siconfi_chamadas_2024.csv` (registro de cada chamada); `dados_brutos/siconfi_extrato_estados_2024.json`; `dados_brutos/siconfi_anexos_relatorios.json` |
| Credibilidade | Fonte primária oficial: são os dados que os próprios entes entregam ao Tesouro. Os valores refletem o que cada ente declarou. |
| Limitações | O estado em `/entes` tem `uf = 'BR'`. O DF é cadastrado com esfera `D`, mas as consultas de RREO e RGF só o encontram com `E`. O catálogo `/anexos-relatorios` lista os anexos do QDCC e da DCA, **não** os do RREO completo (ele deu timeout em duas tentativas e depois respondeu normalmente: falha intermitente). Os **Anexos 08 e 12 do RREO voltam vazios** para o estado e para a capital do RJ; o motivo não está confirmado. Os códigos de status `HO` e `RE` e a regra dos relatórios "Simplificado" não estão confirmados. 12 dos 92 municípios entregam RREO e RGF simplificados, e a comparabilidade desses relatórios com os normais ainda não foi examinada. |

### 1.2 IBGE: API de dados agregados (SIDRA)

| Item | Registro |
|---|---|
| Órgão | Instituto Brasileiro de Geografia e Estatística (IBGE) |
| Endereço da API | https://servicodados.ibge.gov.br/api/v3/agregados |
| Acesso | Público, sem chave. A API pode devolver o JSON comprimido (gzip), e o script trata isso. |
| Coletado em | 20/10/2026 |
| O que foi extraído | Catálogo de pesquisas e tabelas (70 pesquisas, 9.344 tabelas); metadados de 393 tabelas candidatas; lista de localidades de tabelas selecionadas, para conferir a cobertura no RJ |
| Scripts | `scripts/02_catalogo_ibge.py` (catálogo e metadados); `scripts/03_verificacao_niveis_ibge.py` (cobertura real no RJ) |
| Arquivos brutos | `dados_brutos/ibge_catalogo_agregados.json`, `dados_brutos/ibge_candidatas_metadados.json`, `dados_brutos/ibge_candidatas_resumo.tsv`, `dados_brutos/ibge_cobertura_rj.json` |
| Credibilidade | Fonte primária oficial. Até aqui foi extraído **o catálogo (quais tabelas existem)**, não os valores das tabelas. |
| Limitações | O metadado diz que o nível "município" existe, mas isso **não garante cobertura de todos os municípios**. Por isso foi feita a verificação de cobertura (seção 3). |

## 2. Fontes consultadas e **não** usadas como dado

Estas fontes serviram de pista. Nenhum número delas entra no projeto. Todo número será recalculado a partir de fonte primária.

| Fonte | O que informou | Situação |
|---|---|---|
| Forbes, "Estado do Rio fecha acordo com a União para permanecer no regime de recuperação fiscal" (2022) https://forbes.com.br/forbes-money/2022/06/estado-do-rio-fecha-acordo-com-a-uniao-para-permanecer-no-regime-de-recuperacao-fiscal/ | O RJ aderiu ao regime em 2017 e fechou um acordo em 2022 | Imprensa. Pista, não confirmado em fonte oficial |
| Poder360, "RJ deve ser excluído do Regime de Recuperação Fiscal, diz Ceron" https://www.poder360.com.br/poder-economia/rj-deve-ser-excluido-do-regime-de-recuperacao-fiscal-diz-ceron/ | Tesouro falou em excluir o RJ (abril de 2025); o STF mandou mantê-lo | Imprensa. Status atual (out/2026) **não confirmado** |
| Nota técnica da Câmara Municipal de Belo Horizonte https://www.cmbh.mg.gov.br/sites/default/files/publicacoes/2026/04/ar_nt_019_2026.pdf | Piso municipal de saúde de 15% (LC 141/2012) | Fonte secundária. A lei oficial **ainda precisa ser lida** antes de usar o número |
| Fiocruz, UNA-SUS, SciELO, gov.br/saude (páginas sobre DATASUS, SIOPS e mortalidade) | Existência de bases do SUS por município (SIM, SINASC, CNES, SIOPS) | Pista para o módulo SUS. Nada verificado nas bases oficiais |
| SIOPS, Sistema de Informações sobre Orçamentos Públicos em Saúde (Ministério da Saúde). Página: https://www.gov.br/saude/pt-br/acesso-a-informacao/siops; consultas: http://siops.datasus.gov.br/ | Sistema público que acompanha a aplicação mínima em saúde (indicador da EC 29 / LC 141/2012). Os dados são **declaratórios**: cada ente informa. A página lista seções "Indicadores", "Publicações", "Demonstrativos e Dados informados" e "Downloads dos sistemas" | **Candidata** para o mínimo legal de saúde (o Anexo 12 do Siconfi vem vazio). **Verificação de 21/10/2026, parcial.** Confirmado pelas páginas oficiais do gov.br: o SIOPS tem o "Demonstrativo da Saúde - RREO" e o "Cálculo do % aplicado em Saúde conforme LC 141/2012" (dados a partir de 2013), para municípios (`http://siops.datasus.gov.br/rel_perc_LC141.php?e=2`) e para estados e DF (`...?e=1`). Todos são **consultas interativas na web**: as páginas do gov.br não oferecem arquivo para baixar nem API. **Não confirmado:** cobertura dos 92 municípios e dos 27 estados, e se a consulta permite exportar. **Não foi possível testar o acesso:** o servidor `siops.datasus.gov.br` não respondeu a partir deste computador (porta 80 com tempo esgotado; o site do gov.br e outras páginas do Ministério abrem normalmente), e a ferramenta de leitura de páginas recebeu conexão recusada. Motivo desconhecido. **O Matheus também não conseguiu abrir `siops.datasus.gov.br` no navegador (nem em http nem em https), em 21/10/2026**, o que indica servidor fora do ar ou bloqueado, e não problema só deste computador. Nenhuma rota alternativa foi confirmada (o hotsite do Conecta SUS citado pelo governo de Goiás não pôde ser lido, e a busca não achou o dado em outro portal). Fonte secundária (material da UNA-SUS: https://ares.unasus.gov.br/acervo/html/ARES/3806/1/O%20que%20%c3%a9%20e%20como%20funciona%20a%20alimenta%c3%a7%c3%a3o%20do%20SIOPS.pdf) diz que o SIOPS gera o Anexo 12 do RREO, o que é compatível com o Anexo 12 vir vazio no Siconfi, mas não confirma isso. Teste de acesso reexecutável: `scripts/08_teste_acesso_siops.py` (resultado em `dados_brutos/siops_teste_acesso.csv`) |

## 3. IBGE: o que a verificação mostrou (módulo futuro)

Verificação feita por script em 20/10/2026. A coluna "RJ" conta os municípios do estado que a tabela realmente lista.

| Tabela | Conteúdo | Estados | Municípios (Brasil) | Municípios do RJ |
|---|---|---|---|---|
| 6579 | Estimativas de População (2001 a 2026) | 27 | 5.571 | **92** |
| 10157 | Censo 2022: população por sexo e grupos de idade | 27 | 5.570 | **92** |
| 6803 | Censo 2022: água (ligação à rede geral) | 27 | 5.570 | **92** |
| 6805 | Censo 2022: tipo de esgotamento sanitário | 27 | 5.570 | **92** |
| 1300 | Saneamento Básico 2008 (tratamento de esgoto) | 27 | 5.564 | 92 (dado de 2008) |
| 4938 e 4949 | PNS 2013 a 2019: plano de saúde | 27 | **27** | **1** (só a capital) |
| 7358 | Projeção da População 2018 | 27 | 0 | 0 (só estados) |
| 216 | Assistência Médico-Sanitária: leitos (1976 a 2005) | 0 | 0 | 0 (sem cobertura geográfica, dados até 2005) |

**Leitura:**
- **População por idade e saneamento (Censo 2022)** cobrem os 27 estados e os 92 municípios do RJ. São os melhores candidatos para o módulo IBGE.
- **PNS** (saúde) só chega ao estado e às capitais. Serve para comparar estados, não para detalhar os 92 municípios.
- **Leitos pelo IBGE** estão desatualizados (até 2005) e não servem. Leitos precisariam vir do SUS (CNES), ainda não verificado.
- O valor das tabelas **ainda não foi baixado**. Foi verificado que elas existem e quem elas cobrem.

## 4. Divisão regional do estado: tentativas de 22/10/2026

| Fonte | O que foi confirmado | O que não foi |
|---|---|---|
| Relatório do CEPERJ sobre o PIB municipal (https://projetos.ceperj.rj.gov.br/wp-content/uploads/2024/02/relatorio_pib_municipal_0.pdf), lido só pelo trecho que a busca na web devolveu | O estado divide os 92 municípios em **8 Regiões de Governo**: Centro-Sul Fluminense, Médio Paraíba, Costa Verde, Metropolitana, Noroeste Fluminense, Norte Fluminense, Serrana e Baixadas Litorâneas. A divisão foi oficializada em 1987 pela Secretaria de Planejamento (SECPLAN) | **A lista de municípios de cada região.** O servidor do CEPERJ recusou a conexão |
| API de localidades do IBGE (`servicodados.ibge.gov.br/api/v1/localidades/estados/33/municipios`) | Nada | Tempo esgotado em 22/10/2026, embora o mesmo domínio tenha respondido em 21/10/2026 (API de agregados) |
| Trabalhos acadêmicos sobre a Baixada Fluminense (busca na web, fontes secundárias) | **Não há definição oficial consensual.** O núcleo citado são 6 municípios (Belford Roxo, Duque de Caxias, Mesquita, Nilópolis, Nova Iguaçu, São João de Meriti); outros entram em alguns recortes | A lista oficial de 13 municípios que uma fonte atribui ao governo estadual |

### 4.1 Lista de municípios por região (fornecida pelo Matheus em 22/10/2026)

| Item | Registro |
|---|---|
| Arquivo | `dados_brutos/municipios_rj_ceperj.csv` (colunas: município, região de governo) |
| Instituição de origem | Centro de Estatísticas, Estudos e Pesquisas (CEEP), órgão vinculado à Fundação CEPERJ (Governo do Estado do Rio de Janeiro), obtidos diretamente pelo Matheus |
| Data de acesso | 22/10/2026 (data em que o Matheus forneceu o arquivo). Por decisão do Matheus, a origem é citada pela instituição, sem link |
| Conferência feita por nós | 92 linhas, 92 de 92 municípios casam com o Siconfi (nomes idênticos), sem duplicados e sem vazios. Distribuição: Metropolitana 22, Noroeste Fluminense 13, Serrana 13, Centro-Sul Fluminense 11, Médio Paraíba 11, Baixadas Litorâneas 10, Norte Fluminense 9, Costa Verde 3 |
| O que **não** foi conferido | O arquivo contra a publicação original, porque o servidor do CEPERJ estava fora do ar. A origem é a declarada pelo Matheus |
| Credibilidade | Fonte primária oficial do estado (CEPERJ/CEEP), por declaração do Matheus; origem registrada pela instituição |

### 4.2 Malha municipal do IBGE (baixada pelo Matheus em 22/10/2026)

| Item | Registro |
|---|---|
| Arquivos | `dados_brutos/malha_rj/RJ_Municipios_2024.shp/.dbf/.shx/.prj/.cpg` |
| Instituição de origem | Instituto Brasileiro de Geografia e Estatística (IBGE), Malhas Territoriais, edição 2024, baixada pelo Matheus em 22/10/2026 (sem link, por decisão dele) |
| Conteúdo | Polígonos de 92 municípios, sistema de coordenadas SIRGAS 2000, texto em cp1252. Colunas: `CD_MUN`, `NM_MUN`, região geográfica imediata (`CD_RGI`, `NM_RGI`) e intermediária (`CD_RGINT`, `NM_RGINT`), UF, área em km² |
| Conferência feita por nós | 92 polígonos; os 92 códigos `CD_MUN` casam com o `cod_ibge` do Siconfi (nenhum a mais, nenhum a menos) |
| Observação | O arquivo traz as regiões geográficas do IBGE, **que não são as 8 Regiões de Governo do CEPERJ**. O mapa usa os polígonos da malha e a região do CEPERJ do item 4.1, cruzando pelo nome |

Atenção: a região **"Metropolitana"** do CEPERJ não é a mesma coisa que a Região Metropolitana legal (19 municípios, segundo documento do IPEA), e **"Baixadas Litorâneas" não é "Baixada Fluminense"**. A Baixada Fluminense fica dentro da Metropolitana.

## 5. SIOPS: percentual aplicado em saúde (LC 141/2012), municípios (fornecido pelo Matheus em 22/10/2026)

| Item | Registro |
|---|---|
| Arquivo | `dados_brutos/LCL141.xlsx` (1 aba, 92 linhas, 13 colunas: ano, esfera, ente, UF, região, % aplicado em ASPS, mínimo LC 141, pontos acima do mínimo, valor aplicado, valor mínimo, valor abaixo do mínimo, valor acima do mínimo, situação) |
| Instituição de origem | Ministério da Saúde, painel de indicadores do SIOPS (municipal), baixado pelo Matheus em 22/10/2026. Substitui a consulta antiga do SIOPS (`rel_perc_LC141.php`), que devolveu tabela defeituosa |
| Conferência feita por nós | 92 de 92 municípios do RJ casam com o Siconfi (nomes idênticos); ano 2024 em todas as linhas; mínimo de 15,00% em todas; o percentual bate com valor aplicado dividido pela base (valor mínimo ÷ 0,15), diferença máxima de 0,01 ponto percentual; **os 92 aparecem como "acima ou igual ao mínimo"** (menor: Paracambi, 15,09%; maior: Rio das Ostras, 39,32%) |
| O que o arquivo não diz | Qual bimestre ou fechamento anual ele representa; se os valores são os declarados originalmente ou retificados |
| O que **não** é | Não é o mesmo número do nosso "gasto em saúde" do Siconfi. O SIOPS mede **recursos próprios aplicados em ações e serviços públicos de saúde (ASPS)** sobre a base de impostos e transferências; o Siconfi traz a despesa total na função Saúde. Por isso o SIOPS dá, em geral, um valor menor |
| Limitação | O painel municipal não cobre o Distrito Federal (ver seção 5.1) |

### 5.1 SIOPS estadual (fornecido pelo Matheus em 22/10/2026)

| Item | Registro |
|---|---|
| Arquivo | `dados_brutos/LCL141-Estados.xlsx` (208 linhas, mesmas 13 colunas; **8 anos, de 2018 a 2025**, 26 estados por ano). A primeira versão do arquivo trazia por engano o painel municipal do Brasil inteiro (5.568 linhas, esfera "Municipal") e foi trocada pelo Matheus |
| Instituição de origem | Ministério da Saúde, painel de indicadores do SIOPS (estadual), baixado pelo Matheus em 22/10/2026 |
| Conferência feita por nós | Esfera "Estadual" em todas as linhas e mínimo de 12,00% em todas; **2024: 26 estados, sem duplicados, todos acima ou iguais ao mínimo**; o percentual bate com valor aplicado dividido pela base (valor mínimo ÷ 0,12), diferença máxima de 0,009 ponto percentual. Menores: Rio Grande do Sul e Rio Grande do Norte (12,15%); maior: Amazonas (20,69%). Estado do RJ: 14,75% |
| O que **falta** | **O Distrito Federal não está no arquivo** (26 estados, não 27). O DF tem esfera própria no Siconfi (D) e provavelmente também no SIOPS |
| O que o arquivo não diz | Qual bimestre ou fechamento ele representa; se os valores são os originais ou retificados |
| Uso | Só as linhas de 2024 entram no projeto; os demais anos ficam guardados e não são usados |
| Credibilidade | Fonte primária oficial (Ministério da Saúde); dado declarado pelos próprios entes, sem auditoria por nós |


## 6. Fontes oficiais lidas no Measure (23/10/2026)

| Fonte | O que foi lido | Origem | Credibilidade |
|---|---|---|---|
| Lei Complementar 101/2000 (LRF), arts. 19, 20, 22 e 63 | Limites de pessoal (60% da RCL para estados e municípios, repartição por Poder, prudencial de 95%) e a opção dos municípios com menos de 50 mil habitantes | https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp101.htm (lido por download direto, texto compilado) | Fonte primária oficial |
| Lei Complementar 141/2012, arts. 6º e 7º | Mínimo de saúde: 12% (estados e DF) e 15% (municípios e DF) | https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp141.htm | Fonte primária oficial |
| Constituição Federal, arts. 198 e 166-A | § 11 do art. 198 (agentes comunitários de saúde) e § 1º do art. 166-A (emendas individuais) | https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm | Fonte primária oficial |
| Resolução do Senado 40/2001, arts. 3º e 4º | Limites de dívida consolidada líquida: 2 vezes a RCL (estados e DF) e 1,2 vez (municípios) | https://www2.camara.leg.br/legin/fed/ressen/2001/resolucao-40-20-dezembro-2001-429320-normaatualizada-pl.html | Fonte primária oficial (Câmara dos Deputados) |
| Documentação da API do Siconfi | Códigos `HO` e `RE`; RREO e RGF simplificados só para municípios com menos de 50 mil habitantes que optaram | https://apidatalake.tesouro.gov.br/docs/siconfi.yaml | Fonte primária oficial |
| Documentos de tribunais de contas e secretarias estaduais; apresentação do SIOPS; documento sobre a Portaria MOG 42/1999 | Defensoria computada no Executivo; Anexo 12 vem do SIOPS; funções e subfunções padronizadas | Resultados de busca na web (secundários) | **Fonte secundária**, usada só para confirmação parcial |

Dados coletados nesta fase: `dados_brutos/siconfi_dca_ie_2024.csv` (DCA Anexo I-E, 119 entes, script 13), `dados_brutos/siconfi_rreo_anexo03_2024.csv` (RREO Anexo 03, 107 entes, script 14; os 12 simplificados não têm Anexo 03) e as populações do IBGE (SIDRA tabelas 6579 e 4714).

Acrescentado em 23/10/2026 (leitura de texto oficial no Measure, fechando B5, B6, B7 e C2):

| Fonte | O que foi lido | Instituição | Credibilidade |
|---|---|---|---|
| Portaria STN 642/2019 (atualizada) | Art. 2º, § 2º (Anexos 8 e 12 do RREO vão ao SIOPE e ao SIOPS); art. 6º, §§ 3º e 4º (opção semestral); art. 9º (rascunhos automáticos); art. 12 (defensorias homologam o próprio RGF) | Secretaria do Tesouro Nacional | Fonte primária oficial |
| Portaria SOF/SETO/ME 42/1999 (republicada no DOU de 22/03/2022) | Funções e subfunções; função 10 - Saúde, subfunções 301 a 306; abrangência por esfera | Secretaria de Orçamento Federal | Fonte primária oficial |
| Constituição Federal, art. 166, § 16 (EC 100/2019) | Transferência das emendas de bancada fora da base da RCL para os limites de pessoal | Presidência da República (texto compilado) | Fonte primária oficial |
