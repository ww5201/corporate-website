package com.zhuoyi.sdk.webview;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.view.KeyEvent;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.DownloadListener;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import android.widget.RelativeLayout;
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout;

/**
 * 卓翌定制 WebView 封装组件
 * 
 * 提供预配置的 WebView，支持：
 * - 自动 JS/DOM/缓存配置
 * - 进度条显示
 * - 下拉刷新
 * - 文件选择/上传
 * - 外部协议处理（tel: mailto: weixin:// alipays://）
 * - 返回键导航
 * - SSL 错误容忍
 * 
 * 使用示例：
 * <pre>
 *   WebViewWrapper wrapper = new WebViewWrapper.Builder(activity)
 *       .baseUrl("http://8.138.218.146")
 *       .enablePullRefresh(true)
 *       .enableDebug(true)
 *       .build();
 *   RelativeLayout container = activity.findViewById(R.id.container);
 *   wrapper.attach(container);
 * </pre>
 */
public class WebViewWrapper {

    private final Activity activity;
    private final String baseUrl;
    private final boolean enablePullRefresh;
    private final boolean enableZoom;
    private final boolean enableDebug;
    private final String userAgentSuffix;

    private WebView webView;
    private ProgressBar progressBar;
    private SwipeRefreshLayout swipeRefreshLayout;
    private ValueCallback<Uri[]> uploadMessage;
    private OnPageLoadedListener pageLoadedListener;
    private OnUrlInterceptListener urlInterceptListener;
    private OnErrorListener errorListener;

    public static final int FILE_CHOOSER_REQUEST_CODE = 10086;

    public interface OnPageLoadedListener {
        void onPageLoaded(String url);
        void onPageLoadError(String url, int errorCode);
    }

    public interface OnUrlInterceptListener {
        boolean shouldOverrideUrl(String url);
    }

    public interface OnErrorListener {
        void onError(String url, int errorCode, String description);
    }

    private WebViewWrapper(Builder builder) {
        this.activity = builder.activity;
        this.baseUrl = builder.baseUrl;
        this.enablePullRefresh = builder.enablePullRefresh;
        this.enableZoom = builder.enableZoom;
        this.enableDebug = builder.enableDebug;
        this.userAgentSuffix = builder.userAgentSuffix;
    }

    /**
     * 将 WebView 附加到容器
     */
    public void attach(ViewGroup container) {
        // 创建进度条
        progressBar = new ProgressBar(activity, null, android.R.attr.progressBarStyleHorizontal);
        RelativeLayout.LayoutParams progressParams = new RelativeLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            (int) (3 * activity.getResources().getDisplayMetrics().density)
        );
        progressBar.setMax(100);

        // 创建 WebView
        webView = new WebView(activity);
        RelativeLayout.LayoutParams webParams = new RelativeLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.MATCH_PARENT
        );
        setupWebView();

        if (enablePullRefresh) {
            swipeRefreshLayout = new SwipeRefreshLayout(activity);
            swipeRefreshLayout.setColorSchemeResources(
                android.R.color.holo_blue_bright,
                android.R.color.holo_green_light,
                android.R.color.holo_orange_light,
                android.R.color.holo_red_light
            );

            RelativeLayout innerLayout = new RelativeLayout(activity);
            innerLayout.addView(progressBar, progressParams);
            webParams.addRule(RelativeLayout.BELOW, progressBar.getId());
            innerLayout.addView(webView, webParams);
            swipeRefreshLayout.addView(innerLayout,
                new ViewGroup.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.MATCH_PARENT
                )
            );

            container.addView(swipeRefreshLayout,
                new ViewGroup.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.MATCH_PARENT
                )
            );

            setupSwipeRefresh();
        } else {
            container.addView(progressBar, progressParams);
            webParams.addRule(RelativeLayout.BELOW, progressBar.getId());
            container.addView(webView, webParams);
        }

        loadUrl(baseUrl);
    }

    private void setupWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setSupportZoom(enableZoom);
        settings.setBuiltInZoomControls(enableZoom);
        if (enableZoom) {
            settings.setDisplayZoomControls(false);
        }
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);

        String ua = settings.getUserAgentString();
        if (userAgentSuffix != null && !userAgentSuffix.isEmpty()) {
            ua += " " + userAgentSuffix;
        }
        settings.setUserAgentString(ua);

        if (enableDebug) {
            WebView.setWebContentsDebuggingEnabled(true);
        }

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();

                // 外部协议拦截
                if (url.startsWith("tel:") || url.startsWith("mailto:") ||
                    url.startsWith("weixin://") || url.startsWith("alipays://")) {
                    handleExternalUrl(url);
                    return true;
                }

                // 自定义 URL 拦截器
                if (urlInterceptListener != null && urlInterceptListener.shouldOverrideUrl(url)) {
                    return true;
                }

                return false; // 让 WebView 自己加载
            }

            @Override
            public void onReceivedSslError(WebView view,
                                           android.webkit.SslErrorHandler handler,
                                           android.net.http.SslError error) {
                handler.proceed(); // 开发阶段忽略证书错误
            }

            @Override
            public void onReceivedHttpError(WebView view, WebResourceRequest request,
                                             android.webkit.WebResourceResponse errorResponse) {
                // 非关键资源错误可忽略
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request,
                                         WebResourceError error) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    String url = (request != null) ? request.getUrl().toString() : "";
                    if (errorListener != null) {
                        errorListener.onError(url, error.getErrorCode(), error.getDescription().toString());
                    }
                    if (pageLoadedListener != null) {
                        pageLoadedListener.onPageLoadError(url, error.getErrorCode());
                    }
                }
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                if (pageLoadedListener != null) {
                    pageLoadedListener.onPageLoaded(url);
                }
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                if (progressBar != null) {
                    if (newProgress < 100) {
                        progressBar.setVisibility(View.VISIBLE);
                        progressBar.setProgress(newProgress);
                    } else {
                        progressBar.setVisibility(View.GONE);
                    }
                }
            }

            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback,
                                             FileChooserParams fileChooserParams) {
                if (uploadMessage != null) {
                    uploadMessage.onReceiveValue(null);
                }
                uploadMessage = filePathCallback;

                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("*/*");
                try {
                    activity.startActivityForResult(
                        Intent.createChooser(intent, "选择文件"),
                        FILE_CHOOSER_REQUEST_CODE
                    );
                } catch (ActivityNotFoundException e) {
                    uploadMessage.onReceiveValue(null);
                    uploadMessage = null;
                }
                return true;
            }
        });

        webView.setDownloadListener((url, userAgent, contentDisposition, mimeType, contentLength) -> {
            try {
                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                activity.startActivity(intent);
            } catch (Exception e) {
                android.widget.Toast.makeText(activity, "无法打开链接", android.widget.Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void setupSwipeRefresh() {
        if (swipeRefreshLayout == null) return;
        swipeRefreshLayout.setOnRefreshListener(() -> {
            reload();
            new android.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> {
                if (swipeRefreshLayout != null) {
                    swipeRefreshLayout.setRefreshing(false);
                }
            }, 1500);
        });
    }

    private void handleExternalUrl(String url) {
        try {
            activity.startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
        } catch (Exception e) {
            android.widget.Toast.makeText(activity, "未安装对应应用", android.widget.Toast.LENGTH_SHORT).show();
        }
    }

    /** 加载 URL */
    public void loadUrl(String url) { if (webView != null) webView.loadUrl(url); }

    /** 刷新 */
    public void reload() { if (webView != null) webView.reload(); }

    /** 后退 */
    public boolean goBack() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
            return true;
        }
        return false;
    }

    /** 前进 */
    public boolean goForward() { return webView != null && webView.canGoForward(); }

    /** 是否可以后退 */
    public boolean canGoBack() { return webView != null && webView.canGoBack(); }

    /** 获取当前 URL */
    public String getUrl() { return webView != null ? webView.getUrl() : null; }

    /** 获取原始 WebView */
    public WebView getWebView() { return webView; }

    /** 处理文件选择结果 */
    public void handleFileChooserResult(int resultCode, Intent data) {
        if (uploadMessage == null) return;
        Uri[] results = null;
        if (resultCode == Activity.RESULT_OK && data != null) {
            String dataString = data.getDataString();
            if (dataString != null) {
                results = new Uri[]{Uri.parse(dataString)};
            }
        }
        uploadMessage.onReceiveValue(results);
        uploadMessage = null;
    }

    /** 销毁 WebView */
    public void destroy() {
        if (webView != null) {
            webView.stopLoading();
            webView.onPause();
            webView.removeAllViews();
            webView.destroy();
            webView = null;
        }
    }

    /** 暂停 */
    public void onPause() { if (webView != null) webView.onPause(); }

    /** 恢复 */
    public void onResume() { if (webView != null) webView.onResume(); }

    // ==================== Builder ====================

    public static class Builder {
        private final Activity activity;
        private String baseUrl;
        private boolean enablePullRefresh = true;
        private boolean enableZoom = false;
        private boolean enableDebug = false;
        private String userAgentSuffix;

        public Builder(Activity activity) {
            this.activity = activity;
        }

        public Builder baseUrl(String url) { this.baseUrl = url; return this; }
        public Builder enablePullRefresh(boolean enable) { this.enablePullRefresh = enable; return this; }
        public Builder enableZoom(boolean enable) { this.enableZoom = enable; return this; }
        public Builder enableDebug(boolean enable) { this.enableDebug = enable; return this; }
        public Builder userAgentSuffix(String suffix) { this.userAgentSuffix = suffix; return this; }

        public WebViewWrapper build() {
            if (baseUrl == null || baseUrl.isEmpty()) {
                throw new IllegalArgumentException("baseUrl 不能为空");
            }
            return new WebViewWrapper(this);
        }
    }

    // ==================== Setters for listeners ====================

    public WebViewWrapper setOnPageLoadedListener(OnPageLoadedListener listener) {
        this.pageLoadedListener = listener; return this;
    }

    public WebViewWrapper setOnUrlInterceptListener(OnUrlInterceptListener listener) {
        this.urlInterceptListener = listener; return this;
    }

    public WebViewWrapper setOnErrorListener(OnErrorListener listener) {
        this.errorListener = listener; return this;
    }
}
