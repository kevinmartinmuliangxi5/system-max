$ErrorActionPreference = "Stop"

# Official guidance: run Pencil desktop app, then use MCP in your AI client.
# This script prepares a stable local MCP server path and registers it in CODEX_HOME.

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$toolsDir = Join-Path $projectRoot "tools"
$localServer = Join-Path $toolsDir "pencil-mcp-server.exe"
$sourceServer = $null

if (Test-Path $localServer) {
  $sourceServer = $localServer
} else {
  $found = Get-ChildItem -Path "D:\" -Filter "mcp-server-windows-x64.exe" -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -match "\\pencil\\resources\\app\.asar\.unpacked\\out\\" } |
    Select-Object -First 1
  if ($found) {
    $sourceServer = $found.FullName
  }
}

if (-not $sourceServer) {
  throw "Pencil MCP server not found. Start Pencil once, then retry."
}

New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null
if ($sourceServer -ne $localServer) {
  Copy-Item -Force $sourceServer $localServer
}

$env:CODEX_HOME = Join-Path $projectRoot ".codex-home"
New-Item -ItemType Directory -Force -Path $env:CODEX_HOME | Out-Null

codex mcp remove pencil *> $null
codex mcp add pencil -- "$localServer" --app desktop

Write-Host "Configured CODEX_HOME=$env:CODEX_HOME"
Write-Host "Pencil MCP server path: $localServer"
Write-Host ""
codex mcp get pencil
