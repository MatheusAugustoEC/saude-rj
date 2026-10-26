"""Testa se as bases do SUS (DATASUS, Ministério da Saúde) respondem e o que devolvem. Reexecutável.

Uso: python -X utf8 -u scripts/29_teste_acesso_sus.py
Grava dados_brutos/sus_teste_acesso.csv, acrescentando uma linha por teste (data e hora, status, bytes, trecho da resposta, erro).
Candidatos: leitos (CNES) e internações (SIH), para o módulo SUS do projeto. Servidor que não responde é registrado como falha.
"""
import csv
import re
import urllib.request
from datetime import datetime
from pathlib import Path

ARQ = Path(__file__).resolve().parent.parent / "dados_brutos" / "sus_teste_acesso.csv"
PAGINAS = {
    "TABNET: leitos CNES (RJ, por município)": "http://tabnet.datasus.gov.br/cgi/deftohtm.exe?cnes/cnv/leiintrj.def",
    "TABNET: internações SIH (RJ, local de internação)": "http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/nirj.def",
    "TABNET: página inicial": "http://tabnet.datasus.gov.br/",
    "API de dados abertos: leitos CNES": "https://apidadosabertos.saude.gov.br/cnes/leitos?limit=2&offset=0",
    "API de dados abertos: estabelecimentos CNES": "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos?limit=1&offset=0",
    "OpenDataSUS: página inicial": "https://opendatasus.saude.gov.br/",
    "OpenDataSUS: busca por leitos": "https://opendatasus.saude.gov.br/dataset?q=leitos",
    "FTP DATASUS: CNES, leitos (LT)": "ftp://ftp.datasus.gov.br/dissemin/publicos/CNES/200508_/Dados/LT/",
    "FTP DATASUS: SIH reduzida (RD)": "ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/",
    "CNES: página inicial": "https://cnes.datasus.saude.gov.br/",
}


def testar(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(pedido, timeout=40) as r:
            corpo = r.read(300000)
            status = getattr(r, "status", "ftp")
            texto = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", corpo.decode("latin-1", "replace")))[:160]
            return status, len(corpo), texto, ""
    except Exception as e:
        return "", 0, "", str(e)[:110]


novo = not ARQ.exists()
agora = datetime.now().isoformat(timespec="seconds")
with open(ARQ, "a", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    if novo:
        w.writerow(["testado_em", "base", "url", "status", "bytes_lidos", "trecho", "erro"])
    for nome, url in PAGINAS.items():
        s, n, t, e = testar(url)
        w.writerow([agora, nome, url, s, n, t, e])
        print(f"{'OK  ' if s else 'FALHA'} | {nome} | {s} {n} bytes | {t[:90]} {e}", flush=True)
