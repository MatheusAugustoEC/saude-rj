"""Catálogo do IBGE: quais tabelas de população por idade, saneamento e saúde existem, e em que nível geográfico?

Uso: python -I scripts/02_catalogo_ibge.py
Fonte: API de agregados do IBGE (https://servicodados.ibge.gov.br/api/v3/agregados).
Grava o catálogo bruto, os metadados e um resumo (TSV) em dados_brutos/.
Níveis territoriais do IBGE: N1 = Brasil, N2 = Grande Região, N3 = Unidade da Federação, N6 = Município.
Falhas de consulta são listadas no fim, nunca ignoradas.
"""
import gzip
import json
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = "https://servicodados.ibge.gov.br/api/v3/agregados"
PASTA = Path(__file__).resolve().parent.parent / "dados_brutos"

# Critério explícito: para cada pesquisa de interesse (id do catálogo), quais tabelas entram.
# palavras = o nome da tabela precisa ter alguma delas (None = todas as tabelas da pesquisa).
# excluir = o nome da tabela não pode ter nenhuma delas.
ALVOS = {
    "CD": {"nome": "Censo Demográfico",
           "palavras": ["população residente", "esgotamento sanitário", "abastecimento de água"],
           "excluir": ["quilombola", "indígena", "deficiência", "religião", "estrangeir"]},
    "XF": {"nome": "Estimativas de População", "palavras": None, "excluir": []},
    "XE": {"nome": "Projeção da População", "palavras": None, "excluir": []},
    "SB": {"nome": "Pesquisa Nacional de Saneamento Básico",
           "palavras": ["esgot", "abastecimento de água"], "excluir": []},
    "XN": {"nome": "Pesquisa Nacional de Saúde",
           "palavras": ["plano de saúde", "consulta médica", "internação"], "excluir": []},
    "AM": {"nome": "Pesquisa de Assistência Médico-Sanitária", "palavras": None, "excluir": []},
}
MAX_POR_PESQUISA = 200


def consultar(url):
    with urllib.request.urlopen(url, timeout=120) as resposta:
        bruto = resposta.read()
    if bruto[:2] == b"\x1f\x8b":  # a API do IBGE pode devolver o JSON comprimido (gzip)
        bruto = gzip.decompress(bruto)
    return json.loads(bruto.decode("utf-8"))


def main():
    PASTA.mkdir(exist_ok=True)
    catalogo = consultar(BASE)
    (PASTA / "ibge_catalogo_agregados.json").write_text(
        json.dumps({"coletado_em": datetime.now().isoformat(timespec="seconds"),
                    "catalogo": catalogo}, ensure_ascii=False), encoding="utf-8")
    por_id = {p["id"]: p for p in catalogo}
    print(f"Pesquisas: {len(catalogo)} | tabelas (agregados): {sum(len(p['agregados']) for p in catalogo)}")

    metadados, falhas = [], []
    for pid, alvo in ALVOS.items():
        if pid not in por_id:
            falhas.append((pid, alvo["nome"], "pesquisa não encontrada no catálogo"))
            continue
        escolhidas = []
        for tabela in por_id[pid]["agregados"]:
            nome = tabela["nome"].lower()
            if alvo["palavras"] is not None and not any(p in nome for p in alvo["palavras"]):
                continue
            if any(x in nome for x in alvo["excluir"]):
                continue
            escolhidas.append(tabela)
        print(f"{alvo['nome']}: {len(escolhidas)} tabelas pelo critério "
              f"(metadados das primeiras {MAX_POR_PESQUISA})")
        for tabela in escolhidas[:MAX_POR_PESQUISA]:
            try:
                m = consultar(f"{BASE}/{tabela['id']}/metadados")
            except Exception as erro:
                falhas.append((tabela["id"], tabela["nome"], str(erro)))
                continue
            niveis = m.get("nivelTerritorial", {})
            todos = sorted(set(niveis.get("Administrativo", [])) | set(niveis.get("Especial", []))
                           | set(niveis.get("IBGE", [])))
            periodo = m.get("periodicidade") or {}
            metadados.append({"pesquisa": alvo["nome"], "tabela_id": tabela["id"],
                              "tabela": tabela["nome"], "niveis": todos,
                              "ano_inicio": periodo.get("inicio"), "ano_fim": periodo.get("fim")})

    (PASTA / "ibge_candidatas_metadados.json").write_text(
        json.dumps(metadados, ensure_ascii=False, indent=1), encoding="utf-8")
    linhas = ["tabela_id\tpesquisa\tUF_N3\tmunicipio_N6\tano_inicio\tano_fim\tnome"]
    for m in metadados:
        linhas.append(f"{m['tabela_id']}\t{m['pesquisa']}\t{'N3' in m['niveis']}\t"
                      f"{'N6' in m['niveis']}\t{m['ano_inicio']}\t{m['ano_fim']}\t{m['tabela']}")
    resumo = PASTA / "ibge_candidatas_resumo.tsv"
    resumo.write_text("\n".join(linhas), encoding="utf-8")
    print(f"Resumo gravado em {resumo} ({len(metadados)} tabelas)")
    print(f"Falhas de consulta: {len(falhas)}")
    for f in falhas:
        print("  ", f)


if __name__ == "__main__":
    main()
