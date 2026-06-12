import os

PROJECT_DIR = r"C:\Users\w\Desktop\ZhuoYiApp"

# app/build.gradle - 使用 compileSdk 36 但指定 buildToolsVersion
app_gradle = os.path.join(PROJECT_DIR, "app", "build.gradle")
with open(app_gradle, "w", encoding="utf-8") as f:
    f.write("""apply plugin: 'com.android.application'

android {
    namespace 'com.zhuoyi.custom'
    compileSdk 36
    buildToolsVersion "35.0.0"
    
    defaultConfig {
        applicationId "com.zhuoyi.custom"
        minSdk 24
        targetSdk 36
        versionCode 1
        versionName "1.0"
    }
    
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
}
""")
print(f"已更新 {app_gradle}")

# 同时更新 local.properties 确保 SDK 路径正确
local_props = os.path.join(PROJECT_DIR, "local.properties")
with open(local_props, "w", encoding="utf-8") as f:
    f.write("sdk.dir=D:\\\\Android\\\\Sdk\n")
print(f"已更新 {local_props}")
