import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Read current server-v4.js
sftp = ssh.open_sftp()
with sftp.open('/root/backend/server-v4.js', 'r') as f:
    js = f.read().decode('utf-8')
sftp.close()

# Add /api/app-version endpoint if not exists
if '/api/app-version' not in js:
    version_code = """
    
    // ===== APK版本检查 =====
    app.get('/api/app-version', (req, res) => {
      res.json({
        versionCode: 2,
        versionName: '1.1.0',
        updateMessage: '修复微信跳转和电话拨号功能',
        downloadUrl: 'http://8.138.218.146/apk/zhuoyi-latest.apk',
        forceUpdate: false
      });
    });
"""
    # Insert before the last app.listen
    js = js.replace("app.listen(PORT", version_code + "\napp.listen(PORT")
    
    with sftp.open('/root/backend/server-v4.js', 'w') as f:
        f.write(js.encode('utf-8'))
    print("Added /api/app-version endpoint")
else:
    print("Endpoint already exists")

# Create APK directory and set up nginx to serve it
cmds = [
    'mkdir -p /var/www/frontend/apk',
    # Copy current APK to server (we'll do this via Python)
    # Add nginx location for APK files
]

for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()

# Add APK serving location to nginx config
with sftp.open('/etc/nginx/conf.d/site.conf', 'r') as f:
    conf = f.read().decode('utf-8')

if '/apk/' not in conf:
    # Add APK location before the closing brace
    apk_location = """
    # APK下载
    location /apk/ {
        alias /var/www/frontend/apk/;
        autoindex off;
        add_header Content-Disposition 'attachment';
    }
"""
    conf = conf.replace("}", apk_location + "\n}", 1)
    with sftp.open('/etc/nginx/conf.d/site.conf', 'w') as f:
        f.write(conf.encode('utf-8'))
    print("Added APK nginx location")
else:
    print("APK nginx location already exists")

# Reload nginx
stdin, stdout, stderr = ssh.exec_command('nginx -t && nginx -s reload')
nginx_result = stdout.read().decode()
nginx_err = stderr.read().decode()
print(f"Nginx: {nginx_err}")

# Restart backend
stdin, stdout, stderr = ssh.exec_command('systemctl restart zhuoyi-backend')
stdout.read()
import time
time.sleep(2)
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:3000/api/app-version')
ver_result = stdout.read().decode()
print(f"Version API: {ver_result}")

sftp.close()
ssh.close()
