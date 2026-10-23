"""Verifica a cobertura real de tabelas candidatas do IBGE no RJ.

Uso: python -I scripts/03_verificacao_niveis_ibge.py
Fonte: API de agregados do IBGE (https://servicodados.ibge.gov.br/api/v3/agregados).
O metadado diz que o nível "município" existe; aqui conferimos QUANTOS municípios do RJ (código
IBGE começando em 33) a tabela realmente lista, e se o estado (N3, código 33) aparece.
Grava o resultado em dados_brutos/ibge_cobertura_rj.json e escreve o resumo na tela.
"""
import gzip
import json
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = "https://servicodados.ibge.gov.br/api/v3/agregados"
PASTA = Path(__file__).resolve().parent.parent / "dados_brutos"
TABELAS = {
    "6579": "Estimativas de População: população residente estimada",
    "10157": "Censo 2022: população por nacionalidade, sexo e grupos de idade",
    "4938": "PNS 2013-2019: pessoas com plano de saúde, por sexo e situação do domicílio",
    "4949": "PNS 2013-2019: pessoas com plano de saúde, por grupo de idade",
    "6803": "Censo 2022: domicílios por ligação à rede geral de água e forma de abastecimento",
    "6805": "Censo 2022: domicílios por tipo de esgotamento sanitário",
    "7358": "Projeção da População 2018: população por sexo e idade",
    "1300": "PNSB 2008: municípios com tratamento de esgoto sanitário",
    "216": "AMS 1976-2005: leitos para internação",
}


def consultar(url):
    with urllib.request.urlopen(url, timeout=120) as resposta:
        bruto = resposta.read()
    if bruto[:2] == b"\x1f\x8b":
        bruto = gzip.decompress(bruto)
    return json.loads(bruto.decode("utf-8"))


def main():
    PASTA.mkdir(exist_ok=True)
    resultado, falhas = {"coletado_em": datetime.now().isoformat(timespec="seconds"), "tabelas": {}}, []
    for tid, descricao in TABELAS.items():
        item = {"descricao": descricao}
        for nivel in ("N3", "N6"):
            try:
                locais = consultar(f"{BASE}/{tid}/localidades/{nivel}")
            except Exception as erro:
                falhas.append((tid, nivel, str(erro)))
                item[nivel] = None
                continue
            ids = [str(x["id"]) for x in locais]
            item[nivel] = {"total_brasil": len(ids),
                           "rj": len([i for i in ids if i.startswith("33")]),
                           "estado_rj_presente": "33" in ids}
        resultado["tabelas"][tid] = item
        print(f"{tid} | {descricao}")
        print(f"     estados (N3): {item['N3']}")
        print(f"     municípios (N6): {item['N6']}")
    (PASTA / "ibge_cobertura_rj.json").write_text(
        json.dumps({**resultado, "falhas": falhas}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nFalhas de consulta: {len(falhas)}")
    for f in falhas:
        print("  ", f)


if __name__ == "__main__":
    main()
