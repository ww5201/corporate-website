import os

PROJECT_DIR = r"C:\Users\w\Desktop\ZhuoYiApp"

# 简化根 build.gradle - 去掉 allprojects repos（交给 settings.gradle 管）
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

task clean(type: Delete) {
    delete rootProject.buildDir
}
""")
print(f"已更新 {root_gradle}")
print("内容:")
with open(root_gradle) as f:
    print(f.read())
