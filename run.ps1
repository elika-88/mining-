[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendRoot = Join-Path $projectRoot "backend"
$python = Join-Path $backendRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Python environment not found. Follow the Setup section in README.md first."
}

$backend = $null
$frontend = $null

try {
    $backend = Start-Process -FilePath $python `
        -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000" `
        -WorkingDirectory $backendRoot -WindowStyle Hidden -PassThru
    $frontend = Start-Process -FilePath $python `
        -ArgumentList "-m", "http.server", "5173", "--bind", "127.0.0.1" `
        -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru

    Start-Sleep -Seconds 2
    if ($backend.HasExited -or $frontend.HasExited) {
        throw "A demo service failed to start. Check whether ports 8000 and 5173 are available."
    }

    Write-Host "MineShift demo is running." -ForegroundColor Green
    Write-Host "Application: http://127.0.0.1:5173"
    Write-Host "API docs:    http://127.0.0.1:8000/docs"
    Write-Host "Press Ctrl+C to stop both services."

    while (-not $backend.HasExited -and -not $frontend.HasExited) {
        Start-Sleep -Seconds 1
        $backend.Refresh()
        $frontend.Refresh()
    }

    throw "A demo service stopped unexpectedly."
}
finally {
    foreach ($process in @($backend, $frontend)) {
        if ($null -ne $process -and -not $process.HasExited) {
            Stop-Process -Id $process.Id
        }
    }
}
