# Run this script in PowerShell as Administrator

$users = @(
    "user01",
    "user02",
    "user03",
    "user04",
    "user05",
    "user06",
    "user07"
)

# Temporary password for all new users (change this before use)
$tempPassword = ConvertTo-SecureString "Temp@12345" -AsPlainText -Force

foreach ($u in $users) {
    if (Get-LocalUser -Name $u -ErrorAction SilentlyContinue) {
        Write-Host "User '$u' already exists. Skipping."
    } else {
        New-LocalUser `
            -Name $u `
            -Password $tempPassword `
            -FullName $u `
            -Description "Local account $u"

        Add-LocalGroupMember -Group "Users" -Member $u
        Write-Host "Created user: $u"
    }
}
