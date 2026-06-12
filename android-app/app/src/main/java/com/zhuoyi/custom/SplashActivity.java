package com.zhuoyi.custom;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.WindowManager;
import android.widget.TextView;

public class SplashActivity extends Activity {

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
            startActivity(new Intent(SplashActivity.this, MainActivity.class));
            finish();
            overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
        }, 2000);
    }
}
