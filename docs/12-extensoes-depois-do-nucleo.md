# Extensões para depois do núcleo (SUS, idade em faixas, modelo integrado)

Registrado em 24/10/2026. **Não rodar antes de fechar o núcleo** (Marco 3, Improve, Control, Entrega e Banca). Quando o núcleo estiver entregue, voltar aqui. Antes de rodar: mostrar as hipóteses ao responsável, gravá-las em docs/09 com a data, escrever os métodos em docs/10 (o quê, por quê, como) e só então coletar e rodar.

## Ponto de partida

- Módulo IBGE (idade 65+ e esgoto, Censo 2022) **já rodou**: docs/11, scripts/28, dados_tratados/analyze_ibge_*.csv. Falta integrá-lo ao relatório na Entrega.
- Hipótese do responsável sobre saneamento (M2: menos esgoto, mais gasto) **não se sustenta** depois de descontar a receita: o sinal inverte (+3,4% por +10 pp em 2024, IC +0,3% a +6,5%), porque cidades com pouco esgoto têm receita alta. Ideia dele para esta extensão: testar saneamento com um desfecho de saúde, e não só com gasto (ver S4).

## Teste de acesso ao SUS (feito em 24/10/2026; scripts/29, dados_brutos/sus_teste_acesso.csv)

- TABNET (DATASUS) responde: CNES leitos do RJ (cnes/cnv/leiintrj.def) e SIH do RJ (sih/cnv/nirj.def). O FTP do DATASUS também.
- API de dados abertos, OpenDataSUS e site do CNES falharam (conexão fechada ou DNS). Descartados.
- Leitos existentes por município, dez/2024: um único POST ao TABNET devolveu os 92 municípios com código IBGE de 6 dígitos. Cinco sem leito ("-", zero real). Total de 35.676 leitos; capital 16.176, Niterói 2.157, Maricá 188.
- Séries mensais até 2026: usar dez/2024 e dez/2023 (replicação).
- Ressalvas: leito mede oferta, não gasto nem qualidade; cidade-polo atende gente de fora; o SIH registra o local da internação, não a residência; CNES é declarado e não auditado.

## Hipóteses propostas (aprovadas na conversa, ainda não gravadas em docs/09)

| Id | Hipótese (antes de rodar) | Critério |
|---|---|---|
| S1 | Com a mesma receita por habitante, mais leitos por habitante, mais gasto em saúde por habitante | Coeficiente positivo, IC 95% sem zero |
| S2 | Os leitos se concentram nas cidades-polo, o que enfraquece S1 | Spearman entre leitos e população, mais descrição por município |
| S3 | A capital gasta menos que o previsto, mesmo com seus leitos | Valor real fora do intervalo de previsão de 95% (como em M4) |
| S4 | Cidades com menos esgoto têm mais internações por doenças infecciosas intestinais por habitante, para todas as idades e, em separado, para crianças de 0 a 4 anos | Coeficiente do esgoto negativo, IC 95% sem zero, controlando a receita. Ressalva: local da internação |
| M6 | Com a mesma receita, mais crianças e adolescentes (0 a 14 anos) elevam o gasto por habitante; idosos seguem sem efeito claro | IC 95% sem zero; margem de ±10% para "sem efeito" |
| S5 | No modelo com receita, grupos, idosos, esgoto, 0–14 e leitos, o resíduo do Resto da Metropolitana e da capital muda pouco | Mudança maior que 5 pontos percentuais é relevante; VIF acima de 5 lido com reserva |

**Idade em faixas:** usar 0–14 e 65+ com adultos como referência (os percentuais somam 100%, uma faixa fica de fora). Tabela 10157 do IBGE já está baixada. Risco: pouca variação entre cidades (idosos 8% a 17,6%), pode dar "sem conclusão", o que é válido. Só duas faixas, decididas antes, por haver 91 cidades.

**Ordem sugerida:** leitos (S1–S3) → SIH (S4, que exige verificar as combinações de filtro da tabela) → M6 e S5 (dados já em casa).

## Outras extensões abertas

- DF no SIOPS (D1): não obtido; caminho manual possível pelo RREO Anexo 12 do portal de transparência do DF. Ver docs/04.
- Links e bimestre dos painéis do SIOPS.
- B4: qual versão a API do Siconfi devolve para relatórios retificados.
- README do repositório sem o Analyze.
- Opcionais: royalties (ANP), atividade econômica, regiões metropolitanas de outros estados.
- Ao concluir, acrescentar os achados em docs/05 e docs/08, sempre com a ressalva.
