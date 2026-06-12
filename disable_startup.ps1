# Disable unnecessary startup programs
$startupPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$toDisable = @(
    "OneDrive",
    "Steam",
    "QianwenUpdaterTaskUser1.0.0.3",
    "GameViewer",
    "EPSDNMON",
    "qianwen",
    "EPPCCMON"
)

foreach ($item in $toDisable) {
    Remove-ItemProperty -Path $startupPath -Name $item -ErrorAction SilentlyContinue
    Write-Host "Disabled: $item"
}

# Also disable from Task Manager startup
Get-CimInstance Win32_StartupCommand | Where-Object { 
    $_.Name -match "OneDrive|Steam|Qianwen|GameViewer|EPSDNMON|EPPCCMON"
} | ForEach-Object {
    Write-Host "Found: $($_.Name) - Location: $($_.Location)"
}

Write-Host "Done"