$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$running = Get-Process -Name "Pencil" -ErrorAction SilentlyContinue
if (-not $running) {
  Write-Host "Pencil is not running. Please start Pencil desktop app first."
}

$env:CODEX_HOME = Join-Path $projectRoot ".codex-home"
if (-not (Test-Path $env:CODEX_HOME)) {
  New-Item -ItemType Directory -Force -Path $env:CODEX_HOME | Out-Null
}

& codex @args
