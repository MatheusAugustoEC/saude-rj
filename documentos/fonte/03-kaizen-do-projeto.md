# O que mais atrapalhou foi conseguir os dados públicos

**Documento 3 · Kaizen do projeto — Saúde fiscal do Rio de Janeiro · outubro de 2026**

<div class="numero"><b>3</b><span>mudanças que passei a fazer por causa dos tropeços: testar a fonte antes da pergunta, dizer o escopo antes de cada passo e manter uma ficha por fonte</span></div>

<div class="resumo" markdown="1">

**Em poucas linhas.** "Kaizen" é uma palavra japonesa para melhoria contínua: olhar para o próprio jeito de trabalhar e melhorar a cada rodada. Este projeto usa dados públicos para entender por que algumas cidades do Rio de Janeiro gastam menos em saúde por morador do que outras. Os números são públicos, mas pegá-los deu mais trabalho do que analisá-los. Aqui está o que travou, o que mudei e o que deu certo.

</div>

## 1. Os dados públicos existem, mas nem sempre chegam

A cada fonte, uma surpresa diferente. Esta é a **ficha por fonte**, com o que foi testado e o plano B:

| Fonte | O que aconteceu | O que fiz no lugar |
|---|---|---|
| **Tesouro Nacional (Siconfi)**: receitas e despesas | A população informada não bate com a do IBGE, e um número que eu já tinha publicado precisou ser corrigido. Em 2025, uma cidade entregou o relatório incompleto e outra consta como entregue, mas veio vazia | Troquei pela população oficial do IBGE; listei pelo nome as cidades sem dado |
| **IBGE**: população | Não existe estimativa de população municipal para 2023 | Estimei 2023 pela média entre o Censo de 2022 e a estimativa de 2024, e declarei |
| **SIOPS** (quanto cada cidade aplica em saúde) | O Distrito Federal não está disponível no painel, e o servidor devolveu uma tabela defeituosa para ele | O DF ficou de fora; há um caminho manual possível, pelo portal de transparência do DF |
| **SUS** (leitos, internações) | A API de dados abertos, o portal OpenDataSUS e o site do CNES não responderam | O painel TABNET e o servidor de arquivos funcionam. Esta parte virou extensão do projeto |
| **Regiões do estado (CEPERJ)** | Funcionou | — |
| **Balanço anual de 2025** | Ainda estava sendo entregue em outubro de 2026 | Marquei o ano como incompleto e fiz a leitura com e sem as entregas recentes |

> [!IMPORTANT]
> **A causa de fundo:** eu planejava como se as fontes públicas estivessem sempre disponíveis e coerentes entre si. Só descobria o contrário depois de montar a pergunta.

## 2. O segundo problema: o escopo se misturou

O plano original dizia que os dados do IBGE e do SUS seriam **extras**, depois do núcleo do projeto. Mesmo assim, essas tarefas entraram na fila antes da hora e se misturaram com a análise principal. Isso foi corrigido duas vezes. O plano agora é claro: **primeiro o núcleo, depois as extensões**.

## 3. Outros pontos, com peso estimado

Não medi horas. O peso abaixo é uma estimativa por ordem de grandeza, com a evidência de cada caso.

| O que atrapalhou | O que aconteceu | Peso |
|---|---|---|
| **Conclusões refeitas** | Hipóteses escritas depois de ver o padrão nos dados, uma conclusão de fase reescrita e uma redação que ninguém tinha pedido | <span class="ressalva">Médio</span> |
| **Comunicação refeita** | O texto de um dos posts teve cinco versões até achar o tom. Algumas palavras do projeto precisaram ser explicadas depois | <span class="ressalva">Médio</span> |
| **Rigor em excesso** | Dois jeitos independentes de conferir os mesmos números, mais um relatório por fase. Dá segurança, mas custa tempo | <span class="neutro">Baixo a médio</span> |
| **Trabalho parado** | Muita coisa pronta no computador, ainda não publicada | <span class="ressalva">Médio</span> |

## 4. Três mudanças

> [!TIP]
> **1. Testar a fonte antes de escrever a pergunta.** Cada fonte ganha um teste de acesso com data e um plano B registrado. Já foi feito para o SUS e para os dados de 2025.
>
> **2. Dizer o que está no escopo antes de começar cada passo.** Toda pendência é classificada como "núcleo" ou "extensão" no momento em que aparece.
>
> **3. Uma ficha por fonte**, como a da primeira seção. Ela responde de uma vez a pergunta "e se a fonte cair?".

## 5. O que deu certo

- Escrevi as previsões **antes** de abrir os dados de 2025. Das nove conclusões, oito se mantiveram.
- Em cada passo avisei o que os dados não mostram: gasto não é qualidade de atendimento.
- Quando errei, escrevi o que errei e por quê. O número que eu tinha publicado foi corrigido em público.

## 6. No formato "fiz X, medido por Y, ao fazer Z"

- Corrigi uma distorção de população que mudava os resultados, **medido** pela conferência de todos os municípios contra a prestação de contas anual, **ao** trocar a população do Tesouro pela estimativa oficial do IBGE.
- Confirmei que 8 de 9 conclusões se mantiveram em um ano novo (2025), **medido** por critérios escritos antes de abrir os dados, **ao** registrar as previsões e os limites de decisão com data.
- Reduzi o risco de depender de fonte pública, **medido** por testes de acesso datados em cada fonte (SUS, SIOPS e Siconfi de 2025), **ao** registrar uma alternativa antes de planejar a análise.
- Deixei claras as lacunas, **medido** por 6 cidades excluídas de 2025 listadas pelo nome com o motivo, **ao** dizer o que não consegui medir, em vez de preencher com estimativa.

## 7. Em 30 segundos

> "O que mais me atrapalhou não foi a análise, foi o acesso aos dados públicos: fontes fora do ar, o Distrito Federal que o sistema não entregava, população que não batia entre o Tesouro e o IBGE. Aprendi a testar a fonte antes de montar a pergunta, a registrar o plano B e a separar o que é essencial do que é extra, para o projeto não se perder."

## Para saber mais

Todo o trabalho, com dados, contas e relatórios abertos: [github.com/MatheusAugustoEC/saude-rj](https://github.com/MatheusAugustoEC/saude-rj).
