"""Testes automáticos do dado (C7): transformam as conferências do Measure em verificações que falham quando o dado muda de forma, de domínio ou de volume.

Uso: python -m pytest tests -q   (a partir da raiz do repositório; não usa a internet: lê só os arquivos do próprio repositório)
Os testes não provam que o dado está certo. Provam que ele continua com a forma e os limites que o projeto conferiu.
"""
import hashlib
import json
import re
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parent.parent
BR, TR = RAIZ / "dados_brutos", RAIZ / "dados_tratados"
CFG = json.load(open(RAIZ / "config" / "parametros.json", encoding="utf-8"))


@pytest.fixture(scope="module")
def indicadores():
    return pd.read_csv(TR / "indicadores_2024.csv", dtype={"cod_ibge": str})


@pytest.fixture(scope="module")
def municipios(indicadores):
    return indicadores[indicadores.esfera == "M"]


def test_volume_de_entes(indicadores):
    contagem = indicadores.esfera.value_counts().to_dict()
    assert contagem == {"M": CFG["n_municipios"], "E": CFG["n_estados"], "D": 1}


def test_codigos_dos_municipios(municipios):
    assert municipios.cod_ibge.is_unique
    assert municipios.cod_ibge.str.fullmatch(r"33\d{5}").all(), "código do IBGE do RJ tem 7 dígitos e começa com 33"


def test_dominio_dos_valores(municipios):
    for coluna in ("saude", "populacao", "despesa", "receita"):
        assert (municipios[coluna] > 0).all(), f"{coluna} com valor zero ou negativo"


def test_saude_cabe_na_despesa(municipios):
    assert (municipios.saude <= municipios.despesa).all()


def test_populacao_plausivel(municipios):
    assert municipios.populacao.between(CFG["populacao_min"], CFG["populacao_max"]).all()


def test_faixa_do_gasto_por_habitante(municipios):
    gasto = municipios.saude / municipios.populacao
    assert gasto.between(CFG["gasto_hab_min"], CFG["gasto_hab_max"]).all(), "gasto por habitante fora da faixa já conferida"


@pytest.mark.parametrize("ano", [2023, 2025])
def test_dca_dos_anos_de_confirmacao(ano):
    d = pd.read_csv(BR / f"siconfi_dca_ie_{ano}.csv", dtype={"cod_ibge": str}, low_memory=False)
    assert {"cod_ibge", "conta", "coluna", "valor"} <= set(d.columns)
    saude = d[d.conta.str.startswith("10 - Sa") & (d.coluna == "Despesas Empenhadas")]
    assert saude.cod_ibge.nunique() >= CFG["minimo_cidades_dca"][str(ano)], "menos cidades com saúde na DCA do que o conferido"
    assert (saude.valor > 0).all()


@pytest.mark.parametrize("ano", [2023, 2025])
def test_rreo_dos_anos_de_confirmacao(ano):
    r = pd.read_csv(BR / f"siconfi_rreo_anexo01_{ano}.csv", dtype={"cod_ibge": str}, low_memory=False)
    receita = r[(r.cod_conta == "ReceitasExcetoIntraOrcamentarias") & (r.coluna == "Até o Bimestre (c)")]
    assert receita.cod_ibge.nunique() >= CFG["minimo_cidades_rreo"][str(ano)]
    assert (receita.valor > 0).all()


def test_populacao_2025_confere_com_2024(municipios):
    p = pd.read_csv(BR / "teste_acesso_2025.csv", dtype={"cod_ibge": str}).set_index("cod_ibge")
    m = municipios.set_index("cod_ibge")
    razao = pd.to_numeric(p.pop2025) / m.populacao
    assert razao.notna().all()
    assert razao.between(1 - CFG["variacao_populacao_max"], 1 + CFG["variacao_populacao_max"]).all(), razao[~razao.between(0.9, 1.1)].to_dict()


def test_elasticidade_no_intervalo_conferido():
    c = pd.read_csv(TR / "analyze_a2_coeficientes.csv")
    # M1 a M3 (sem ponderar por população); o M4 é ponderado e tem outra elasticidade (0,67), já explicada no relatório do Analyze
    x = c[(c.termo == "x") & c.modelo.str.match(r"M[123] ")].coef
    assert len(x) == 3
    assert x.between(CFG["elasticidade_min"], CFG["elasticidade_max"]).all()


def _sha(caminho):
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def _variantes(caminho):
    """O mesmo arquivo com fim de linha do Windows ou do Linux (o Git converte)."""
    bruto = caminho.read_bytes()
    lf = bruto.replace(b"\r\n", b"\n")
    return {hashlib.sha256(v).hexdigest() for v in (bruto, lf, lf.replace(b"\n", b"\r\n"))}


def test_dados_brutos_nao_mudaram():
    """Os dados brutos citados com SHA-256 nos manifestos das fases continuam os mesmos."""
    achados = 0
    for manifesto in (RAIZ / "fases").glob("*/manifesto.md"):
        for linha in manifesto.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\| `(dados_brutos|dados_tratados)/([^`]+)` \| `([0-9a-f]{64})` \|", linha)
            if not m:
                continue
            arquivo = RAIZ / m.group(1) / m.group(2)
            assert arquivo.exists(), f"{arquivo} citado em {manifesto.parent.name} não existe"
            assert m.group(3) in _variantes(arquivo), f"{arquivo.name} mudou desde o manifesto de {manifesto.parent.name}"
            achados += 1
    assert achados >= 10, "o teste não encontrou os hashes dos manifestos"
