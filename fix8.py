import os
import shutil

PROJECT_DIR = r"C:\Users\w\Desktop\ZhuoYiApp"

# 清理缓存
for d in ["build", ".gradle", "app/build"]:
    path = os.path.join(PROJECT_DIR, d)
    if os.path.exists(path):
        shutil.rmtree(path)

# 用 compileSdk 36 + buildTools 36.0.0（原始SDK）
app_gradle = os.path.join(PROJECT_DIR, "app", "build.gradle")
with open(app_gradle, "w", encoding="utf-8") as f:
    f.write("""plugins {
    id 'com.android.application'
}

android {
    namespace 'com.zhuoyi.custom'
    compileSdk 36
    buildToolsVersion "36.0.0"
    
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
print("Updated: compileSdk 36 + buildTools 36.0.0")
