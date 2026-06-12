import paramiko, base64, os

# Upload APK to server
apk_path = r'C:\Users\w\Desktop\ZhuoYiApp\app\build\outputs\apk\debug\app-debug.apk'

with open(apk_path, 'rb') as f:
    apk_data = f.read()

print(f"APK size: {len(apk_data)} bytes")

# Upload via base64 in chunks
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Clear remote file first
stdin, stdout, stderr = ssh.exec_command('> /var/www/frontend/apk/zhuoyi-latest.apk')
stdout.read()

# Upload in 1MB chunks
chunk_size = 700000  # base64 safe chunk
for i in range(0, len(apk_data), chunk_size):
    chunk = apk_data[i:i+chunk_size]
    encoded = base64.b64encode(chunk).decode('ascii')
    cmd = f"echo '{encoded}' | base64 -d >> /var/www/frontend/apk/zhuoyi-latest.apk"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()
    print(f"  Uploaded chunk {i//chunk_size + 1}")

# Verify file size
stdin, stdout, stderr = ssh.exec_command('stat -c %s /var/www/frontend/apk/zhuoyi-latest.apk')
remote_size = stdout.read().decode().strip()
print(f"Remote APK size: {remote_size} (local: {len(apk_data)})")

if int(remote_size) == len(apk_data):
    print("APK uploaded successfully!")
else:
    print("WARNING: Size mismatch!")

# Test download URL
stdin, stdout, stderr = ssh.exec_command('curl -sI http://127.0.0.1/apk/zhuoyi-latest.apk | head -5')
headers = stdout.read().decode()
print(f"Download headers:\n{headers}")

ssh.close()
