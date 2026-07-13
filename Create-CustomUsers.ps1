# Run this script in PowerShell as Administrator

# Define custom users and unique passwords
$accounts = @(
    @{ Username = "alice"; Password = "Alice@12345" },
    @{ Username = "bob"; Password = "Bob@12345" },
    @{ Username = "charlie"; Password = "Charlie@12345" },
    @{ Username = "diana"; Password = "Diana@12345" },
    @{ Username = "ethan"; Password = "Ethan@12345" },
    @{ Username = "fiona"; Password = "Fiona@12345" },
    @{ Username = "george"; Password = "George@12345" }
)

foreach ($account in $accounts) {
    $username = $account.Username
    $securePassword = ConvertTo-SecureString $account.Password -AsPlainText -Force

    if (Get-LocalUser -Name $username -ErrorAction SilentlyContinue) {
        Write-Host "User '$username' already exists. Skipping."
    } else {
        New-LocalUser `
            -Name $username `
            -Password $securePassword `
            -FullName $username `
            -Description "Local account $username"

        Add-LocalGroupMember -Group "Users" -Member $username
        Write-Host "Created user: $username"
    }
}
