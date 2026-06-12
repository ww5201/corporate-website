package com.zhuoyi.custom;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.method.LinkMovementMethod;
import android.text.style.ClickableSpan;
import android.text.style.ForegroundColorSpan;
import android.view.View;
import android.view.WindowManager;
import android.widget.TextView;

public class SplashActivity extends Activity {

    private static final String PREFS_NAME = "zhuoyi_prefs";
    private static final String KEY_PRIVACY_AGREED = "privacy_agreed";
    private static final String PRIVACY_URL = "http://8.138.218.146/privacy.html";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );

        setContentView(R.layout.activity_splash);

        TextView versionText = findViewById(R.id.tvVersion);
        try {
            String ver = getPackageManager().getPackageInfo(getPackageName(), 0).versionName;
            versionText.setText("V " + ver);
        } catch (Exception e) {
            versionText.setText("V 1.0");
        }

        new Handler(Looper.getMainLooper()).postDelayed(() -> {
            if (isPrivacyAgreed()) {
                goToMain();
            } else {
                showPrivacyDialog();
            }
        }, 2000);
    }

    private boolean isPrivacyAgreed() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        return prefs.getBoolean(KEY_PRIVACY_AGREED, false);
    }

    private void setPrivacyAgreed() {
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        prefs.edit().putBoolean(KEY_PRIVACY_AGREED, true).apply();
    }

    private void showPrivacyDialog() {
        String text = "在使用卓翌定制前，请您阅读并同意《用户协议》和《隐私政策》。我们将依法保护您的个人信息安全。";

        SpannableString spannable = new SpannableString(text);

        // Make "隐私政策" clickable
        int privacyStart = text.indexOf("\u300a\u9690\u79c1\u653f\u7b56\u300b");
        int privacyEnd = privacyStart + "\u300a\u9690\u79c1\u653f\u7b56\u300b".length();

        if (privacyStart >= 0) {
            ClickableSpan privacyLink = new ClickableSpan() {
                @Override
                public void onClick(View widget) {
                    Intent intent = new Intent(SplashActivity.this, PrivacyActivity.class);
                    startActivity(intent);
                }
            };
            spannable.setSpan(privacyLink, privacyStart, privacyEnd, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
            spannable.setSpan(new ForegroundColorSpan(0xFFFF5722), privacyStart, privacyEnd, Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        }

        TextView msgView = new TextView(this);
        msgView.setText(spannable);
        msgView.setMovementMethod(LinkMovementMethod.getInstance());
        msgView.setPadding(40, 20, 40, 10);
        msgView.setTextSize(14);
        msgView.setLineSpacing(6, 1);

        new AlertDialog.Builder(this)
            .setTitle("\u7528\u6237\u534f\u8bae\u4e0e\u9690\u79c1\u653f\u7b56")
            .setView(msgView)
            .setPositiveButton("\u540c\u610f\u5e76\u7ee7\u7eed", (dialog, which) -> {
                setPrivacyAgreed();
                goToMain();
            })
            .setNegativeButton("\u4e0d\u540c\u610f", (dialog, which) -> {
                finish();
            })
            .setCancelable(false)
            .show();
    }

    private void goToMain() {
        startActivity(new Intent(SplashActivity.this, MainActivity.class));
        finish();
        overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
    }
}
