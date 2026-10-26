"""
Cópia usada pelo projeto (Edge sem cabeça, no Windows). Gera o PDF de um relatório de fase a partir do relatorio.md, com o estilo do método.

Uso:
    python gerar_pdf.py <relatorio.md> [--acento "#2F5D8A"] [--projeto "Nome do projeto"]

Grava relatorio.pdf (e relatorio.html, útil para conferir) ao lado do .md.
Precisa de: pip install markdown playwright  e  python -m playwright install chromium

O que o markdown pode usar, além do comum:
  > [!IMPORTANT]  vira caixa de ACHADO
  > [!TIP]        vira caixa de DECISÃO
  > [!NOTE]       vira caixa de DETALHE TÉCNICO
  > [!WARNING]    vira caixa de CUIDADO
  > [!CAUTION]    vira caixa de FALHA
  (a mesma sintaxe dos alertas do GitHub — o .md continua bonito no GitHub também)

  <div class="numero"><b>64,3%</b><span>da ausência é evitável</span></div>
  <div class="numeros"> …vários .numero… </div>
  <div class="resumo" markdown="1"> …texto… </div>
  <span class="ok">OK</span> <span class="ressalva">RESSALVA</span> <span class="falha-t">FALHA</span>
  ![legenda](artefatos/grafico.png)   — imagens com caminho relativo ao .md
"""
import sys, re, pathlib, argparse, base64, mimetypes
import markdown
import subprocess, shutil, tempfile

ap = argparse.ArgumentParser()
ap.add_argument('md')
ap.add_argument('--acento', default=None)
ap.add_argument('--projeto', default='')
ap.add_argument('--saida', default=None, help='caminho do PDF; o HTML intermediário vai para uma pasta temporária')
a = ap.parse_args()

src = pathlib.Path(a.md).resolve()
css = (pathlib.Path(__file__).parent / 'relatorio.css').read_text(encoding='utf-8')
if a.acento:
    css += '\n:root{--acc:%s}\n' % a.acento
texto = src.read_text(encoding='utf-8')

TIPOS = {'IMPORTANT': ('achado', 'Achado'), 'TIP': ('decisao', 'Decisão'),
         'NOTE': ('tecnico', 'Detalhe técnico'), 'WARNING': ('cuidado', 'Cuidado'),
         'CAUTION': ('falha', 'Falha')}

def listas(md):
    """Lista logo abaixo de um parágrafo precisa de linha em branco antes, senão
    vira texto corrido — erro comum de quem escreve o relatório."""
    out = []
    for ln in md.split('\n'):
        eh_item = re.match(r'^\s*([-*+]|\d+\.)\s', ln)
        if eh_item and out and out[-1].strip() and not re.match(r'^\s*([-*+]|\d+\.)\s', out[-1]) and not out[-1].startswith('>'):
            out.append('')
        out.append(ln)
    return '\n'.join(out)

def caixas(md):
    """Troca blocos '> [!TIPO]' por <div class="caixa tipo" markdown="1">."""
    out, i, linhas = [], 0, md.split('\n')
    while i < len(linhas):
        m = re.match(r'^>\s*\[!(\w+)\]\s*(.*)$', linhas[i])
        if m and m.group(1).upper() in TIPOS:
            cls, rot = TIPOS[m.group(1).upper()]
            corpo = [m.group(2)] if m.group(2) else []
            i += 1
            while i < len(linhas) and linhas[i].startswith('>'):
                corpo.append(re.sub(r'^>\s?', '', linhas[i])); i += 1
            out += ['', f'<div class="caixa {cls}" markdown="1">', f'<div class="rot">{rot}</div>', '']
            out += corpo + ['', '</div>', '']
            continue
        out.append(linhas[i]); i += 1
    return '\n'.join(out)

corpo = markdown.markdown(caixas(listas(texto)), extensions=['tables', 'fenced_code', 'md_in_html', 'attr_list', 'sane_lists'])

# cabeçalho: o H1 e a linha de metadados logo abaixo dele viram o bloco .cab
m = re.search(r'<h1>(.*?)</h1>\s*<p>(.*?)</p>', corpo, re.S)
if m:
    titulo, meta = m.group(1), m.group(2)
    fase = ''
    mf = re.match(r'(Fase[^·—\-]*)[·—\-]\s*(.*)', meta)
    if mf:
        fase, meta = mf.group(1).strip(), mf.group(2).strip()
    cab = f'<header class="cab"><div class="fase">{fase}</div><h1>{titulo}</h1><div class="meta">{meta}</div></header>'
    corpo = corpo[:m.start()] + cab + corpo[m.end():]

# numeração dos H2 ("## 1. A pergunta" → número em destaque)
corpo = re.sub(r'<h2>(\d+)\.\s*', r'<h2><span class="n">\1</span>', corpo)

# imagens embutidas no próprio HTML: o PDF não depende do caminho (nem do limite
# de 260 caracteres do Windows) e o .html fica autocontido
faltando_arq = []
def embute(m):
    alvo = m.group(2)
    if re.match(r'^(data:|https?:)', alvo):
        return m.group(0)
    arq = (src.parent / alvo).resolve()
    if not arq.exists():
        faltando_arq.append(alvo); return m.group(0)
    tipo = mimetypes.guess_type(str(arq))[0] or 'image/png'
    return '%s"data:%s;base64,%s"' % (m.group(1), tipo, base64.b64encode(arq.read_bytes()).decode())
corpo = re.sub(r'(<img[^>]*?src=)"([^"]+)"', embute, corpo)

html = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;650;700&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
{corpo}
</body></html>'''

out_html = (pathlib.Path(tempfile.mkdtemp()) / (src.stem + '.html')) if a.saida else src.with_suffix('.html')
out_html.write_text(html, encoding='utf-8')
out_pdf = pathlib.Path(a.saida).resolve() if a.saida else src.with_suffix('.pdf')
edge = shutil.which('msedge') or r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
cmd = [edge, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--run-all-compositor-stages-before-draw',
       '--virtual-time-budget=15000', '--print-to-pdf=' + str(out_pdf), out_html.as_uri()]
subprocess.run(cmd, check=True, capture_output=True, timeout=180)
print('PDF:', out_pdf)
if faltando_arq:
    print('IMAGENS QUE NAO CARREGARAM (confira o caminho):', faltando_arq)
