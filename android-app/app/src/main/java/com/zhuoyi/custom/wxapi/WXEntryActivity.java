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
    private static final String APP_ID = "wxbf90ff43ddc3b955";
    private IWXAPI api;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.e(TAG, "=== onCreate START ===");
        api = WXAPIFactory.createWXAPI(this, APP_ID, false);
        api.registerApp(APP_ID);
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
        Log.e(TAG, "=== onResp type=" + resp.getType() + " errCode=" + resp.errCode + " ===");

        if (resp instanceof SendAuth.Resp) {
            SendAuth.Resp authResp = (SendAuth.Resp) resp;
            String code = authResp.code;
            int errCode = resp.errCode;
            Log.e(TAG, "Auth code=" + code + " errCode=" + errCode);

            // 方式1: 保存到 SharedPreferences (备用方案)
            SharedPreferences.Editor ed = getSharedPreferences("wx_login", MODE_PRIVATE).edit();
            if (errCode == 0 && code != null && !code.isEmpty()) {
                ed.putString("wx_code", code);
                ed.putLong("wx_time", System.currentTimeMillis());
                Log.e(TAG, "Saved code to SP OK");
            } else {
                ed.putInt("wx_errcode", errCode);
                Log.e(TAG, "Saved error to SP: " + errCode);
            }
            ed.apply();

            // 方式2: 通过 Intent Extra 传递给 MainActivity (主方案，更可靠)
            Intent main = new Intent(this, com.zhuoyi.custom.MainActivity.class);
            main.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
            if (errCode == 0 && code != null && !code.isEmpty()) {
                main.putExtra("wx_code", code);
                Log.e(TAG, "Passing code via intent extra");
            } else {
                main.putExtra("wx_errcode", errCode);
                Log.e(TAG, "Passing errcode via intent extra: " + errCode);
            }
            startActivity(main);
        } else {
            Log.e(TAG, "Non-auth response, type=" + resp.getType());
        }

        finish();
    }
}
