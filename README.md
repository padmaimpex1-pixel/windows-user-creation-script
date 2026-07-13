# windows-user-creation-script

PowerShell scripts to create and prepare local Windows user accounts.

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

## Script 4: Set up git + SSH for each user and clone starter repo

Configures per-user git identity, generates SSH keys, and clones starter repo.

```powershell
.\Setup-Git-For-Users.ps1
```

## Script 5: Export all users' public SSH keys

Collects keys into one file:

```powershell
.\Export-User-SSH-PublicKeys.ps1
```

Output file:

- `C:\Users\Public\all-user-ssh-public-keys.txt`

## Script 6: Free up C drive (standard cleanup)

```powershell
.\Free-Up-CDrive.ps1
```

Optional aggressive mode:

```powershell
.\Free-Up-CDrive.ps1 -Aggressive
```

## Script 7: Free up C drive (deep cleanup)

```powershell
.\Deep-Free-Up-CDrive.ps1
```

Optional downloads + aggressive mode:

```powershell
.\Deep-Free-Up-CDrive.ps1 -CleanDownloads -DownloadsDays 30 -Aggressive
```

## Notes

- Run scripts in **PowerShell as Administrator**.
- Users that already exist are skipped by creation scripts.
- Replace example passwords before production use.
