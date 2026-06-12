import os

PROJECT_DIR = r"C:\Users\w\Desktop\ZhuoYiApp"

# 1. 更新 gradle-wrapper.properties 用腾讯镜像
wrapper_path = os.path.join(PROJECT_DIR, "gradle", "wrapper", "gradle-wrapper.properties")
with open(wrapper_path, "w", encoding="utf-8") as f:
    f.write("""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://mirrors.cloud.tencent.com/gradle/gradle-8.0-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")
print(f"1. 已更新 {wrapper_path}")

# 2. 更新根 build.gradle 用阿里云镜像
root_gradle = os.path.join(PROJECT_DIR, "build.gradle")
with open(root_gradle, "w", encoding="utf-8") as f:
    f.write("""buildscript {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/google' }
        maven { url 'https://maven.aliyun.com/repository/central' }
        maven { url 'https://maven.aliyun.com/repository/public' }
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.0.2'
    }
}

allprojects {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/google' }
        maven { url 'https://maven.aliyun.com/repository/central' }
        maven { url 'https://maven.aliyun.com/repository/public' }
        google()
        mavenCentral()
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
""")
print(f"2. 已更新 {root_gradle}")

# 3. 更新 app/build.gradle
app_gradle = os.path.join(PROJECT_DIR, "app", "build.gradle")
with open(app_gradle, "w", encoding="utf-8") as f:
    f.write("""apply plugin: 'com.android.application'

android {
    namespace 'com.zhuoyi.custom'
    compileSdk 36
    
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
print(f"3. 已更新 {app_gradle}")

# 4. 更新 AndroidManifest.xml 去掉 package（AGP 8.0 不需要）
manifest = os.path.join(PROJECT_DIR, "app", "src", "main", "AndroidManifest.xml")
with open(manifest, "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")
print(f"4. 已更新 {manifest}")

# 5. 更新 settings.gradle
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
print(f"5. 已更新 {settings}")

# 6. 更新 gradle.properties
props = os.path.join(PROJECT_DIR, "gradle.properties")
with open(props, "w", encoding="utf-8") as f:
    f.write("""android.useAndroidX=false
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.nonTransitiveRClass=true
""")
print(f"6. 已更新 {props}")

print("\n=== 所有文件已更新为国内镜像源 ===")
print("请在 Android Studio 中点击 File → Sync Project with Gradle Files")
