Write-Host "=== C盘空间紧急清理 ==="

# 1. 清理Windows临时文件
$winTemp = 'C:\Windows\Temp'
$count = (Get-ChildItem $winTemp -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue -PassThru).Count
Write-Host "Windows Temp清理完成 ($count 项)"

# 2. 清理用户临时文件
$userTemp = $env:TEMP
$count = (Get-ChildItem $userTemp -Recurse -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue -PassThru).Count
Write-Host "用户 Temp清理完成 ($count 项)"

# 3. 清理Prefetch
$prefetch = 'C:\Windows\Prefetch'
$count = (Get-ChildItem $prefetch -File -Force -ErrorAction SilentlyContinue | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } | Remove-Item -Force -ErrorAction SilentlyContinue -PassThru).Count
Write-Host "Prefetch清理完成 ($count 项)"

# 4. 清理Recent
$recent = 'C:\Users\*\AppData\Roaming\Microsoft\Windows\Recent'
$count = (Get-ChildItem $recent -File -Force -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue -PassThru).Count
Write-Host "Recent清理完成 ($count 项)"

# 显示清理后空间
$free = (Get-PSDrive C).Free
Write-Host "C盘剩余空间: $([math]::Round($free/1GB,2)) GB"