"""Conferência da coleta de valores (passo 2): o que veio está completo e coerente?

Uso: python -u -I scripts/05_conferencia_coleta.py
Lê os CSVs de dados_brutos/ gerados por 04_coleta_valores.py e imprime os resultados das verificações.
Não altera nenhum arquivo.
"""
import csv
from collections import Counter, defaultdict
from pathlib import Path

PASTA = Path(__file__).resolve().parent.parent / "dados_brutos"
ANO = 2024
COD_RJ = "33"


def ler(nome):
    with open(PASTA / nome, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def eh_numero(texto):
    try:
        float(texto)
        return True
    except ValueError:
        return False


def main():
    rreo, rgf, chamadas = ler(f"siconfi_rreo_{ANO}.csv"), ler(f"siconfi_rgf_{ANO}.csv"), ler(f"siconfi_chamadas_{ANO}.csv")
    entes_esperados = {c["cod_ibge"]: (c["ente"], c["esfera"]) for c in chamadas if c["relatorio"] == "extrato_entregas"}
    estados = {k for k, v in entes_esperados.items() if v[1] in ("E", "D")}
    municipios = set(entes_esperados) - estados
    print(f"Entes esperados: {len(entes_esperados)} ({len(estados)} estados incl. DF, {len(municipios)} municípios do RJ)")
    print(f"Linhas: RREO {len(rreo)} | RGF {len(rgf)} | chamadas registradas {len(chamadas)}")

    print("\n1. Chamadas")
    erros = [c for c in chamadas if c["erro"]]
    vazias = [c for c in chamadas if not c["erro"] and c["linhas"] == "0"]
    print(f"   com erro: {len(erros)} | vazias: {len(vazias)} | com mais páginas (dado cortado): "
          f"{sum(c['tem_mais_paginas'] == 'True' for c in chamadas)}")
    for c in vazias:
        print(f"   VAZIA: {c['cod_ibge']} {c['ente']} | {c['relatorio']}")

    print("\n2. Cobertura (quantos entes têm linhas em cada relatório)")
    cobertura = {
        "RREO Anexo 01": {r["cod_ibge"] for r in rreo if r["anexo"] == "RREO-Anexo 01"},
        "RREO Anexo 02": {r["cod_ibge"] for r in rreo if r["anexo"] == "RREO-Anexo 02"},
        "RREO Anexo 07 (restos a pagar)": {r["cod_ibge"] for r in rreo if r["anexo"] == "RREO-Anexo 07"},
        "RGF Anexo 01 (Executivo)": {r["cod_ibge"] for r in rgf if r["co_poder"] == "E" and r["anexo"] == "RGF-Anexo 01"},
        "RGF Anexo 02 (dívida)": {r["cod_ibge"] for r in rgf if r["anexo"] == "RGF-Anexo 02"},
    }
    for nome, presentes in cobertura.items():
        faltam = sorted(set(entes_esperados) - presentes)
        print(f"   {nome}: {len(presentes & estados)} de {len(estados)} estados | "
              f"{len(presentes & municipios)} de {len(municipios)} municípios")
        for k in faltam:
            print(f"      sem dados: {k} {entes_esperados[k][0]}")

    print("\n3. Tipo de relatório e período usados (da coleta)")
    tipos = Counter()
    for c in chamadas:
        if c["relatorio"] != "extrato_entregas" and not c["erro"]:
            partes = c["relatorio"].split(" / ")
            tipos[(partes[0], partes[-1].split("período")[-1].strip() if "período" in partes[-1] else "?")] += 1
    for chave, n in sorted(tipos.items()):
        print(f"   {chave[0]} | período {chave[1]}: {n} chamadas")

    print("\n4. Qualidade dos valores")
    for nome, linhas in (("RREO", rreo), ("RGF", rgf)):
        vazios = sum(1 for r in linhas if r["valor"] == "")
        nao_num = sum(1 for r in linhas if r["valor"] != "" and not eh_numero(r["valor"]))
        duplicadas = len(linhas) - len({tuple(sorted(r.items())) for r in linhas})
        print(f"   {nome}: valor vazio {vazios} | valor não numérico {nao_num} | linhas exatamente duplicadas {duplicadas}")

    print("\n5. Conferência com o que vimos antes no estado do RJ (consultas avulsas de 20/10/2026)")
    esperado = {("RREO-Anexo 02", "rreo"): 2021, ("RGF-Anexo 01 E", "rgf"): 214}
    obtido_rreo02 = sum(1 for r in rreo if r["cod_ibge"] == COD_RJ and r["anexo"] == "RREO-Anexo 02")
    obtido_rgf = sum(1 for r in rgf if r["cod_ibge"] == COD_RJ and r["co_poder"] == "E" and r["anexo"] == "RGF-Anexo 01")
    print(f"   RREO Anexo 02 do RJ: coletado {obtido_rreo02} | visto antes {esperado[('RREO-Anexo 02', 'rreo')]}")
    print(f"   RGF Anexo 01 Executivo do RJ: coletado {obtido_rgf} | visto antes {esperado[('RGF-Anexo 01 E', 'rgf')]}")

    print("\n6. Poderes presentes no RGF (linhas por poder, estados / municípios)")
    por_poder = defaultdict(lambda: [0, 0])
    for r in rgf:
        por_poder[r["co_poder"]][0 if r["cod_ibge"] in estados else 1] += 1
    for poder, (e, m) in sorted(por_poder.items()):
        print(f"   {poder}: estados {e} | municípios {m}")

    print("\n7. Saúde no RREO Anexo 02 (linhas de função 'Saúde' no RJ estado)")
    saude = [r for r in rreo if r["cod_ibge"] == COD_RJ and r["anexo"] == "RREO-Anexo 02" and r["conta"].strip().lower() == "saúde"]
    print(f"   linhas 'Saúde': {len(saude)} | colunas: {sorted({r['coluna'] for r in saude})}")


if __name__ == "__main__":
    main()
