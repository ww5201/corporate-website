import os
import shutil

PROJECT_DIR = r"C:\Users\w\Desktop\ZhuoYiApp"
RES_DIR = os.path.join(PROJECT_DIR, "app", "src", "main", "res")

# 创建 mipmap 目录
sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

for folder, size in sizes.items():
    dir_path = os.path.join(RES_DIR, folder)
    os.makedirs(dir_path, exist_ok=True)

# 生成简单的纯色 PNG 图标 (用 Python 内置方式，不依赖 PIL)
# 最简单的 PNG: 1x1 红色像素，然后用 Android 的 adaptive icon
# 实际上更简单：直接用 XML vector drawable

# 创建 mipmap-anydpi-v26 目录
anydpi = os.path.join(RES_DIR, "mipmap-anydpi-v26")
os.makedirs(anydpi, exist_ok=True)

# 创建 values 目录
values_dir = os.path.join(RES_DIR, "values")
os.makedirs(values_dir, exist_ok=True)

# colors.xml
colors_xml = os.path.join(values_dir, "colors.xml")
with open(colors_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="ic_launcher_background">#FF1A73E8</color>
</resources>
""")
print("OK: colors.xml")

# 创建 drawable 目录
drawable_dir = os.path.join(RES_DIR, "drawable")
os.makedirs(drawable_dir, exist_ok=True)

# ic_launcher_background.xml
bg_xml = os.path.join(drawable_dir, "ic_launcher_background.xml")
with open(bg_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#FF1A73E8"/>
</shape>
""")
print("OK: ic_launcher_background.xml")

# ic_launcher_foreground.xml - 简单的 "卓" 字图标
fg_xml = os.path.join(drawable_dir, "ic_launcher_foreground.xml")
with open(fg_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <!-- 外圆背景 -->
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M54,54m-30,0a30,30 0,1 1,60 0a30,30 0,1 1,-60 0"/>
    <!-- 简化的 "Z" 字形代表"卓翌" -->
    <path
        android:fillColor="#FF1A73E8"
        android:strokeWidth="0"
        android:pathData="M38,40 L70,40 L38,68 L70,68"
        android:strokeColor="#FF1A73E8"
        android:strokeLineCap="round"
        android:strokeLineJoin="round"/>
</vector>
""")
print("OK: ic_launcher_foreground.xml")

# ic_launcher.xml (adaptive icon)
launcher_xml = os.path.join(anydpi, "ic_launcher.xml")
with open(launcher_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
""")
print("OK: ic_launcher.xml (adaptive icon)")

# ic_launcher_round.xml
round_xml = os.path.join(anydpi, "ic_launcher_round.xml")
with open(round_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
""")
print("OK: ic_launcher_round.xml")

# 同时创建简单的 PNG fallback 给低版本
# 生成 1x1 最小 PNG 的 base64 并按尺寸放大
# 用 Python 标准库生成最小 PNG
import struct
import zlib

def create_simple_png(width, height, r, g, b):
    """Create a minimal solid-color PNG"""
    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    
    # Create raw pixel data
    raw = b''
    for y in range(height):
        raw += b'\x00'  # filter byte
        for x in range(width):
            raw += bytes([r, g, b])
    
    idat = chunk(b'IDAT', zlib.compress(raw))
    iend = chunk(b'IEND', b'')
    
    return header + ihdr + idat + iend

# 为每个 mipmap 尺寸生成蓝色 PNG
for folder, size in sizes.items():
    png_data = create_simple_png(size, size, 0x1A, 0x73, 0xE8)  # #1A73E8
    png_path = os.path.join(RES_DIR, folder, "ic_launcher.png")
    with open(png_path, "wb") as f:
        f.write(png_data)
    
    round_path = os.path.join(RES_DIR, folder, "ic_launcher_round.png")
    with open(round_path, "wb") as f:
        f.write(png_data)

print("OK: PNG fallback icons for all mipmap sizes")

# AndroidManifest.xml 确保正确
manifest = os.path.join(PROJECT_DIR, "app", "src", "main", "AndroidManifest.xml")
with open(manifest, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="卓翌定制"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.ZhuoYiApp"
        android:usesCleartextTraffic="true">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait"
            android:configChanges="orientation|screenSize|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
""")
print("OK: AndroidManifest.xml")

# themes.xml
themes_dir = os.path.join(RES_DIR, "values")
themes_xml = os.path.join(themes_dir, "themes.xml")
with open(themes_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.ZhuoYiApp" parent="android:Theme.Material.Light.NoActionBar">
        <item name="android:statusBarColor">#FF1A73E8</item>
        <item name="android:navigationBarColor">#FF1A73E8</item>
    </style>
</resources>
""")
print("OK: themes.xml")

# 确保 MainActivity.java 存在
java_dir = os.path.join(PROJECT_DIR, "app", "src", "main", "java", "com", "zhuoyi", "custom")
os.makedirs(java_dir, exist_ok=True)

main_activity = os.path.join(java_dir, "MainActivity.java")
with open(main_activity, "w", encoding="utf-8") as f:
    f.write("""package com.zhuoyi.custom;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;

public class MainActivity extends Activity {
    private WebView webView;
    private ProgressBar progressBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // 全屏
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        
        setContentView(R.layout.activity_main);
        
        progressBar = findViewById(R.id.progressBar);
        webView = findViewById(R.id.webView);
        
        // WebView 设置
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);
        
        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                if (newProgress < 100) {
                    progressBar.setVisibility(View.VISIBLE);
                    progressBar.setProgress(newProgress);
                } else {
                    progressBar.setVisibility(View.GONE);
                }
            }
        });
        
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
    
    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.destroy();
        }
        super.onDestroy();
    }
}
""")
print("OK: MainActivity.java")

# layout/activity_main.xml
layout_dir = os.path.join(RES_DIR, "layout")
os.makedirs(layout_dir, exist_ok=True)

layout_xml = os.path.join(layout_dir, "activity_main.xml")
with open(layout_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ProgressBar
        android:id="@+id/progressBar"
        style="?android:attr/progressBarStyleHorizontal"
        android:layout_width="match_parent"
        android:layout_height="3dp"
        android:layout_alignParentTop="true"
        android:max="100"
        android:visibility="gone"/>

    <WebView
        android:id="@+id/webView"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:layout_below="@id/progressBar"/>

</RelativeLayout>
""")
print("OK: activity_main.xml")

print("\nDone! All resources created.")
