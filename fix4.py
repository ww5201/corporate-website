import os
import shutil

PROJECT_DIR = r"C:\Users\w\Desktop\ZhuoYiApp"

# 删掉 build 和 .gradle 缓存
for d in ["build", ".gradle", "app/build"]:
    path = os.path.join(PROJECT_DIR, d)
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"已删除: {d}")

# 使用 compileSdk 35 + buildTools 35.0.0
app_gradle = os.path.join(PROJECT_DIR, "app", "build.gradle")
with open(app_gradle, "w", encoding="utf-8") as f:
    f.write("""plugins {
    id 'com.android.application'
}

android {
    namespace 'com.zhuoyi.custom'
    compileSdk 35
    buildToolsVersion "35.0.0"
    
    defaultConfig {
        applicationId "com.zhuoyi.custom"
        minSdk 24
        targetSdk 35
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

# 更新根 build.gradle 使用 plugins DSL
root_gradle = os.path.join(PROJECT_DIR, "build.gradle")
with open(root_gradle, "w", encoding="utf-8") as f:
    f.write("""plugins {
    id 'com.android.application' version '8.0.2' apply false
}
""")
print(f"已更新 {root_gradle}")

# 更新 settings.gradle
settings = os.path.join(PROJECT_DIR, "settings.gradle")
with open(settings, "w", encoding="utf-8") as f:
    f.write("""pluginManagement {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/google' }
        maven { url 'https://maven.aliyun.com/repository/central' }
        maven { url 'https://maven.aliyun.com/repository/public' }
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        maven { url 'https://maven.aliyun.com/repository/google' }
        maven { url 'https://maven.aliyun.com/repository/central' }
        maven { url 'https://maven.aliyun.com/repository/public' }
        google()
        mavenCentral()
    }
}

rootProject.name = "ZhuoYiApp"
include ':app'
""")
print(f"已更新 {settings}")

# 检查 android-35 是否存在
android35 = r"D:\Android\Sdk\platforms\android-35"
if os.path.exists(android35):
    print(f"\n✅ android-35 已存在: {android35}")
else:
    print(f"\n❌ android-35 不存在，需要安装")
    # 检查 android-36.1
    android361 = r"D:\Android\Sdk\platforms\android-36.1"
    if os.path.exists(android361):
        print(f"发现 android-36.1: {android361}")
        # 尝试用 android-36.1
        with open(app_gradle, "w", encoding="utf-8") as f:
            f.write("""plugins {
    id 'com.android.application'
}

android {
    namespace 'com.zhuoyi.custom'
    compileSdk "android-36.1"
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
        print(f"已改用 android-36.1")

print("\n完成！请在 Android Studio 中重新同步并构建")
