@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

echo ========================================
echo   卓翌定制 - Android 构建脚本
echo ========================================

:: === 环境配置 ===
set "JAVA_HOME=C:\Users\w\.toclaw\tools\jdk17\jdk-17.0.12+7"
set "ANDROID_HOME=D:\android-sdk"
set "PATH=%JAVA_HOME%\bin;%ANDROID_HOME%\cmdline-tools\latest\bin;%ANDROID_HOME%\platform-tools;%PATH%"

echo [1/5] Java 环境...
"%JAVA_HOME%\bin\java.exe" -version
if %ERRORLEVEL% neq 0 (
    echo [错误] Java 未就绪
    exit /b 1
)

echo.
echo [2/5] 安装 Android SDK 组件...
echo | sdkmanager --licenses >nul 2>&1
sdkmanager "platforms;android-34" "build-tools;34.0.0" "platform-tools" --no_https 2>&1
if %ERRORLEVEL% neq 0 (
    echo [警告] SDK 组件安装可能失败，重试中...
    sdkmanager "platforms;android-34" "build-tools;34.0.0" "platform-tools"
)

echo.
echo [3/5] 编译 SDK 模块 (AAR) ...
call gradlew :sdk:assembleRelease --no-daemon -Porg.gradle.jvmargs=-Xmx2048m 2>&1
if %ERRORLEVEL% neq 0 (
    echo [错误] SDK 编译失败
    exit /b 1
)
echo [✓] SDK AAR 编译成功

echo.
echo [4/5] 编译用户端 APK (前端) ...
call gradlew :app:assembleRelease --no-daemon -Porg.gradle.jvmargs=-Xmx2048m 2>&1
if %ERRORLEVEL% neq 0 (
    echo [错误] 前端 APK 编译失败
    exit /b 1
)
echo [✓] 前端 APK 编译成功

echo.
echo [5/5] 编译管理后台 APK (后端) ...
call gradlew :admin:assembleRelease --no-daemon -Porg.gradle.jvmargs=-Xmx2048m 2>&1
if %ERRORLEVEL% neq 0 (
    echo [错误] 后端 APK 编译失败
    exit /b 1
)
echo [✓] 后端 APK 编译成功

echo.
echo ========================================
echo   ✅ 全部构建完成！
echo ========================================
echo.
echo 产物位置：
echo   SDK  AAR: android-app\sdk\build\outputs\aar\
echo   前端 APK: android-app\app\build\outputs\apk\release\
echo   后端 APK: android-app\admin\build\outputs\apk\release\
echo.

dir /s /b "D:\tokai\android-app\sdk\build\outputs\aar\*.aar" 2>nul
dir /s /b "D:\tokai\android-app\app\build\outputs\apk\release\*.apk" 2>nul
dir /s /b "D:\tokai\android-app\admin\build\outputs\apk\release\*.apk" 2>nul

endlocal
