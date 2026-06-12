import os
import subprocess
import urllib.request
import zipfile
import shutil

# 路径配置
ANDROID_HOME = os.path.expanduser("~\\AppData\\Local\\Android\\Sdk")
CMD_TOOLS_DIR = os.path.join(ANDROID_HOME, "cmdline-tools", "latest")
PROJECT_DIR = os.path.expanduser("~\\Desktop\\ZhuoYiApp")

print("=== 步骤1: 创建项目目录 ===")
os.makedirs(PROJECT_DIR, exist_ok=True)

# 创建 Android 项目结构
dirs = [
    "app/src/main/java/com/zhuoyi/custom",
    "app/src/main/res/layout",
    "app/src/main/res/values",
    "app/src/main/res/mipmap-hdpi",
    "app/src/main/res/mipmap-xhdpi",
    "app/src/main/res/mipmap-xxhdpi",
]
for d in dirs:
    os.makedirs(os.path.join(PROJECT_DIR, d), exist_ok=True)

print("=== 步骤2: 生成 AndroidManifest.xml ===")
manifest = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.zhuoyi.custom">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="卓翌定制"
        android:supportsRtl="true"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
'''
with open(os.path.join(PROJECT_DIR, "app/src/main/AndroidManifest.xml"), "w", encoding="utf-8") as f:
    f.write(manifest)

print("=== 步骤3: 生成 MainActivity.java ===")
main_activity = '''package com.zhuoyi.custom;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);
        settings.setAllowFileAccess(true);
        settings.setMediaPlaybackRequiresUserGesture(false);

        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());
        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);

        webView.loadUrl("http://8.138.218.146");
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
'''
with open(os.path.join(PROJECT_DIR, "app/src/main/java/com/zhuoyi/custom/MainActivity.java"), "w", encoding="utf-8") as f:
    f.write(main_activity)

print("=== 步骤4: 生成布局文件 ===")
layout = '''<?xml version="1.0" encoding="utf-8"?>
<FrameLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
</FrameLayout>
'''
with open(os.path.join(PROJECT_DIR, "app/src/main/res/layout/activity_main.xml"), "w", encoding="utf-8") as f:
    f.write(layout)

print("=== 步骤5: 生成资源文件 ===")
styles = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="android:Theme.DeviceDefault.Light.NoActionBar">
        <item name="android:statusBarColor">#FF8B7355</item>
    </style>
</resources>
'''
with open(os.path.join(PROJECT_DIR, "app/src/main/res/values/styles.xml"), "w", encoding="utf-8") as f:
    f.write(styles)

strings = '''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">卓翌定制</string>
</resources>
'''
with open(os.path.join(PROJECT_DIR, "app/src/main/res/values/strings.xml"), "w", encoding="utf-8") as f:
    f.write(strings)

print("=== 步骤6: 生成 build.gradle 文件 ===")
# 根 build.gradle
root_gradle = '''buildscript {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/google' }
        maven { url 'https://maven.aliyun.com/repository/central' }
        maven { url 'https://maven.aliyun.com/repository/public' }
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.4.2'
    }
}

allprojects {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/google' }
        maven { url 'https://maven.aliyun.com/repository/central' }
        maven { url 'https://maven.aliyun.com/repository/public' }
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
'''
with open(os.path.join(PROJECT_DIR, "build.gradle"), "w", encoding="utf-8") as f:
    f.write(root_gradle)

# app/build.gradle
app_gradle = '''apply plugin: 'com.android.application'

android {
    compileSdkVersion 36
    
    defaultConfig {
        applicationId "com.zhuoyi.custom"
        minSdkVersion 24
        targetSdkVersion 36
        versionCode 1
        versionName "1.0"
    }
    
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
}
'''
with open(os.path.join(PROJECT_DIR, "app/build.gradle"), "w", encoding="utf-8") as f:
    f.write(app_gradle)

# settings.gradle
settings = "include ':app'\n"
with open(os.path.join(PROJECT_DIR, "settings.gradle"), "w", encoding="utf-8") as f:
    f.write(settings)

# gradle.properties
props = '''android.useAndroidX=false
org.gradle.jvmargs=-Xmx1536m
'''
with open(os.path.join(PROJECT_DIR, "gradle.properties"), "w", encoding="utf-8") as f:
    f.write(props)

# gradle wrapper properties
wrapper_dir = os.path.join(PROJECT_DIR, "gradle", "wrapper")
os.makedirs(wrapper_dir, exist_ok=True)
wrapper_props = '''distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://mirrors.cloud.tencent.com/gradle/gradle-7.5.1-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
'''
with open(os.path.join(wrapper_dir, "gradle-wrapper.properties"), "w", encoding="utf-8") as f:
    f.write(wrapper_props)

# proguard-rules.pro
with open(os.path.join(PROJECT_DIR, "app/proguard-rules.pro"), "w") as f:
    f.write("# Proguard rules\n")

print("=== 项目已生成 ===")
print(f"项目目录: {PROJECT_DIR}")
print("文件列表:")
for root, dirs_list, files in os.walk(PROJECT_DIR):
    for file in files:
        rel = os.path.relpath(os.path.join(root, file), PROJECT_DIR)
        print(f"  {rel}")

print("\n=== 下一步 ===")
print("1. 打开 Android Studio")
print("2. 选择 'Open an Existing Project'")
print(f"3. 选择目录: {PROJECT_DIR}")
print("4. 等待 Gradle 同步完成")
print("5. 点击 Build > Build Bundle(s) / APK(s) > Build APK(s)")
