# Check user profile folders
Get-ChildItem C:\Users\w -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    [PSCustomObject]@{Name=$_.Name; SizeGB=[math]::Round($size/1GB,2)}
} | Sort-Object SizeGB -Descending | Select-Object -First 15