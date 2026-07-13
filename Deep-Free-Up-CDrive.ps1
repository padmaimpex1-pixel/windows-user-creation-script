# Deep-Free-Up-CDrive.ps1
# Run in PowerShell as Administrator
# Safe defaults: cleans temp/cache/logs/dumps only.
# Optional: clean Downloads older than N days using -CleanDownloads -DownloadsDays 30

param(
    [switch]$Aggressive,
    [switch]$CleanDownloads,
    [int]$DownloadsDays = 30,
    [switch]$NoPrompt
)

$ErrorActionPreference = "Stop"

function Get-FreeGB {
    $drive = Get-PSDrive -Name C
    [math]::Round($drive.Free / 1GB, 2)
}

function Remove-PathSafe {
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

function Remove-ChildrenSafe {
    param([string]$Path)
    if (Test-Path $Path) {
        try {
            Get-ChildItem -Path $Path -Force -ErrorAction SilentlyContinue |
                Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "Cleaned contents: $Path"
        } catch {
            Write-Warning "Could not clean contents of $Path : $($_.Exception.Message)"
        }
    }
}

$before = Get-FreeGB
Write-Host "Free space before cleanup: $before GB"

if (-not $NoPrompt) {
    $ans = Read-Host "Proceed with deep cleanup? (Y/N)"
    if ($ans -notin @("Y", "y", "Yes", "yes")) {
        Write-Host "Cleanup canceled."
        exit 0
    }
}

Write-Host "`n[1/8] Cleaning temp locations..."
Remove-ChildrenSafe "$env:TEMP"
Remove-ChildrenSafe "C:\Windows\Temp"

Write-Host "`n[2/8] Cleaning update caches..."
try {
    Stop-Service wuauserv -Force -ErrorAction SilentlyContinue
    Stop-Service bits -Force -ErrorAction SilentlyContinue
    Remove-ChildrenSafe "C:\Windows\SoftwareDistribution\Download"
    Remove-ChildrenSafe "C:\Windows\SoftwareDistribution\DeliveryOptimization"
    Start-Service wuauserv -ErrorAction SilentlyContinue
    Start-Service bits -ErrorAction SilentlyContinue
} catch {
    Write-Warning "Update cache cleanup issue: $($_.Exception.Message)"
}

Write-Host "`n[3/8] Cleaning dump and error report files..."
Remove-ChildrenSafe "C:\Windows\Minidump"
Remove-PathSafe "C:\Windows\MEMORY.DMP"
Remove-ChildrenSafe "C:\ProgramData\Microsoft\Windows\WER\ReportArchive"
Remove-ChildrenSafe "C:\ProgramData\Microsoft\Windows\WER\ReportQueue"

Write-Host "`n[4/8] Cleaning log files..."
Get-ChildItem "C:\Windows\Logs" -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -in ".log", ".etl", ".txt", ".old" } |
    ForEach-Object {
        try { Remove-Item $_.FullName -Force -ErrorAction Stop } catch {}
    }
Write-Host "Cleaned log files under C:\Windows\Logs"

Write-Host "`n[5/8] Cleaning Prefetch..."
Remove-ChildrenSafe "C:\Windows\Prefetch"

Write-Host "`n[6/8] Emptying Recycle Bin..."
try {
    Clear-RecycleBin -Force -ErrorAction SilentlyContinue
} catch {
    Write-Warning "Could not fully clear Recycle Bin."
}

if ($CleanDownloads) {
    Write-Host "`n[7/8] Cleaning Downloads older than $DownloadsDays days..."
    $cutoff = (Get-Date).AddDays(-$DownloadsDays)
    Get-ChildItem "C:\Users" -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $dl = Join-Path $_.FullName "Downloads"
        if (Test-Path $dl) {
            Get-ChildItem $dl -Force -ErrorAction SilentlyContinue | Where-Object {
                $_.LastWriteTime -lt $cutoff
            } | ForEach-Object {
                try {
                    Remove-Item $_.FullName -Recurse -Force -ErrorAction Stop
                } catch {
                    Write-Warning "Could not remove $($_.FullName)"
                }
            }
            Write-Host "Processed: $dl"
        }
    }
} else {
    Write-Host "`n[7/8] Skipping Downloads cleanup (use -CleanDownloads to enable)."
}

if ($Aggressive) {
    Write-Host "`n[8/8] Running DISM component cleanup (can take time)..."
    try {
        DISM /Online /Cleanup-Image /StartComponentCleanup
    } catch {
        Write-Warning "DISM cleanup failed: $($_.Exception.Message)"
    }
} else {
    Write-Host "`n[8/8] Skipping DISM cleanup (use -Aggressive to enable)."
}

$after = Get-FreeGB
$freed = [math]::Round($after - $before, 2)

Write-Host "`nFree space after cleanup: $after GB"
Write-Host "Total freed: $freed GB"
