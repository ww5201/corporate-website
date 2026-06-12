import os
import shutil

PROJECT_DIR = r"C:\Users\w\Desktop\ZhuoYiApp"

# 清理缓存
for d in ["build", ".gradle", "app/build"]:
    path = os.path.join(PROJECT_DIR, d)
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Cleaned: {d}")

# 用 compileSdk 36 + buildTools 37.0.0（最新，修复了 AAPT2 bug）
app_gradle = os.path.join(PROJECT_DIR, "app", "build.gradle")
with open(app_gradle, "w", encoding="utf-8") as f:
    f.write("""plugins {
    id 'com.android.application'
}

android {
    namespace 'com.zhuoyi.custom'
    compileSdk 36
    buildToolsVersion "37.0.0"
    
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
print("Updated app/build.gradle -> buildTools 37.0.0")

# 根 build.gradle
root_gradle = os.path.join(PROJECT_DIR, "build.gradle")
with open(root_gradle, "w", encoding="utf-8") as f:
    f.write("""plugins {
    id 'com.android.application' version '8.0.2' apply false
}
""")
print("Updated root build.gradle")

# settings.gradle
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
print("Updated settings.gradle")

# gradle-wrapper.properties
wrapper = os.path.join(PROJECT_DIR, "gradle", "wrapper", "gradle-wrapper.properties")
with open(wrapper, "w", encoding="utf-8") as f:
    f.write("""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://mirrors.cloud.tencent.com/gradle/gradle-8.0-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")
print("Updated gradle-wrapper.properties -> Gradle 8.0")

# gradle.properties
props = os.path.join(PROJECT_DIR, "gradle.properties")
with open(props, "w", encoding="utf-8") as f:
    f.write("""android.useAndroidX=false
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.nonTransitiveRClass=true
""")
print("Updated gradle.properties")

# local.properties
lp = os.path.join(PROJECT_DIR, "local.properties")
with open(lp, "w", encoding="utf-8") as f:
    f.write("sdk.dir=D:\\\\Android\\\\Sdk\n")
print("Updated local.properties")

print("\nDone! All files updated. Use build-tools 37.0.0 + compileSdk 36")
