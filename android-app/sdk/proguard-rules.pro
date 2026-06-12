# Zhuoyi SDK ProGuard Rules
# 卓翌定制 SDK 混淆规则

-keep public class com.zhuoyi.sdk.** { *; }
-keep public interface com.zhuoyi.sdk.** { *; }
-keepclassmembers class com.zhuoyi.sdk.** {
    public *** (...);
}

# 保持模型类
-keep class com.zhuoyi.sdk.model.** { *; }

# 保持回调接口
-keep interface com.zhuoyi.sdk.callback.** { *; }

# Gson 序列化
-keepattributes Signature
-keepattributes *Annotation*
-dontwarn com.google.gson.**
-keep class com.google.gson.** { *; }
-keep class sun.misc.Unsafe { *; }
-keep class com.google.gson.stream.** { *; }
-keep class com.zhuoyi.sdk.model.** { *; }

# OkHttp
-dontwarn okhttp3.**
-keep class okhttp3.** { *; }
-keep interface okhttp3.** { *; }

# WebKit
-keep class android.webkit.** { *; }
