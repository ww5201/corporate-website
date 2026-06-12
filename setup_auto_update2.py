import paramiko, base64, time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. Read current server-v4.js
sftp = ssh.open_sftp()
with sftp.open('/root/backend/server-v4.js', 'r') as f:
    js = f.read().decode('utf-8')
sftp.close()

# 2. Add /api/app-version endpoint
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
    js = js.replace("app.listen(PORT", version_code + "\napp.listen(PORT")
    
    encoded = base64.b64encode(js.encode('utf-8')).decode('ascii')
    cmd = f"echo '{encoded}' | base64 -d > /root/backend/server-v4.js"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()
    print("Added /api/app-version endpoint")
else:
    print("Endpoint already exists")

# 3. Create APK directory
stdin, stdout, stderr = ssh.exec_command('mkdir -p /var/www/frontend/apk')
stdout.read()

# 4. Add APK serving to nginx
sftp = ssh.open_sftp()
with sftp.open('/etc/nginx/conf.d/site.conf', 'r') as f:
    conf = f.read().decode('utf-8')
sftp.close()

if '/apk/' not in conf:
    apk_location = """
    # APK下载
    location /apk/ {
        alias /var/www/frontend/apk/;
        autoindex off;
    }
"""
    # Insert before the last closing brace of the server block
    last_brace = conf.rfind('}')
    conf = conf[:last_brace] + apk_location + conf[last_brace:]
    
    encoded = base64.b64encode(conf.encode('utf-8')).decode('ascii')
    cmd = f"echo '{encoded}' | base64 -d > /etc/nginx/conf.d/site.conf"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()
    print("Added APK nginx location")
else:
    print("APK nginx location already exists")

# 5. Test and reload nginx
stdin, stdout, stderr = ssh.exec_command('nginx -t 2>&1 && nginx -s reload')
result = stderr.read().decode()
print(f"Nginx: {result}")

# 6. Restart backend
stdin, stdout, stderr = ssh.exec_command('systemctl restart zhuoyi-backend')
stdout.read()
time.sleep(2)

# 7. Verify version API
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:3000/api/app-version')
ver = stdout.read().decode()
print(f"Version API: {ver}")

ssh.close()
