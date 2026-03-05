# Disable Windows Store Python Alias
Write-Host "Disabling Python Store Alias..." -ForegroundColor Cyan

# Method 1: Disable via registry
$keyPath = "HKLM:\Software\Microsoft\Windows\CurrentVersion\AppExecutionAlias"
if (Test-Path $keyPath) {
    try {
        $pythonVal = (Get-ItemProperty -Path $keyPath -Name "python.exe" -ErrorAction SilentlyContinue)."python.exe"
        $python3Val = (Get-ItemProperty -Path $keyPath -Name "python3.exe" -ErrorAction SilentlyContinue)."python3.exe"
        
        Write-Host "Current python.exe value: $pythonVal" -ForegroundColor Yellow
        Write-Host "Current python3.exe value: $python3Val" -ForegroundColor Yellow
        
        Set-ItemProperty -Path $keyPath -Name "python.exe" -Value "" -Force
        Set-ItemProperty -Path $keyPath -Name "python3.exe" -Value "" -Force
        
        Write-Host "OK: Disabled system-level Python aliases" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: $_" -ForegroundColor Red
    }
} else {
    Write-Host "Registry path not found" -ForegroundColor Yellow
}

# Method 2: Check WindowsApps directory
$wappsPath = "$env:LOCALAPPDATA\Microsoft\WindowsApps"
if (Test-Path $wappsPath) {
    Write-Host "Checking WindowsApps directory..." -ForegroundColor Cyan
    
    $pythonExe = Join-Path $wappsPath "python.exe"
    $python3Exe = Join-Path $wappsPath "python3.exe"
    
    if (Test-Path $pythonExe) {
        Write-Host "Found: $pythonExe" -ForegroundColor Yellow
        $target = Get-Item $pythonExe
        if ($target.LinkType -eq "SymbolicLink" -or $target.LinkType -eq "Junction") {
            Remove-Item -Path $pythonExe -Force -ErrorAction SilentlyContinue
            Write-Host "Removed python.exe symlink" -ForegroundColor Green
        } else {
            Rename-Item -Path $pythonExe -NewName "python.exe.disabled" -Force -ErrorAction SilentlyContinue
            Write-Host "Disabled python.exe alias" -ForegroundColor Green
        }
    }
    
    if (Test-Path $python3Exe) {
        Write-Host "Found: $python3Exe" -ForegroundColor Yellow
        $target = Get-Item $python3Exe
        if ($target.LinkType -eq "SymbolicLink" -or $target.LinkType -eq "Junction") {
            Remove-Item -Path $python3Exe -Force -ErrorAction SilentlyContinue
            Write-Host "Removed python3.exe symlink" -ForegroundColor Green
        } else {
            Rename-Item -Path $python3Exe -NewName "python3.exe.disabled" -Force -ErrorAction SilentlyContinue
            Write-Host "Disabled python3.exe alias" -ForegroundColor Green
        }
    }
}

Write-Host ""
Write-Host "Done! Please restart your terminal." -ForegroundColor Green
