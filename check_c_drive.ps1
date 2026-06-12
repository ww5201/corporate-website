$folders = @("C:\Users", "C:\Windows", "C:\Program Files", "C:\Program Files (x86)", "C:\ProgramData", "C:\temp")
foreach ($f in $folders) {
    $size = (Get-ChildItem -Path $f -Recurse -Force -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    Write-Host "$f : $([math]::Round($size/1GB,2)) GB"
}