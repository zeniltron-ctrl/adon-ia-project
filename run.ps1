Write-Host "┌────────────────────────┐" -ForegroundColor Cyan
Write-Host "│      Adon-ia LLM      │" -ForegroundColor Cyan
Write-Host "└────────────────────────┘" -ForegroundColor Cyan
Write-Host ""

$ollama = $null
# Troque "eurico" pelo seu usuário do Windows
$ollamaPath = "C:\Users\eurico\AppData\Local\Programs\Ollama\ollama app.exe"

try {
  $null = Invoke-WebRequest -Uri 'http://127.0.0.1:11434/api/tags' -UseBasicParsing -TimeoutSec 2
  Write-Host "  Ollama ja esta rodando." -ForegroundColor Green
} catch {
  Write-Host "  Iniciando Ollama em 2o plano..." -ForegroundColor Yellow
  $ollama = Start-Process -FilePath $ollamaPath -WindowStyle Hidden -PassThru
  $i = 0
  while ($i -lt 15) {
    Start-Sleep -Seconds 1
    try { $null = Invoke-WebRequest -Uri 'http://127.0.0.1:11434/api/tags' -UseBasicParsing -TimeoutSec 1; break } catch {}
    $i++
  }
  if ($i -eq 15) { Write-Host "  Falha ao iniciar Ollama!" -ForegroundColor Red; exit 1 }
  Write-Host "  Ollama pronto." -ForegroundColor Green
}

$app = Join-Path $PSScriptRoot "app.py"
$webui = Start-Process -FilePath "python" -ArgumentList $app -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 2
Write-Host "  WebUI pronto." -ForegroundColor Green
Write-Host ""
Write-Host "  http://localhost:12800" -ForegroundColor Cyan
Write-Host "  ESC para parar tudo." -ForegroundColor Yellow
Write-Host ""

while ($true) {
  if ([Console]::KeyAvailable) {
    $key = [Console]::ReadKey($true)
    if ($key.Key -eq 'Escape') { break }
  }
  if ($webui.HasExited) { Write-Host "  WebUI encerrou." -ForegroundColor Red; break }
  Start-Sleep -Milliseconds 200
}

Write-Host "  Parando..." -ForegroundColor Yellow
if (-not $webui.HasExited) { $webui.Kill() }
if ($ollama -and -not $ollama.HasExited) { $ollama.Kill() }
Write-Host "  Processos encerrados." -ForegroundColor Green
