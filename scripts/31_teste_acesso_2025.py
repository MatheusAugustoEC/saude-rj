"""Control, passo 1: verifica se os dados de 2025 estão disponíveis para os 92 municípios, SEM baixar valores (só o extrato de entregas e a população).

Uso: python -X utf8 -u scripts/31_teste_acesso_2025.py
Grava dados_brutos/teste_acesso_2025.csv: por município, último bimestre do RREO entregue, se há DCA, data da entrega mais recente e população 2025 do IBGE.
O recorte de 2025 é o de confirmação (C5): só se abre depois de registrar as previsões. Este script não lê nenhum valor de receita ou despesa.
"""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt"
UA = {"User-Agent": "Mozilla/5.0"}


def pega(url):
    for t in range(1, 4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return json.load(r), ""
        except Exception as e:
            erro = str(e)[:100]
            time.sleep(3 * t)
    return None, erro


entes = pd.read_csv(RAIZ / "dados_tratados" / "indicadores_2024.csv", dtype={"cod_ibge": str})
entes = entes[entes.esfera == "M"][["cod_ibge", "ente"]]
assert len(entes) == 92
pop, _ = pega("https://apisidra.ibge.gov.br/values/t/6579/n6/" + ",".join(entes.cod_ibge) + "/v/all/p/2025")
pop = {l["D1C"]: l["V"] for l in (pop or [])[1:]}
linhas = []
for n, e in enumerate(entes.itertuples(index=False), 1):
    d, erro = pega(f"{BASE}/extrato_entregas?" + urllib.parse.urlencode({"id_ente": e.cod_ibge, "an_referencia": 2025}))
    it = (d or {}).get("items", [])
    rreo = [i for i in it if i["entregavel"].startswith("Relatório Resumido")]
    dca = [i for i in it if "DCA" in i["entregavel"]]
    linhas.append({"cod_ibge": e.cod_ibge, "ente": e.ente, "rreo_ultimo_periodo": max((i["periodo"] for i in rreo), default=0),
                   "rreo_simplificado": any(i["entregavel"].endswith("Simplificado") for i in rreo), "dca_entregue": bool(dca),
                   "dca_data": max((i["data_status"] for i in dca), default=""), "pop2025": pop.get(e.cod_ibge, ""), "erro": erro})
    if n % 20 == 0:
        print(n, "de 92", flush=True)
r = pd.DataFrame(linhas)
r.to_csv(RAIZ / "dados_brutos" / "teste_acesso_2025.csv", index=False, encoding="utf-8-sig")
print("RREO: último bimestre entregue:", r.rreo_ultimo_periodo.value_counts().sort_index().to_dict())
print("RREO simplificado:", int(r.rreo_simplificado.sum()), "| DCA entregue:", int(r.dca_entregue.sum()), "de 92 | população 2025:", int((r.pop2025.astype(str).str.len() > 0).sum()), "de 92 | erros:", int((r.erro != "").sum()))
print("Sem DCA:", r[~r.dca_entregue].ente.tolist(), "| RREO antes do 6º bimestre:", r[r.rreo_ultimo_periodo < 6][["ente", "rreo_ultimo_periodo"]].values.tolist())
print("Datas da DCA: de", r[r.dca_data != ""].dca_data.min()[:10], "a", r[r.dca_data != ""].dca_data.max()[:10])
