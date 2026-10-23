# Relatório da coleta de valores (Siconfi, exercício 2024)

Data: 21/10/2026. Passos concluídos: 1 (coleta) e 2 (conferência da coleta). Próximo: 3 (EDA em notebook), com pausa para revisão antes da planilha.

## O que foi coletado

- **Quem:** 27 estados (incluindo o DF) e os 92 municípios do RJ, ou seja, 119 entes.
- **Fonte:** API de dados abertos do Tesouro Nacional (Siconfi). Detalhes em `docs/02-fontes-de-dados.md`.
- **O quê:**
  - RREO, último bimestre entregue (6): Anexo 01 (balanço orçamentário), Anexo 02 (despesa por função, onde está a Saúde) e Anexo 07 (restos a pagar).
  - RGF, último período entregue: Anexo 01 (despesa com pessoal e receita corrente líquida), por Poder, e Anexo 02 (dívida consolidada).
  - O Anexo 07 do RREO e o Anexo 02 do RGF foram acrescentados em 21/10/2026, por decisão do Matheus, para saber se os dados permitem testar a hipótese da dívida no Analyze.
- **Como:** `scripts/04_coleta_valores.py`. O tipo de relatório (normal ou simplificado), o período e a periodicidade de cada ente foram lidos do extrato de entregas do próprio ente.
- **Resultado:** 914 chamadas, sendo 119 de extrato, 357 de RREO e 438 de RGF. Gravadas em `dados_brutos/`: `siconfi_rreo_2024.csv` (187.539 linhas), `siconfi_rgf_2024.csv` (63.192 linhas) e `siconfi_chamadas_2024.csv` (registro de cada chamada).

## O que a conferência verificou (`scripts/05_conferencia_coleta.py`)

| Verificação | Resultado |
|---|---|
| Chamadas com erro | 0 |
| Chamadas com mais páginas (dado cortado) | 0 |
| Cobertura de RREO Anexos 01 e 02 e RGF Anexo 01 (Executivo) | 27 de 27 estados e 92 de 92 municípios |
| Valores vazios ou não numéricos | 0 |
| Linhas exatamente duplicadas | 0 |
| Bate com as consultas avulsas do RJ de 20/10/2026 | Sim (RREO Anexo 02: 2.021 linhas; RGF Anexo 01 Executivo: 214 linhas) |
| Função "Saúde" no RREO Anexo 02 do estado do RJ | Presente, com dotação, empenhado, liquidado e percentuais |

## Tipos de relatório usados

| Tipo | Chamadas |
|---|---|
| RREO normal, bimestre 6 | 321 |
| RREO simplificado, bimestre 6 | 36 |
| RGF normal, período 3 (quadrimestre) | 402 |
| RGF simplificado, período 2 (semestre) | 36 |

Os números da tabela são **chamadas** à API, não municípios. Cada município simplificado gera 3 chamadas de RREO (3 anexos) e 3 de RGF (2 Poderes no Anexo 01 e 1 no Anexo 02). Logo, **12 dos 92 municípios do RJ entregam relatórios simplificados** (os mesmos 12 no RREO e no RGF), no RGF com periodicidade semestral. A regra de quem pode usar a versão simplificada não está confirmada. *(Correção de 21/10/2026: uma versão anterior deste relatório dizia "24 municípios", o que era a contagem de chamadas.)*

## Achados e problemas encontrados

1. **Erro do script, corrigido:** o DF é cadastrado com esfera `D`, mas a API só o encontra com `E`. Na primeira coleta, o DF veio vazio. Corrigi e refiz a coleta inteira.
2. **4 chamadas vazias, sem erro:**
   - DF, RGF, Poder Judiciário e Ministério Público. Explicação provável: esses órgãos do DF não entregam como os dos estados. **Não confirmado.**
   - Legislativo de Laje do Muriaé e de Miracema. O extrato de entregas mostra só um RGF por quadrimestre, o que sugere que só o Executivo entregou. **Não confirmado.**
3. **Anexos 08 e 12 do RREO (educação e saúde) voltam vazios** para o estado e para a capital do RJ, em 2024. O motivo não está confirmado. Consequência: o indicador "percentual da receita aplicado em saúde, comparado ao mínimo legal" **não sai desse anexo**. O que existe é a despesa por função "Saúde" (Anexo 02).
4. O catálogo de anexos da API não serve para saber quais anexos do RREO existem. Foi preciso testar anexo por anexo.

## Limitações desta coleta

- Um ano só (2024), e só o último período de cada relatório.
- Apenas cinco anexos (RREO 01, 02 e 07; RGF 01 e 02). Não há a DCA nesta coleta.
- **Dívida e restos a pagar (acrescentados em 21/10/2026):** cobertura de 27 de 27 estados e 92 de 92 municípios nos dois anexos. O percentual da dívida consolidada líquida sobre a RCL (`PercentualDaDCLSobreARCL`) existe para os 119 entes. O saldo total de restos a pagar (`SaldoTotal`) existe para 118 dos 119; falta identificar o ente. No Anexo 02 do RGF o valor do período vem em colunas que mudam com a periodicidade do ente ("Até o 3º Quadrimestre", "Até o 2º Semestre"), então a leitura precisa tratar isso. Os valores ainda **não foram analisados**: isso fica para depois da revisão da EDA.
- Os valores são o que cada ente declarou. Não foram auditados.
- Retificações (status `RE`): não foi examinado se a API devolve a versão original ou a retificada.

## Passo 3: EDA (feita em 21/10/2026)

Notebook: `notebooks/01_eda_siconfi_2024.ipynb` (executado de cima para baixo, sem erro). Tabela de indicadores gerada por ele: `dados_tratados/indicadores_2024.csv` (119 entes, uma linha por ente).

Principais achados, todos explicados no próprio notebook:
- Os 4 indicadores (saúde por habitante, saúde como % da despesa, pessoal como % da RCL, despesa como % da receita) saem completos para os 119 entes.
- O percentual de saúde comparado ao mínimo legal **não sai** (Anexo 12 vazio na API).
- Dado atípico: 3 municípios com RCL muito abaixo da receita (Areal, Itaperuna, Miracema), que fazem a despesa com pessoal passar de 100% da RCL. Armação dos Búzios declara dois totais de despesa diferentes.
- O RJ tem o menor gasto em saúde por habitante e a menor parcela da despesa em saúde entre os 27 estados.
- Saúde por habitante acompanha a receita por habitante (correlação de 0,80 nos estados e 0,82 nos municípios).

### Reescrita do notebook (21/10/2026)

O notebook foi reescrito a pedido do Matheus: tabelas e textos em Markdown, **números dos textos gerados a partir dos dados**, legenda ao fim de cada seção, tabela "De onde vem cada número", glossário e dicionário das 45 colunas (conferido por código). A primeira versão está guardada em `notebooks/arquivo/01_eda_siconfi_2024_v1.ipynb`.

Conteúdo novo: pessoal pela **soma dos Poderes** como indicador principal, resultados **com e sem** os casos especiais, e dívida e restos a pagar (descritivos). Achados da revisão, todos corrigidos ou registrados no notebook:
- **RCL ajustada:** além das emendas individuais e de bancada, há uma terceira dedução (transferências da União para agentes comunitários de saúde). Com as três, a RCL ajustada se reproduz em 118 dos 119 entes (a exceção é Sumidouro).
- **Restos a pagar:** a conta `SaldoTotal` traz uma linha por Poder e órgão. Foi preciso filtrar a linha do total do ente (o aviso do código pegou o erro). Itatiaia não tem essa linha.
- **Limites de dívida declarados:** 8 municípios (Belford Roxo, Conceição de Macabu, Cordeiro, Duas Barras, Nova Iguaçu, São Fidélis, Sumidouro, Trajano de Moraes) declararam o limite do Senado já como **percentual (120)** em vez de reais. O primeiro cálculo tratou o 120 como reais e deu 0% (erro de leitura nosso, corrigido em 21/10/2026 após olhar os dados brutos). **Seguem fora do padrão e precisam de checagem 3 entes:** Roraima (90,3%), Carmo (21,3%) e Paracambi (126,7%). Eles ficam fora da contagem de "acima do limite".
- **Dívida do RJ:** 211,3% da RCL, acima do limite do Senado que o estado declara (200%). É o 1º maior entre os 27. Valor declarado, não conferido com a lei.
- A posição do RJ muda no máximo 1 casa quando o DF sai.

**Pausa:** o Matheus revisa o notebook antes de qualquer planilha. Decisões pendentes estão na seção 9 do notebook.

### Planilha Excel (21/10/2026)

Arquivo: `planilhas/saude_fiscal_rj_2024.xlsx`. Abas: Leia-me, Estados (27), Municípios RJ (92), Com e sem, Dados dos gráficos, Gráficos (4 gráficos de barras com o RJ em azul) e Legenda. Texto azul = dado da API; texto preto = fórmula. Os indicadores e as posições são **fórmulas** sobre as colunas de entrada (3.081 fórmulas), para qualquer pessoa conferir o cálculo.

Como foi gerada e conferida (reprodutível):
1. `scripts/09_gerar_planilha.py` gera a planilha a partir de `dados_tratados/indicadores_2024.csv` e do RGF bruto.
2. `scripts/11_recalcular_planilha.ps1` recalcula com o Excel (grava os valores das fórmulas) e exporta cada gráfico como imagem para conferência visual. A ferramenta de recálculo em LibreOffice não está disponível neste computador.
3. `scripts/10_conferir_planilha.py` compara a planilha com o notebook.

Resultado da conferência: **0 erros de fórmula, 0 diferenças** em 8 indicadores para os 119 entes; posições do RJ e medianas "com e sem" iguais às do notebook. A conferência achou e corrigiu: restos a pagar de Itatiaia aparecia como 0% em vez de ficar em branco; e quatro defeitos de formatação nos gráficos (título sobre as barras, título de eixo sobre os números, grade preta, barras negativas brancas).

### Etapa 1 do pedido de 22/10/2026: maior e menor com nome (feita)

No notebook, toda comparação entre municípios passou a mostrar **quem é o maior e quem é o menor**: tabela-resumo com "Menor", "Maior", os mesmos **sem os casos especiais**, e a **posição da capital** entre os 92; histogramas com o menor e o maior nomeados; tabelas de estados e de dívida e restos a pagar com os nomes. O símbolo ⚠ marca extremos que pertencem a um caso especial. Exemplos: o menor gasto em saúde por habitante é de Armação dos Búzios (R$ 867, ⚠ caso especial) e, sem os casos especiais, de São Pedro da Aldeia (R$ 1.026); o maior é de Carapebus (R$ 6.853). A capital gasta R$ 1.153 por habitante, o 85º maior valor entre os 92.

**Regiões:** o Matheus escolheu a Opção A (8 Regiões de Governo do CEPERJ, capital à parte). Aguarda a lista oficial de municípios por região (ver `docs/04-pendencias-measure.md`, seção E). **Mapa e aba "Extremos" da planilha** dependem disso e ficam para depois.

### Decisões do Matheus durante a revisão (21/10/2026)

1. **Mínimo de saúde:** buscar outra fonte. O SIOPS é a candidata, mas o servidor dele estava fora do ar em 21/10/2026 (ver `docs/02-fontes-de-dados.md`). O núcleo segue sem ele, e o mínimo legal vira módulo futuro. **Lembrete: ao terminar o núcleo, testar o SIOPS de novo** (`scripts/08_teste_acesso_siops.py`).
2. **Dados atípicos (Areal, Itaperuna, Miracema, Armação dos Búzios) e os 12 municípios simplificados:** manter, sinalizar e mostrar o resultado com e sem eles.
3. **Pessoal, Executivo ou soma dos Poderes:** em análise (ver `scripts/06_pessoal_por_poder.py`).
4. **Dívida e restos a pagar:** coletar o RGF Anexo 02 e o RREO Anexo 07. O teste formal da hipótese fica para o Analyze; na EDA e no Define serve para saber se os dados permitem testá-la.
