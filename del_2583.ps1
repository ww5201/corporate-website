Remove-Item -Path 'D:\腾讯应用宝\Androws\Image\5.10.6000.2583\system.vhd' -Force -ErrorAction SilentlyContinue
Remove-Item -Path 'D:\腾讯应用宝\Androws\Image\5.10.6000.2583\system.vhd.patch' -Force -ErrorAction SilentlyContinue
Remove-Item -Path 'D:\腾讯应用宝\Androws\Image\5.10.6000.2583' -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "2583 deleted"