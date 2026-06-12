# Check if restart is pending
$pendingRestart = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending" -ErrorAction SilentlyContinue
$wuReboot = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired" -ErrorAction SilentlyContinue

if ($pendingRestart -or $wuReboot) {
    Write-Host "RESTART PENDING - System needs reboot to complete updates"
} else {
    Write-Host "No restart pending"
}

# Check if Windows is still indexing
$wsearch = Get-Service WSearch
Write-Host "Windows Search Status: $($wsearch.Status)"
Write-Host "Windows Search StartType: $($wsearch.StartType)"

# Check disk space
$cDrive = Get-PSDrive C
Write-Host "C Drive Free: $([math]::Round($cDrive.Free/1GB,2)) GB"
Write-Host "D Drive Free: $([math]::Round((Get-PSDrive D).Free/1GB,2)) GB"