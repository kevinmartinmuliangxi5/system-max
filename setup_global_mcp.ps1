$ErrorActionPreference = "Stop"

$codexHome = "$env:USERPROFILE\.codex"
New-Item -ItemType Directory -Force -Path $codexHome | Out-Null
$env:CODEX_HOME = $codexHome

Write-Host "Using CODEX_HOME=$env:CODEX_HOME"

codex mcp add context7 -- npx -y @upstash/context7-mcp
codex mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
codex mcp add pencil -- "D:\AI相关\pencil\resources\app.asar.unpacked\out\mcp-server-windows-x64.exe" --app desktop

Write-Host "`nDone. Current global MCP servers:"
codex mcp list
