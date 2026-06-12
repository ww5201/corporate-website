# Check Windows Update status
$updateSession = New-Object -ComObject Microsoft.Update.Session
$updateSearcher = $updateSession.CreateUpdateSearcher()
$pendingUpdates = $updateSearcher.Search("IsInstalled=0")
Write-Host "待安装更新: $($pendingUpdates.Updates.Count) 个"

# Check disk health
$disk = Get-PhysicalDisk | Select-Object -First 1
Write-Host "磁盘健康: $($disk.HealthStatus)"
Write-Host "磁盘类型: $($disk.MediaType)"

# Check for Windows Update cleanup
$softwareDist = (Get-ChildItem "C:\Windows\SoftwareDistribution" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
Write-Host "Windows更新缓存: $([math]::Round($softwareDist/1GB,2)) GB"

# Check temp files
$tempSize = (Get-ChildItem "$env:TEMP" -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
Write-Host "临时文件: $([math]::Round($tempSize/1GB,2)) GB"