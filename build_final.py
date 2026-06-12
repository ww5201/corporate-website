import subprocess, os

env = os.environ.copy()
env['JAVA_HOME'] = r'D:\Android\as\jbr'

result = subprocess.run(
    [r'D:\Android\as\jbr\bin\java.exe', '-version'],
    capture_output=True, env=env
)
print(f"Java: {result.stderr.decode()[:80]}")

result = subprocess.run(
    [r'C:\Users\w\Desktop\ZhuoYiApp\gradlew.bat', 'assembleDebug'],
    capture_output=True, env=env,
    cwd=r'C:\Users\w\Desktop\ZhuoYiApp',
    timeout=180
)

print(f"Return: {result.returncode}")
out = result.stdout.decode('utf-8', errors='replace')
if 'BUILD' in out:
    for line in out.split('\n'):
        if 'BUILD' in line:
            print(line.strip())

err = result.stderr.decode('utf-8', errors='replace')
if err and 'WARNING' in err:
    for line in err.split('\n'):
        if 'WARNING' in line:
            print(line.strip()[:100])

# Check APK
import glob
apks = glob.glob(r'C:\Users\w\Desktop\ZhuoYiApp\app\build\outputs\apk\debug\*.apk')
for apk in apks:
    size = os.path.getsize(apk)
    print(f"APK: {apk} ({size} bytes)")
