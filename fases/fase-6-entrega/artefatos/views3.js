/* ---------- Biblioteca ---------- */
const GRUPOS_BIB = ["Para ler", "Imagens e gráficos", "Planilhas, dados e apresentação", "Para reproduzir e citar"];
const CITACAO = `MatheusAugustoEC. Saúde fiscal do Rio de Janeiro: gasto em saúde por habitante nas 92 cidades e no estado, Siconfi 2023 a 2025. Versão ${D.meta.versao}, ${D.meta.data}. ${D.meta.repositorio}`;
function viewBiblioteca(el) {
  const uniq = k => [...new Set(BIB.map(b => b[k]).filter(Boolean))];
  el.innerHTML = `<h1>Biblioteca: tudo o que o projeto produziu, para baixar</h1><p class="lede">Relatórios, imagens, planilhas e dados. Cada item diz para quem serve, de que etapa vem e quanto pesa.</p>
  <div class="ctrl"><label>Buscar<input type="search" id="bBusca" placeholder="Palavra do título ou da descrição"></label>${sel1("bPara", "Para quem", [["", "Todos"], ...uniq("para").map(x => [x, x])], "")}${sel1("bTipo", "Tipo", [["", "Todos"], ...uniq("tipo").map(x => [x, x])], "")}${sel1("bEtapa", "Etapa", [["", "Todas"], ...uniq("etapa").map(x => [x, x])], "")}${sel1("bAno", "Ano dos dados", [["", "Todos"], ...uniq("ano").map(x => [x, x])], "")}<a class="btn" href="arquivos/saude-fiscal-rj-biblioteca.zip" download>Baixar tudo (.zip)</a><button class="btn sec" id="bPptx">Baixar a apresentação (.pptx)</button></div><div id="bTags" class="tags"></div><div id="bOut"></div>`;
  const f = { q: "", para: "", tipo: "", etapa: "", ano: "" };
  const draw = () => {
    const ok = b => (!f.q || normaliza(b.titulo + " " + b.desc).includes(normaliza(f.q))) && (!f.para || b.para === f.para) && (!f.tipo || b.tipo === f.tipo) && (!f.etapa || b.etapa === f.etapa) && (!f.ano || b.ano === f.ano);
    $("#bTags").innerHTML = [["para", f.para], ["tipo", f.tipo], ["etapa", f.etapa], ["ano", f.ano]].filter(t => t[1]).map(t => `<span class="tag">${esc(t[1])}<button data-rt="${t[0]}" aria-label="Remover filtro">×</button></span>`).join("");
    $$("[data-rt]", el).forEach(b => b.onclick = () => { f[b.dataset.rt] = ""; $("#b" + { para: "Para", tipo: "Tipo", etapa: "Etapa", ano: "Ano" }[b.dataset.rt]).value = ""; draw(); });
    let h = "";
    GRUPOS_BIB.forEach(g => {
      const l = BIB.filter(b => b.grupo === g && ok(b)); h += `<h2>${g} <span class="pill">${l.length}</span></h2>`;
      if (!l.length) { h += `<p class="nota">Nenhum item com esses filtros.</p>`; return; }
      h += `<div class="biblio">${l.map(b => `<div class="arq">${b.img ? `<img src="${b.arq}" alt="${esc(b.alt || b.titulo)}" loading="lazy">` : ""}<h4>${esc(b.titulo)}</h4><p>${esc(b.desc)}</p><span class="m">${esc(b.para)} · ${esc(b.etapa)} · ${esc(b.ano)} · ${esc(b.tipo)} · ${esc(b.tam)} · ${esc(b.data)}</span><div class="acoes">${b.ext ? `<a class="btn" href="${b.arq}" target="_blank" rel="noopener">Abrir no GitHub</a>` : `<a class="btn" href="${b.arq}" download>Baixar</a>`}</div></div>`).join("")}${g === "Para reproduzir e citar" ? `<div class="arq"><h4>Como citar</h4><p>${esc(CITACAO)}</p><div class="acoes"><button class="btn sec" id="bCita">Copiar citação</button></div></div>` : ""}</div>`;
    });
    $("#bOut").innerHTML = h;
    const bc = $("#bCita"); if (bc) bc.onclick = () => { const ok = () => { bc.textContent = "Copiado"; }; try { navigator.clipboard.writeText(CITACAO).then(ok, () => { bc.textContent = "Selecione e copie o texto acima"; }); } catch (e) { bc.textContent = "Selecione e copie o texto acima"; } };
  };
  $("#bBusca").oninput = e => { f.q = e.target.value; draw(); };
  [["bPara", "para"], ["bTipo", "tipo"], ["bEtapa", "etapa"], ["bAno", "ano"]].forEach(([id, k]) => $("#" + id).onchange = e => { f[k] = e.target.value; draw(); });
  $("#bPptx").onclick = geraPptx;
  draw();
}

/* ---------- apresentação (.pptx) feita no navegador, a partir dos mesmos dados ---------- */
function geraPptx() {
  if (typeof PptxGenJS === "undefined") { alert("A biblioteca de apresentação não carregou."); return; }
  const p = new PptxGenJS(); p.layout = "LAYOUT_WIDE"; p.title = "Saúde fiscal do Rio de Janeiro";
  const NAVY = "002147", AZ = "286BBB", VM = "B13507", CINZA = "55626F";
  const nit = C.find(c => c.n === "Niterói"), bl = C.filter(c => c.r === "Baixadas Litorâneas");
  const regs = [...D.regioes].sort((a, b) => b.gh - a.gh);
  const S_ = [
    ["O Rio gasta menos em saúde por habitante do que qualquer outro estado", `${EST.pos_gh}º de 27`, `O estado gasta ${rs(EST.gh)} por habitante, 2024. Esfera estadual: não comparável diretamente com a das cidades.`],
    [`Dentro do estado, as cidades variam ${fm(G.razao_extremos, 0)} vezes`, `${fm(G.razao_extremos, 1)}×`, `${G.maior_nome} (${rs(G.maior_gh)}) contra ${G.menor_nome} (${rs(G.menor_gh)}) por habitante, 2024.`],
    ["A receita por habitante explica cerca de 80% da diferença", `${fm(G.r2_total * 100, 0)}%`, `Sensibilidade do gasto à receita: ${fm(G.elast_total[2024], 2)} em 2024 e ${fm(G.elast_total[2023], 2)} em 2023.`],
    ["O gasto segue os repasses, e não a arrecadação própria", `${fm(SIM.entre.rep[0], 2)} × ${fm(SIM.entre.prop[0], 2)}`, "Sensibilidade do gasto aos repasses contra a da arrecadação própria, entre cidades, 2024. Dentro de uma cidade, a da arrecadação própria não se distingue de zero."],
    [`Comparar por receita parecida reduz a diferença em ${G.pares_reducao}%`, `−${G.pares_reducao}%`, `De ${fm(G.dif_regiao, 3)} (por região) para ${fm(G.dif_pares, 3)} (por faixa de receita), 2024. Em parte por construção.`],
    ["A triagem serve para perguntar, não para fazer lista fixa", `${C.filter(c => c.o24).length} cidades`, "Fora do intervalo em 2024. A ordem das cidades se mantém em 2025; a lista exata enfraqueceu."],
    ["Niterói fica fora da faixa esperada três anos seguidos", `${fm(nit.r25, 0)}%`, `Em 2025 (${fm(nit.r23, 0)}% em 2023 e ${fm(nit.r24, 0)}% em 2024), em relação ao que a receita prevê. Um alerta é um convite para olhar, não uma conclusão.`],
    [`${C.filter(c => c.ap >= 15).length} de 92 cumprem o mínimo de 15%, e ${G.folga_menor1} estão a menos de 1 ponto`, `${G.folga_menor1} cidades`, "Aplicam menos de 1 ponto percentual acima do mínimo de 15% (SIOPS), 2024."],
    ["Oito das nove conclusões se mantiveram num ano novo", `${G.k_sustentam} de ${G.k_total}`, "Previsões escritas antes de abrir os dados de 2025."],
    ["O que ficou sem explicação: Baixadas Litorâneas", `${fm(med(bl.map(c => c.r24)), 0)}%`, "Resíduo mediano das dez cidades, 2024. Corrigir a população pelo veraneio não explicou."],
    ["O que mais atrapalhou foi conseguir os dados", "Fontes", "SUS fora do ar, Distrito Federal indisponível no SIOPS, populações diferentes entre Tesouro e IBGE, balanços de 2025 atrasados."],
    ["Limites: gasto não é qualidade, e o dado é declarado", "Cuidado", "Os números são declarados pelas prefeituras e não foram auditados. Gasto por habitante não mede qualidade nem necessidade."]
  ];
  S_.forEach((t, i) => {
    const s = p.addSlide(); s.background = { color: "FFFFFF" };
    s.addShape(p.ShapeType.rect, { x: 0, y: 0, w: 13.33, h: 0.12, fill: { color: VM } });
    s.addText(t[0], { x: 0.6, y: 0.4, w: 12.1, h: 1.3, fontFace: "Georgia", fontSize: 30, bold: true, color: NAVY, valign: "top" });
    s.addText(t[1], { x: 0.6, y: 2.0, w: 5.2, h: 1.6, fontFace: "Calibri", fontSize: 54, bold: true, color: i === 0 ? VM : AZ, valign: "middle" });
    s.addText(t[2], { x: 6.0, y: 2.0, w: 6.7, h: 1.6, fontFace: "Calibri", fontSize: 18, color: "1B2733", valign: "middle" });
    if (i === 0) s.addChart(p.charts.BAR, [{ name: "Gasto por habitante (R$)", labels: regs.map(r => r.k), values: regs.map(r => r.gh) }], { x: 0.6, y: 3.8, w: 12.1, h: 3.2, barDir: "bar", chartColors: [AZ], showValue: true, dataLabelFormatCode: "#,##0", catAxisLabelFontSize: 11, valAxisHidden: true, valGridLine: { style: "none" }, showTitle: true, title: "Gasto em saúde por habitante por região do estado, R$, 2024", titleFontSize: 12 });
    s.addText(`Fonte: Siconfi e SIOPS, ${D.meta.janela_principal}; dados declarados, não auditados. Versão ${D.meta.versao}, ${D.meta.data}. ${D.meta.repositorio}`, { x: 0.6, y: 7.0, w: 12.1, h: 0.35, fontSize: 10, color: CINZA, fontFace: "Calibri" });
    s.addText(`${i + 1} / ${S_.length}`, { x: 11.9, y: 7.0, w: 0.9, h: 0.35, fontSize: 10, color: CINZA, align: "right" });
  });
  p.writeFile({ fileName: "saude-fiscal-rj-apresentacao.pptx" });
}

/* ---------- roteador, tema, rodapé ---------- */
const ROTAS = { inicio: viewInicio, cidade: viewCidade, gestor: viewGestor, controle: viewControle, como: viewComo, biblioteca: viewBiblioteca };
const TITULOS = { inicio: "Início", cidade: "Cidade", gestor: "Gestor", controle: "Controle e auditoria", como: "Como cheguei aqui", biblioteca: "Biblioteca" };
function rota() {
  const k = (location.hash || "#inicio").slice(1); const r = ROTAS[k] ? k : "inicio";
  $$("nav a").forEach(a => a.removeAttribute("aria-current")); const a = $(`nav a[href="#${r}"]`); if (a) a.setAttribute("aria-current", "page");
  const el = $("#conteudo"); el.innerHTML = ""; ROTAS[r](el); document.title = TITULOS[r] + " · Saúde fiscal do Rio de Janeiro"; window.scrollTo(0, 0); tip.hidden = true;
}
function iniciaTema() {
  const b = $("#tema"); let t = ""; try { t = localStorage.getItem("tema") || ""; } catch (e) { }
  const ap = () => { if (t) document.documentElement.setAttribute("data-theme", t); else document.documentElement.removeAttribute("data-theme"); b.textContent = t === "dark" ? "Tema: escuro" : t === "light" ? "Tema: claro" : "Tema: automático"; try { localStorage.setItem("tema", t); } catch (e) { } };
  b.onclick = () => { t = t === "" ? "light" : t === "light" ? "dark" : ""; ap(); const h = (location.hash || "#inicio").slice(1); if (ROTAS[h]) rota(); }; ap();
}
$("#subbar").innerHTML = `Siconfi · 92 cidades + estado · 2023 a 2025 · Dados declarados, não auditados · Versão ${D.meta.versao} · ${D.meta.data} · <a href="${D.meta.repositorio}" target="_blank" rel="noopener">Repositório</a>`;
window.onhashchange = rota; iniciaTema(); rota();
