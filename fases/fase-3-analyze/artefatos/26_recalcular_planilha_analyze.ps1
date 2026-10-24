# Recalcula a planilha do Analyze com o Excel (grava os valores das formulas).
# Uso (PowerShell, na raiz do projeto): powershell -ExecutionPolicy Bypass -File .\scripts\26_recalcular_planilha_analyze.ps1
$raiz = Split-Path -Parent $PSScriptRoot
$origem = Join-Path $raiz "planilhas\saude_fiscal_rj_analyze.xlsx"
$copia = Join-Path $raiz "planilhas\saude_fiscal_rj_analyze_calc.xlsx"
if (Test-Path $copia) { Remove-Item $copia -Force }
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false
try {
    $wb = $xl.Workbooks.Open($origem)
    $xl.CalculateFull()
    $wb.SaveAs($copia, 51)
    "Recalculada: $copia"
    $wb.Close($false)
} catch { "ERRO: " + $_.Exception.Message } finally { $xl.Quit(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) }
