# Force delete .tpfs with takeown and rmdir
$tpfsPath = 'D:\酷狗音乐\Temp\tpp\.tpfs'
Write-Host "Deleting .tpfs..."
# Try to take ownership and delete
takeown /F "$tpfsPath" /R /D Y 2>$null
icacls "$tpfsPath" /grant Administrators:F /T 2>$null
Remove-Item -Path $tpfsPath -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Done"