# Manifesto, fase 6 (Entrega)

Gerado em 26/10/2026. O conteúdo de `artefatos/` é uma **cópia congelada**; correção é adendo datado, nunca edição.

## Produzidos (cópia em `artefatos/`)

| Arquivo | O que é | SHA-256 |
|---|---|---|
| `artefatos/35_dados_pagina.py` | gera os dados da página a partir do pipeline | `daa0dbc7d9a0015b…` |
| `artefatos/36_gerar_pagina.py` | monta a página, a planilha e o .zip | `976f46c10e356c10…` |
| `artefatos/template.html` | molde da página | `55c945332e3730cc…` |
| `artefatos/estilo.css` | estilo | `c9f78b9c309a2f24…` |
| `artefatos/app.js` | mapas, gráficos e utilidades | `44074bf3b13d7250…` |
| `artefatos/views1.js` | Início e Cidade | `fe4c1d77f6c66dbc…` |
| `artefatos/views2.js` | Gestor, Controle e Como cheguei aqui | `5f36a21ddc77d4c5…` |
| `artefatos/views3.js` | Biblioteca, apresentação e roteador | `c14c47d437492383…` |
| `artefatos/test_pagina.py` | 8 testes da página | `742d32adf74f9263…` |
| `artefatos/run_all.py` | refaz as contas e os testes, agora com 35 e 36 | `9a5f7c10f3cde24e…` |
| `artefatos/pagina_dados.json` | dados da página (números, curiosidades, fontes) | `48ac8edd0e58a921…` |
| `artefatos/index.html` | a página de entrega | `a510327771bff55c…` |
| `artefatos/saude-fiscal-rj-cidades.xlsx` | planilha das cidades | `b7d89ae3fbe8f99c…` |
| `artefatos/saude-fiscal-rj-biblioteca.zip` | todos os arquivos da Biblioteca | `c19c2fc8c8a123af…` |

A coluna SHA-256 mostra os 16 primeiros caracteres; o código completo pode ser recalculado com `sha256sum`.

## Dados brutos novos (não copiados; SHA-256 completo)

| Arquivo | SHA-256 |
|---|---|
| `dados_brutos/malha_ibge_api/br_uf_qualidade_minima.json` | `07c671aa87aa1ab296c446de6294df9827112782537b996c0a160284907e7c0f` |
| `dados_brutos/malha_ibge_api/rj_municipios_qualidade_minima.json` | `e40ff0e8b87be8e95cc88b1197c28e0c831a9c825baa6b4e99a9ced063631be8` |

Biblioteca de apresentação: `pagina_fonte/pptxgen.bundle.js` (PptxGenJS 3.12.0, com JSZip), copiada ao lado da página; não editada.
