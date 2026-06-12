# 卓翌定制 Android 原生项目

> 高端家具定制平台 - Android 原生应用 & SDK

## 📦 项目结构

```
android-app/
├── sdk/              # 🔹 原生 SDK (AAR 库)
│   ├── src/main/java/com/zhuoyi/sdk/
│   │   ├── ZhuoyiSdk.java          # SDK 主入口
│   │   ├── api/ApiClient.java      # HTTP API 客户端
│   │   ├── auth/AuthManager.java    # 认证管理
│   │   ├── webview/WebViewWrapper.java  # WebView 封装
│   │   ├── payment/PaymentHelper.java   # 支付集成
│   │   ├── callback/               # 回调接口
│   │   └── model/                  # 数据模型
│   └── build.gradle                # library 模块
│
├── app/              # 🔹 用户端 APK (前端)
│   ├── src/main/java/com/zhuoyi/custom/
│   │   ├── SplashActivity.java     # 启动页 (2秒品牌展示)
│   │   └── MainActivity.java       # WebView 主界面
│   └── build.gradle                # application 模块
│
├── admin/            # 🔹 管理后台 APK (后端)
│   ├── src/main/java/com/zhuoyi/admin/
│   │   └── AdminMainActivity.java  # Admin WebView
│   └── build.gradle                # application 模块
│
├── settings.gradle   # 三模块配置
├── build.gradle      # 项目级配置
└── build-all.bat     # 一键构建脚本
```

## 🚀 快速开始

### 环境要求

- **JDK**: 17+ (推荐 Eclipse Temurin 17)
- **Android SDK**: platform-tools, platforms;android-34, build-tools;34.0.0
- **Gradle**: 8.2 (Wrapper 已配置)
- **minSdk**: 24 (Android 7.0)
- **targetSdk**: 34 (Android 14)

### 构建

```bash
# 方式一：一键构建脚本（推荐）
build-all.bat

# 方式二：手动 Gradle 构建
set JAVA_HOME=<你的JDK17路径>
set ANDROID_HOME=D:\android-sdk

gradlew :sdk:assembleRelease      # 编译 SDK (AAR)
gradlew :app:assembleRelease      # 编译用户端 APK
gradlew :admin:assembleRelease    # 编译管理后台 APK
```

### 构建产物

| 产物 | 路径 | 说明 |
|------|------|------|
| SDK AAR | `sdk/build/outputs/aar/sdk-release.aar` | 可被第三方 App 集成 |
| 用户端 APK | `app/build/outputs/apk/release/app-release.apk` | 客户面向 App |
| 管理后台 APK | `admin/build/outputs/apk/release/admin-release.apk` | 运营管理 App |

## 📱 功能特性

### 用户端 App (`app`)
- 品牌 Splash 启动页（2秒）
- 全屏 WebView 加载 http://8.138.218.146
- 下拉刷新 + 顶部加载进度条
- 缩放支持 + 文件选择/上传
- 外部协议处理（tel: mailto: weixin:// alipays://）
- 返回键导航历史 + 网络错误提示

### 管理后台 App (`admin`)
- 全屏 WebView 加载 http://8.138.218.146/admin
- 下拉刷新 + 进度条 + 文件上传
- WebView 调试模式 + 横竖屏自适应
- 独立图标和主题色（深蓝 #16213E）

### 原生 SDK (`sdk`)
- **ZhuoyiSdk** - 单例入口，一行初始化
- **ApiClient** - RESTful API 客户端（OkHttp 3 + Gson）
- **AuthManager** - 认证管理（登录/登出/Token持久化）
- **WebViewWrapper** - WebView 封装组件（Builder模式）
- **PaymentHelper** - 支付集成（支付宝/微信/银联）

## 🔌 SDK 集成指南

```java
// 1. 初始化
ZhuoyiSdk.init(context, "http://8.138.218.146");

// 2. API 调用
ZhuoyiSdk.getApiClient().getProducts(callback);

// 3. WebView 组件
WebViewWrapper wrapper = ZhuoyiSdk.createWebView(activity).build();
wrapper.attach(container);

// 4. 支付
PaymentHelper payment = ZhuoyiSdk.createPaymentHelper(activity);
payment.createPayment(orderId, amount, PaymentHelper.PAYMENT_ALIPAY, listener);
```

## 🏗️ 技术栈

| 组件 | 技术 |
|------|------|
| 语言 | Java 8 |
| 构建工具 | Gradle 8.2 + AGP 8.1.0 |
| HTTP | OkHttp 4.12 |
| JSON | Gson 2.10 |
| UI | Android原生 + WebView |
| 最低版本 | Android 7.0 (API 24) |
| 目标版本 | Android 14 (API 34) |

## 📝 配置说明

服务器地址可在以下位置修改：
- `app/.../MainActivity.java` → WEBSITE_URL
- `admin/.../AdminMainActivity.java` → ADMIN_URL
- SDK → ZhuoyiSdk.init(context, baseUrl) 动态传入

## 📄 License

© 2026 卓翌定制. All Rights Reserved.
