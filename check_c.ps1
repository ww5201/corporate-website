$drive = Get-PSDrive C
Write-Host "C盘已用: $([math]::Round($drive.Used/1GB,2)) GB"
Write-Host "C盘剩余: $([math]::Round($drive.Free/1GB,2)) GB"