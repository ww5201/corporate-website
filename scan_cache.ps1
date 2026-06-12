Write-Host "=== 酷狗音乐目录结构 ==="
Get-ChildItem -Path 'D:\酷狗音乐' -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
    $size = (Get-ChildItem -Path $_.FullName -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{Name=$_.Name; SizeMB=[math]::Round($size/1MB,2)}
} | Sort-Object SizeMB -Descending | Format-Table -AutoSize
Write-Host ""
Write-Host "=== 腾讯应用宝目录结构 ==="
Get-ChildItem -Path 'D:\腾讯应用宝' -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
    $size = (Get-ChildItem -Path $_.FullName -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{Name=$_.Name; SizeMB=[math]::Round($size/1MB,2)}
} | Sort-Object SizeMB -Descending | Format-Table -AutoSize