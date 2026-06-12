package com.zhuoyi.sdk.api;

import android.os.Handler;
import android.os.Looper;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.zhuoyi.sdk.callback.ZhuoyiCallback;
import com.zhuoyi.sdk.model.ApiResponse;
import com.zhuoyi.sdk.model.Product;
import com.zhuoyi.sdk.model.Order;
import okhttp3.*;
import org.json.JSONObject;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

/**
 * 卓翌定制 API 客户端
 * 
 * 使用示例：
 * <pre>
 *   ApiClient client = new ApiClient("http://8.138.218.146");
 *   client.getProducts(new ZhuoyiCallback&lt;List&lt;Product&gt;&gt;() {
 *       public void onSuccess(List&lt;Product&gt; data) { ... }
 *       public void onFailure(int code, String msg) { ... }
 *   });
 * </pre>
 */
public class ApiClient {

    private static final String TAG = "ZhuoyiApiClient";
    private final String baseUrl;
    private final OkHttpClient httpClient;
    private final Gson gson;
    private final Handler mainHandler;
    private String authToken;

    public ApiClient(String baseUrl) {
        this.baseUrl = baseUrl.endsWith("/") ? baseUrl.substring(0, baseUrl.length() - 1) : baseUrl;
        this.gson = new Gson();
        this.mainHandler = new Handler(Looper.getMainLooper());
        this.httpClient = new OkHttpClient.Builder()
            .connectTimeout(15, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(15, TimeUnit.SECONDS)
            .retryOnConnectionFailure(true)
            .build();
    }

    /** 设置认证 Token */
    public void setAuthToken(String token) {
        this.authToken = token;
    }

    /** 获取当前 Token */
    public String getAuthToken() { return authToken; }

    // ==================== 产品 API ====================

    /**
     * 获取产品列表
     * @param callback 回调
     */
    public void getProducts(ZhuoyiCallback<List<Product>> callback) {
        get("/api/products", new TypeToken<ApiResponse<List<Product>>>(){}.getType(), callback);
    }

    /**
     * 获取产品详情
     * @param productId 产品ID
     * @param callback 回调
     */
    public void getProduct(String productId, ZhuoyiCallback<Product> callback) {
        get("/api/products/" + productId, new TypeToken<ApiResponse<Product>>(){}.getType(), callback);
    }

    /**
     * 按分类获取产品
     * @param category 分类名称
     * @param callback 回调
     */
    public void getProductsByCategory(String category, ZhuoyiCallback<List<Product>> callback) {
        get("/api/products?category=" + encodeParam(category),
            new TypeToken<ApiResponse<List<Product>>>(){}.getType(), callback);
    }

    // ==================== 订单 API ====================

    /**
     * 创建订单
     * @param orderData 订单数据（JSON格式）
     * @param callback 回调
     */
    public void createOrder(JSONObject orderData, ZhuoyiCallback<Order> callback) {
        post("/api/orders", orderData.toString(), new TypeToken<ApiResponse<Order>>(){}.getType(), callback);
    }

    /**
     * 获取订单列表（管理端）
     * @param callback 回调
     */
    public void getOrders(ZhuoyiCallback<List<Order>> callback) {
        get("/api/orders", new TypeToken<ApiResponse<List<Order>>>(){}.getType(), callback);
    }

    /**
     * 更新订单状态
     * @param orderId 订单ID
     * @param status 新状态
     * @param callback 回调
     */
    public void updateOrderStatus(String orderId, String status, ZhuoyiCallback<Order> callback) {
        JSONObject body = new JSONObject();
        try {
            body.put("status", status);
        } catch (Exception e) { /* ignore */ }
        put("/api/orders/" + orderId, body.toString(),
            new TypeToken<ApiResponse<Order>>(){}.getType(), callback);
    }

    // ==================== 留言 API ====================

    /**
     * 提交留言
     * @param messageData 留言数据
     * @param callback 回调
     */
    public void submitMessage(JSONObject messageData, ZhuoyiCallback<Object> callback) {
        post("/api/messages", messageData.toString(),
            new TypeToken<ApiResponse<Object>>(){}.getType(), callback);
    }

    /**
     * 获取留言列表（管理端）
     * @param callback 回调
     */
    public void getMessages(ZhuoyiCallback<List<Object>> callback) {
        get("/api/messages", new TypeToken<ApiResponse<List<Object>>>(){}.getType(), callback);
    }

    // ==================== 通用 HTTP 方法（公开给 SDK 内部使用） ====================

    /**
     * 通用 POST 请求
     */
    public <T> void post(String path, String jsonBody, java.lang.reflect.Type type,
                          ZhuoyiCallback<T> callback) {
        postInternal(path, jsonBody, type, callback);
    }

    /**
     * 通用 GET 请求
     */
    public <T> void get(String path, java.lang.reflect.Type type,
                         ZhuoyiCallback<T> callback) {
        getInternal(path, type, callback);
    }

    // ==================== HTTP 核心方法（内部） ====================

    private void getInternal(final String path, final java.lang.reflect.Type type,
                     final ZhuoyiCallback<?> callback) {
        Request.Builder builder = new Request.Builder()
            .url(baseUrl + path)
            .get();

        addAuthHeader(builder);

        httpClient.newCall(builder.build()).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                mainHandler.post(() -> callback.onFailure(-1, "网络连接失败: " + e.getMessage()));
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                String body = response.body().string();
                handleResponse(body, type, callback);
            }
        });
    }

    private void postInternal(final String path, final String jsonBody,
                      final java.lang.reflect.Type type, final ZhuoyiCallback<?> callback) {
        MediaType JSON = MediaType.parse("application/json; charset=utf-8");
        RequestBody body = RequestBody.create(jsonBody, JSON);

        Request.Builder builder = new Request.Builder()
            .url(baseUrl + path)
            .post(body);

        addAuthHeader(builder);

        httpClient.newCall(builder.build()).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                mainHandler.post(() -> callback.onFailure(-1, "网络连接失败: " + e.getMessage()));
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                String respBody = response.body().string();
                handleResponse(respBody, type, callback);
            }
        });
    }

    private void put(final String path, final String jsonBody,
                     final java.lang.reflect.Type type, final ZhuoyiCallback<?> callback) {
        MediaType JSON = MediaType.parse("application/json; charset=utf-8");
        RequestBody body = RequestBody.create(jsonBody, JSON);

        Request.Builder builder = new Request.Builder()
            .url(baseUrl + path)
            .put(body);

        addAuthHeader(builder);

        httpClient.newCall(builder.build()).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                mainHandler.post(() -> callback.onFailure(-1, "网络连接失败: " + e.getMessage()));
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                String respBody = response.body().string();
                handleResponse(respBody, type, callback);
            }
        });
    }

    @SuppressWarnings("unchecked")
    private <T> void handleResponse(String body, java.lang.reflect.Type type,
                                     ZhuoyiCallback<T> callback) {
        try {
            ApiResponse<T> response = gson.fromJson(body, type);
            if (response != null && response.isSuccess()) {
                mainHandler.post(() -> callback.onSuccess(response.getData()));
            } else {
                String msg = (response != null) ? response.getMessage() : "服务器响应异常";
                int code = (response != null) ? response.getCode() : -1;
                mainHandler.post(() -> callback.onFailure(code, msg));
            }
        } catch (Exception e) {
            mainHandler.post(() -> callback.onFailure(-2, "数据解析错误: " + e.getMessage()));
        }
    }

    private void addAuthHeader(Request.Builder builder) {
        if (authToken != null && !authToken.isEmpty()) {
            builder.addHeader("Authorization", "Bearer " + authToken);
        }
        builder.addHeader("Accept", "application/json");
        builder.addHeader("User-Agent", "ZhuoyiSDK-Android/1.0");
    }

    private String encodeParam(String param) {
        try {
            return java.net.URLEncoder.encode(param, "UTF-8");
        } catch (Exception e) {
            return param;
        }
    }
}
