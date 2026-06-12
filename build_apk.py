import subprocess
import os

env = os.environ.copy()
env["JAVA_HOME"] = r"D:\Android\as\jbr"
env["PATH"] = r"D:\Android\as\jbr\bin;" + env.get("PATH", "")

result = subprocess.run(
    [r"C:\Users\w\Desktop\ZhuoYiApp\gradlew.bat", "-p", r"C:\Users\w\Desktop\ZhuoYiApp", "assembleDebug", 
     "-Dorg.gradle.jvmargs=-Xmx1024m"],
    cwd=r"C:\Users\w\Desktop\ZhuoYiApp",
    env=env,
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace"
)

print("STDOUT:")
print(result.stdout[-3000:] if len(result.stdout) > 3000 else result.stdout)
print("\nSTDERR:")
print(result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr)
print(f"\nReturn code: {result.returncode}")
