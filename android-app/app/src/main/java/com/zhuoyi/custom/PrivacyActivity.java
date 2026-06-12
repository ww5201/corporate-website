package com.zhuoyi.custom;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.ProgressBar;
import android.widget.TextView;

public class PrivacyActivity extends Activity {

    private WebView webView;
    private ProgressBar progressBar;
    private static final String PRIVACY_URL = "http://8.138.218.146/privacy.html";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(createLayout());
        setupWebView();
        webView.loadUrl(PRIVACY_URL);
    }

    private View createLayout() {
        android.widget.LinearLayout layout = new android.widget.LinearLayout(this);
        layout.setOrientation(android.widget.LinearLayout.VERTICAL);
        layout.setBackgroundColor(0xFFF5F5F7);

        // Top bar
        android.widget.RelativeLayout topBar = new android.widget.RelativeLayout(this);
        topBar.setBackgroundColor(0xFFFFFFFF);
        topBar.setPadding(16, 12, 16, 12);
        topBar.setElevation(4);

        TextView backBtn = new TextView(this);
        backBtn.setText("\u2039 \u8fd4\u56de");
        backBtn.setTextSize(16);
        backBtn.setTextColor(0xFF333333);
        backBtn.setPadding(16, 8, 16, 8);
        backBtn.setOnClickListener(v -> finish());

        TextView titleView = new TextView(this);
        titleView.setText("\u9690\u79c1\u653f\u7b56");
        titleView.setTextSize(18);
        titleView.setTextColor(0xFF1D1D1F);
        titleView.setGravity(android.view.Gravity.CENTER);

        android.widget.RelativeLayout.LayoutParams backParams = new android.widget.RelativeLayout.LayoutParams(
            android.widget.RelativeLayout.LayoutParams.WRAP_CONTENT,
            android.widget.RelativeLayout.LayoutParams.WRAP_CONTENT
        );
        backParams.addRule(android.widget.RelativeLayout.ALIGN_PARENT_LEFT);
        backParams.addRule(android.widget.RelativeLayout.CENTER_VERTICAL);
        topBar.addView(backBtn, backParams);

        android.widget.RelativeLayout.LayoutParams titleParams = new android.widget.RelativeLayout.LayoutParams(
            android.widget.RelativeLayout.LayoutParams.WRAP_CONTENT,
            android.widget.RelativeLayout.LayoutParams.WRAP_CONTENT
        );
        titleParams.addRule(android.widget.RelativeLayout.CENTER_IN_PARENT);
        topBar.addView(titleView, titleParams);

        layout.addView(topBar, new android.widget.LinearLayout.LayoutParams(
            android.widget.LinearLayout.LayoutParams.MATCH_PARENT,
            android.widget.LinearLayout.LayoutParams.WRAP_CONTENT
        ));

        // Progress bar
        progressBar = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progressBar.setMax(100);
        progressBar.setVisibility(View.GONE);
        layout.addView(progressBar, new android.widget.LinearLayout.LayoutParams(
            android.widget.LinearLayout.LayoutParams.MATCH_PARENT, 6
        ));

        // WebView
        webView = new WebView(this);
        layout.addView(webView, new android.widget.LinearLayout.LayoutParams(
            android.widget.LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f
        ));

        return layout;
    }

    private void setupWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);
        settings.setSupportZoom(true);

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

        webView.setWebViewClient(new WebViewClient());
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
