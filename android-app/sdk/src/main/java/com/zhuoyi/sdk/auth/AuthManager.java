package com.zhuoyi.sdk.auth;

import android.content.Context;
import android.content.SharedPreferences;
import com.zhuoyi.sdk.api.ApiClient;

/**
 * 认证管理器 - 处理登录、Token 管理、用户会话
 * 
 * 使用示例：
 * <pre>
 *   AuthManager auth = AuthManager.getInstance(context);
 *   auth.login("admin", "password123", callback);
 * </pre>
 */
public class AuthManager {

    private static final String PREFS_NAME = "zhuoyi_sdk_auth";
    private static final String KEY_TOKEN = "auth_token";
    private static final String KEY_USER_ID = "user_id";
    private static final String KEY_USER_NAME = "user_name";
    private static final String KEY_USER_ROLE = "user_role";
    private static final String KEY_LOGIN_TIME = "login_time";

    private static volatile AuthManager instance;
    private final Context appContext;
    private final SharedPreferences prefs;
    private ApiClient apiClient;

    private AuthManager(Context context) {
        this.appContext = context.getApplicationContext();
        this.prefs = appContext.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
    }

    public static synchronized AuthManager getInstance(Context context) {
        if (instance == null) {
            instance = new AuthManager(context);
        }
        return instance;
    }

    /** 绑定 API 客户端，自动同步 Token */
    public void bindApiClient(ApiClient client) {
        this.apiClient = client;
        // 恢复已保存的 Token
        String token = getToken();
        if (token != null && !token.isEmpty()) {
            client.setAuthToken(token);
        }
    }

    /**
     * 登录
     * @param username 用户名
     * @param password 密码
     * @param callback 回调
     */
    public void login(String username, String password,
                      com.zhuoyi.sdk.callback.ZhuoyiCallback<Object> callback) {
        if (apiClient == null) {
            callback.onFailure(-1, "API 客户端未初始化");
            return;
        }

        try {
            org.json.JSONObject body = new org.json.JSONObject();
            body.put("username", username);
            body.put("password", password);

            apiClient.post("/api/auth/login", body.toString(),
                new com.google.gson.reflect.TypeToken<com.zhuoyi.sdk.model.ApiResponse<Object>>(){}.getType(),
                new com.zhuoyi.sdk.callback.ZhuoyiCallback<Object>() {
                    @Override
                    public void onSuccess(Object data) {
                        try {
                            org.json.JSONObject result = (org.json.JSONObject) data;
                            String token = result.optString("token", "");
                            String userId = result.optString("userId", "");
                            String userName = result.optString("username", "");
                            String role = result.optString("role", "user");

                            saveSession(token, userId, userName, role);

                            if (apiClient != null) {
                                apiClient.setAuthToken(token);
                            }
                            callback.onSuccess(data);
                        } catch (Exception e) {
                            callback.onFailure(-2, "登录响应解析失败");
                        }
                    }

                    @Override
                    public void onFailure(int code, String message) {
                        callback.onFailure(code, message);
                    }
                });

        } catch (Exception e) {
            callback.onFailure(-3, "登录请求构建失败");
        }
    }

    /** 登出 */
    public void logout() {
        prefs.edit().clear().apply();
        if (apiClient != null) {
            apiClient.setAuthToken(null);
        }
    }

    /** 是否已登录 */
    public boolean isLoggedIn() {
        String token = getToken();
        return token != null && !token.isEmpty();
    }

    /** 获取 Token */
    public String getToken() {
        return prefs.getString(KEY_TOKEN, null);
    }

    /** 获取用户 ID */
    public String getUserId() {
        return prefs.getString(KEY_USER_ID, null);
    }

    /** 获取用户名 */
    public String getUserName() {
        return prefs.getString(KEY_USER_NAME, null);
    }

    /** 获取用户角色 */
    public String getUserRole() {
        return prefs.getString(KEY_USER_ROLE, "guest");
    }

    /** 是否为管理员 */
    public boolean isAdmin() {
        return "admin".equals(getUserRole()) || "manager".equals(getUserRole());
    }

    private void saveSession(String token, String userId, String userName, String role) {
        prefs.edit()
            .putString(KEY_TOKEN, token)
            .putString(KEY_USER_ID, userId)
            .putString(KEY_USER_NAME, userName)
            .putString(KEY_USER_ROLE, role)
            .putLong(KEY_LOGIN_TIME, System.currentTimeMillis())
            .apply();
    }
}
