# Check .toclaw folder
Get-ChildItem "C:\Users\w\.toclaw" -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    [PSCustomObject]@{Name=$_.Name; SizeGB=[math]::Round($size/1GB,2)}
} | Sort-Object SizeGB -Descending