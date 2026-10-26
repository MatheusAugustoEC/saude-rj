/* Página de entrega: Saúde fiscal do Rio de Janeiro. Todo número vem de DADOS (pipeline). */
"use strict";
const D = DADOS, C = D.cidades, UF = D.ufs, G = D.globais, EST = D.estado_rj, SIM = D.simulador;
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const fm = (x, c = 0) => x == null || Number.isNaN(x) ? "sem dado" : x.toLocaleString("pt-BR", { minimumFractionDigits: c, maximumFractionDigits: c });
const rs = (x, c = 0) => x == null ? "sem dado" : "R$ " + fm(x, c);
const pc = (x, c = 1) => x == null ? "sem dado" : fm(x, c) + "%";
const esc = s => String(s).replace(/[&<>"]/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m]));
const med = a => { const b = a.filter(x => x != null).sort((x, y) => x - y), n = b.length; return n ? (n % 2 ? b[(n - 1) / 2] : (b[n / 2 - 1] + b[n / 2]) / 2) : null; };
const quant = (a, q) => { const b = [...a].sort((x, y) => x - y); const i = (b.length - 1) * q, lo = Math.floor(i); return b[lo] + (b[Math.min(lo + 1, b.length - 1)] - b[lo]) * (i - lo); };
const CAP = C.find(c => c.c === 3304557);
const S = { cidade: CAP.c, modo: "cidade", comp: "pares", extras: [], ind: "gh", indBR: "gh", regiao: "Metropolitana", regExtras: [], regComp: "todas", metroAberta: false, ufSel: 33, fReg: "", fFx: "", curFiltro: {} };
const IND = { gh: ["Gasto em saúde por habitante", v => rs(v), "R$ por habitante, 2024"], pd: ["Parte da despesa que vai para a saúde", v => pc(v), "% da despesa, 2024"], rh: ["Receita por habitante", v => rs(v), "R$ por habitante, 2024"] };
const cid = c => C.find(x => x.c === c);
const NOMES_REG = { "Metropolitana": "Metropolitana" };
const GRUPO_NUM = {}; D.grupos.forEach((g, i) => GRUPO_NUM[g.k] = i + 1);
const GRUPO_COR = {}; D.grupos.forEach((g, i) => GRUPO_COR[g.k] = `var(--g${i + 1})`);

/* ---------- tooltip ---------- */
const tip = document.createElement("div"); tip.className = "tip"; tip.hidden = true; document.body.appendChild(tip);
document.onmousemove = e => {
  const t = e.target.closest && e.target.closest("[data-tip]");
  if (!t) { tip.hidden = true; return; }
  tip.innerHTML = t.getAttribute("data-tip"); tip.hidden = false;
  const w = tip.offsetWidth; tip.style.left = Math.min(e.clientX + 14, innerWidth - w - 8) + "px"; tip.style.top = (e.clientY + 16) + "px";
};
document.onscroll = () => { tip.hidden = true; };

/* ---------- geometria ---------- */
function rings(g) { return g.type === "Polygon" ? [g.coordinates] : g.coordinates; }
function projeta(geo, W, margem = 0) {
  let x0 = 1e9, x1 = -1e9, y0 = 1e9, y1 = -1e9, lat = 0, n = 0;
  geo.features.forEach(f => rings(f.geometry).forEach(p => p[0].forEach(([x, y]) => { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); lat += y; n++; })));
  const k = Math.cos((lat / n) * Math.PI / 180), s = (W - 2 * margem) / ((x1 - x0) * k), H = (y1 - y0) * s + 2 * margem;
  const P = ([x, y]) => [margem + (x - x0) * k * s, margem + (y1 - y) * s];
  const out = {};
  geo.features.forEach(f => {
    let d = "", best = null, bestA = -1;
    rings(f.geometry).forEach(p => {
      p.forEach((ring, ri) => { d += "M" + ring.map(pt => P(pt).map(v => v.toFixed(1)).join(",")).join("L") + "Z"; });
      const r = p[0].map(P); let a = 0, cx = 0, cy = 0;
      for (let i = 0; i < r.length - 1; i++) { const q = r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1]; a += q; cx += (r[i][0] + r[i + 1][0]) * q; cy += (r[i][1] + r[i + 1][1]) * q; }
      a /= 2; if (Math.abs(a) > bestA) { bestA = Math.abs(a); best = a ? [cx / (6 * a), cy / (6 * a)] : r[0]; }
    });
    out[f.properties.codarea] = { d, c: best, a: bestA };
  });
  return { W, H, out };
}
const PRJ_UF = projeta(GEO_UF, 560, 8), PRJ_RJ = projeta(GEO_RJ, 600, 6);

/* ---------- escalas ---------- */
const RAMPA = ["var(--r1)", "var(--r2)", "var(--r3)", "var(--r4)", "var(--r5)"];
function classes(vals) { const q = [0.2, 0.4, 0.6, 0.8].map(p => quant(vals, p)); return { q, cls: v => v == null ? -1 : q.filter(b => v >= b).length }; }
function legenda(cl, fmt) {
  const lim = [Math.min(...cl.vals), ...cl.q, Math.max(...cl.vals)];
  return `<div class="leg" aria-hidden="true">${RAMPA.map((c, i) => `<span><i style="background:${c}"></i> ${fmt(lim[i])} a ${fmt(lim[i + 1])}</span>`).join("")}</div>`;
}
function escala(vals) { const c = classes(vals); c.vals = vals; return c; }

/* ---------- gráficos em SVG ---------- */
function eixoLog(lo, hi) { const t = []; for (let e = Math.floor(Math.log10(lo)); e <= Math.ceil(Math.log10(hi)); e++) [1, 2, 5].forEach(m => { const v = m * 10 ** e; if (v >= lo && v <= hi) t.push(v); }); return t; }
function dispersao({ pts, xl, yl, fit, alt, W = 640, H = 380 }) {
  const m = { l: 62, r: 14, t: 12, b: 46 }, xs = pts.map(p => p.x), ys = pts.map(p => p.y);
  const x0 = Math.min(...xs) * 0.85, x1 = Math.max(...xs) * 1.15, y0 = Math.min(...ys) * 0.85, y1 = Math.max(...ys) * 1.15;
  const X = v => m.l + (Math.log(v) - Math.log(x0)) / (Math.log(x1) - Math.log(x0)) * (W - m.l - m.r), Y = v => H - m.b - (Math.log(v) - Math.log(y0)) / (Math.log(y1) - Math.log(y0)) * (H - m.t - m.b);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(alt)}">`;
  eixoLog(y0, y1).forEach(v => s += `<line class="gr" x1="${m.l}" x2="${W - m.r}" y1="${Y(v)}" y2="${Y(v)}"/><text class="mut" x="${m.l - 6}" y="${Y(v) + 4}" text-anchor="end" font-size="11">${fm(v)}</text>`);
  eixoLog(x0, x1).forEach(v => s += `<line class="gr" y1="${m.t}" y2="${H - m.b}" x1="${X(v)}" x2="${X(v)}"/><text class="mut" y="${H - m.b + 16}" x="${X(v)}" text-anchor="middle" font-size="11">${fm(v)}</text>`);
  s += `<line class="ax" x1="${m.l}" x2="${W - m.r}" y1="${H - m.b}" y2="${H - m.b}"/><line class="ax" x1="${m.l}" x2="${m.l}" y1="${m.t}" y2="${H - m.b}"/>`;
  s += `<text x="${(W + m.l) / 2}" y="${H - 6}" text-anchor="middle" font-size="12" class="mut">${esc(xl)}</text><text transform="translate(14 ${(H - m.b) / 2}) rotate(-90)" text-anchor="middle" font-size="12" class="mut">${esc(yl)}</text>`;
  if (fit) { const a = [x0, x1].map(v => [X(v), Y(Math.exp(fit.a + fit.b * Math.log(v)))]); s += `<line x1="${a[0][0]}" y1="${a[0][1]}" x2="${a[1][0]}" y2="${a[1][1]}" stroke="var(--mut)" stroke-width="1.5" stroke-dasharray="6 4"/>`; }
  pts.filter(p => !p.hl).forEach(p => s += `<circle cx="${X(p.x)}" cy="${Y(p.y)}" r="${p.r || 4}" fill="${p.cor || "var(--azul)"}" fill-opacity=".75" stroke="var(--bg)" stroke-width=".8" data-tip="${esc(p.tip)}"/>`);
  pts.filter(p => p.hl).forEach(p => { s += `<circle cx="${X(p.x)}" cy="${Y(p.y)}" r="${(p.r || 4) + 2.5}" fill="var(--verm)" stroke="var(--bg)" stroke-width="1.5" data-tip="${esc(p.tip)}"/>`; if (p.lab) { const right = X(p.x) < W * 0.62; s += `<text class="halo" x="${X(p.x) + (right ? 10 : -10)}" y="${Y(p.y) - 8}" text-anchor="${right ? "start" : "end"}" font-size="12" font-weight="700" style="fill:var(--verm)">${esc(p.lab)}</text>`; } });
  return s + "</svg>";
}
function ols(pts) { const n = pts.length, lx = pts.map(p => Math.log(p.x)), ly = pts.map(p => Math.log(p.y)), mx = lx.reduce((a, b) => a + b) / n, my = ly.reduce((a, b) => a + b) / n; let sxy = 0, sxx = 0, syy = 0; lx.forEach((v, i) => { sxy += (v - mx) * (ly[i] - my); sxx += (v - mx) ** 2; syy += (ly[i] - my) ** 2; }); const b = sxy / sxx; return { a: my - b * mx, b, r2: sxy * sxy / (sxx * syy) }; }
function barras({ rows, fmt, W = 620, rotW = 170, alt, linha, linhaRot, max }) {
  const h = 22, m = { t: 6, b: 26 }, H = rows.length * h + m.t + m.b, mx = max || Math.max(...rows.map(r => r.v), linha || 0) * 1.1, bw = W - rotW - 70;
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(alt)}">`;
  rows.forEach((r, i) => { const y = m.t + i * h, w = Math.max(0, r.v / mx * bw); s += `<text x="${rotW - 8}" y="${y + 15}" text-anchor="end" font-size="12" ${r.hl ? 'font-weight="700" style="fill:var(--verm)"' : ""}>${esc(r.l)}</text><rect x="${rotW}" y="${y + 3}" width="${w}" height="${h - 7}" rx="2" fill="${r.hl ? "var(--verm)" : r.cor || "var(--azul)"}" data-tip="${esc(r.tip || r.l + ": " + fmt(r.v))}"/><text x="${rotW + w + 5}" y="${y + 15}" font-size="12" class="mut">${fmt(r.v)}</text>`; });
  if (linha != null) { const x = rotW + linha / mx * bw; s += `<line x1="${x}" x2="${x}" y1="${m.t}" y2="${H - m.b}" stroke="var(--fg)" stroke-width="1.4" stroke-dasharray="5 3"/><text x="${x}" y="${H - 8}" text-anchor="middle" font-size="11" class="mut">${esc(linhaRot)}</text>`; }
  return s + "</svg>";
}
function colunas({ vals, rot, W = 620, H = 260, fmt, alt, destaque = -1, titulo }) {
  const m = { l: 40, r: 10, t: 18, b: 40 }, mx = Math.max(...vals) * 1.12, bw = (W - m.l - m.r) / vals.length;
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(alt)}"><line class="ax" x1="${m.l}" x2="${W - m.r}" y1="${H - m.b}" y2="${H - m.b}"/>`;
  vals.forEach((v, i) => { const h = v / mx * (H - m.b - m.t), x = m.l + i * bw; s += `<rect x="${x + 3}" y="${H - m.b - h}" width="${bw - 6}" height="${h}" fill="${i === destaque ? "var(--verm)" : "var(--azul)"}" data-tip="${esc(rot[i] + ": " + fmt(v))}"/><text x="${x + bw / 2}" y="${H - m.b - h - 4}" text-anchor="middle" font-size="11">${fmt(v)}</text><text x="${x + bw / 2}" y="${H - m.b + 15}" text-anchor="middle" font-size="11" class="mut">${esc(rot[i])}</text>`; });
  return s + "</svg>";
}
function histograma(vals, nb, fmt, selVal, alt) {
  const lo = Math.log(Math.min(...vals)), hi = Math.log(Math.max(...vals)), b = Array(nb).fill(0), edges = [];
  for (let i = 0; i <= nb; i++) edges.push(Math.exp(lo + (hi - lo) * i / nb));
  vals.forEach(v => { let i = Math.min(nb - 1, Math.floor((Math.log(v) - lo) / (hi - lo) * nb)); b[i]++; });
  const W = 620, H = 250, m = { l: 36, r: 10, t: 14, b: 44 }, bw = (W - m.l - m.r) / nb, mx = Math.max(...b) * 1.15;
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(alt)}"><line class="ax" x1="${m.l}" x2="${W - m.r}" y1="${H - m.b}" y2="${H - m.b}"/>`;
  const sIdx = selVal == null ? -1 : Math.min(nb - 1, Math.floor((Math.log(selVal) - lo) / (hi - lo) * nb));
  b.forEach((n, i) => { const h = n / mx * (H - m.b - m.t), x = m.l + i * bw; s += `<rect x="${x + 1}" y="${H - m.b - h}" width="${bw - 2}" height="${h}" fill="${i === sIdx ? "var(--verm)" : "var(--azul)"}" data-tip="${n} cidades entre ${fmt(edges[i])} e ${fmt(edges[i + 1])}"/>`; if (n) s += `<text x="${x + bw / 2}" y="${H - m.b - h - 3}" text-anchor="middle" font-size="10" class="mut">${n}</text>`; });
  [0, Math.floor(nb / 2), nb].forEach(i => s += `<text x="${m.l + i * bw}" y="${H - m.b + 15}" text-anchor="middle" font-size="11" class="mut">${fmt(edges[i])}</text>`);
  return s + `<text x="${W / 2}" y="${H - 6}" text-anchor="middle" font-size="12" class="mut">Escala logarítmica; cada coluna mostra quantas cidades caem na faixa</text></svg>`;
}
function curva(alt) {
  const ord = [...C].sort((a, b) => a.gh - b.gh), tot = ord.reduce((a, c) => a + c.pop, 0); let ac = 0;
  const W = 620, H = 300, m = { l: 56, r: 14, t: 14, b: 44 }, mx = Math.max(...C.map(c => c.gh)) * 1.05, X = p => m.l + p / 100 * (W - m.l - m.r), Y = v => H - m.b - v / mx * (H - m.t - m.b);
  let d = `M${X(0)},${Y(ord[0].gh)}`; ord.forEach(c => { d += `L${X(ac / tot * 100)},${Y(c.gh)}`; ac += c.pop; d += `L${X(ac / tot * 100)},${Y(c.gh)}`; });
  const yMed = Y(G.mediana_gh), xMed = X(G.pop_abaixo_mediana_pct);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(alt)}">`;
  [0, 2000, 4000, 6000].forEach(v => s += `<line class="gr" x1="${m.l}" x2="${W - m.r}" y1="${Y(v)}" y2="${Y(v)}"/><text class="mut" x="${m.l - 6}" y="${Y(v) + 4}" text-anchor="end" font-size="11">${fm(v)}</text>`);
  [0, 25, 50, 75, 100].forEach(p => s += `<text class="mut" x="${X(p)}" y="${H - m.b + 16}" text-anchor="middle" font-size="11">${p}%</text>`);
  s += `<path d="${d}" fill="none" stroke="var(--azul)" stroke-width="2.2"/><line x1="${m.l}" x2="${xMed}" y1="${yMed}" y2="${yMed}" stroke="var(--verm)" stroke-width="1.4" stroke-dasharray="5 3"/><line x1="${xMed}" x2="${xMed}" y1="${yMed}" y2="${H - m.b}" stroke="var(--verm)" stroke-width="1.4" stroke-dasharray="5 3"/>`;
  s += `<circle cx="${xMed}" cy="${yMed}" r="5" fill="var(--verm)"/><text x="${xMed - 8}" y="${yMed - 10}" text-anchor="end" font-size="12" font-weight="700" style="fill:var(--verm)">${pc(G.pop_abaixo_mediana_pct, 0)} das pessoas moram em cidades abaixo da do meio</text>`;
  return s + `<text x="${(W + m.l) / 2}" y="${H - 6}" text-anchor="middle" font-size="12" class="mut">Parcela acumulada da população, das cidades que menos gastam às que mais gastam</text></svg>`;
}

/* ---------- peças de página ---------- */
const sel1 = (id, rot, opts, val) => `<label>${rot}<select id="${id}">${opts.map(o => `<option value="${esc(o[0])}"${String(o[0]) === String(val) ? " selected" : ""}>${esc(o[1])}</option>`).join("")}</select></label>`;
const card = (t, corpo, sub = "") => `<section class="card"><div class="tit"><span>${t}</span>${sub ? `<small>${sub}</small>` : ""}</div><div class="corpo">${corpo}</div></section>`;
const chipV = v => `<span class="chip ${/^Sustent/.test(v) ? "ok" : /^N[ãa]o/.test(v) ? "no" : "cn"}">${esc(v)}</span>`;
function curios(sec, { max = 99, so = null } = {}) {
  return D.curiosidades.filter(c => c.s === sec && (!so || c.t === so)).slice(0, max);
}
function cardCur(c) { return `<div class="cur${c.d ? " d" : ""}">${c.v ? `<span class="v">${esc(c.v)}</span>` : ""}<span class="t">${esc(c.ti)}</span><span class="x">${esc(c.x)}</span><span class="m"><span class="chip ${c.t}">${c.t}</span><span>${esc(c.j)}</span></span></div>`; }
function voceSabia(sec, titulo = "Você sabia?") {
  const todos = curios(sec), l = [...todos.filter(c => c.t === "Curiosidade" || c.t === "Insight"), ...todos.filter(c => !(c.t === "Curiosidade" || c.t === "Insight"))].slice(0, 4);
  return `<h2>${titulo}</h2><div class="sabia">${l.map(cardCur).join("")}</div>`;
}
function maisItens(sec, id) {
  const todos = curios(sec);
  return `<details class="mais" id="${id}"><summary>Quero ver mais curiosidades, insights e alertas desta parte</summary><div class="ctrl" style="margin-top:12px"><div class="seg" role="group" aria-label="Filtrar por tipo">${["Tudo", "Curiosidade", "Insight", "Alerta", "Achado"].map((t, i) => `<button aria-pressed="${i === 0}" data-f="${t}">${t === "Tudo" ? "Tudo" : t + "s"}</button>`).join("")}</div></div><div class="sabia" data-lista>${todos.map(cardCur).join("")}</div><p class="nota">Cada item traz a janela de tempo; as fontes estão em <a href="#biblioteca">Biblioteca</a>. Alerta e achado são perguntas para olhar, não conclusões.</p></details>`;
}
function ligaMais(id, sec) {
  const d = $("#" + id); if (!d) return; const todos = curios(sec);
  $$("button[data-f]", d).forEach(b => b.onclick = () => { $$("button[data-f]", d).forEach(x => x.setAttribute("aria-pressed", x === b)); const f = b.dataset.f; $("[data-lista]", d).innerHTML = todos.filter(c => f === "Tudo" || c.t === f).map(cardCur).join("") || '<p class="nota">Nada deste tipo nesta parte.</p>'; });
}
function listaRank(itens, selKey, fmt, onSel, cor) {
  const ul = document.createElement("div"); ul.className = "lista";
  ul.innerHTML = `<ol>${itens.map((it, i) => `<li tabindex="0" data-k="${it.k}" class="${it.k == selKey ? "sel" : ""}"><span class="pos">${i + 1}º</span><span class="sw" style="background:${cor ? cor(it) : "var(--azul)"}"></span><span class="nm">${esc(it.n)}</span><span class="vl">${fmt(it.v)}</span></li>`).join("")}</ol>`;
  $$("li", ul).forEach(li => { li.onclick = () => onSel(li.dataset.k); li.onkeydown = e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onSel(li.dataset.k); } }; });
  return ul;
}
function centraNaLista(box) { const s = $("li.sel", box); if (s) box.scrollTop = Math.max(0, s.offsetTop - box.clientHeight / 2 + s.clientHeight / 2 - 8); }
