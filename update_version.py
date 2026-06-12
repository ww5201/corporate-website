import paramiko, base64

apk_path = r'C:\Users\w\Desktop\ZhuoYiApp\app\build\outputs\apk\debug\app-debug.apk'

with open(apk_path, 'rb') as f:
    apk_data = f.read()

print(f"APK size: {len(apk_data)} bytes")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Upload APK
stdin, stdout, stderr = ssh.exec_command('> /var/www/frontend/apk/zhuoyi-latest.apk')
stdout.read()

chunk_size = 700000
for i in range(0, len(apk_data), chunk_size):
    chunk = apk_data[i:i+chunk_size]
    encoded = base64.b64encode(chunk).decode('ascii')
    cmd = f"echo '{encoded}' | base64 -d >> /var/www/frontend/apk/zhuoyi-latest.apk"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()

# Verify
stdin, stdout, stderr = ssh.exec_command('stat -c %s /var/www/frontend/apk/zhuoyi-latest.apk')
remote_size = stdout.read().decode().strip()
print(f"Remote: {remote_size} (local: {len(apk_data)})")

# Update version API - bump versionCode to 3
sftp = ssh.open_sftp()
with sftp.open('/root/backend/server-v4.js', 'r') as f:
    js = f.read().decode('utf-8')
sftp.close()

# Update version info
js = js.replace('versionCode: 2', 'versionCode: 3')
js = js.replace("versionName: '1.1.0'", "versionName: '1.2.0'")
js = js.replace("updateMessage: '修复微信跳转和电话拨号功能'", "updateMessage: '微信自动复制号码+咨询按钮修复+云更新'")

encoded = base64.b64encode(js.encode('utf-8')).decode('ascii')
cmd = f"echo '{encoded}' | base64 -d > /root/backend/server-v4.js"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()

# Restart backend
import time
stdin, stdout, stderr = ssh.exec_command('systemctl restart zhuoyi-backend')
stdout.read()
time.sleep(2)

# Verify
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:3000/api/app-version')
ver = stdout.read().decode()
print(f"Version API: {ver}")

ssh.close()
print("Done!")
