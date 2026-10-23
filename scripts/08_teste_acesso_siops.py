"""Testa se as páginas do SIOPS (Ministério da Saúde) respondem. Reexecutável: rode de novo em outro dia.

Uso: python -u -I scripts/08_teste_acesso_siops.py
Grava o resultado em dados_brutos/siops_teste_acesso.csv, acrescentando uma linha por teste (com data e hora).
Um servidor que não responde é registrado como falha, nunca ignorado.
"""
import csv
import urllib.request
from datetime import datetime
from pathlib import Path

PASTA = Path(__file__).resolve().parent.parent / "dados_brutos"
ARQUIVO = PASTA / "siops_teste_acesso.csv"
PAGINAS = {
    "gov.br: página do SIOPS": "https://www.gov.br/saude/pt-br/acesso-a-informacao/siops",
    "SIOPS: % aplicado LC 141, municípios": "http://siops.datasus.gov.br/rel_perc_LC141.php?e=2",
    "SIOPS: % aplicado LC 141, estados e DF": "http://siops.datasus.gov.br/rel_perc_LC141.php?e=1",
    "SIOPS: demonstrativo da saúde (RREO), municípios": "http://siops.datasus.gov.br/consleirespfiscal.php",
    "SIOPS: página inicial (http)": "http://siops.datasus.gov.br/",
    "SIOPS: página inicial (https)": "https://siops.datasus.gov.br/",
}


def testar(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(pedido, timeout=25) as resposta:
            return resposta.status, len(resposta.read()), ""
    except Exception as erro:
        return "", 0, str(erro)[:100]


def main():
    PASTA.mkdir(exist_ok=True)
    novo = not ARQUIVO.exists()
    agora = datetime.now().isoformat(timespec="seconds")
    with open(ARQUIVO, "a", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f)
        if novo:
            escritor.writerow(["testado_em", "pagina", "url", "status_http", "bytes", "erro"])
        for nome, url in PAGINAS.items():
            status, tamanho, erro = testar(url)
            escritor.writerow([agora, nome, url, status, tamanho, erro])
            print(f"{'OK  ' if status == 200 else 'FALHA'} | {nome} | {status or erro}")


if __name__ == "__main__":
    main()
