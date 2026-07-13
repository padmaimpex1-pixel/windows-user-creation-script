# Run in PowerShell as Administrator

$accounts = @(
    @{ User = "alice";   Password = "Alice@12345" },
    @{ User = "bob";     Password = "Bob@12345" },
    @{ User = "charlie"; Password = "Charlie@12345" },
    @{ User = "diana";   Password = "Diana@12345" },
    @{ User = "ethan";   Password = "Ethan@12345" },
    @{ User = "fiona";   Password = "Fiona@12345" },
    @{ User = "george";  Password = "George@12345" }
)

$computer = $env:COMPUTERNAME

foreach ($a in $accounts) {
    $user = $a.User
    $secure = ConvertTo-SecureString $a.Password -AsPlainText -Force
    $cred = New-Object System.Management.Automation.PSCredential("$computer\$user", $secure)

    try {
        $p = Start-Process -FilePath "cmd.exe" `
            -ArgumentList "/c whoami > `"%TEMP%\$user-whoami.txt`"" `
            -Credential $cred `
            -LoadUserProfile `
            -WindowStyle Hidden `
            -PassThru

        $p.WaitForExit()
        Write-Host "Login/logout successful for $user"
    }
    catch {
        Write-Host "Failed for $user : $($_.Exception.Message)"
    }
}
