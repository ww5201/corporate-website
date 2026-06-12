@echo off
chcp 65001 >nul 2>&1
title 卓翌定制网站恢复工具
echo.
echo   ============================================
echo     卓翌定制网站 - 一键恢复工具
echo   ============================================
echo.
echo   正在尝试连接服务器...
echo.

set SERVER=8.138.218.146
set USER=root
set PASS=ww0987654.
set LOCAL_FILE=D:\tokai\index-fixed2.html
set REMOTE_FILE=/var/www/frontend/index.html

:: Check local file exists
if not exist "%LOCAL_FILE%" (
    echo   [错误] 找不到修复文件: %LOCAL_FILE%
    echo   请确保 D:\tokai\index-fixed2.html 存在
    pause
    exit /b 1
)

:: Try SSH with plink (PuTTY) if available
where plink >nul 2>&1
if %errorlevel% equ 0 (
    echo   [方式1] 尝试 PuTTY plink...
    plink -ssh %USER%@%SERVER% -pw "%PASS%" -batch "echo SSH_OK" >nul 2>&1
    if %errorlevel% equ 0 goto :UPLOAD_PLINK
)

:: Try SSH with ssh command
where ssh >nul 2>&1
if %errorlevel% equ 0 (
    echo   [方式2] 尝试 ssh...
    ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no %USER%@%SERVER% "echo SSH_OK" >nul 2>&1
    if %errorlevel% equ 0 goto :UPLOAD_SSH
)

:: Try Python paramiko
python -c "import paramiko" >nul 2>&1
if %errorlevel% equ 0 (
    echo   [方式3] 尝试 Python paramiko...
    python -c "
import paramiko, sys
try:
    c=paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect('%SERVER%',username='%USER',password='%PASS%',timeout=15)
    sftp=c.open_sftp()
    f=open(r'%LOCAL_FILE%','r',encoding='utf-8')
    html=f.read(); f.close()
    f=sftp.open('%REMOTE_FILE%','w')
    f.write(html); f.close()
    sftp.close()
    c.exec_command('nginx -s reload')
    print('UPLOAD_OK')
    c.close()
except Exception as e:
    print('FAIL:'+str(e))
    sys.exit(1)
" 2>&1 | findstr "UPLOAD_OK FAIL"
    if %errorlevel% equ 0 (
        for %%a in ('python -c ...') do set RESULT=%%~a
        echo %RESULT% | findstr "UPLOAD_OK" >nul 2>&1
        if !errorlevel! equ 0 goto :SUCCESS
    )
)

echo.
echo   [!] 所有 SSH 方式均失败（端口 22 被封锁）
echo.
echo   请使用阿里云控制台手动恢复：
echo.
echo   步骤：
echo   1. 打开 https://ecs.console.aliyun.com/
echo   2. 找到服务器 8.138.218.146，点【远程连接】→【Workbench】
echo   3. 登录 root / ww0987654.
echo   4. 粘贴下面命令并回车：
echo.
echo   ================================================================
echo   cd /var/www/frontend ^&^& wget -O index.html "http://YOUR_PC_IP/index-fixed2.html"
echo   ================================================================
echo.
echo   或者直接在 Workbench 中运行这个 Python one-liner 来从 base64 恢复：
echo.
pause
exit /b 1

:UPLOAD_SSH
echo   ssh 连接成功！正在上传...
scp -o ConnectTimeout=15 -o StrictHostKeyChecking=no "%LOCAL_FILE%" %USER%@%SERVER%:"%REMOTE_FILE%"
if %errorlevel% neq 0 (
    echo   [错误] 上传失败
    pause
    exit /b 1
)
ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no %USER%@%SERVER% "nginx -s reload && echo RELOAD_OK"
goto :SUCCESS

:UPLOAD_PLINK
echo   plink 连接成功！正在上传...
pscp -o ConnectTimeout=15 -o StrictHostKeyChecking=no "%LOCAL_FILE%" %USER%@%SERVER%:"%REMOTE_FILE%"
if %errorlevel% neq 0 (
    echo   [错误] 上传失败
    pause
    exit /b 1
)
plink -ssh %USER%@%SERVER% -pw "%PASS%" -batch "nginx -s reload && echo RELOAD_OK"
goto :SUCCESS

:SUCCESS
echo.
echo   ============================================
echo     恢复成功！请 Ctrl+F5 刷新浏览器测试
echo   ============================================
echo.
pause
