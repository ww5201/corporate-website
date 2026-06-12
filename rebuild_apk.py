import subprocess
import os

# 修改 MainActivity.java - 强制清除缓存
java_code = '''package com.zhuoyi.custom;

import android.app.Activity;
import android.os.Bundle;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
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
        settings.setCacheMode(WebSettings.LOAD_NO_CACHE);
        settings.setDatabaseEnabled(true);
        
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                if (url.startsWith("http://8.138.218.146") || url.startsWith("https://8.138.218.146")) {
                    return false;
                }
                return true;
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                if (newProgress < 100) {
                    progressBar.setVisibility(android.view.View.VISIBLE);
                    progressBar.setProgress(newProgress);
                } else {
                    progressBar.setVisibility(android.view.View.GONE);
                }
            }
        });
        
        webView.clearCache(true);
        webView.clearHistory();
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
'''

# 写入 Java 文件
java_path = r'C:\Users\w\Desktop\ZhuoYiApp\app\src\main\java\com\zhuoyi\custom\MainActivity.java'
with open(java_path, 'w', encoding='utf-8') as f:
    f.write(java_code)

print("Java file updated")

# 编译 APK
gradle_bat = r'C:\Users\w\Desktop\ZhuoYiApp\gradlew.bat'
result = subprocess.run(
    [gradle_bat, 'assembleDebug'],
    cwd=r'C:\Users\w\Desktop\ZhuoYiApp',
    capture_output=True, text=True, timeout=300
)
print(f"Build exit code: {result.returncode}")
if 'BUILD SUCCESSFUL' in result.stdout:
    print("BUILD SUCCESSFUL!")
elif 'BUILD FAILED' in result.stdout:
    # 输出最后20行
    lines = result.stdout.split('\n')
    for line in lines[-20:]:
        print(line)
