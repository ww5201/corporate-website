import os
import shutil

PROJECT_DIR = r"C:\Users\w\Desktop\ZhuoYiApp"

# 清理缓存
for d in ["build", ".gradle", "app/build"]:
    path = os.path.join(PROJECT_DIR, d)
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Cleaned: {d}")

# 1. gradle-wrapper.properties -> Gradle 8.11.1
wrapper = os.path.join(PROJECT_DIR, "gradle", "wrapper", "gradle-wrapper.properties")
with open(wrapper, "w", encoding="utf-8") as f:
    f.write("""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://mirrors.cloud.tencent.com/gradle/gradle-8.11.1-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")
print("OK: gradle-wrapper.properties -> Gradle 8.11.1")

# 2. settings.gradle - Aliyun mirrors
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
print("OK: settings.gradle")

# 3. root build.gradle - AGP 8.7.3
root_gradle = os.path.join(PROJECT_DIR, "build.gradle")
with open(root_gradle, "w", encoding="utf-8") as f:
    f.write("""plugins {
    id 'com.android.application' version '8.7.3' apply false
}
""")
print("OK: root build.gradle -> AGP 8.7.3")

# 4. app/build.gradle
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
print("OK: app/build.gradle")

# 5. gradle.properties
props = os.path.join(PROJECT_DIR, "gradle.properties")
with open(props, "w", encoding="utf-8") as f:
    f.write("""android.useAndroidX=false
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.nonTransitiveRClass=true
""")
print("OK: gradle.properties")

print("\nDone! Upgraded to AGP 8.7.3 + Gradle 8.11.1")
