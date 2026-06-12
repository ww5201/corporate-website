package com.zhuoyi.admin;

import android.app.Activity;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import android.widget.Toast;
import androidx.appcompat.app.AlertDialog;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

public class AdminMainActivity extends Activity {

    private WebView webView;
    private ProgressBar progressBar;
    private SwipeRefreshLayout swipeRefreshLayout;
    private static final String ADMIN_URL = "http://8.138.218.146/admin";
    private ValueCallback<Uri[]> uploadMessage;
    private static final int FILE_CHOOSER_RESULT_CODE = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );

        setContentView(R.layout.activity_admin_main);

        progressBar = findViewById(R.id.progressBar);
        swipeRefreshLayout = findViewById(R.id.swipeRefresh);
        webView = findViewById(R.id.webView);

        setupSwipeRefresh();
        setupWebView();
        webView.loadUrl(ADMIN_URL);
    }

    private void setupSwipeRefresh() {
        swipeRefreshLayout.setColorSchemeResources(
            android.R.color.holo_blue_bright,
            android.R.color.holo_green_light,
            android.R.color.holo_orange_light,
            android.R.color.holo_red_light
        );
        swipeRefreshLayout.setOnRefreshListener(() -> {
            webView.reload();
            new android.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> {
                swipeRefreshLayout.setRefreshing(false);
            }, 1500);
        });
    }

    private void setupWebView() {
        WebSettings settings = webView.getSettings();

        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);
        settings.setDatabaseEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setSupportZoom(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        settings.setUserAgentString(settings.getUserAgentString() + " ZhuoyiAdmin/1.0");

        // 启用调试（管理后台需要）
        WebView.setWebContentsDebuggingEnabled(true);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                if (url.startsWith("tel:") || url.startsWith("mailto:") ||
                    url.startsWith("weixin://") || url.startsWith("alipays://")) {
                    try {
                        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                        startActivity(intent);
                    } catch (Exception e) {
                        Toast.makeText(AdminMainActivity.this, "未安装对应应用", Toast.LENGTH_SHORT).show();
                    }
                    return true;
                }
                view.loadUrl(url);
                return true;
            }

            @Override
            public void onReceivedSslError(WebView view, android.webkit.SslErrorHandler handler,
                                           android.net.http.SslError error) {
                handler.proceed();
            }

            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                showErrorDialog();
            }
        });

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

            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback,
                                             WebChromeClient.FileChooserParams fileChooserParams) {
                if (uploadMessage != null) {
                    uploadMessage.onReceiveValue(null);
                }
                uploadMessage = filePathCallback;
                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("*/*");
                startActivityForResult(Intent.createChooser(intent, "选择文件"), FILE_CHOOSER_RESULT_CODE);
                return true;
            }
        });
    }

    private void showErrorDialog() {
        new AlertDialog.Builder(this)
            .setTitle("连接失败")
            .setMessage("无法连接到服务器，请检查网络")
            .setPositiveButton("重试", (dialog, which) -> webView.reload())
            .setNegativeButton("退出", (dialog, which) -> finish())
            .setCancelable(false)
            .show();
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            if (webView.canGoBack()) {
                webView.goBack();
                return true;
            }
            showExitDialog();
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }

    private void showExitDialog() {
        new AlertDialog.Builder(this)
            .setTitle("确认退出")
            .setMessage("确定要退出管理后台吗？")
            .setPositiveButton("退出", (dialog, which) -> finish())
            .setNegativeButton("取消", null)
            .show();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == FILE_CHOOSER_RESULT_CODE && uploadMessage != null) {
            Uri[] results = null;
            if (resultCode == RESULT_OK && data != null) {
                String dataString = data.getDataString();
                if (dataString != null) {
                    results = new Uri[]{Uri.parse(dataString)};
                }
            }
            uploadMessage.onReceiveValue(results);
            uploadMessage = null;
        }
    }

    @Override
    protected void onResume() { super.onResume(); webView.onResume(); }

    @Override
    protected void onPause() { super.onPause(); webView.onPause(); }

    @Override
    protected void onDestroy() {
        if (webView != null) webView.destroy();
        super.onDestroy();
    }
}
