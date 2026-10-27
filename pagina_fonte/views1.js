/* ---------- Início (só estados) ---------- */
const CALL_DIR = { RN: 1, PB: 1, PE: 1, AL: 1, SE: 1, DF: 1, ES: 1, RJ: 1, AC: -1 };
function mapaBR(ind) {
  const vals = UF.map(u => u[ind]), E = escala(vals), fmt = v => IND[ind][1](v).replace("R$ ", "");
  const W = PRJ_UF.W, H = PRJ_UF.H; let s = `<svg viewBox="-120 0 ${W + 240} ${H}" role="img" aria-label="Mapa do Brasil por estado: ${esc(IND[ind][0])}, 2024. O Rio de Janeiro aparece em vermelho e tem o menor valor entre os 27 estados.">`;
  const cent = [];
  UF.forEach(u => {
    const g = PRJ_UF.out[u.c]; if (!g) return; const rj = u.s === "RJ", k = E.cls(u[ind]);
    s += `<path d="${g.d}" fill="${rj ? "var(--verm)" : RAMPA[k]}" data-uf="${u.c}" data-tip="${esc(u.n)}: ${IND[ind][1](u[ind])}" style="${S.ufSel === u.c && !rj ? "stroke:var(--fg);stroke-width:2" : ""}"/>`;
    if (CALL_DIR[u.s]) cent.push({ u, g }); else s += `<text class="${k < 2 ? "t1" : "t2"}" x="${g.c[0]}" y="${g.c[1] - 1}" text-anchor="middle" font-size="${g.a > 3000 ? 11 : 8.5}">${u.s}</text><text class="${k < 2 ? "t1" : "t2"}" x="${g.c[0]}" y="${g.c[1] + 9}" text-anchor="middle" font-size="${g.a > 3000 ? 9.5 : 7.5}">${fmt(u[ind])}</text>`;
  });
  const dir = cent.filter(o => CALL_DIR[o.u.s] > 0).sort((a, b) => a.g.c[1] - b.g.c[1]); let y = 0;
  dir.forEach(o => { y = Math.max(y + 24, o.g.c[1] - 10); o.y = y; });
  const ult = dir[dir.length - 1].y; if (ult > H - 16) dir.forEach(o => o.y -= ult - (H - 16));
  dir.forEach(o => { const x = W + 14; s += `<polyline class="lead" points="${o.g.c[0]},${o.g.c[1]} ${x - 6},${o.y} ${x},${o.y}"/><text class="out" x="${x + 4}" y="${o.y + 4}" font-size="11" font-weight="${o.u.s === "RJ" ? 800 : 600}" ${o.u.s === "RJ" ? 'style="fill:var(--verm)"' : ""}>${o.u.s} ${fmt(o.u[ind])}</text>`; });
  cent.filter(o => CALL_DIR[o.u.s] < 0).forEach(o => { s += `<polyline class="lead" points="${o.g.c[0]},${o.g.c[1]} -40,${o.g.c[1] - 20} -44,${o.g.c[1] - 20}"/><text class="out" x="-46" y="${o.g.c[1] - 16}" text-anchor="end" font-size="11" font-weight="600">${o.u.s} ${fmt(o.u[ind])}</text>`; });
  return { svg: s + "</svg>", E, fmt };
}
function viewInicio(el) {
  el.innerHTML = `<h1>O Rio de Janeiro gasta menos em saúde por habitante do que qualquer outro estado do Brasil.</h1>
  <p class="lede">Gasto em saúde por habitante em 2024, a partir das contas que os 26 estados e o Distrito Federal declaram ao Tesouro Nacional (Siconfi). Dados declarados, não auditados. Para ver as cidades do Rio, vá para <a href="#cidade">Cidade</a>.</p>
  <div class="blocos">
    <div class="bloco v"><b>${EST.pos_gh}º de 27</b><span>posição do estado do Rio em gasto em saúde por habitante (R$ ${fm(EST.gh)}), 2024</span></div>
    <div class="bloco v"><b>${EST.pos_pd}º de 27</b><span>posição do estado do Rio na parte da despesa que vai para a saúde (${pc(EST.pd)}), 2024</span></div>
    <div class="bloco"><b>${EST.pos_rh}º de 27</b><span>posição do estado do Rio em receita por habitante (R$ ${fm(EST.rh)}), 2024</span></div>
    <div class="bloco v"><b>${pc(EST.dcl)}</b><span>da receita corrente líquida é a dívida líquida do estado, acima do limite de ${EST.lim_dcl}% (2024)</span></div>
  </div>
  <section class="card"><div class="tit"><span>O estado diante do Brasil</span><small>27 unidades da federação</small></div><div class="corpo">
    <div class="ctrl">${sel1("indBR", "Indicador", Object.keys(IND).map(k => [k, IND[k][0]]), S.indBR)}</div>
    <p class="nota" id="defBR"></p>
    <div class="grade"><div class="mapa" id="mapaBR"></div><div id="listaBR"></div></div>
    <div id="legBR"></div>
    <p class="nota" id="notaBR"></p>
    ${fonte("Siconfi (Tesouro Nacional): RREO e DCA de 2024, 26 estados e Distrito Federal; população estimada pelo IBGE. Arquivo: dados_tratados/indicadores_2024.csv.")}</div></section>
  ${voceSabia("inicio")}
  ${maisItens("inicio", "maisInicio")}
  <h2>Por onde seguir</h2>
  <div class="etapas"><a class="card" style="padding:14px;text-decoration:none;color:inherit" href="#cidade"><b>Cidade</b><br><span class="nota">A sua cidade em uma tela: posição, comparação e regiões.</span></a><a class="card" style="padding:14px;text-decoration:none;color:inherit" href="#gestor"><b>Gestor</b><br><span class="nota">Cidades parecidas, simulador de repasses e folga sobre o mínimo.</span></a><a class="card" style="padding:14px;text-decoration:none;color:inherit" href="#controle"><b>Controle e auditoria</b><br><span class="nota">Triagem por ano, conferência entre fontes e limites fiscais.</span></a><a class="card" style="padding:14px;text-decoration:none;color:inherit" href="#como"><b>Como cheguei aqui</b><br><span class="nota">As cinco etapas do projeto e o que cada uma decidiu.</span></a></div>`;
  const DEF = { gh: "Gasto em saúde por habitante: despesa em saúde declarada pelo estado ÷ população estimada pelo IBGE, em reais de 2024.", pd: "Parte da despesa: quanto da despesa total do estado foi para a função Saúde, em %.", rh: "Receita por habitante: receita total declarada pelo estado ÷ população estimada pelo IBGE, em reais de 2024." };
  const draw = () => {
    const ind = S.indBR, m = mapaBR(ind);
    $("#defBR").textContent = DEF[ind];
    $("#mapaBR").innerHTML = m.svg;
    $$("#mapaBR path").forEach(p => p.onclick = () => { S.ufSel = +p.dataset.uf; draw(); });
    const itens = UF.map(u => ({ k: u.c, n: `${u.n} (${u.s})`, v: u[ind] })).sort((a, b) => b.v - a.v);
    const l = listaRank(itens, S.ufSel, v => m.fmt(v), k => { S.ufSel = +k; draw(); }, it => it.k === 33 ? "var(--verm)" : RAMPA[m.E.cls(it.v)]);
    $("#listaBR").innerHTML = ""; $("#listaBR").appendChild(l); centraNaLista(l);
    $("#legBR").innerHTML = legenda(m.E, v => m.fmt(v));
    const u = UF.find(x => x.c === S.ufSel), pos = UF.filter(x => x[ind] > u[ind]).length + 1;
    $("#notaBR").innerHTML = `<b>${esc(u.n)}</b>: ${IND[ind][1](u[ind])}, ${pos}º de 27. ${IND[ind][2]}. Cada tom de azul reúne cinco ou seis estados (quintis). O Rio de Janeiro aparece em vermelho. Toque ou clique num estado para destacá-lo na lista.`;
  };
  $("#indBR").onchange = e => { S.indBR = e.target.value; draw(); };
  draw(); ligaMais("maisInicio", "inicio");
}

/* ---------- Cidade ---------- */
function peers(c) { return C.filter(x => x.fx === c.fx && x.c !== c.c); }
function posIn(c, k) { return C.filter(x => x[k] > c[k]).length + 1; }
function mapaRJ({ cor, selSet = [], peersSet = [], rotulo }) {
  const W = PRJ_RJ.W, H = PRJ_RJ.H; let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(rotulo)}">`, lab = "";
  C.forEach(c => {
    const g = PRJ_RJ.out[c.c]; if (!g) return; const f = cor(c), sel = selSet.includes(c.c), pe = peersSet.includes(c.c);
    s += `<path d="${g.d}" fill="${sel ? "var(--verm)" : f}" data-c="${c.c}" data-tip="${esc(c.n)}: ${esc(cor.tip ? cor.tip(c) : "")}" style="${pe ? "stroke:var(--navy);stroke-width:1.6;stroke-dasharray:3 2" : ""}${sel ? ";stroke:var(--fg);stroke-width:1.6" : ""}"/>`;
    if (sel) { const right = g.c[0] < W * 0.6; lab += `<text class="halo" x="${g.c[0] + (right ? 12 : -12)}" y="${g.c[1] - 10}" text-anchor="${right ? "start" : "end"}" font-size="13" font-weight="800" style="fill:var(--verm)">${esc(c.n)}</text><line class="lead" x1="${g.c[0]}" y1="${g.c[1]}" x2="${g.c[0] + (right ? 10 : -10)}" y2="${g.c[1] - 8}"/>`; }
  });
  return s + lab + "</svg>";
}
const normaliza = s => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
const COMP_C = [["pares", "Cidades parecidas (mesma faixa de receita)"], ["escolher", "Escolher cidades…"], ["estado", "Estado do Rio"], ["mediana", "Mediana das 92"]];
const COMP_R = [["todas", "Todas as regiões"], ["escolher", "Escolher regiões…"]];
function viewCidade(el) {
  const sc = cid(S.cidade);
  el.innerHTML = `<h1>A sua cidade em uma tela</h1>
  <p class="lede">Digite o nome ou escolha na lista, ou clique no mapa. Tudo abaixo muda junto. Dados de 2024, declarados ao Siconfi e ao SIOPS.</p>
  <div class="ctrl" id="ctrlCid">
    <label>Cidade<input type="search" id="busca" list="dlCid" placeholder="Digite o nome ou escolha na lista" autocomplete="off" value="${esc(sc.n)}"></label>
    <datalist id="dlCid">${C.map(c => `<option value="${esc(c.n)}">`).join("")}</datalist>
    <label>Ano<select id="ano"><option>2024</option></select></label>
    <label>Ver por<span class="seg" role="group" aria-label="Ver por"><button data-m="cidade" aria-pressed="${S.modo === "cidade"}">Cidade</button><button data-m="regiao" aria-pressed="${S.modo === "regiao"}">Região</button></span></label>
    <label>Comparar com<select id="comp"></select></label>
    <span id="multi"></span>
    <label id="lbInd">Indicador no mapa<select id="indC">${Object.keys(IND).map(k => `<option value="${k}"${k === S.ind ? " selected" : ""}>${IND[k][0]}</option>`).join("")}</select></label>
  </div>
  <p class="nota">O Ano fica em 2024 porque é o ano com todas as fontes cruzadas; 2023 e 2025 aparecem na triagem, em <a href="#controle">Controle e auditoria</a>.</p>
  <div id="extras" class="tags"></div>
  <div id="saidaCid"></div>`;
  const lista = () => S.modo === "cidade" ? S.extras : S.regExtras;
  const montaMulti = () => {
    const box = $("#multi"), ativo = S.modo === "cidade" ? S.comp === "escolher" : S.regComp === "escolher";
    if (!ativo) { box.innerHTML = ""; return; }
    const itens = S.modo === "cidade" ? C.map(c => [c.c, c.n]) : D.regioes.map(r => [r.k, r.k]);
    box.innerHTML = `<details class="multi"><summary>${S.modo === "cidade" ? "Escolher até 5 cidades" : "Escolher até 5 regiões"}</summary><div class="painel">${S.modo === "cidade" ? '<input type="search" placeholder="Filtrar a lista" aria-label="Filtrar a lista">' : ""}<div class="opts">${itens.map(([k, n]) => `<label data-n="${esc(normaliza(n))}"><input type="checkbox" value="${esc(k)}"${lista().map(String).includes(String(k)) ? " checked" : ""}> ${esc(n)}</label>`).join("")}</div></div></details>`;
    const f = $("input[type=search]", box); if (f) f.oninput = () => $$(".opts label", box).forEach(l => l.hidden = !l.dataset.n.includes(normaliza(f.value)));
    $$("input[type=checkbox]", box).forEach(cb => cb.onchange = () => {
      const k = S.modo === "cidade" ? +cb.value : cb.value, l = lista(), i = l.findIndex(x => x === k);
      if (cb.checked && i < 0) { if (l.length >= 5) { cb.checked = false; return; } l.push(k); } else if (!cb.checked && i >= 0) l.splice(i, 1);
      draw();
    });
  };
  const fillComp = () => {
    const o = S.modo === "cidade" ? COMP_C : COMP_R;
    $("#comp").innerHTML = o.map(x => `<option value="${x[0]}">${x[1]}</option>`).join(""); $("#comp").value = S.modo === "cidade" ? S.comp : S.regComp; $("#lbInd").hidden = S.modo === "regiao"; montaMulti();
  };
  fillComp();
  const set = c => { S.cidade = c; S.regiao = cid(c).r; $("#busca").value = cid(c).n; draw(); };
  $("#busca").onchange = e => { const v = normaliza(e.target.value), c = C.find(x => normaliza(x.n) === v) || C.find(x => normaliza(x.n).startsWith(v) && v.length > 2); if (c) set(c.c); };
  $("#busca").oninput = e => { const c = C.find(x => normaliza(x.n) === normaliza(e.target.value)); if (c && c.c !== S.cidade) set(c.c); };
  $$("[data-m]", el).forEach(b => b.onclick = () => { S.modo = b.dataset.m; $$("[data-m]", el).forEach(x => x.setAttribute("aria-pressed", x === b)); fillComp(); draw(); });
  $("#comp").onchange = e => { if (S.modo === "cidade") S.comp = e.target.value; else S.regComp = e.target.value; montaMulti(); draw(); };
  $("#indC").onchange = e => { S.ind = e.target.value; draw(); };
  const draw = () => {
    const sc = cid(S.cidade), ex = $("#extras"), l = lista(), ativo = S.modo === "cidade" ? S.comp === "escolher" : S.regComp === "escolher";
    ex.innerHTML = ativo ? (l.length ? l.map(k => `<span class="tag">${esc(S.modo === "cidade" ? cid(k).n : k)}<button data-rm="${esc(k)}" aria-label="Remover ${esc(S.modo === "cidade" ? cid(k).n : k)}">×</button></span>`).join("") : `<span class="nota">Abra “${S.modo === "cidade" ? "Escolher até 5 cidades" : "Escolher até 5 regiões"}” e marque as que quer comparar.</span>`) : "";
    $$("[data-rm]", ex).forEach(b => b.onclick = () => { const i = l.findIndex(x => String(x) === b.dataset.rm); l.splice(i, 1); montaMulti(); draw(); });
    $("#saidaCid").innerHTML = S.modo === "cidade" ? corpoCidade(sc) : corpoRegiao();
    (S.modo === "cidade" ? ligaCidade : ligaRegiao)(); sincroniza();
  };
  S.drawCidade = draw; S.setCidade = set;
  draw();
}
function compSet(sc) {
  if (S.comp === "pares") { const p = peers(sc); return { rot: `Mediana das ${p.length} cidades parecidas`, cols: [{ r: `Mediana dos pares (n = ${p.length})`, v: k => med(p.map(x => x[k])) }], peers: p.map(x => x.c), nota: `Cidades parecidas: as ${p.length + 1} da mesma faixa de receita por habitante (${rs(Math.min(...[sc, ...p].map(x => x.rh)))} a ${rs(Math.max(...[sc, ...p].map(x => x.rh)))}).` }; }
  if (S.comp === "escolher") { const l = S.extras.map(cid); return { rot: "Cidades escolhidas", cols: l.map(x => ({ r: x.n, v: k => x[k] })), peers: l.map(x => x.c), nota: l.length ? "" : "Escolha até cinco cidades em “Escolher até 5 cidades”." }; }
  if (S.comp === "estado") return { rot: "Estado do Rio", cols: [{ r: "Estado do Rio (esfera estadual)", v: k => ({ gh: EST.gh, rh: EST.rh, pd: EST.pd })[k] ?? null }], peers: [], nota: "Atenção: o estado e o município têm funções diferentes no SUS; os valores da esfera estadual não são comparáveis diretamente com os das cidades. Só gasto por habitante, receita por habitante e parte da despesa existem para o estado." };
  return { rot: "Mediana das 92", cols: [{ r: "Mediana das 92 cidades", v: k => med(C.map(x => x[k])) }], peers: [], nota: "" };
}
const LINHAS = [["gh", "Gasto em saúde por habitante", v => rs(v)], ["rh", "Receita por habitante", v => rs(v)], ["pd", "Parte da despesa que vai para saúde", v => pc(v)], ["fa", "Saúde como parte da receita (Siconfi)", v => pc(v)], ["ap", "Aplicado em saúde com recursos próprios (SIOPS), mínimo 15%", v => pc(v)], ["fo", "Folga sobre o mínimo, em pontos", v => v == null ? "sem dado" : fm(v, 1) + " p.p."]];
function corpoCidade(sc) {
  const cs = compSet(sc), pos = posIn(sc, "gh"), ind = S.ind;
  const tabela = `<div class="rolar"><table class="t"><thead><tr><th class="l">Indicador (2024)</th><th>${esc(sc.n)}</th>${cs.cols.map(c => `<th>${esc(c.r)}</th>`).join("")}</tr></thead><tbody>${LINHAS.map(([k, n, f]) => `<tr><td class="l">${n}</td><td><b>${f(sc[k])}</b></td>${cs.cols.map(c => `<td>${f(c.v(k))}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
  return `<div class="grade"><section class="card" style="margin:0"><div class="tit"><span>${IND[ind][0]} nas 92 cidades</span><small>${IND[ind][2]}</small></div><div class="corpo"><div class="mapa" id="mapaC"></div><div id="legC"></div></div></section>
    <section class="card" style="margin:0"><div class="tit"><span>Ranking das 92 cidades</span></div><div class="corpo" id="listaC"></div></section></div>
  <h2>${esc(sc.n)}: a ficha</h2>
  <div class="kpis"><div class="kpi"><b>${rs(sc.gh)}</b><span>por habitante em saúde, 2024</span></div><div class="kpi"><b>${pos}º de 92</b><span>posição em gasto por habitante (1º = gasta mais)</span></div><div class="kpi"><b>${pc(sc.ap)}</b><span>da base de cálculo aplicados em saúde (SIOPS); mínimo legal de 15%</span></div><div class="kpi"><b>${pc(sc.fa)}</b><span>da receita total vai para saúde (Siconfi), 2024</span></div></div>
  <p class="nota">Gasto em saúde por habitante não mede qualidade nem necessidade. Um número baixo é uma pergunta, não um defeito.</p>
  ${card(`Comparação: ${esc(sc.n)} e ${esc(cs.rot.toLowerCase())}`, `${tabela}${cs.nota ? `<p class="${S.comp === "estado" ? "aviso v" : "nota"}">${esc(cs.nota)}</p>` : ""}${fonte("Siconfi (RREO e DCA) e SIOPS, 2024; população estimada pelo IBGE. Arquivos: indicadores_2024.csv, improve_r2_pares.csv, improve_r5_r6_siops.csv.")}`, "2024")}
  <div class="grade2">${card("Receita e gasto, cidade por cidade", `<figure class="fig" id="figDisp"></figure><p class="leg2">Cada ponto é uma cidade, em escala logarítmica. A reta tracejada é o ajuste das 92 cidades; ${esc(sc.n)} aparece em vermelho.</p>${fonte("Siconfi, 2024. Arquivo: indicadores_2024.csv.")}`, "2024")}
  ${card("Cidade típica e pessoa típica", `<figure class="fig" id="figCurva"></figure><p class="leg2">${pc(G.pop_abaixo_mediana_pct, 0)} da população mora em cidades que gastam menos que a cidade do meio (${rs(G.mediana_gh)} por habitante).</p>${fonte("Siconfi, 2024; população do IBGE. Arquivo: indicadores_2024.csv.")}`, "2024")}</div>
  ${card("Folga sobre o mínimo de 15%", `<figure class="fig" id="figFolga"></figure><p class="leg2">Pontos percentuais acima do mínimo de 15% da base de cálculo que a lei manda aplicar em saúde (LC 141/2012). Mostradas as 12 menores folgas e a sua cidade, em vermelho.</p>${fonte("SIOPS, 2024. Arquivo: improve_r5_r6_siops.csv.")}`, "2024")}
  ${voceSabia("cidade", "Para puxar assunto")}
  ${maisItens("cidade", "maisCidade")}`;
}
function ligaCidade() {
  const sc = cid(S.cidade), ind = S.ind, vals = C.map(c => c[ind]), E = escala(vals), cs = compSet(sc);
  const cor = c => RAMPA[E.cls(c[ind])]; cor.tip = c => IND[ind][1](c[ind]);
  const troca = c => { S.cidade = +c; S.regiao = cid(S.cidade).r; $("#busca").value = cid(S.cidade).n; S.drawCidade(); };
  $("#mapaC").innerHTML = mapaRJ({ cor, selSet: [sc.c], peersSet: cs.peers, rotulo: `Mapa do estado do Rio de Janeiro com as 92 cidades por ${IND[ind][0]}; a cidade selecionada, ${sc.n}, em vermelho.` });
  $$("#mapaC path").forEach(p => p.onclick = () => troca(p.dataset.c));
  $("#legC").innerHTML = legenda(E, v => IND[ind][1](v).replace("R$ ", "")) + `<p class="leg2">${cs.peers.length ? "Contorno tracejado: cidades comparadas. " : ""}Em cada tom há cerca de 18 cidades. Toque numa cidade para trocar a seleção.</p>`;
  const itens = C.map(c => ({ k: c.c, n: c.n, v: c[ind] })).sort((a, b) => b.v - a.v);
  const l = listaRank(itens, sc.c, v => IND[ind][1](v).replace("R$ ", ""), troca, it => RAMPA[E.cls(it.v)]);
  $("#listaC").appendChild(l); centraNaLista(l);
  const pts = C.map(c => ({ x: c.rh, y: c.gh, hl: c.c === sc.c, lab: c.c === sc.c ? c.n : null, tip: `${c.n}: receita ${rs(c.rh)} e gasto ${rs(c.gh)} por habitante`, cor: cs.peers.includes(c.c) ? "var(--navy)" : null }));
  $("#figDisp").innerHTML = dispersao({ pts, xl: "Receita por habitante (R$, escala log)", yl: "Gasto em saúde por habitante (R$, log)", fit: ols(pts), alt: `Dispersão da receita por habitante contra o gasto em saúde por habitante, 92 cidades, ${sc.n} em vermelho.` });
  $("#figCurva").innerHTML = curva("Curva da parcela acumulada da população contra o gasto por habitante das cidades");
  const menores = [...C].sort((a, b) => a.fo - b.fo).slice(0, 12); if (!menores.find(x => x.c === sc.c)) menores.push(sc);
  $("#figFolga").innerHTML = barras({ rows: menores.map(c => ({ l: c.n, v: c.fo, hl: c.c === sc.c })), fmt: v => fm(v, 1) + " p.p.", alt: "Folga sobre o mínimo de 15% das cidades com menor folga", linha: 3, linhaRot: "3 p.p.", max: Math.max(...menores.map(c => c.fo), 3.5) * 1.05 });
  ligaMais("maisCidade", "cidade");
}
/* ----- modo região: o clique escolhe a região inteira, nunca a cidade ----- */
function regStats(k) { return D.regioes.find(r => r.k === k); }
function corpoRegiao() {
  const rg = regStats(S.regiao), regs = [...D.regioes].sort((a, b) => b.gh - a.gh), pos = regs.findIndex(r => r.k === rg.k) + 1, cs = C.filter(c => c.r === rg.k), pop = C.reduce((a, c) => a + c.pop, 0);
  const sel = cs.find(c => c.c === S.cidade);
  const ficha = `<div class="kpis"><div class="kpi"><b>${rs(rg.gh)}</b><span>por habitante em saúde na região (soma do gasto ÷ soma da população), 2024</span></div><div class="kpi"><b>${pos}º de 8</b><span>posição entre as 8 regiões de governo</span></div><div class="kpi"><b>${pc(rg.pop / pop * 100)}</b><span>da população do estado, em ${rg.n} cidades</span></div><div class="kpi"><b>${pc(rg.tr, 0)}</b><span>da receita vem de repasses (média ponderada), 2024</span></div></div>`;
  const aviso = rg.n < 5 ? `<p class="aviso">${esc(rg.k)} tem só ${rg.n} cidades: o valor da região é descritivo e não vale como tendência.</p>` : "";
  return `<div class="grade"><section class="card" style="margin:0"><div class="tit"><span>As 92 cidades pelos 10 grupos do estudo</span><small>As 8 regiões de governo; a Metropolitana tem 3 grupos</small></div><div class="corpo"><div class="mapa" id="mapaR"></div><div id="legR" class="leg"></div><p class="leg2">Clique numa região para ver as cidades dela ao lado. O contorno escuro mostra a região escolhida.</p></div></section>
    <section class="card" style="margin:0"><div class="tit"><span>Ranking das cidades de ${esc(rg.k)}</span><small>${cs.length} cidades · R$ por habitante, 2024</small></div><div class="corpo"><div id="listaCR"></div><p class="nota" id="notaCR"></p>${fonte("Siconfi (RREO e DCA), 2024; regiões de governo do CEPERJ. Arquivo: indicadores_2024.csv.")}</div></section></div>
  <h2>${esc(rg.k)}: a ficha</h2>${ficha}${aviso}
  <div class="grade2">${card("Ranking das 8 regiões", `<div id="listaR"></div>${fonte("Siconfi, 2024; soma do gasto ÷ soma da população de cada região.")}`, "R$ por habitante, 2024")}
  ${card("A região contra as outras", `<figure class="fig" id="figRB"></figure><p class="leg2">Gasto em saúde por habitante de cada região, 2024. ${esc(rg.k)} em vermelho.</p>`, "2024")}</div>
  <div class="grade2">${card("Receita e gasto, cidade por cidade", `<figure class="fig" id="figRD"></figure><p class="leg2">As cidades de ${esc(rg.k)} em vermelho, entre as 92.${sel ? ` ${esc(sel.n)} tem um ponto maior.` : ""}</p>`, "2024")}
  ${card(`Cidades de ${esc(rg.k)}: receita e posição`, `<div class="rolar"><table class="t"><thead><tr><th class="l">Cidade</th><th>Gasto por habitante</th><th>Receita por habitante</th><th>Posição de 92</th></tr></thead><tbody>${[...cs].sort((a, b) => b.gh - a.gh).map(c => `<tr data-c="${c.c}" class="${c.c === S.cidade ? "sel" : ""}"><td class="l">${esc(c.n)}</td><td>${rs(c.gh)}</td><td>${rs(c.rh)}</td><td>${posIn(c, "gh")}º</td></tr>`).join("")}</tbody></table></div>`, "2024")}</div>
  ${voceSabia("cidade", "Para puxar assunto")}${maisItens("cidade", "maisCidade")}`;
}
function ligaRegiao() {
  const rg = regStats(S.regiao), G10 = D.grupos, W = PRJ_RJ.W;
  const escolheRegiao = k => { S.regiao = k; S.drawCidade(); };
  let s = `<svg viewBox="0 0 ${W} ${PRJ_RJ.H}" role="img" aria-label="Mapa do estado do Rio de Janeiro com as cidades coloridas pelos 10 grupos do estudo; a região selecionada, ${esc(rg.k)}, tem contorno escuro.">`;
  C.forEach(c => { const g = PRJ_RJ.out[c.c]; s += `<path d="${g.d}" fill="${GRUPO_COR[c.g]}" data-c="${c.c}" data-r="${esc(c.r)}" data-tip="${esc(c.r)}: ${rs(regStats(c.r).gh)} por habitante. Clique para escolher a região." style="${c.r === rg.k ? "stroke:var(--fg);stroke-width:1.8" : ""}"/>`; });
  G10.forEach(g => { const cs = C.filter(c => c.g === g.k); const x = cs.reduce((a, c) => a + PRJ_RJ.out[c.c].c[0], 0) / cs.length, y = cs.reduce((a, c) => a + PRJ_RJ.out[c.c].c[1], 0) / cs.length; s += `<text class="halo" x="${x}" y="${y + 4}" text-anchor="middle" font-size="13" font-weight="800">${GRUPO_NUM[g.k]}</text>`; });
  $("#mapaR").innerHTML = s + "</svg>";
  $$("#mapaR path").forEach(p => p.onclick = () => escolheRegiao(p.dataset.r));
  $("#legR").innerHTML = G10.map(g => `<span><i style="background:${GRUPO_COR[g.k]};width:14px;height:14px"></i> <b>${GRUPO_NUM[g.k]}</b> ${esc(g.nome)} (${g.n})</span>`).join("&nbsp; ");
  /* ranking das cidades da região, em cima */
  const cs = C.filter(c => c.r === rg.k).sort((a, b) => b.gh - a.gh);
  const itens = cs.map(c => ({ k: c.c, n: c.n, v: c.gh, g: c.g }));
  const lc = listaRank(itens, S.cidade, v => fm(v), k => { S.cidade = +k; S.drawCidade(); }, it => GRUPO_COR[it.g]);
  $("#listaCR").appendChild(lc); const sel = cs.find(c => c.c === S.cidade); centraNaLista(lc);
  $("#notaCR").innerHTML = sel ? `<b>${esc(sel.n)}</b>: ${cs.indexOf(sel) + 1}º de ${cs.length} em ${esc(rg.k)} e ${posIn(sel, "gh")}º de 92 no estado. <button class="btn sec" id="abreFicha" style="padding:3px 10px;font-size:13px">Abrir a ficha de ${esc(sel.n)}</button>` : `Clique numa cidade da lista para destacá-la no mapa e nos gráficos.`;
  const ab = $("#abreFicha"); if (ab) ab.onclick = () => { S.modo = "cidade"; $$("[data-m]").forEach(x => x.setAttribute("aria-pressed", x.dataset.m === "cidade")); $("#comp").innerHTML = COMP_C.map(x => `<option value="${x[0]}">${x[1]}</option>`).join(""); $("#comp").value = S.comp; $("#lbInd").hidden = false; $("#multi").innerHTML = ""; S.drawCidade(); };
  /* ranking das regiões, embaixo */
  const regs = [...D.regioes].sort((a, b) => b.gh - a.gh);
  const box = $("#listaR"); let h = `<div class="lista" style="max-height:none"><ol>`;
  regs.forEach((r, i) => {
    h += `<li tabindex="0" data-r="${esc(r.k)}" class="${r.k === S.regiao ? "sel" : ""}"><span class="pos">${i + 1}º</span><span class="nm">${esc(r.k)} (${r.n})</span><span class="vl">${fm(r.gh)}</span></li>`;
    if (r.k === "Metropolitana") { h += `<li class="sub-t" style="cursor:default"><span class="nm"><button class="btn sec" id="abreMetro" style="padding:2px 8px;font-size:12px" aria-expanded="${S.metroAberta}">${S.metroAberta ? "Recolher" : "Ver os 3 grupos da Metropolitana"}</button></span></li>`; if (S.metroAberta) D.grupos.filter(g => g.regiao === "Metropolitana").sort((a, b) => b.gh - a.gh).forEach(g => h += `<li style="padding-left:32px;cursor:default"><span class="sw" style="background:${GRUPO_COR[g.k]}"></span><span class="nm">${GRUPO_NUM[g.k]}. ${esc(g.nome)} (${g.n})</span><span class="vl">${fm(g.gh)}</span></li>`); }
  });
  box.innerHTML = h + "</ol></div>";
  $$("li[data-r]", box).forEach(li => { li.onclick = () => escolheRegiao(li.dataset.r); li.onkeydown = e => { if (e.key === "Enter") li.click(); }; });
  $("#abreMetro").onclick = () => { S.metroAberta = !S.metroAberta; ligaRegiao(); };
  let rows = regs.map(r => ({ l: r.k, v: r.gh, hl: r.k === S.regiao, tip: `${r.k}: ${rs(r.gh)} por habitante (${r.n} cidades)` }));
  if (S.regComp === "escolher") rows = rows.filter(r => r.hl || S.regExtras.includes(r.l));
  $("#figRB").innerHTML = barras({ rows, fmt: v => rs(v), alt: "Gasto em saúde por habitante das regiões de governo", rotW: 150 });
  const pts = C.map(c => ({ x: c.rh, y: c.gh, hl: c.r === S.regiao, r: c.c === S.cidade ? 7 : 4, tip: `${c.n}: receita ${rs(c.rh)} e gasto ${rs(c.gh)} por habitante` }));
  $("#figRD").innerHTML = dispersao({ pts, xl: "Receita por habitante (R$, escala log)", yl: "Gasto em saúde por habitante (R$, log)", fit: ols(pts), alt: `Dispersão da receita contra o gasto por habitante; cidades de ${S.regiao} em vermelho.` });
  $$("tr[data-c]", $("#saidaCid")).forEach(tr => tr.onclick = () => { S.cidade = +tr.dataset.c; S.drawCidade(); });
  ligaMais("maisCidade", "cidade");
}
