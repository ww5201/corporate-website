package com.zhuoyi.custom.wxapi;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import com.tencent.mm.opensdk.modelbase.BaseReq;
import com.tencent.mm.opensdk.modelbase.BaseResp;
import com.tencent.mm.opensdk.modelmsg.SendAuth;
import com.tencent.mm.opensdk.openapi.IWXAPI;
import com.tencent.mm.opensdk.openapi.IWXAPIEventHandler;
import com.tencent.mm.opensdk.openapi.WXAPIFactory;

public class WXEntryActivity extends Activity implements IWXAPIEventHandler {
    private static final String TAG = "WXEntry";
    private IWXAPI api;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.e(TAG, "=== onCreate START ===");
        api = WXAPIFactory.createWXAPI(this, "wxbf90ff43ddc3b955", false);
        api.registerApp("wxbf90ff43ddc3b955");
        api.handleIntent(getIntent(), this);
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        if (api != null) api.handleIntent(intent, this);
    }

    @Override
    public void onReq(BaseReq req) {}

    @Override
    public void onResp(BaseResp resp) {
        Log.e(TAG, "=== onResp errCode=" + resp.errCode + " ===");
        if (resp instanceof SendAuth.Resp) {
            SendAuth.Resp authResp = (SendAuth.Resp) resp;
            String code = authResp.code;
            int errCode = resp.errCode;
            Log.e(TAG, "code=" + code + " errCode=" + errCode);

            // Save to SharedPreferences (persistent)
            SharedPreferences.Editor ed = getSharedPreferences("wx_login", MODE_PRIVATE).edit();
            if (errCode == 0 && code != null && !code.isEmpty()) {
                ed.putString("wx_code", code);
                ed.putLong("wx_time", System.currentTimeMillis());
                Log.e(TAG, "Saved code OK");
            } else {
                ed.putInt("wx_errcode", errCode);
                Log.e(TAG, "Saved error: " + errCode);
            }
            ed.apply();
        }

        // Start MainActivity - it will load login.html which checks for the code
        Intent main = new Intent(this, com.zhuoyi.custom.MainActivity.class);
        main.putExtra("wx_code", "true");  // flag to tell MainActivity to load login.html
        main.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
        startActivity(main);
        finish();
    }
}
