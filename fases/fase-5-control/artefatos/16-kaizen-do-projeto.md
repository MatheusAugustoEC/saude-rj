# Kaizen do projeto: o que atrapalhou, o que mudou e o que deu certo

Escrito em 25/10/2026, ao fim da fase Control. "Kaizen" é uma palavra japonesa para melhoria contínua: olhar para o próprio jeito de trabalhar e melhorar a cada rodada. Este texto é para qualquer pessoa ler, sem precisar conhecer o projeto por dentro.

**Sobre o projeto em uma frase.** Usei dados públicos para entender por que algumas cidades do Rio de Janeiro gastam menos em saúde por morador que outras. Os números são declarados pelas prefeituras e não foram auditados. Gasto não é qualidade de atendimento.

## O que mais atrapalhou: conseguir os dados

Os números são públicos, mas pegá-los deu trabalho:

- No SUS, a API de dados abertos, o portal OpenDataSUS e o site do CNES não responderam. Só um painel antigo, o TABNET, funcionou.
- No SIOPS (que mostra quanto cada cidade aplica em saúde), o Distrito Federal não estava disponível e o servidor devolveu uma tabela defeituosa para ele. O DF ficou de fora dessa parte.
- O IBGE não divulgou a população de 2023 de cada cidade, e foi preciso estimar.
- O Tesouro e o IBGE informavam populações diferentes para a mesma cidade, e um número que eu mesmo já tinha publicado precisou ser corrigido.
- Em 2025, algumas cidades entregaram suas contas incompletas ou atrasadas. Uma consta como entregue, mas o anexo veio vazio.

**Por que isso aconteceu.** Eu planejava como se as fontes públicas estivessem sempre disponíveis e consistentes, e só descobria o contrário depois de montar a pergunta.

## O segundo problema: escopo misturado

O plano original dizia que os dados do IBGE e do SUS seriam extras, depois do núcleo do projeto. Mesmo assim, essas tarefas entraram na fila antes da hora e se misturaram com a análise principal. Isso foi corrigido duas vezes, e o plano agora é: **primeiro o núcleo, depois as extensões**.

## Outros pontos, com peso estimado

Não medi horas. O peso abaixo é qualitativo, com a evidência de cada caso.

| O que atrapalhou | O que aconteceu | Peso |
|---|---|---|
| Conclusões refeitas | Hipóteses escritas depois de ver o padrão nos dados, uma conclusão de fase reescrita e uma redação que ninguém tinha pedido | Médio |
| Comunicação refeita | O texto de um dos posts teve cinco versões até achar o tom. Algumas palavras do projeto precisaram ser explicadas depois | Médio |
| Rigor em excesso | Dois jeitos independentes de conferir os mesmos números, mais um relatório por fase. Dá segurança, mas custa tempo | Baixo a médio |
| Trabalho parado | Muita coisa pronta no computador, ainda não publicada | Médio |

## Três mudanças

1. **Testar a fonte antes de escrever a pergunta.** Cada fonte ganha um teste de acesso com data e um plano B registrado. Já foi feito para o SUS e para os dados de 2025.
2. **Dizer o que está no escopo antes de começar cada passo.** Toda pendência é classificada como "núcleo" ou "extensão" no momento em que aparece.
3. **Uma ficha por fonte**, com a data do teste, o que falhou e o que foi feito no lugar. Responde de uma vez à pergunta "e se a fonte cair?".

## O que deu certo

- Escrevi as previsões **antes** de abrir os dados de 2025. Das nove conclusões, oito se mantiveram.
- Em cada passo avisei o que os dados não mostram.
- Quando errei, escrevi o que errei e por quê.

## No formato "fiz X, medido por Y, ao fazer Z"

- Corrigi uma distorção de população que mudava os resultados, medido pela conferência de todos os municípios contra a prestação de contas anual, ao trocar a população do Tesouro pela estimativa oficial do IBGE.
- Confirmei que 8 de 9 conclusões se mantiveram em um ano novo (2025), medido por critérios escritos antes de abrir os dados, ao registrar as previsões e os limites de decisão com data.
- Reduzi o risco de depender de fonte pública, medido por testes de acesso datados em cada fonte (SUS, SIOPS e Siconfi de 2025), ao registrar uma alternativa antes de planejar a análise.
- Deixei claras as lacunas, medido por 6 cidades excluídas de 2025 listadas pelo nome com o motivo, ao dizer o que não consegui medir, em vez de preencher com estimativa.

## Como contar isso em 30 segundos

"O que mais me atrapalhou não foi a análise, foi o acesso aos dados públicos: fontes fora do ar, o Distrito Federal que o sistema não entregava, população que não batia entre o Tesouro e o IBGE. Aprendi a testar a fonte antes de montar a pergunta, a registrar o plano B e a separar o que é essencial do que é extra, para o projeto não se perder."

## Nota de bastidores

Falhas de ferramenta (comandos, caminhos de arquivo) não entram no texto principal. Se alguém quiser vê-las, elas aparecem no histórico do repositório.
