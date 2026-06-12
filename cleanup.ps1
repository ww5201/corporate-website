# Check recycle bin size
$shell = New-Object -ComObject Shell.Application
$recycleBin = $shell.NameSpace(0xA)
$totalSize = 0
$count = 0
$recycleBin.Items() | ForEach-Object { $totalSize += $_.Size; $count++ }
Write-Host "回收站项目数: $count"
Write-Host "回收站大小: $([math]::Round($totalSize/1GB,2)) GB"
