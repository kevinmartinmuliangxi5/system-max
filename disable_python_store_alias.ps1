# PowerShell脚本 - 禁用Python Store Alias
# 管理员权限运行

Write-Host "禁用Windows应用商店的Python别名..." -ForegroundColor Yellow

# 禁用python.exe别名
$keyPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\AppExecutionAlias"
if (Test-Path "$keyPath") {
    Set-ItemProperty -Path "$keyPath" -Name "python.exe" -Value "" -Force
    Set-ItemProperty -Path "$keyPath" -Name "python3.exe" -Value "" -Force
    Write-Host "✅ 已禁用python.exe和python3.exe的应用商店别名" -ForegroundColor Green
} else {
    Write-Host "⚠️  未找到AppExecutionAlias注册表项" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "完成！现在重启终端即可生效。" -ForegroundColor Green
Write-Host "如果仍有问题，请确保Python已正确安装并添加到PATH。" -ForegroundColor Cyan
