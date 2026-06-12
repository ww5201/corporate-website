# ProGuard rules for 卓翌定制
-keepattributes *Annotation*
-keepattributes SourceFile,LineNumberTable
-keep public class * extends java.lang.Exception

# ====== WeChat Open Platform SDK ======
-keep class com.tencent.mm.opensdk.** { *; }
-keep class com.tencent.wxop.** { *; }
-keep class com.tencent.mm.opensdk.modelmsg.WXMessage { *; }
-keep class com.tencent.mm.opensdk.modelmsg.** { *; }
-keep class com.tencent.mm.opensdk.modelbase.** { *; }
-keep class com.tencent.mm.opensdk.openapi.IWXAPI { *; }
-keep class com.tencent.mm.opensdk.openapi.WXAPIFactory { *; }
-dontwarn com.tencent.mm.opensdk.**
-dontwarn com.tencent.wxop.**

# ====== SDK Module ======
-keep class com.zhuoyi.sdk.** { *; }

# ====== App classes ======
-keep class com.zhuoyi.custom.** { *; }
