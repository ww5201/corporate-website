package com.zhuoyi.sdk.payment;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Handler;
import android.os.Looper;
import com.zhuoyi.sdk.api.ApiClient;
import com.zhuoyi.sdk.callback.ZhuoyiCallback;
import org.json.JSONObject;

/**
 * 支付助手 - 支付宝/微信支付集成
 * 
 * 使用示例：
 * <pre>
 *   PaymentHelper payment = new PaymentHelper(apiClient, activity);
 *   payment.createPayment(orderId, amount, "alipay", callback);
 * </pre>
 */
public class PaymentHelper {

    public static final String PAYMENT_ALIPAY = "alipay";
    public static final String PAYMENT_WECHAT = "wechat";
    public static final String PAYMENT_UNIONPAY = "unionpay";

    private final ApiClient apiClient;
    private final Activity activity;
    private final Handler mainHandler;

    public interface OnPaymentResultListener {
        void onPaymentSuccess(String orderId, String transactionId);
        void onPaymentFailed(String orderId, int code, String message);
        void onPaymentCancelled(String orderId);
    }

    public PaymentHelper(ApiClient apiClient, Activity activity) {
        this.apiClient = apiClient;
        this.activity = activity;
        this.mainHandler = new Handler(Looper.getMainLooper());
    }

    /**
     * 创建支付订单
     * @param orderId 订单ID
     * @param amount 金额（元）
     * @param payType 支付类型：alipay / wechat / unionpay
     * @param listener 结果回调
     */
    public void createPayment(String orderId, double amount, String payType,
                               OnPaymentResultListener listener) {
        try {
            JSONObject body = new JSONObject();
            body.put("orderId", orderId);
            body.put("amount", amount);
            body.put("payType", payType);

            apiClient.post("/api/payment/create", body.toString(),
                Object.class, new ZhuoyiCallback<Object>() {
                    @Override
                    public void onSuccess(Object data) {
                        try {
                            JSONObject result = (JSONObject) data;
                            String payUrl = result.optString("payUrl", "");
                            String tradeNo = result.optString("tradeNo", "");

                            if (!payUrl.isEmpty()) {
                                launchPayApp(payUrl, payType, orderId, tradeNo, listener);
                            } else {
                                listener.onPaymentFailed(orderId, -1, "获取支付链接失败");
                            }
                        } catch (Exception e) {
                            listener.onPaymentFailed(orderId, -2, "解析支付数据失败");
                        }
                    }

                    @Override
                    public void onFailure(int code, String message) {
                        listener.onPaymentFailed(orderId, code, message);
                    }
                });
        } catch (Exception e) {
            listener.onPaymentFailed(orderId, -3, "创建支付请求失败");
        }
    }

    /**
     * 查询支付结果
     * @param orderId 订单ID
     * @param listener 回调
     */
    public void queryPaymentStatus(String orderId, ZhuoyiCallback<Object> listener) {
        apiClient.get("/api/payment/status?orderId=" + orderId,
            Object.class, listener);
    }

    private void launchPayApp(String payUrl, String payType, String orderId,
                               String tradeNo, OnPaymentResultListener listener) {
        try {
            Uri uri = Uri.parse(payUrl);
            Intent intent = new Intent(Intent.ACTION_VIEW, uri);

            if (PAYMENT_ALIPAY.equals(payType)) {
                // 支付宝 scheme 跳转
                if (payUrl.startsWith("alipays://") || payUrl.contains("alipay.com")) {
                    intent = new Intent(Intent.ACTION_VIEW, uri);
                }
            } else if (PAYMENT_WECHAT.equals(payType)) {
                // 微信支付需要通过 URL scheme 或浏览器
                if (payUrl.startsWith("weixin://")) {
                    intent = new Intent(Intent.ACTION_VIEW, uri);
                }
            }

            activity.startActivity(intent);

            // 延迟查询支付结果
            mainHandler.postDelayed(() -> queryAndNotify(orderId, listener), 3000);

        } catch (Exception e) {
            // 如果无法唤起支付 App，尝试用浏览器打开
            try {
                Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(payUrl));
                activity.startActivity(browserIntent);
                mainHandler.postDelayed(() -> queryAndNotify(orderId, listener), 5000);
            } catch (Exception e2) {
                listener.onPaymentFailed(orderId, -4, "无法启动支付");
            }
        }
    }

    private void queryAndNotify(String orderId, OnPaymentResultListener listener) {
        queryPaymentStatus(orderId, new ZhuoyiCallback<Object>() {
            @Override
            public void onSuccess(Object data) {
                try {
                    JSONObject result = (JSONObject) data;
                    String status = result.optString("status", "");
                    String tradeId = result.optString("tradeNo", "");

                    if ("paid".equals(status) || "success".equals(status)) {
                        listener.onPaymentSuccess(orderId, tradeId);
                    } else if ("pending".equals(status)) {
                        // 继续轮询
                        mainHandler.postDelayed(() -> queryAndNotify(orderId, listener), 3000);
                    } else {
                        listener.onPaymentCancelled(orderId);
                    }
                } catch (Exception e) {
                    listener.onPaymentCancelled(orderId);
                }
            }

            @Override
            public void onFailure(int code, String message) {
                listener.onPaymentCancelled(orderId);
            }
        });
    }
}
