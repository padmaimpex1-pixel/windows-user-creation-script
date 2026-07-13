# Free-Up-CDrive.ps1
# Run in PowerShell as Administrator

param(
    [switch]$Aggressive,
    [switch]$NoPrompt
)

$ErrorActionPreference = "Stop"

function Get-FreeGB {
    $drive = Get-PSDrive -Name C
    [math]::Round($drive.Free / 1GB, 2)
}

function Remove-IfExists {
    param([string]$Path)
    if (Test-Path $Path) {
        try {
            Remove-Item -Path $Path -Recurse -Force -ErrorAction Stop
            Write-Host "Cleaned: $Path"
        } catch {
            Write-Warning "Could not clean $Path : $($_.Exception.Message)"
        }
    }
}

$before = Get-FreeGB
Write-Host "Free space before cleanup: $before GB"

if (-not $NoPrompt) {
    $ans = Read-Host "Proceed with cleanup? (Y/N)"
    if ($ans -notin @("Y", "y", "Yes", "yes")) {
        Write-Host "Cleanup canceled."
        exit 0
    }
}

Write-Host "`nCleaning temp files..."
Remove-IfExists "$env:TEMP\*"
Remove-IfExists "C:\Windows\Temp\*"

Write-Host "`nCleaning Windows Update cache..."
try {
    Stop-Service wuauserv -Force -ErrorAction SilentlyContinue
    Stop-Service bits -Force -ErrorAction SilentlyContinue
    Remove-IfExists "C:\Windows\SoftwareDistribution\Download\*"
    Start-Service wuauserv -ErrorAction SilentlyContinue
    Start-Service bits -ErrorAction SilentlyContinue
} catch {
    Write-Warning "Windows Update cache cleanup issue: $($_.Exception.Message)"
}

Write-Host "`nCleaning Delivery Optimization cache..."
Remove-IfExists "C:\Windows\SoftwareDistribution\DeliveryOptimization\*"

Write-Host "`nEmptying Recycle Bin..."
try {
    Clear-RecycleBin -Force -ErrorAction SilentlyContinue
} catch {
    Write-Warning "Could not fully clear Recycle Bin."
}

if ($Aggressive) {
    Write-Host "`nRunning DISM component cleanup (can take time)..."
    try {
        DISM /Online /Cleanup-Image /StartComponentCleanup
    } catch {
        Write-Warning "DISM cleanup failed: $($_.Exception.Message)"
    }
}

$after = Get-FreeGB
$freed = [math]::Round($after - $before, 2)

Write-Host "`nFree space after cleanup: $after GB"
Write-Host "Total freed: $freed GB"
