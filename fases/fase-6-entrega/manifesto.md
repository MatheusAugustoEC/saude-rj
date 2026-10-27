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

## Adendo de 27/10/2026 (cópias atualizadas após a segunda rodada de ajustes)

Os arquivos de `artefatos/` foram atualizados; `util.js` é novo. A tabela acima mostra os hashes de 26/10; os de agora são estes:

| Arquivo | SHA-256 |
|---|---|
| `artefatos/35_dados_pagina.py` | `342b2167932f5c9b7155bf44afb9f751c3ac0d504bf1e282517f834fd4d76f69` |
| `artefatos/36_gerar_pagina.py` | `5fb120cb24d40697467214b622cd1030fc4ef0124401e970b3fd269a35c0125b` |
| `artefatos/app.js` | `44074bf3b13d7250a7409fbee51a7808721d2afe436a59980dfa33970b7024de` |
| `artefatos/estilo.css` | `065ec60ca19742b8b536e45410e5e003e8a6c999d45d13b61beff4e40a6aef78` |
| `artefatos/index.html` | `8db9c514744598ac02977c2de300fa3590e2a87b3e7346c4b014622098c06c4a` |
| `artefatos/pagina_dados.json` | `bc9d95cb7d480bbc1f0ae8c04483ad4f42dbd898babeb38aa1936126b4d88cb0` |
| `artefatos/run_all.py` | `9a5f7c10f3cde24ea2f610d50d6bf3ce333fe3fa77b8ad91721c89502432a964` |
| `artefatos/saude-fiscal-rj-biblioteca.zip` | `c6155021b419a9b6ff475d0f05a19fd7dc3a5bfdadbd811f198df1353820f4c2` |
| `artefatos/saude-fiscal-rj-cidades.xlsx` | `3087f09f27a1a3624451c124d012207f87d190c81c17962b2e10354aba0ab608` |
| `artefatos/template.html` | `b98d6a6731abf8daa6db83f523c8691527d88ff7858a91006068fb9a0ca777c2` |
| `artefatos/test_pagina.py` | `742d32adf74f9263afb00ef427324cae8cfe83143743ffde2a09792b38b28350` |
| `artefatos/util.js` | `fa358ccbcdcca939dade91318b9a57e9acddea38f90526f0ba0d32a65a158a16` |
| `artefatos/views1.js` | `1fef8fd3e55c848d75998e6c827957a2f8164171b10ad7a4955fae80f4836f76` |
| `artefatos/views2.js` | `8bba8c08b344808df678f2c9efc7818ac87bbec43e13fd94278c1ccff1e3c903` |
| `artefatos/views3.js` | `4855bc2226a1e5e017a3055c94df0a26175fbf2eba894a91aec9a4ce7c9db81c` |

## Dados brutos novos (não copiados; SHA-256 completo)

| Arquivo | SHA-256 |
|---|---|
| `dados_brutos/malha_ibge_api/br_uf_qualidade_minima.json` | `07c671aa87aa1ab296c446de6294df9827112782537b996c0a160284907e7c0f` |
| `dados_brutos/malha_ibge_api/rj_municipios_qualidade_minima.json` | `e40ff0e8b87be8e95cc88b1197c28e0c831a9c825baa6b4e99a9ced063631be8` |

Biblioteca de apresentação: `pagina_fonte/pptxgen.bundle.js` (PptxGenJS 3.12.0, com JSZip), copiada ao lado da página; não editada.
