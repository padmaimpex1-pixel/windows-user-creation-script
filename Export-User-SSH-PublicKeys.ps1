# Run in PowerShell as Administrator (or user with permission to read all profiles)
# Exports all configured users' public SSH keys into one text file.

$users = @("alice","bob","charlie","diana","ethan","fiona","george")
$outputPath = "C:\Users\Public\all-user-ssh-public-keys.txt"

$lines = @()
foreach ($u in $users) {
    $keyPath = "C:\Users\$u\.ssh\id_ed25519.pub"
    $lines += "[$u]"

    if (Test-Path $keyPath) {
        $lines += (Get-Content -Path $keyPath -Raw).Trim()
    } else {
        $lines += "MISSING"
    }

    $lines += ""
}

Set-Content -Path $outputPath -Value $lines -Encoding ASCII
Write-Host "Exported keys to: $outputPath"
Get-Content -Path $outputPath
