# windows-user-creation-script

PowerShell scripts to create local Windows user accounts.

## Script 1: Create 7 default users

Creates users `user01` to `user07` with a shared temporary password.

```powershell
.\Create-7Users.ps1
```

## Script 2: Create custom users with unique passwords

Edit the `$accounts` list in `Create-CustomUsers.ps1` with your own usernames and passwords, then run:

```powershell
.\Create-CustomUsers.ps1
```

## Script 3: Login/logout each custom account once

Runs a non-interactive process under each account, then exits it.

```powershell
.\Login-Logout-Users.ps1
```

## Notes

- Run scripts in **PowerShell as Administrator**.
- Users that already exist are skipped.
- Replace example passwords before production use.
