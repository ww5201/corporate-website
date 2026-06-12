# Final optimization steps
Write-Host "=== Final Optimization ==="

# 1. Clear DNS cache
ipconfig /flushdns | Out-Null
Write-Host "1. DNS cache cleared"

# 2. Clear Windows temp files
Remove-Item "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "2. Temp files cleared"

# 3. Clear thumbnail cache
Remove-Item "$env:LOCALAPPDATA\Microsoft\Windows\Explorer\thumbcache_*.db" -Force -ErrorAction SilentlyContinue
Write-Host "3. Thumbnail cache cleared"

# 4. Disable unnecessary scheduled tasks
$tasksToDisable = @(
    "\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser",
    "\Microsoft\Windows\Application Experience\ProgramDataUpdater",
    "\Microsoft\Windows\Autochk\Proxy",
    "\Microsoft\Windows\Customer Experience Improvement Program\Consolidator",
    "\Microsoft\Windows\Customer Experience Improvement Program\UsbCeip",
    "\Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector",
    "\Microsoft\Windows\Feedback\Siuf\DmClient",
    "\Microsoft\Windows\Maps\MapsToastTask",
    "\Microsoft\Windows\Maps\MapsUpdateTask"
)

foreach ($task in $tasksToDisable) {
    Disable-ScheduledTask -TaskName $task -ErrorAction SilentlyContinue | Out-Null
}
Write-Host "4. Unnecessary tasks disabled"

# 5. Clear Windows Update cache
Stop-Service wuauserv -Force -ErrorAction SilentlyContinue
Remove-Item "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
Start-Service wuauserv -ErrorAction SilentlyContinue
Write-Host "5. Windows Update cache cleared"

# 6. Optimize drive (TRIM for SSD)
Optimize-Volume -DriveLetter C -Revert -ErrorAction SilentlyContinue
Write-Host "6. Drive optimized"

Write-Host "`nOptimization complete!"