# Self-elevate check if you want (optional)

$currentUser = "$env:USERDOMAIN\$env:USERNAME"

$action = New-ScheduledTaskAction -Execute "C:\Program Files\obs-studio\bin\64bit\obs64.exe" `
    -Argument "--disable-shutdown-check --startreplaybuffer --minimize-to-tray" `
    -WorkingDirectory "C:\Program Files\obs-studio\bin\64bit\"

$trigger = New-ScheduledTaskTrigger -AtLogOn -User $currentUser

$principal = New-ScheduledTaskPrincipal -UserId $currentUser -LogonType Interactive -RunLevel Highest

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "Start OBS Replay Buffer" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force

Write-Host "Scheduled task created successfully."
Pause
