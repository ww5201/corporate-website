package com.zhuoyi.custom;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;
import com.tencent.mm.opensdk.modelmsg.SendAuth;
import com.tencent.mm.opensdk.openapi.IWXAPI;
import com.tencent.mm.opensdk.openapi.WXAPIFactory;

/**
 * 微信SDK封装 - 安全版本
 * 特点：
 * 1. 延迟初始化（首次调用时才init）
 * 2. 完整try-catch防闪退
 * 3. 静态单例模式
 */
public class WeChatAuthHelper {

    private static final String TAG = "WeChatAuth";
    private static final String APP_ID = "wxbf90ff43ddc3b955";

    private static IWXAPI sApi = null;
    private static boolean sInitAttempted = false;
    private static boolean sInitSuccess = false;

    /**
     * 安全初始化 - 只执行一次，失败不会崩溃
     */
    public static synchronized void init(Context context) {
        if (sInitSuccess && sApi != null) return;  // Already initialized OK

        // Allow retry if previous init failed
        sInitAttempted = true;
        try {
            if (context == null || context.getApplicationContext() == null) {
                Log.w(TAG, "init: context is null");
                return;
            }
            sApi = WXAPIFactory.createWXAPI(context.getApplicationContext(), APP_ID, false); // skip signature check
            if (sApi == null) {
                Log.w(TAG, "init: WXAPIFactory returned null");
                return;
            }
            sApi.registerApp(APP_ID);
            sInitSuccess = true;
            Log.i(TAG, "init: success");
        } catch (NoClassDefFoundError e) {
            // SDK not available (e.g., debug build without SDK)
            Log.w(TAG, "init: NoClassDefFoundError - SDK may not be included", e);
        } catch (Exception e) {
            Log.w(TAG, "init: unexpected error", e);
        }
    }

    /**
     * 检查微信是否已安装
     */
    public static boolean isWeChatInstalled(Context context) {
        if (!sInitSuccess || sApi == null) {
            if (context != null) init(context);
        }
        if (!sInitSuccess || sApi == null) return false;
        try {
            return sApi.isWXAppInstalled();
        } catch (Exception e) {
            return false;
        }
    }

    public static boolean isWeChatInstalled() {
        return sInitSuccess && sApi != null && sApi.isWXAppInstalled();
    }

    /**
     * 发起微信登录
     */
    public static boolean login(String scope, String state) {
        if (!sInitSuccess || sApi == null) {
            Log.w(TAG, "login: SDK not initialized");
            return false;
        }
        try {
            // Skip isWeChatInstalled check - just try sendReq directly
            SendAuth.Req req = new SendAuth.Req();
            req.scope = scope;
            req.state = state;
            return sApi.sendReq(req);
        } catch (Exception e) {
            Log.w(TAG, "login: failed", e);
            return false;
        }
    }

    /**
     * 获取API实例（供WXEntryActivity使用）
     */
    public static IWXAPI getApi() {
        return sApi;
    }

    /**
     * 获取初始化状态（调试用）
     */
    public static boolean isReady() {
        return sInitSuccess && sApi != null;
    }
}
