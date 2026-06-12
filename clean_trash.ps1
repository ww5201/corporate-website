# Clean up .toclaw/.trash
$trashPath = "C:\Users\w\.toclaw\.trash"
Get-ChildItem $trashPath -Recurse -Force -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem $trashPath -Recurse -Force -Directory -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
Write-Host "Cleaned"