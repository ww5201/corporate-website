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

    /**
     * 微信登录（OAuth2）
     * 将微信授权码发送到后端，后端通过微信开放平台换取 openid
     *
     * @param code     微信授权码（从 WeChatAuthHelper 获取）
     * @param nickname 微信昵称（可选，新用户注册时使用）
     * @param avatar   微信头像 URL（可选）
     * @param callback 回调
     */
    public void loginByWechat(String code, String nickname, String avatar,
                              com.zhuoyi.sdk.callback.ZhuoyiCallback<Object> callback) {
        if (apiClient == null) {
            callback.onFailure(-1, "API 客户端未初始化");
            return;
        }
        if (code == null || code.isEmpty()) {
            callback.onFailure(-2, "微信授权码为空");
            return;
        }

        try {
            org.json.JSONObject body = new org.json.JSONObject();
            body.put("code", code);
            if (nickname != null && !nickname.isEmpty()) {
                body.put("nickname", nickname);
            }
            if (avatar != null && !avatar.isEmpty()) {
                body.put("avatar", avatar);
            }

            apiClient.post("/api/auth/wechat/login", body.toString(),
                new com.google.gson.reflect.TypeToken<com.zhuoyi.sdk.model.ApiResponse<Object>>(){}.getType(),
                new com.zhuoyi.sdk.callback.ZhuoyiCallback<Object>() {
                    @Override
                    public void onSuccess(Object data) {
                        handleLoginResponse(data, callback);
                    }

                    @Override
                    public void onFailure(int code, String message) {
                        callback.onFailure(code, message);
                    }
                });

        } catch (Exception e) {
            callback.onFailure(-3, "微信登录请求构建失败: " + e.getMessage());
        }
    }

    /**
     * 手机号 + 验证码登录
     *
     * @param phone    手机号
     * @param smsCode  短信验证码
     * @param callback 回调
     */
    public void loginByPhone(String phone, String smsCode,
                             com.zhuoyi.sdk.callback.ZhuoyiCallback<Object> callback) {
        if (apiClient == null) {
            callback.onFailure(-1, "API 客户端未初始化");
            return;
        }
        if (phone == null || smsCode == null) {
            callback.onFailure(-2, "手机号或验证码为空");
            return;
        }

        try {
            org.json.JSONObject body = new org.json.JSONObject();
            body.put("phone", phone);
            body.put("code", smsCode);

            apiClient.post("/api/auth/phone/login", body.toString(),
                new com.google.gson.reflect.TypeToken<com.zhuoyi.sdk.model.ApiResponse<Object>>(){}.getType(),
                new com.zhuoyi.sdk.callback.ZhuoyiCallback<Object>() {
                    @Override
                    public void onSuccess(Object data) {
                        handleLoginResponse(data, callback);
                    }

                    @Override
                    public void onFailure(int code, String message) {
                        callback.onFailure(code, message);
                    }
                });

        } catch (Exception e) {
            callback.onFailure(-3, "手机登录请求构建失败: " + e.getMessage());
        }
    }

    /**
     * 发送短信验证码
     *
     * @param phone    手机号
     * @param callback 回调
     */
    public void sendSmsCode(String phone,
                            com.zhuoyi.sdk.callback.ZhuoyiCallback<Object> callback) {
        if (apiClient == null) {
            callback.onFailure(-1, "API 客户端未初始化");
            return;
        }

        try {
            org.json.JSONObject body = new org.json.JSONObject();
            body.put("phone", phone);

            apiClient.post("/api/auth/sms/send", body.toString(),
                new com.google.gson.reflect.TypeToken<com.zhuoyi.sdk.model.ApiResponse<Object>>(){}.getType(),
                callback);

        } catch (Exception e) {
            callback.onFailure(-3, "发送验证码请求失败: " + e.getMessage());
        }
    }

    /** 统一处理登录响应（提取 token/user 并保存会话） */
    private void handleLoginResponse(Object data,
                                     com.zhuoyi.sdk.callback.ZhuoyiCallback<Object> callback) {
        try {
            org.json.JSONObject result;
            if (data instanceof org.json.JSONObject) {
                result = (org.json.JSONObject) data;
            } else {
                result = new org.json.JSONObject(data.toString());
            }

            String token = result.optString("token", "");
            org.json.JSONObject user = result.optJSONObject("user");

            String userId = "";
            String userName = "";
            String role = "user";
            String phone = "";

            if (user != null) {
                userId = user.optString("id", "");
                userName = user.optString("nickname", "");
                role = user.optString("role", "user");
                phone = user.optString("phone", "");
            }

            saveSession(token, userId, userName.isEmpty() ? phone : userName, role);

            if (apiClient != null && !token.isEmpty()) {
                apiClient.setAuthToken(token);
            }

            callback.onSuccess(data);
        } catch (Exception e) {
            callback.onFailure(-4, "登录响应解析失败: " + e.getMessage());
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
