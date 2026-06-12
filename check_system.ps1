# Check system status
$disk = Get-PhysicalDisk | Select-Object -First 1
Write-Host "Disk Health: $($disk.HealthStatus)"
Write-Host "Disk Type: $($disk.MediaType)"

# Check Windows Update cache
$softwareDist = (Get-ChildItem "C:\Windows\SoftwareDistribution" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
Write-Host "Windows Update Cache: $([math]::Round($softwareDist/1GB,2)) GB"

# Check temp files
$tempSize = (Get-ChildItem "$env:TEMP" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
Write-Host "Temp Files: $([math]::Round($tempSize/1GB,2)) GB"

# Check Prefetch
$prefetchSize = (Get-ChildItem "C:\Windows\Prefetch" -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
Write-Host "Prefetch: $([math]::Round($prefetchSize/1MB,2)) MB"

# Check recent updates
Write-Host "`nRecent Updates:"
Get-HotFix | Where-Object { $_.InstalledOn -gt (Get-Date).AddDays(-7) } | Select-Object HotFixID,Description,InstalledOn | Format-Table -AutoSize