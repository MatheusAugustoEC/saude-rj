"""Planilha de conferência do Analyze: a decomposição (A1) e a regressão simples em fórmulas de Excel.

Uso: python -X utf8 scripts/25_gerar_planilha_analyze.py
Grava planilhas/saude_fiscal_rj_analyze.xlsx (sem valores calculados). Depois: scripts/26_recalcular_planilha_analyze.ps1 e scripts/27_conferir_planilha_analyze.py.
Texto AZUL = dado de entrada (Siconfi, IBGE). Texto PRETO = fórmula. A capital fica na última linha de dados, para o modelo sem a capital usar as linhas 2 a 92.
Escopo (limitado de propósito): o Excel confere a aritmética e a regressão simples; erros robustos HC3, bootstrap e intervalo de previsão ficam só no notebook.
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.worksheet.formula import ArrayFormula

import _mapa_comum as c

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "planilhas" / "saude_fiscal_rj_analyze.xlsx"
AZUL, PRETO = Font(name="Arial", size=10, color="0000FF"), Font(name="Arial", size=10)
NEG = Font(name="Arial", size=10, bold=True)
CAB = PatternFill("solid", fgColor="D9E2F3")

mun, _, _ = c.carrega_dados()
mun = mun.assign(ord=(mun.grupo == c.CAPITAL).astype(int)).sort_values(["ord", "ente"]).reset_index(drop=True)
assert len(mun) == 92 and mun.grupo.iloc[-1] == c.CAPITAL
N = len(mun) + 1  # última linha de dados (93)

wb = Workbook()
ws = wb.active
ws.title = "Dados"
for j, h in enumerate(["cod_ibge", "ente", "grupo", "populacao (IBGE 2024)", "saude (R$, Siconfi DCA)", "receita (R$, RREO Anexo 01)"], 1):
    ws.cell(1, j, h).font, ws.cell(1, j).fill = NEG, CAB
for i, r in enumerate(mun.itertuples(index=False), 2):
    for j, v in enumerate([r.cod_ibge, r.ente, r.grupo, r.populacao, r.saude, r.receita], 1):
        ws.cell(i, j, v).font = AZUL

a = wb.create_sheet("A1_decomposicao")
cab = ["ente", "gasto_hab", "receita_hab", "fatia", "ln_gasto", "ln_receita", "ln_fatia", "desvio_gasto", "desvio_receita", "desvio_fatia",
       "conferência (gasto - receita - fatia)", "gasto vs referência", "receita vs referência", "fatia vs referência"]
for j, h in enumerate(cab, 1):
    a.cell(1, j, h).font, a.cell(1, j).fill = NEG, CAB
for i in range(2, N + 1):
    f = {1: f"=Dados!B{i}", 2: f"=Dados!E{i}/Dados!D{i}", 3: f"=Dados!F{i}/Dados!D{i}", 4: f"=Dados!E{i}/Dados!F{i}",
         5: f"=LN(B{i})", 6: f"=LN(C{i})", 7: f"=LN(D{i})",
         8: f"=E{i}-AVERAGE(E$2:E${N})", 9: f"=F{i}-AVERAGE(F$2:F${N})", 10: f"=G{i}-AVERAGE(G$2:G${N})",
         11: f"=H{i}-(I{i}+J{i})", 12: f"=EXP(H{i})-1", 13: f"=EXP(I{i})-1", 14: f"=EXP(J{i})-1"}
    for j, v in f.items():
        a.cell(i, j, v).font = PRETO

m = wb.create_sheet("Modelos")
for j, h in enumerate(["ente", "const", "ln_receita (x)", "Baixada (0/1)", "Resto da Metropolitana (0/1)", "ln_gasto (y)"], 1):
    m.cell(1, j, h).font, m.cell(1, j).fill = NEG, CAB
for i in range(2, N + 1):
    f = {1: f"=Dados!B{i}", 2: 1, 3: f"=A1_decomposicao!F{i}", 4: f'=IF(Dados!C{i}="{c.BAIXADA}",1,0)', 5: f'=IF(Dados!C{i}="{c.RESTO}",1,0)', 6: f"=A1_decomposicao!E{i}"}
    for j, v in f.items():
        m.cell(i, j, v).font = PRETO
# previsão da capital pelo modelo M3 ajustado nas 91 cidades (linhas 2 a N-1); a capital entra como "resto da Metropolitana"
m["H1"], m["H1"].font = "x0 da capital: const, ln_receita, Baixada, Resto", NEG
for j, v in enumerate([1, f"=C{N}", 0, 1]):
    m.cell(2, 8 + j, v).font = PRETO
m["H4"], m["H4"].font = "(X'X)^-1 do M3, 91 cidades", NEG
m["H5"] = ArrayFormula("H5:K8", f"=MINVERSE(MMULT(TRANSPOSE(B2:E{N-1}),B2:E{N-1}))")
m["H5"].font = PRETO

r = wb.create_sheet("Resumo")
linhas = [
    ("Referência (média geométrica das 92 cidades)", None),
    ("gasto por habitante (R$)", f"=EXP(AVERAGE(A1_decomposicao!E2:E{N}))"),
    ("receita por habitante (R$)", f"=EXP(AVERAGE(A1_decomposicao!F2:F{N}))"),
    ("fatia da receita na saúde", f"=EXP(AVERAGE(A1_decomposicao!G2:G{N}))"),
    ("Correlação (log)", None),
    ("gasto x receita", f"=CORREL(A1_decomposicao!E2:E{N},A1_decomposicao!F2:F{N})"),
    ("gasto x fatia", f"=CORREL(A1_decomposicao!E2:E{N},A1_decomposicao!G2:G{N})"),
    ("Regressão simples em log: ln(gasto) = a + b ln(receita)", None),
    ("elasticidade b, 92 cidades", f"=SLOPE(A1_decomposicao!E2:E{N},A1_decomposicao!F2:F{N})"),
    ("R2, 92 cidades", f"=RSQ(A1_decomposicao!E2:E{N},A1_decomposicao!F2:F{N})"),
    ("elasticidade b, sem a capital (91)", f"=SLOPE(A1_decomposicao!E2:E{N-1},A1_decomposicao!F2:F{N-1})"),
    ("R2, sem a capital (91)", f"=RSQ(A1_decomposicao!E2:E{N-1},A1_decomposicao!F2:F{N-1})"),
    ("Capital (última linha de dados)", None),
    ("gasto por habitante da capital (R$)", f"=A1_decomposicao!B{N}"),
    ("receita por habitante da capital (R$)", f"=A1_decomposicao!C{N}"),
    ("fatia da capital", f"=A1_decomposicao!D{N}"),
    ("gasto da capital vs referência", f"=A1_decomposicao!L{N}"),
    ("receita da capital vs referência", f"=A1_decomposicao!M{N}"),
    ("fatia da capital vs referência", f"=A1_decomposicao!N{N}"),
    ("mediana da fatia nas 92", f"=MEDIAN(A1_decomposicao!D2:D{N})"),
    ("maior erro da identidade (deve ser ~0)", f"=MAX(MAX(A1_decomposicao!K2:K{N}),-MIN(A1_decomposicao!K2:K{N}))"),
    ("Modelo M3 (91 cidades, sem a capital): ln(gasto) = a + b ln(receita) + Baixada + Resto, mínimos quadrados (LINEST)", None),
    ("M3 elasticidade b", f"=INDEX(LINEST(Modelos!F2:F{N-1},Modelos!C2:E{N-1},TRUE,TRUE),1,3)"),
    ("M3 efeito Baixada (%)", f"=EXP(INDEX(LINEST(Modelos!F2:F{N-1},Modelos!C2:E{N-1},TRUE,TRUE),1,2))-1"),
    ("M3 efeito Resto da Metropolitana (%)", f"=EXP(INDEX(LINEST(Modelos!F2:F{N-1},Modelos!C2:E{N-1},TRUE,TRUE),1,1))-1"),
    ("M3 R2", f"=INDEX(LINEST(Modelos!F2:F{N-1},Modelos!C2:E{N-1},TRUE,TRUE),3,1)"),
    ("M3 erro-padrão da regressão (s)", f"=INDEX(LINEST(Modelos!F2:F{N-1},Modelos!C2:E{N-1},TRUE,TRUE),3,2)"),
    ("Capital prevista pelo M3 (como resto da Metropolitana)", None),
    ("ln do gasto previsto", f"=INDEX(LINEST(Modelos!F2:F{N-1},Modelos!C2:E{N-1},TRUE,TRUE),1,4)+INDEX(LINEST(Modelos!F2:F{N-1},Modelos!C2:E{N-1},TRUE,TRUE),1,3)*Modelos!I2+INDEX(LINEST(Modelos!F2:F{N-1},Modelos!C2:E{N-1},TRUE,TRUE),1,1)"),
    ("gasto previsto (R$ por habitante)", "=EXP(B{prev})"),
    ("alavanca da capital (x0 (X'X)^-1 x0')", "=SUMPRODUCT(MMULT(Modelos!H2:K2,Modelos!H5:K8),Modelos!H2:K2)"),
    ("t crítico (95%, 87 graus de liberdade)", "=TINV(0.05,87)"),
    ("limite inferior do intervalo de previsão (R$)", "=EXP(B{prev}-B{tcrit}*B{s}*SQRT(1+B{h}))"),
    ("limite superior do intervalo de previsão (R$)", "=EXP(B{prev}+B{tcrit}*B{s}*SQRT(1+B{h}))"),
    ("gasto real da capital em relação ao previsto", "=B{real}/B{prevr}-1"),
]
# resolve as referências de linha usadas nas fórmulas acima (a primeira linha de dados do Resumo é a 3)
_idx = {rot: k for k, (rot, _) in enumerate(linhas, 3)}
_ref = dict(prev=_idx["ln do gasto previsto"], tcrit=_idx["t crítico (95%, 87 graus de liberdade)"], s=_idx["M3 erro-padrão da regressão (s)"],
            h=_idx["alavanca da capital (x0 (X'X)^-1 x0')"], real=_idx["gasto por habitante da capital (R$)"], prevr=_idx["gasto previsto (R$ por habitante)"])
linhas = [(rot, f.format(**_ref) if f and "{" in f and "LINEST" not in f else f) for rot, f in linhas]
r.cell(1, 1, "Conferência do Analyze (A1 e regressão simples)").font = NEG
for i, (rot, form) in enumerate(linhas, 3):
    r.cell(i, 1, rot).font = NEG if form is None else PRETO
    if form:
        r.cell(i, 2, form).font = PRETO
r.column_dimensions["A"].width = 58
r.column_dimensions["B"].width = 18
ws.column_dimensions["B"].width = 28
ws.column_dimensions["C"].width = 28
for col in "DEF":
    ws.column_dimensions[col].width = 26
wb.save(SAIDA)
print("Gravado", SAIDA, "| formulas:", sum(1 for s in wb for row in s.iter_rows() for x in row if isinstance(x.value, str) and x.value.startswith("=")))
