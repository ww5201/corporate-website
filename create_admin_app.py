import os
import shutil

# 复制现有项目
SRC = r"C:\Users\w\Desktop\ZhuoYiApp"
DST = r"C:\Users\w\Desktop\ZhuoYiAdmin"

if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns(".gradle", "build", "app/build", "*.iml", ".idea"))
print(f"Copied project to {DST}")

# 清理缓存
for d in ["build", ".gradle", "app/build"]:
    path = os.path.join(DST, d)
    if os.path.exists(path):
        shutil.rmtree(path)

# 1. AndroidManifest.xml - 改 app 名称
manifest = os.path.join(DST, "app", "src", "main", "AndroidManifest.xml")
with open(manifest, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="卓翌管理"
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
print("OK: AndroidManifest.xml -> label=卓翌管理")

# 2. app/build.gradle - 改包名
app_gradle = os.path.join(DST, "app", "build.gradle")
with open(app_gradle, "w", encoding="utf-8") as f:
    f.write("""plugins {
    id 'com.android.application'
}

android {
    namespace 'com.zhuoyi.admin'
    compileSdk 36
    buildToolsVersion "36.0.0"
    
    defaultConfig {
        applicationId "com.zhuoyi.admin"
        minSdk 24
        targetSdk 36
        versionCode 1
        versionName "1.0"
    }
    
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
}
""")
print("OK: app/build.gradle -> com.zhuoyi.admin")

# 3. MainActivity.java - 加载 admin.html
java_dir = os.path.join(DST, "app", "src", "main", "java", "com", "zhuoyi", "admin")
os.makedirs(java_dir, exist_ok=True)

main_activity = os.path.join(java_dir, "MainActivity.java")
with open(main_activity, "w", encoding="utf-8") as f:
    f.write("""package com.zhuoyi.admin;

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
        
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        
        setContentView(R.layout.activity_main);
        
        progressBar = findViewById(R.id.progressBar);
        webView = findViewById(R.id.webView);
        
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
        
        // 加载管理后台页面
        webView.loadUrl("http://8.138.218.146/admin.html");
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
print("OK: MainActivity.java -> loadUrl admin.html")

# 4. 图标颜色改为橙色（区分前台的蓝色）
import struct
import zlib

def create_simple_png(width, height, r, g, b):
    def chunk(chunk_type, data):
        c = chunk_type + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    header = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    raw = b''
    for y in range(height):
        raw += b'\x00'
        for x in range(width):
            raw += bytes([r, g, b])
    idat = chunk(b'IDAT', zlib.compress(raw))
    iend = chunk(b'IEND', b'')
    return header + ihdr + idat + iend

RES_DIR = os.path.join(DST, "app", "src", "main", "res")

# 橙色背景
bg_xml = os.path.join(RES_DIR, "drawable", "ic_launcher_background.xml")
with open(bg_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#FFE65100"/>
</shape>
""")
print("OK: icon background -> orange #E65100")

# 前景 - 齿轮图标代表管理
fg_xml = os.path.join(RES_DIR, "drawable", "ic_launcher_foreground.xml")
with open(fg_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M54,54m-30,0a30,30 0,1 1,60 0a30,30 0,1 1,-60 0"/>
    <path
        android:fillColor="#FFE65100"
        android:pathData="M54,36 C63.9,36 72,44.1 72,54 C72,63.9 63.9,72 54,72 C44.1,72 36,63.9 36,54 C36,44.1 44.1,36 54,36z M54,42 C47.4,42 42,47.4 42,54 C42,60.6 47.4,66 54,66 C60.6,66 66,60.6 66,54 C66,47.4 60.6,42 54,42z"/>
    <path
        android:fillColor="#FFE65100"
        android:pathData="M54,48 L54,60 L62,54z"/>
</vector>
""")
print("OK: icon foreground -> gear/admin")

# 橙色 PNG fallback
sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}
for folder, size in sizes.items():
    png_data = create_simple_png(size, size, 0xE6, 0x51, 0x00)  # orange
    png_path = os.path.join(RES_DIR, folder, "ic_launcher.png")
    with open(png_path, "wb") as f:
        f.write(png_data)
    round_path = os.path.join(RES_DIR, folder, "ic_launcher_round.png")
    with open(round_path, "wb") as f:
        f.write(png_data)

print("OK: orange PNG icons for all mipmap sizes")

# 5. colors.xml - 橙色主题
colors_xml = os.path.join(RES_DIR, "values", "colors.xml")
with open(colors_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#FFE65100</color>
</resources>
""")
print("OK: colors.xml -> orange")

# 6. themes.xml - 橙色状态栏
themes_xml = os.path.join(RES_DIR, "values", "themes.xml")
with open(themes_xml, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.ZhuoYiApp" parent="android:Theme.Material.Light.NoActionBar">
        <item name="android:statusBarColor">#FFE65100</item>
        <item name="android:navigationBarColor">#FFE65100</item>
    </style>
</resources>
""")
print("OK: themes.xml -> orange status bar")

# 删除不需要的 Java 源文件（前台项目的）
old_java = os.path.join(DST, "app", "src", "main", "java", "com", "zhuoyi", "custom")
if os.path.exists(old_java):
    shutil.rmtree(old_java)
    print("OK: removed old com.zhuoyi.custom package")

print("\nDone! Admin app project created at:")
print(f"  {DST}")
print("  Package: com.zhuoyi.admin")
print("  App name: 卓翌管理")
print("  URL: http://8.138.218.146/admin.html")
print("  Theme: Orange")
