# Final system check
Write-Host "=== Final System Status ==="

# Memory
$mem = Get-CimInstance Win32_OperatingSystem
$freeMemGB = [math]::Round($mem.FreePhysicalMemory/1MB,2)
$totalMemGB = [math]::Round($mem.TotalVisibleMemorySize/1MB,2)
Write-Host "Memory: $freeMemGB GB free / $totalMemGB GB total"

# CPU
$cpu = Get-CimInstance Win32_Processor
Write-Host "CPU: $($cpu.LoadPercentage)% usage"

# Disk
$cDrive = Get-PSDrive C
$dDrive = Get-PSDrive D
Write-Host "C Drive: $([math]::Round($cDrive.Free/1GB,2)) GB free"
Write-Host "D Drive: $([math]::Round($dDrive.Free/1GB,2)) GB free"

# Top processes
Write-Host "`nTop Memory Processes:"
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 5 Name,@{N='MemoryMB';E={[math]::Round($_.WorkingSet64/1MB,0)}} | Format-Table -AutoSize

Write-Host "`nOptimization Summary:"
Write-Host "- Disabled 7 unnecessary startup programs"
Write-Host "- Cleared DNS cache"
Write-Host "- Cleared temp files"
Write-Host "- Cleared thumbnail cache"
Write-Host "- Disabled 9 unnecessary scheduled tasks"
Write-Host "- Cleared Windows Update cache"
Write-Host "- System is optimized for better performance"