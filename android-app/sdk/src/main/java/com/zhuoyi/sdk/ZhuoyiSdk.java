package com.zhuoyi.sdk;

import android.app.Activity;
import android.content.Context;
import com.zhuoyi.sdk.api.ApiClient;
import com.zhuoyi.sdk.auth.AuthManager;
import com.zhuoyi.sdk.payment.PaymentHelper;
import com.zhuoyi.sdk.webview.WebViewWrapper;

/**
 * 卓翌定制 Android SDK - 主入口
 * 
 * 一站式集成卓翌定制平台能力，包括：
 * - API 客户端（产品、订单、留言）
 * - 认证管理（登录/登出/Token 持久化）
 * - WebView 封装组件
 * - 支付集成（支付宝/微信/银联）
 * 
 * 快速开始：
 * <pre>
 *   // 1. 初始化（建议在 Application.onCreate 中）
 *   ZhuoyiSdk.init(context, "http://8.138.218.146");
 *   
 *   // 2. 获取 API 客户端
 *   ApiClient api = ZhuoyiSdk.getApiClient();
 *   api.getProducts(callback);
 *   
 *   // 3. 使用 WebView 组件
 *   WebViewWrapper wrapper = ZhuoyiSdk.createWebView(activity)
 *       .baseUrl("http://8.138.218.146")
 *       .build();
 *   wrapper.attach(container);
 *   
 *   // 4. 支付功能
 *   PaymentHelper payment = ZhuoyiSdk.createPaymentHelper(activity);
 *   payment.createPayment(orderId, 99.9, PaymentHelper.PAYMENT_ALIPAY, listener);
 * </pre>
 */
public class ZhuoyiSdk {

    private static final String VERSION = "1.0.0";
    private static volatile ZhuoyiSdk instance;

    private String baseUrl;
    private ApiClient apiClient;
    private AuthManager authManager;
    private boolean initialized = false;

    /** 私有构造 */
    private ZhuoyiSdk() {}

    /**
     * 初始化 SDK
     * @param context Application Context
     * @param serverBaseUrl 服务器地址，如 "http://8.138.218.146"
     */
    public static void init(Context context, String serverBaseUrl) {
        if (instance == null) {
            synchronized (ZhuoyiSdk.class) {
                if (instance == null) {
                    instance = new ZhuoyiSdk();
                    instance.doInit(context, serverBaseUrl);
                }
            }
        }
    }

    private void doInit(Context context, String serverBaseUrl) {
        this.baseUrl = serverBaseUrl;
        this.apiClient = new ApiClient(serverBaseUrl);
        this.authManager = AuthManager.getInstance(context);
        this.authManager.bindApiClient(apiClient);
        this.initialized = true;
    }

    /** 获取 SDK 单例 */
    public static ZhuoyiSdk getInstance() {
        if (instance == null) {
            throw new IllegalStateException("SDK 未初始化！请先调用 ZhuoyiSdk.init()");
        }
        return instance;
    }

    /** 是否已初始化 */
    public boolean isInitialized() { return initialized; }

    /** 获取 SDK 版本号 */
    public static String getVersion() { return VERSION; }

    /** 获取服务器基础地址 */
    public String getBaseUrl() { return baseUrl; }

    // ==================== 核心组件获取 ====================

    /** 获取 API 客户端 */
    public static ApiClient getApiClient() { return getInstance().apiClient; }

    /** 获取认证管理器 */
    public static AuthManager getAuthManager() { return getInstance().authManager; }

    /**
     * 创建 WebView 封装器（Builder 模式）
     * @param activity 当前 Activity
     * @return WebViewWrapper.Builder
     */
    public static WebViewWrapper.Builder createWebView(Activity activity) {
        return new WebViewWrapper.Builder(activity).baseUrl(getInstance().baseUrl);
    }

    /**
     * 创建支付助手
     * @param activity 当前 Activity
     * @return PaymentHelper 实例
     */
    public static PaymentHelper createPaymentHelper(Activity activity) {
        return new PaymentHelper(getInstance().apiClient, activity);
    }

    // ==================== 便捷方法 ====================

    /**
     * 快速加载用户端页面到 WebView
     * @param activity Activity
     * @param container 容器 ViewGroup
     */
    public static void loadCustomerApp(Activity activity, android.view.ViewGroup container) {
        WebViewWrapper wrapper = createWebView(activity)
            .enablePullRefresh(true)
            .enableZoom(true)
            .userAgentSuffix("ZhuoyiCustom/1.0")
            .build();
        wrapper.attach(container);
    }

    /**
     * 快速加载管理后台页面到 WebView
     * @param activity Activity
     * @param container 容器 ViewGroup
     */
    public static void loadAdminApp(Activity activity, android.view.ViewGroup container) {
        WebViewWrapper wrapper = createWebView(activity)
            .baseUrl(getInstance().baseUrl + "/admin")
            .enablePullRefresh(true)
            .enableZoom(true)
            .enableDebug(true)
            .userAgentSuffix("ZhuoyiAdmin/1.0")
            .build();
        wrapper.attach(container);
    }
}
