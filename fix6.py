import os
import shutil

PROJECT_DIR = r"C:\Users\w\Desktop\ZhuoYiApp"

# 清理缓存
for d in ["build", ".gradle", "app/build"]:
    path = os.path.join(PROJECT_DIR, d)
    if os.path.exists(path):
        shutil.rmtree(path)

# 用 compileSdk 35 + buildTools 35.0.0
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
print("Updated: compileSdk 35 + buildTools 35.0.0")

# 修改 source.properties 让 android-35 识别为 API 35
src_props = r"D:\Android\Sdk\platforms\android-35\source.properties"
if os.path.exists(src_props):
    with open(src_props, "w", encoding="utf-8") as f:
        f.write("Pkg.Desc=Android SDK Platform 35\nPkg.UserSrc=false\nPkg.Revision=1\nAndroidVersion.ApiLevel=35\nLayoutlib.Api=15\nLayoutlib.Revision=1\nPlatform.MinToolsRev=22\n")
    print("Updated source.properties for API 35")

# 修改 package.xml
pkg_xml = r"D:\Android\Sdk\platforms\android-35\package.xml"
if os.path.exists(pkg_xml):
    with open(pkg_xml, "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ns2:repository xmlns:ns2="http://schemas.android.com/repository/android/common/02" xmlns:ns3="http://schemas.android.com/sdk/android/repo/addon2/02" xmlns:ns4="http://schemas.android.com/sdk/android/repo/sys-img2/02">
    <localPackage path="platforms;android-35">
        <type-details xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="ns2:platformDetailsType">
            <api-level>35</api-level>
            <codename></codename>
            <layoutlib api="15"/>
        </type-details>
        <revision><major>1</major></revision>
        <display-name>Android SDK Platform 35</display-name>
    </localPackage>
</ns2:repository>
""")
    print("Updated package.xml for API 35")

# build.prop
build_prop = r"D:\Android\Sdk\platforms\android-35\build.prop"
if os.path.exists(build_prop):
    with open(build_prop, "w", encoding="utf-8") as f:
        f.write("ro.build.version.sdk=35\nro.build.version.codename=REL\n")
    print("Updated build.prop")

print("\nDone! android-35 SDK configured as API 35")
