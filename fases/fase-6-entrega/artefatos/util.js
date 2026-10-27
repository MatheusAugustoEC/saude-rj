/* ---------- fonte, glossário, endereço compartilhável, planilha .xlsx feita no navegador ---------- */
const fonte = t => `<p class="fonte">Fonte: ${esc(t)}</p>`;
const GLOSSARIO = [
  ["Siconfi", "Sistema do Tesouro Nacional em que estados e municípios declaram suas contas. É a fonte principal desta página."],
  ["RREO e DCA", "RREO é o relatório bimestral de execução do orçamento; DCA é a Declaração de Contas Anuais, o balanço do ano que cada prefeitura entrega ao Tesouro."],
  ["SIOPS", "Sistema do Ministério da Saúde em que cada ente declara quanto aplicou em saúde com recursos próprios. A lei manda aplicar ao menos 15% da base de cálculo, formada por impostos e transferências constitucionais (municípios) e 12% (estados)."],
  ["Repasses", "Dinheiro que a cidade recebe de outros entes (União e estado), como o Fundo de Participação dos Municípios e as transferências do SUS."],
  ["Receita própria", "O que a cidade arrecada por conta própria, como IPTU e ISS."],
  ["Folga sobre o mínimo", "Quantos pontos percentuais a cidade aplica acima do mínimo de 15% da base de cálculo. Folga de 0,1 ponto significa que está quase no mínimo."],
  ["Cidades parecidas", "As cidades da mesma faixa de receita por habitante. A página divide as 92 cidades em 5 faixas, de tamanho parecido."],
  ["Distância do previsto", "Quanto o gasto declarado da cidade fica acima ou abaixo do que o modelo prevê a partir da receita dela. É um alerta para perguntar, nunca uma prova de problema."],
  ["Intervalo de previsão de 95%", "Faixa em que se espera o gasto da cidade, dada a receita, com 95% de confiança. “Fora” significa abaixo do limite inferior dessa faixa."],
  ["Mediana", "O valor do meio: metade das cidades fica acima e metade abaixo. Evita que uma cidade muito grande ou muito pequena distorça a média."],
  ["Sensibilidade", "Quanto o gasto muda quando a receita muda 1%. Sensibilidade de 0,8 significa que 10% a mais de receita vêm com cerca de 8% a mais de gasto."],
  ["Tons de azul (quintis)", "Cada tom do mapa reúne a mesma quantidade de cidades (ou de estados), do quinto que tem menos ao quinto que tem mais."],
  ["RCL", "Receita corrente líquida: a base usada pela Lei de Responsabilidade Fiscal para medir os limites de pessoal e de dívida."],
  ["LRF", "Lei de Responsabilidade Fiscal. Fixa limites de gasto com pessoal e de endividamento. O limite prudencial é um alerta antes do limite máximo."],
  ["p.p.", "Ponto percentual: a diferença entre duas porcentagens (de 15% para 17% são 2 p.p.)."],
];
function montaGlossario() {
  $("#glossario").innerHTML = `<summary>Glossário: termos que aparecem na página</summary><dl>${GLOSSARIO.map(([t, d]) => `<dt>${esc(t)}</dt><dd>${esc(d)}</dd>`).join("")}</dl>`;
}

/* endereço compartilhável: #cidade?c=3304557&m=regiao ... */
const PARAMS = { c: "cidade", m: "modo", r: "regiao", comp: "comp", ind: "ind", gc: "gc", fr: "fReg", fx: "fFx", kt: "tabCtl", kr: "kReg", kc: "kCid", e: "etapa" };
const NUM = new Set(["cidade", "gc", "kCid"]);
function lerHash() {
  const [rota_, q] = (location.hash || "#inicio").slice(1).split("?"); const p = new URLSearchParams(q || "");
  for (const [k, campo] of Object.entries(PARAMS)) if (p.has(k)) S[campo] = NUM.has(campo) ? +p.get(k) : p.get(k);
  if (S.cidade && !cid(S.cidade)) S.cidade = CAP.c;
  return rota_;
}
function sincroniza() {
  const r = (location.hash || "#inicio").slice(1).split("?")[0], p = new URLSearchParams();
  const usa = { cidade: ["c", "m", "r", "comp", "ind"], gestor: ["c", "fr", "fx", "gc"], controle: ["kt", "kr", "kc"], como: ["e"] }[r] || [];
  usa.forEach(k => { const v = S[PARAMS[k]]; if (v !== undefined && v !== "" && v !== 0 && v !== null) p.set(k, v); });
  const q = p.toString(); history.replaceState(null, "", "#" + r + (q ? "?" + q : ""));
}

/* planilha .xlsx sem biblioteca: arquivos XML dentro de um zip sem compressão */
const CRC = (() => { const t = []; for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
const crc32 = b => { let c = 0xFFFFFFFF; for (let i = 0; i < b.length; i++) c = CRC[(c ^ b[i]) & 255] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
function zipSimples(arqs) {
  const enc = new TextEncoder(), partes = [], central = []; let pos = 0;
  const u16 = v => [v & 255, v >> 8 & 255], u32 = v => [v & 255, v >> 8 & 255, v >> 16 & 255, v >>> 24];
  Object.entries(arqs).forEach(([nome, txt]) => {
    const n = enc.encode(nome), d = enc.encode(txt), c = crc32(d);
    const h = new Uint8Array([0x50, 0x4b, 3, 4, 20, 0, 0, 8, 0, 0, 0, 0, 0x21, 0, ...u32(c), ...u32(d.length), ...u32(d.length), ...u16(n.length), 0, 0]);
    partes.push(h, n, d);
    central.push(new Uint8Array([0x50, 0x4b, 1, 2, 20, 0, 20, 0, 0, 8, 0, 0, 0, 0, 0x21, 0, ...u32(c), ...u32(d.length), ...u32(d.length), ...u16(n.length), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...u32(pos)]), n);
    pos += h.length + n.length + d.length;
  });
  const tam = central.reduce((a, b) => a + b.length, 0), N = Object.keys(arqs).length;
  const fim = new Uint8Array([0x50, 0x4b, 5, 6, 0, 0, 0, 0, ...u16(N), ...u16(N), ...u32(tam), ...u32(pos), 0, 0]);
  return new Blob([...partes, ...central, fim], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
}
const xe = s => String(s).replace(/[&<>"]/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m]));
const colL = i => { let s = "", n = i + 1; while (n > 0) { const m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); } return s; };
/* aba = { nome, cab: [[título, estilo]], linhas: [[valores]], larg } ; estilo: 0 texto, 2 inteiro, 3 uma casa, 4 duas casas, 5 texto com quebra */
function xlsxBlob(abas) {
  const sheet = a => {
    const n = a.linhas.length + 1, cols = a.cab.length;
    let x = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0">${a.sobre ? "" : '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'}</sheetView></sheetViews><cols>${a.cab.map((c, i) => `<col min="${i + 1}" max="${i + 1}" width="${i === 0 ? (a.larg0 || 30) : (a.larg || 16)}" customWidth="1"/>`).join("")}</cols><sheetData>`;
    x += `<row r="1" ht="${a.sobre ? 20 : 48}" customHeight="1">${a.cab.map((c, i) => `<c r="${colL(i)}1" s="1" t="inlineStr"><is><t>${xe(c[0])}</t></is></c>`).join("")}</row>`;
    a.linhas.forEach((l, r) => { x += `<row r="${r + 2}">` + l.map((v, i) => { const ref = colL(i) + (r + 2), st = a.cab[i][1]; if (v === null || v === undefined || v === "") return ""; return typeof v === "number" && Number.isFinite(v) ? `<c r="${ref}" s="${st}"><v>${v}</v></c>` : `<c r="${ref}" s="${st === 5 ? 5 : 0}" t="inlineStr"><is><t>${xe(v)}</t></is></c>`; }).join("") + "</row>"; });
    return x + `</sheetData>${a.sobre ? "" : `<autoFilter ref="A1:${colL(cols - 1)}${n}"/>`}</worksheet>`;
  };
  const arq = {};
  arq["[Content_Types].xml"] = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>${abas.map((a, i) => `<Override PartName="/xl/worksheets/sheet${i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`).join("")}</Types>`;
  arq["_rels/.rels"] = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>`;
  arq["xl/workbook.xml"] = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>${abas.map((a, i) => `<sheet name="${xe(a.nome)}" sheetId="${i + 1}" r:id="rId${i + 1}"/>`).join("")}</sheets></workbook>`;
  arq["xl/_rels/workbook.xml.rels"] = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${abas.map((a, i) => `<Relationship Id="rId${i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${i + 1}.xml"/>`).join("")}<Relationship Id="rId${abas.length + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`;
  arq["xl/styles.xml"] = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><numFmts count="1"><numFmt numFmtId="164" formatCode="#,##0.0"/></numFmts><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF002147"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="6"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment wrapText="1" vertical="center"/></xf><xf numFmtId="3" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="2" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf></cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>`;
  abas.forEach((a, i) => arq[`xl/worksheets/sheet${i + 1}.xml`] = sheet(a));
  return zipSimples(arq);
}
function baixaBlob(blob, nome) { const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = nome; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500); }
const COLS_CID = [["Cidade", 0, "n"], ["Região", 0, "r"], ["Grupo do estudo", 0, "g"], ["População", 2, "pop"], ["Gasto em saúde por habitante (R$, 2024)", 3, "gh"], ["Receita por habitante (R$, 2024)", 3, "rh"], ["Parte da despesa em saúde (%)", 4, "pd"], ["Saúde como parte da receita (%)", 4, "fa"], ["Aplicado em saúde, SIOPS (%)", 4, "ap"], ["Folga sobre o mínimo de 15% (p.p.)", 4, "fo"], ["Queda do valor aplicado que zera a folga (%)", 3, "qz"], ["Parte da receita que vem de repasses (%)", 3, "pt"], ["Distância do previsto, 2023 (%)", 3, "r23"], ["Distância do previsto, 2024 (%)", 3, "r24"], ["Distância do previsto, 2025 (%)", 3, "r25"], ["Pessoal (% da RCL, 2024)", 4, "pes"], ["Limite prudencial (%)", 4, "prud"]];
function abaCidades(nome, l) { return { nome, cab: COLS_CID.map(c => [c[0], c[1]]), linhas: l.map(c => COLS_CID.map(k => c[k[2]] ?? null)), larg: 16 }; }
function baixaPlanilha(filtros, cidadesSel, parecidas) {
  const sobre = { nome: "Sobre", sobre: true, larg0: 140, cab: [["Saúde fiscal do Rio de Janeiro: planilha filtrada da página", 5]], linhas: [
    [`Versão ${D.meta.versao}, ${D.meta.data}. Janela dos dados: ${D.meta.janela_principal}.`], [`Filtros usados: ${filtros}.`], [`Linhas da aba Cidades: ${cidadesSel.length}.`],
    ["Fonte: Siconfi (Tesouro Nacional), SIOPS (Ministério da Saúde) e IBGE. Valores declarados pelos entes, não auditados."], ["Gasto em saúde por habitante não mede qualidade nem necessidade."], [`Repositório: ${D.meta.repositorio}`]] };
  const abas = [sobre, abaCidades("Cidades", cidadesSel)]; if (parecidas && parecidas.length) abas.push(abaCidades("Cidades parecidas", parecidas));
  return xlsxBlob(abas);
}
