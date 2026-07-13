# Run in PowerShell as Administrator
# Sets git name/email, creates SSH key, and clones starter repo for each user.

$accounts = @(
    @{ User = "alice";   Password = "Alice@12345" },
    @{ User = "bob";     Password = "Bob@12345" },
    @{ User = "charlie"; Password = "Charlie@12345" },
    @{ User = "diana";   Password = "Diana@12345" },
    @{ User = "ethan";   Password = "Ethan@12345" },
    @{ User = "fiona";   Password = "Fiona@12345" },
    @{ User = "george";  Password = "George@12345" }
)

$starterRepoUrl = "https://github.com/padmaimpex1-pixel/starter-repo.git"
$bootstrapScript = "C:\Users\Public\setup-user-git-bootstrap.ps1"
$statusDir = "C:\Users\Public\git-setup-status"
New-Item -ItemType Directory -Path $statusDir -Force | Out-Null

@'
param(
    [string]$UserName,
    [string]$UserEmail,
    [string]$RepoUrl,
    [string]$StatusDir
)
$ErrorActionPreference = "Stop"
$env:HOME = $env:USERPROFILE

git config --global user.name $UserName
if ($LASTEXITCODE -ne 0) { throw "git config user.name failed" }

git config --global user.email $UserEmail
if ($LASTEXITCODE -ne 0) { throw "git config user.email failed" }

$sshDir = Join-Path $env:USERPROFILE ".ssh"
if (-not (Test-Path $sshDir)) { New-Item -ItemType Directory -Path $sshDir -Force | Out-Null }

$keyPath = Join-Path $sshDir "id_ed25519"
if (-not (Test-Path $keyPath)) {
    $cmd = "ssh-keygen -t ed25519 -C `"" + $UserEmail + "`" -N `"`" -f `"" + $keyPath + "`""
    cmd.exe /c $cmd | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "ssh-keygen failed" }
}

$docs = Join-Path $env:USERPROFILE "Documents"
if (-not (Test-Path $docs)) { New-Item -ItemType Directory -Path $docs -Force | Out-Null }

$target = Join-Path $docs "starter-repo"
if (-not (Test-Path $target)) {
    git clone $RepoUrl $target | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
}

[PSCustomObject]@{
    user = $UserName
    name = (git config --global user.name)
    email = (git config --global user.email)
    repoPath = $target
    repoExists = (Test-Path (Join-Path $target ".git"))
    sshPublicKeyPath = "$keyPath.pub"
    sshPublicKeyExists = (Test-Path "$keyPath.pub")
} | ConvertTo-Json -Compress | Set-Content -Encoding ASCII -Path (Join-Path $StatusDir ($UserName + ".json"))
'@ | Set-Content -Path $bootstrapScript -Encoding ASCII

$computer = $env:COMPUTERNAME

foreach ($a in $accounts) {
    $u = $a.User
    $secure = ConvertTo-SecureString $a.Password -AsPlainText -Force
    $cred = New-Object System.Management.Automation.PSCredential("$computer\$u", $secure)

    try {
        $args = "-NoProfile -ExecutionPolicy Bypass -File `"$bootstrapScript`" -UserName `"$u`" -UserEmail `"$u@local`" -RepoUrl `"$starterRepoUrl`" -StatusDir `"$statusDir`""
        $p = Start-Process -FilePath "powershell.exe" -Credential $cred -LoadUserProfile -ArgumentList $args -WindowStyle Hidden -PassThru
        $p.WaitForExit()

        if ($p.ExitCode -eq 0) {
            Write-Host "Configured git+ssh for $u"
        } else {
            Write-Host "Failed for $u (exit $($p.ExitCode))"
        }
    }
    catch {
        Write-Host "Failed for $u : $($_.Exception.Message)"
    }
}

Write-Host "--- Status ---"
Get-ChildItem -Path $statusDir -Filter "*.json" | Select-Object -ExpandProperty FullName

# Cleanup bootstrap script
Remove-Item -Path $bootstrapScript -Force -ErrorAction SilentlyContinue
