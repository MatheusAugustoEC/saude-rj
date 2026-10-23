# Recalcula a planilha com o Excel (grava os valores das formulas) e exporta os graficos como imagem, para conferencia visual.
# Uso (PowerShell, na raiz do projeto): powershell -ExecutionPolicy Bypass -File .\scripts\11_recalcular_planilha.ps1
# Entrada: planilhas\saude_fiscal_rj_2024.xlsx (gerada por 09_gerar_planilha.py, sem valores calculados)
# Saidas:  planilhas\saude_fiscal_rj_2024_calc.xlsx (recalculada) e imagens dos graficos na pasta temporaria do usuario.
# Observacao: o Excel automatizado as vezes rejeita chamadas quando esta ocupado. Por isso ha esperas e repeticoes.
$raiz = Split-Path -Parent $PSScriptRoot
$origem = Join-Path $raiz "planilhas\saude_fiscal_rj_2024.xlsx"
$copia = Join-Path $raiz "planilhas\saude_fiscal_rj_2024_calc.xlsx"
if (Test-Path $copia) { Remove-Item $copia -Force }
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false
try {
    $wb = $xl.Workbooks.Open($origem)
    $xl.CalculateFull()
    $wb.SaveAs($copia, 51)
    "Recalculada: $copia"
    $aba = $wb.Worksheets.Item(6)   # aba dos graficos (sexta); por posicao porque o PowerShell 5.1 nao le o acento do nome
    $n = $aba.ChartObjects().Count
    for ($i = 1; $i -le $n; $i++) {
        $img = Join-Path $env:TEMP ("graficos_planilha_{0}.png" -f $i)
        if (Test-Path $img) { Remove-Item $img -Force }
        for ($tentativa = 1; $tentativa -le 6; $tentativa++) {
            try { Start-Sleep -Seconds 4; [void]$aba.ChartObjects().Item($i).Chart.Export($img); break } catch { if ($tentativa -eq 6) { throw } }
        }
        "Grafico $i exportado: $img"
    }
    $wb.Close($false)
} catch { "ERRO: " + $_.Exception.Message } finally { $xl.Quit(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) }
