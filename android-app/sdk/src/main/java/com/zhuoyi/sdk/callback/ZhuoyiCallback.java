package com.zhuoyi.sdk.callback;

/**
 * 卓翌定制 SDK 回调接口
 */
public interface ZhuoyiCallback<T> {
    void onSuccess(T data);
    void onFailure(int code, String message);
}
