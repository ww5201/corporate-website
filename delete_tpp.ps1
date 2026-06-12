# Get items in tpp and delete in batches
$items = Get-ChildItem -Path 'D:\酷狗音乐\Temp\tpp' -Force -ErrorAction SilentlyContinue
$count = 0
foreach ($item in $items) {
    Remove-Item -Path $item.FullName -Recurse -Force -ErrorAction SilentlyContinue
    $count++
    if ($count % 10 -eq 0) { Write-Host "Deleted $count items..." }
}
Write-Host "Deleted $count total items from tpp"