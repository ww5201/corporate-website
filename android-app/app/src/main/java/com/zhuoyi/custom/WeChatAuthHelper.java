package com.zhuoyi.custom;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;

import com.tencent.mm.opensdk.modelmsg.SendAuth;
import com.tencent.mm.opensdk.openapi.IWXAPI;
import com.tencent.mm.opensdk.openapi.WXAPIFactory;

public class WeChatAuthHelper {

    public static final String WECHAT_APP_ID = "wx187d6ca3a6da9ca3";
    private static IWXAPI wxApi;

    /**
     * 初始化微信 SDK
     */
    public static void init(Context context) {
        wxApi = WXAPIFactory.createWXAPI(context, WECHAT_APP_ID, true);
        wxApi.registerApp(WECHAT_APP_ID);
    }

    /**
     * 获取微信 API 实例
     */
    public static IWXAPI getApi() {
        return wxApi;
    }

    /**
     * 检查微信是否已安装
     */
    public static boolean isWeChatInstalled() {
        return wxApi != null && wxApi.isWXAppInstalled();
    }

    /**
     * 发起微信登录授权
     * @param scope 权限范围，默认 "snsapi_userinfo"
     * @param state 防 CSRF 攻击的随机字符串
     */
    public static boolean login(String scope, String state) {
        if (wxApi == null || !wxApi.isWXAppInstalled()) {
            return false;
        }

        SendAuth.Req req = new SendAuth.Req();
        req.scope = (scope != null && !scope.isEmpty()) ? scope : "snsapi_userinfo";
        req.state = (state != null && !state.isEmpty()) ? state : "zhuoyi_login_" + System.currentTimeMillis();

        return wxApi.sendReq(req);
    }

    /**
     * 处理微信回调（从 WXEntryActivity 调用）
     * 返回 code 或 null
     */
    public static String handleResp(SendAuth.Resp resp) {
        if (resp.errCode == 0) { // SendAuth.Resp.Success = 0
            return resp.code;
        }
        return null;
    }
}
