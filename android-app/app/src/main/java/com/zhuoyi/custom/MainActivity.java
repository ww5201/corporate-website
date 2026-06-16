package com.zhuoyi.custom;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.ConsoleMessage;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import android.widget.Toast;

import android.app.AlertDialog;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

public class MainActivity extends Activity {

    private static final String TAG = "ZhuoyiApp";
    private WebView webView;
    private ProgressBar progressBar;
    private SwipeRefreshLayout swipeRefreshLayout;
    private static final String HOME_URL = "file:///android_asset/index.html";
    private ValueCallback<Uri[]> uploadMessage;
    private final static int FILE_CHOOSER_RESULT_CODE = 1;
    private Handler mainHandler;
    private Runnable hideProgressRunnable;
    private boolean pageLoaded = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.activity_main);

        mainHandler = new Handler(Looper.getMainLooper());

        progressBar = findViewById(R.id.progressBar);
        swipeRefreshLayout = findViewById(R.id.swipeRefresh);
        webView = findViewById(R.id.webView);

        // Set background matching page color to prevent white flash
        webView.setBackgroundColor(Color.parseColor("#f5f5f5"));

        setupSwipeRefresh();
        setupWebView();

        try {
            WeChatAuthHelper.init(this);
        } catch (Throwable t) {
            Log.w(TAG, "WeChat init skipped", t);
        }

        webView.addJavascriptInterface(new Object() {
            @android.webkit.JavascriptInterface
            public boolean isInstalled() {
                WeChatAuthHelper.init(MainActivity.this);
                return WeChatAuthHelper.isWeChatInstalled();
            }
            @android.webkit.JavascriptInterface
            public boolean login() {
                Log.i(TAG, "login() called");
                WeChatAuthHelper.init(MainActivity.this);
                boolean ok = WeChatAuthHelper.login("snsapi_userinfo", "zhuoyi_" + System.currentTimeMillis());
                Log.i(TAG, "login() result=" + ok);
                return ok;
            }
        }, "AndroidWeChat");

        showProgress();

        // 关键修复：在加载首页之前，先检查是否有微信回调的 code
        String wxCode = getIntent().getStringExtra("wx_code");
        // 立即清除 Intent Extra 和 SharedPreferences，防止 onResume 重复处理
        getIntent().removeExtra("wx_code");
        getSharedPreferences("wx_login", MODE_PRIVATE).edit()
            .remove("wx_code").remove("wx_time").remove("wx_errcode").apply();

        if (wxCode != null && !wxCode.isEmpty()) {
            Log.i(TAG, "onCreate: got wx_code from intent=" + wxCode);
            webView.loadUrl("file:///android_asset/login.html?wxcode=" + wxCode);
        } else {
            webView.loadUrl(HOME_URL);
        }

        handleDeepLink(getIntent()); // Handle deep link on cold start
    }

    private void showProgress() {
        progressBar.setVisibility(View.VISIBLE);
        progressBar.setProgress(0);
        pageLoaded = false;

        // Auto-hide progress after 10 seconds max
        if (hideProgressRunnable != null) mainHandler.removeCallbacks(hideProgressRunnable);
        hideProgressRunnable = () -> {
            if (!pageLoaded) {
                Log.w(TAG, "Loading timeout, hiding progress");
                hideProgress();
            }
        };
        mainHandler.postDelayed(hideProgressRunnable, 10000);
    }

    private void hideProgress() {
        pageLoaded = true;
        progressBar.setVisibility(View.GONE);
        if (hideProgressRunnable != null) mainHandler.removeCallbacks(hideProgressRunnable);
    }

    private void setupSwipeRefresh() {
        swipeRefreshLayout.setColorSchemeResources(
            android.R.color.holo_blue_bright,
            android.R.color.holo_green_light,
            android.R.color.holo_orange_light,
            android.R.color.holo_red_light
        );
        swipeRefreshLayout.setOnRefreshListener(() -> {
            showProgress();
            webView.reload();
            mainHandler.postDelayed(() -> swipeRefreshLayout.setRefreshing(false), 2000);
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
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setAllowFileAccessFromFileURLs(true);
        settings.setBlockNetworkImage(false);
        settings.setLoadsImagesAutomatically(true);
        settings.setJavaScriptCanOpenWindowsAutomatically(true);
        settings.setUserAgentString(settings.getUserAgentString() + " ZhuoyiCustom/1.0");

        webView.setLayerType(View.LAYER_TYPE_HARDWARE, null); // enable GPU acceleration
        webView.setOverScrollMode(View.OVER_SCROLL_NEVER); // prevent overscroll artifacts

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                Log.d(TAG, "shouldOverrideUrlLoading: " + url);

                // Allow same-origin and file:// navigation
                if (url.startsWith("file:///android_asset/")) {
                    return false;
                }

                // External schemes - open in system browser
                if (url.startsWith("tel:") || url.startsWith("mailto:")) {
                    try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); } catch (Exception e) {}
                    return true;
                }

                if (url.startsWith("weixin://") || url.startsWith("alipays://")) {
                    try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); } catch (Exception e) {
                        Toast.makeText(MainActivity.this, "未安装对应应用", Toast.LENGTH_SHORT).show();
                    }
                    return true;
                }

                // Allow WeChat OAuth URLs in WebView
                if (url.contains("open.weixin.qq.com") || url.contains("api.weixin.qq.com")) {
                    return false;
                }

                // Allow server API URLs in WebView (for wechat-callback etc)
                if (url.contains("8.138.218.146") || url.contains("wgh2026.top")) {
                    return false;
                }

                // Other HTTP/HTTPS links - open in system browser
                if (url.startsWith("http://") || url.startsWith("https://")) {
                    try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); } catch (Exception e) {}
                    return true;
                }

                return false;
            }

            @Override
            public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
                super.onPageStarted(view, url, favicon);
                Log.d(TAG, "onPageStarted: " + url);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                Log.d(TAG, "onPageFinished: " + url);
                hideProgress();
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, WebResourceError error) {
                super.onReceivedError(view, request, error);
                String url = request.getUrl().toString();
                Log.w(TAG, "onReceivedError: " + url);

                // Only show error for main page load failure
                if (request.isForMainFrame()) {
                    hideProgress();
                    runOnUiThread(() -> {
                        Toast.makeText(MainActivity.this, "页面加载失败，请下拉刷新重试", Toast.LENGTH_LONG).show();
                    });
                }
            }

            @Override
            public void onReceivedSslError(WebView view, android.webkit.SslErrorHandler handler,
                                           android.net.http.SslError error) {
                handler.proceed();
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                if (newProgress < 100) {
                    progressBar.setVisibility(View.VISIBLE);
                    progressBar.setProgress(newProgress);
                } else {
                    hideProgress();
                }
            }

            @Override
            public boolean onConsoleMessage(ConsoleMessage consoleMessage) {
                Log.d(TAG, "JS: " + consoleMessage.message() + " [" + consoleMessage.lineNumber() + "]");
                return true;
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

        webView.setDownloadListener((url, userAgent, contentDisposition, mimeType, contentLength) -> {
            try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); } catch (Exception e) {}
        });
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            return handleBack();
        }
        return super.onKeyDown(keyCode, event);
    }

    @Override
    public void onBackPressed() {
        handleBack();
    }

    private boolean handleBack() {
        // If we can go back in WebView history, do it
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
            return true;
        }

        // No more history - show exit dialog
        showExitDialog();
        return true;
    }

    private void showExitDialog() {
        new AlertDialog.Builder(this)
            .setTitle("确认退出")
            .setMessage("确定要退出卓翌定制吗？")
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
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        // 优先处理微信回调 code
        String wxCode = intent.getStringExtra("wx_code");
        // 立即清除 Intent Extra 和 SharedPreferences，防止 onResume 重复处理
        intent.removeExtra("wx_code");
        getSharedPreferences("wx_login", MODE_PRIVATE).edit()
            .remove("wx_code").remove("wx_time").remove("wx_errcode").apply();

        if (wxCode != null && !wxCode.isEmpty()) {
            Log.i(TAG, "onNewIntent: got wx_code=" + wxCode);
            String url = "file:///android_asset/login.html?wxcode=" + wxCode;
            if (webView != null) webView.loadUrl(url);
            return;
        }
        // 处理微信错误
        int wxErrCode = intent.getIntExtra("wx_errcode", Integer.MIN_VALUE);
        if (wxErrCode != Integer.MIN_VALUE) {
            Log.w(TAG, "onNewIntent: wx_errcode=" + wxErrCode);
            handleWeChatResult(wxErrCode, null);
            intent.removeExtra("wx_errcode");
            return;
        }
        // 处理深链接
        handleDeepLink(intent);
    }

    private void handleDeepLink(Intent intent) {
        if (intent == null || intent.getData() == null) return;
        Uri uri = intent.getData();
        if ("zhuoyi".equals(uri.getScheme()) && "login".equals(uri.getHost())) {
            String token = uri.getQueryParameter("token");
            String userJson = uri.getQueryParameter("user");
            if (token != null && !token.isEmpty()) {
                Log.i(TAG, "Deep link: got login token");
                String js = "localStorage.setItem('token','" + token.replace("'", "\'") + "');"
                    + (userJson != null ? "localStorage.setItem('user',decodeURIComponent('" + 
                    java.net.URLEncoder.encode(userJson, java.nio.charset.StandardCharsets.UTF_8).replace("'", "\'") + "'));" : "")
                    + "window.location.href='login.html';";
                runOnUiThread(() -> webView.evaluateJavascript(js, null));
            }
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (webView != null) webView.onResume();

        // 检查 Intent Extra 中的微信 code (主方案)
        String intentCode = getIntent().getStringExtra("wx_code");
        if (intentCode != null && !intentCode.isEmpty()) {
            Log.i(TAG, "onResume: got wx_code from intent=" + intentCode);
            String url = "file:///android_asset/login.html?wxcode=" + intentCode;
            runOnUiThread(() -> { if (webView != null) webView.loadUrl(url); });
            getIntent().removeExtra("wx_code");
            return;
        }

        // 检查 Intent Extra 中的错误码
        int intentErrCode = getIntent().getIntExtra("wx_errcode", Integer.MIN_VALUE);
        if (intentErrCode != Integer.MIN_VALUE) {
            Log.w(TAG, "onResume: wx_errcode from intent=" + intentErrCode);
            handleWeChatResult(intentErrCode, null);
            getIntent().removeExtra("wx_errcode");
            return;
        }

        // SharedPreferences 备用检查 (兼容旧流程)
        try {
            SharedPreferences sp = getSharedPreferences("wx_login", MODE_PRIVATE);
            String code = sp.getString("wx_code", null);
            long ts = sp.getLong("wx_time", 0);
            if (code != null && !code.isEmpty() && (System.currentTimeMillis() - ts) < 120000) {
                Log.i(TAG, "onResume: got wx_code from SP=" + code);
                String url = "file:///android_asset/login.html?wxcode=" + code.replace("'", "");
                runOnUiThread(() -> { if (webView != null) webView.loadUrl(url); });
                sp.edit().remove("wx_code").remove("wx_time").apply();
            } else if (sp.getInt("wx_errcode", -1) != -1) {
                int errCode = sp.getInt("wx_errcode", -1);
                sp.edit().remove("wx_errcode").apply();
                Log.w(TAG, "onResume: wx_errcode from SP=" + errCode);
            }
        } catch (Exception e) {
            Log.w(TAG, "wx code read error", e);
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (webView != null) webView.onPause();
    }

    @Override
    protected void onDestroy() {
        if (mainHandler != null) {
            mainHandler.removeCallbacksAndMessages(null);
        }
        if (webView != null) {
            webView.stopLoading();
            webView.setWebViewClient(null);
            webView.setWebChromeClient(null);
            webView.removeAllViews();
            webView.destroy();
        }
        super.onDestroy();
    }

    private void handleWeChatResult(int errCode, String code) {
        runOnUiThread(() -> {
            String js;
            if (errCode == 0 && code != null && !code.isEmpty()) {
                js = "window._onWechatCode && window._onWechatCode('" + code + "')";
            } else if (errCode == -2) {
                js = "window._onWechatCancel && window._onWechatCancel()";
            } else {
                js = "window._onWechatError && window._onWechatError(" + errCode + ")";
            }
            webView.evaluateJavascript(js, null);
        });
    }
}
