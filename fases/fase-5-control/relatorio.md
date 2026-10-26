# Oito de nove conclusões resistiram a um ano novo; a lista de cidades da triagem, não

**Fase 5 · Control, Saúde fiscal do Rio de Janeiro · Siconfi 2023 a 2025 · 25/10/2026**

> [!NOTE]
> Os dados são declarados pelas prefeituras e pelo estado, e não foram auditados. Gasto em saúde por habitante não mede qualidade nem necessidade. Cidade sinalizada é cidade para olhar, não cidade errada. Nada foi implementado em órgão nenhum.

<div class="numero"><b>8 de 9</b><span>conclusões se mantiveram em 2025, um ano que eu só abri depois de escrever as previsões (86 cidades do Rio de Janeiro)</span></div>

<div class="resumo" markdown="1">

**Em três linhas.** Abri 2025 uma única vez, com critérios escritos antes: oito conclusões se sustentaram, uma enfraqueceu (a lista de cidades da triagem) e nenhuma caiu. Escrevi o plano de acompanhamento, 13 testes automáticos do dado e um comando que refaz tudo em cerca de dois minutos. O Kaizen (documento à parte) mostra que o maior problema do projeto foi conseguir os dados.

</div>

## 1. A pergunta desta fase

O Improve propôs ferramentas de controle. O Control pergunta se o que foi concluído **continua valendo** com dado novo e como acompanhar isso sem perder o rumo. Duas coisas são controladas: o processo (o plano de acompanhamento) e o próprio projeto (os testes e a reprodução).

## 2. O que eu encontrei

### 2.1 Em 2025, oito conclusões se mantêm e a lista de cidades da triagem enfraquece

**Das nove conclusões que vinham de antes, oito se sustentam, uma enfraquece e nenhuma cai.** O recorte tem 86 cidades. Ficaram de fora seis: Carmo, Magé, Mendes, Miracema, São Francisco de Itabapoana e Volta Redonda (esta aparece como entregue, mas o anexo veio vazio).

| Id | Conclusão | Resultado em 2025 | Classificação |
|---|---|---|---|
| K1 | Elasticidade da receita abaixo de 1 | 0,74 (0,63 a 0,86) | Sustenta |
| K2 | Metropolitana sem conclusão | −7,2% (−20,7% a +8,6%) | Sustenta |
| K3 | Capital abaixo do previsto | −33,5% | Sustenta |
| K4 | O gasto segue os repasses | 0,67 contra 0,11 da receita própria | Sustenta |
| K5 | A triagem se repete | Só 1 das 3 repete | **Enfraquece** |
| K6 | Pares leem melhor que região | Dispersão cai 46% | Sustenta |
| K7 | Repasses movem o gasto dentro da cidade | 0,59 (0,27 a 0,92) | Sustenta |
| K8 | Baixadas Litorâneas abaixo do previsto | −15,6% | Sustenta |
| K9 | Somar visitantes piora o resíduo | −15,6% vai a −18,8% | Sustenta |

- **A triagem é estável como ordem, não como lista.** A correlação dos resíduos entre 2024 e 2025 é de +0,83. Mas só Niterói fica fora do intervalo nos três anos (−49%, −48% e −44%). A capital e São Pedro da Aldeia voltam para dentro. Araruama entra (−33%): achado novo para auditoria.
- **A elasticidade dos repasses dentro da cidade depende do par de anos:** 0,28 (2023→2024) e 0,59 (2024→2025). O teste de estresse mostra as duas, e a elasticidade entre cidades (0,67, estável nos três anos) é a referência.
- **Maturidade:** quatro DCAs entraram depois de 31/08/2026. A leitura sem elas não muda nenhuma classificação.
- **Meus palpites:** um errou (K7, que eu previa entre 0,10 e 0,45). Seis acertaram. A K5 foi o ponto fraco.

> [!WARNING]
> **Limite da confirmação.** São as mesmas cidades de 2023 e 2024, então 2025 mostra estabilidade no tempo, não vale para outros lugares. 2025 é o primeiro ano dos novos mandatos municipais, e a DCA ainda recebe entregas.

### 2.2 O plano de acompanhamento

O plano está em [docs/15](../../docs/15-plano-de-controle.md): para cada ferramenta (R1, R2, R4, R5, R6, R7), o que se acompanha, de onde vem o dado, com que frequência, quando soa o alerta, quem olha (como papel) e o que fazer. Inclui ainda quando o dado fica completo, o que invalidaria a análise e o gatilho de revisão da triagem (elasticidade fora de 0,60 a 0,95, poder de explicação abaixo de 0,70).

- **Regra de ouro (C13):** o período ainda incompleto aparece **marcado**, não interpretado. Cidade sem dado aparece como "sem dado", nunca como zero.
- **Limiar de julgamento meu:** o alerta de dependência de repasses (mais de 90% da receita) é escolha minha, não regra legal.

### 2.3 Testes automáticos e reprodução

- **13 testes** (`tests/`) conferem volume (92 municípios, 26 estados e o DF), códigos, valores positivos, faixa do gasto por habitante, população de 2025 contra 2024, completude dos balanços de 2023 e 2025 e a elasticidade dentro da faixa conferida. Um deles confere que os dados brutos citados com SHA-256 nos manifestos **não mudaram**.
- **Um comando** (`scripts/run_all.py`) refaz todas as contas e roda os testes. Na conferência, os 8 scripts rodaram em cerca de dois minutos e **todos os arquivos de resultado saíram idênticos** aos gravados.
- **No GitHub:** os testes rodam a cada mudança e uma vez por mês, sem usar a internet para buscar dado novo e sem publicar nada. O arquivo foi escrito, mas **ainda não rodou lá**, porque nada foi enviado ao repositório.
- **Ambiente e parâmetros:** versões fixadas em `requirements.txt`; parâmetros em `config/parametros.json`.

> [!NOTE]
> **Parâmetros no código.** Os scripts novos e os testes leem o arquivo de configuração. Os scripts congelados de fases anteriores mantêm as mesmas constantes dentro do código (listadas no arquivo), porque mexer neles quebraria a cópia congelada de cada fase.

### 2.4 Kaizen: o maior problema foi conseguir os dados

O Kaizen do projeto tem documento próprio, em linguagem universal: [docs/16](../../docs/16-kaizen-do-projeto.md). Em resumo:

- **O que mais atrapalhou:** obter os dados (fontes fora do ar, o Distrito Federal ausente do SIOPS, população que não batia entre o Tesouro e o IBGE) e o escopo misturado entre núcleo e extensões.
- **Três mudanças:** testar a fonte antes de escrever a pergunta; dizer o escopo antes de cada passo; uma ficha por fonte com o plano B.
- **Horas não medidas:** o peso é qualitativo, com a evidência de cada caso.

## 3. O que eu decidi

| Escolha | O que usei | O que mais considerei | Por que esta | Evidência | Regra |
|---|---|---|---|---|---|
| Confirmação | 2025, aberto uma única vez, com critérios e desempates fixados antes | Rodar 2023 de novo, ou separar uma parte de 2024 | 2023 já tinha sido usado na replicação; 2025 é ano novo de verdade | docs/14 | C5 |
| Classificação final | A pior entre "todas as cidades" e "sem as DCAs recentes" | Só a leitura com todas | Dado ainda imaturo não deve ajudar a conclusão | 4 DCAs recentes; nenhuma classificação mudou | C6 |
| Carta de controle | **Não usei** | Coletar seis bimestres de vários anos | Só há dois pontos anuais e o RREO é cumulativo; a carta pediria dezenas de pontos | docs/15 | C2, C3 |
| Ganho a verificar | **Não se aplica**: nada foi implementado | Medir um ganho | Troquei pela pergunta "o desvio é maior que a variação normal de um ano ao outro?": respondida pelo retroteste do Improve (+0,77) e por 2025 (+0,83) | docs/13 e docs/14 | C4 |
| Testes | Leem só os arquivos do repositório | Baixar o dado a cada teste | Teste que depende do site do Tesouro falha por motivo alheio ao dado | 13 testes | C7 |
| Automação | Teste automático no GitHub; página estática atualizada por comando | Atualização agendada completa | O dado chega aos poucos e é retificado; publicar sem olhar causaria alarme falso | 4 DCAs recentes | C8, C13 |

## 4. Para você explicar esta fase

**A fase em 30 segundos.** "Depois de propor as ferramentas, fui testar se elas resistem a um ano novo. Escrevi as previsões antes de abrir o dado de 2025. Oito das nove conclusões se mantiveram. A que enfraqueceu foi a lista de cidades da triagem: o ranking é estável, mas a lista muda de um ano para o outro. Deixei também um plano de acompanhamento, testes automáticos do dado e um comando que refaz tudo."

| Pergunta que vão fazer | Resposta |
|---|---|
| O que você fez de diferente em 2025? | Escrevi as previsões com data antes de baixar o dado e fixei como cada resultado seria classificado. Se desse errado, eu teria de registrar. |
| Por que a triagem enfraqueceu? | O ranking das cidades é estável (+0,83), mas o intervalo é estreito e poucas cidades ficam fora dele. Só Niterói repete nos três anos. A triagem serve para ordenar e para perguntar, não para fazer lista fixa. |
| Por que não há carta de controle? | Só tenho dois pontos anuais, e o relatório bimestral é cumulativo. Uma carta pede dezenas de pontos. |
| Isso funciona em outro estado? | Não sei. As mesmas 86 cidades aparecem nos três anos. O desenho está pronto para outros estados, que o Siconfi cobre. |
| E se a fonte cair? | Cada fonte foi testada com data, e o plano B está registrado. O teste automático avisa se o dado mudar de forma. |

**Números para saber de cor:** 8 de 9 conclusões se sustentaram em 2025; 3 anos seguidos de Niterói fora do intervalo; correlação +0,83 entre os resíduos de 2024 e 2025; 13 testes; 2 minutos para refazer tudo.

## 5. O que ainda não sei

- Se a triagem funciona em outras cidades. Falta olhar outros estados.
- Se a elasticidade de ano a ano é estável: 0,28 e 0,59 são só dois pares de anos.
- Por que Niterói e Araruama destoam. Pergunta para quem acessa os livros.
- Qual versão do relatório a API devolve quando há retificação (B4 aberto).
- Se o teste automático roda sem problema no GitHub. Só saberei depois do primeiro envio.
- O que pode invalidar o plano está em docs/15, seção 4.

## 6. O veredito

**APROVADO pelo responsável em 26/10/2026.** O critério é a qualidade do processo, e não se as previsões se confirmaram.

| Critério | Veredito | Motivo |
|---|---|---|
| Reação escrita antes do problema (C1) | <span class="ok">OK</span> | docs/15, uma linha por ferramenta |
| Confirmação aberta uma vez, resultado registrado (C5) | <span class="ok">OK</span> | docs/14, incluindo o "enfraquece" e o palpite errado |
| Fim de série imaturo (C6, C13) | <span class="ok">OK</span> | DCAs recentes marcadas; leitura com e sem |
| Qualidade do dado em teste automático (C7) | <span class="ok">OK</span> | 13 testes passando |
| Reprodutível por um estranho (C8) | <span class="ok">OK</span> | um comando; saídas idênticas |
| Teste automático no GitHub | <span class="ressalva">RESSALVA</span> | escrito, mas ainda não rodou lá (nada foi enviado) |
| O que invalida e quando revisar (C9, C10) | <span class="ok">OK</span> | docs/15, seções 4 e 5 |
| Padrões reutilizáveis (C11) | <span class="ok">OK</span> | docs/15, seção 6 |
| Kaizen (C12) | <span class="ok">OK</span> | docs/16; horas não medidas, peso qualitativo |
| Não se aplicam, declarados | <span class="ok">OK</span> | C2, C3 (sem série), C4 (sem ganho), C10 completo (sem modelo preditivo) |

## 7. O próximo capítulo

**Entrega:** uma página única, estática, que reúne o relatório, o painel e os slides, em linguagem universal. Com ela, o plano de controle vira a seção "como acompanhar". A página mostra a data da coleta e a versão do código. Antes, resolvo as pendências menores (B4) e peço o seu aval para o primeiro envio ao GitHub, quando o teste automático rodará pela primeira vez. As extensões (SUS, IBGE integrado, idade em faixas, DF no SIOPS) só entram depois do núcleo.

## Bastidores

| Passo | Script ou arquivo |
|---|---|
| Verificação de acesso a 2025 | `scripts/31_teste_acesso_2025.py` |
| Previsões, critérios e desempates | `docs/14-control-previsoes-2025.md` |
| Coleta de 2025 | `scripts/32_coleta_2025_confirmacao.py` |
| Análise de 2025 (aberta uma vez) | `scripts/33_control_confirmacao_2025.py` |
| Plano de controle | `docs/15-plano-de-controle.md` |
| Kaizen do projeto | `docs/16-kaizen-do-projeto.md` |
| Testes e configuração | `tests/test_dados.py`, `config/parametros.json`, `.github/workflows/testes.yml` |
| Refazer tudo | `scripts/run_all.py`, `requirements.txt` |
