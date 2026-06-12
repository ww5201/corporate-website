package com.zhuoyi.custom.wxapi;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

import com.tencent.mm.opensdk.constants.ConstantsAPI;
import com.tencent.mm.opensdk.modelbase.BaseReq;
import com.tencent.mm.opensdk.modelbase.BaseResp;
import com.tencent.mm.opensdk.modelmsg.SendAuth;

import com.zhuoyi.custom.WeChatAuthHelper;

public class WXEntryActivity extends Activity implements com.tencent.mm.opensdk.openapi.IWXAPIEventHandler {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (WeChatAuthHelper.getApi() != null) {
            WeChatAuthHelper.getApi().handleIntent(getIntent(), this);
        }
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        if (WeChatAuthHelper.getApi() != null) {
            WeChatAuthHelper.getApi().handleIntent(intent, this);
        }
    }

    @Override
    public void onReq(BaseReq req) {
        // WeChat request from WeChat app to our app (rare)
    }

    @Override
    public void onResp(BaseResp resp) {
        if (resp.getType() == ConstantsAPI.COMMAND_SENDAUTH) {
            SendAuth.Resp authResp = (SendAuth.Resp) resp;
            String code = WeChatAuthHelper.handleResp(authResp);

            if (code != null) {
                // Send code back to the activity that initiated login
                Intent result = new Intent();
                result.setAction("com.zhuoyi.custom.WX_LOGIN_RESULT");
                result.putExtra("code", code);
                result.putExtra("state", authResp.state);
                sendBroadcast(result);
            } else {
                // Login cancelled or failed
                Intent result = new Intent();
                result.setAction("com.zhuoyi.custom.WX_LOGIN_RESULT");
                result.putExtra("error", "微信授权失败或取消");
                result.putExtra("errCode", resp.errCode);
                sendBroadcast(result);
            }
        }
        finish();
    }
}
