# Use short path to avoid encoding issues
$path = 'D:\酷狗音乐\Temp\tpp'
cmd /c "rd /s /q `"$path`"" 2>&1 | Out-Null
if (Test-Path $path) {
    Write-Host "Failed"
} else {
    Write-Host "Success"
}