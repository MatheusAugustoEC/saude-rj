"""Monta e executa o notebook (versão 2) a partir de cells_measure.py. Uso: python build_nb2.py"""
import importlib.util
import subprocess
import sys
from pathlib import Path

import nbformat

ESCRATCH = Path(__file__).resolve().parent
PROJETO = Path(__file__).resolve().parents[2]
destino = PROJETO / "notebooks" / "02_measure_qualidade_e_baseline.ipynb"

spec = importlib.util.spec_from_file_location("cells_measure", ESCRATCH / "cells_measure.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

nb = nbformat.v4.new_notebook()
nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
for tipo, texto in mod.CELULAS:
    nb.cells.append(nbformat.v4.new_markdown_cell(texto) if tipo == "md" else nbformat.v4.new_code_cell(texto))
nbformat.write(nb, destino)
print("Notebook montado:", destino, "|", len(nb.cells), "células")

r = subprocess.run([sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute", "--inplace",
                    "--ExecutePreprocessor.timeout=600", str(destino)], capture_output=True, text=True)
print("nbconvert exit", r.returncode)
print((r.stderr or "")[-3500:])
