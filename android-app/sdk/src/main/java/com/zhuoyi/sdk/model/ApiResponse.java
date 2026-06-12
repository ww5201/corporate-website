package com.zhuoyi.sdk.model;

import com.google.gson.annotations.SerializedName;

/**
 * API 统一响应模型
 */
public class ApiResponse<T> {

    @SerializedName("code")
    private int code;

    @SerializedName("message")
    private String message;

    @SerializedName("data")
    private T data;

    public int getCode() { return code; }
    public void setCode(int code) { this.code = code; }
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    public T getData() { return data; }
    public void setData(T data) { this.data = data; }

    public boolean isSuccess() { return code == 0 || code == 200 || code == 1000; }
}
