import paramiko, base64

apk_path = r'C:\Users\w\Desktop\ZhuoYiApp\app\build\outputs\apk\debug\app-debug.apk'
with open(apk_path, 'rb') as f:
    apk_data = f.read()
print(f"APK: {len(apk_data)} bytes")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

stdin, stdout, stderr = ssh.exec_command('> /var/www/frontend/apk/zhuoyi-latest.apk')
stdout.read()
chunk_size = 700000
for i in range(0, len(apk_data), chunk_size):
    chunk = apk_data[i:i+chunk_size]
    encoded = base64.b64encode(chunk).decode('ascii')
    cmd = f"echo '{encoded}' | base64 -d >> /var/www/frontend/apk/zhuoyi-latest.apk"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()

stdin, stdout, stderr = ssh.exec_command('stat -c %s /var/www/frontend/apk/zhuoyi-latest.apk')
remote_size = stdout.read().decode().strip()
print(f"Remote: {remote_size} (match: {int(remote_size)==len(apk_data)})")

ssh.close()
print("Done!")
