# Delete directly without moving to trash
$tpfs = 'D:\酷狗音乐\Temp\tpp\.tpfs'
Get-ChildItem -Path $tpfs -Recurse -Force | Remove-Item -Recurse -Force
Remove-Item -Path $tpfs -Recurse -Force
Write-Host "Deleted"