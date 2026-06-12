import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Find and replace handleWechatClick
idx = html.find('function handleWechatClick')
end = html.find('\n    }\n\n    // ===== 启动', idx)
if end < 0:
    # Try alternative end marker
    end = html.find('\n    }\n\n    // =====', idx)
if end < 0:
    end = html.find('\n    }\n  </script>', idx)

print(f"Function from {idx} to {end}")

old_func = html[idx:end]
new_func = """function handleWechatClick() {
    // Open WeChat app
    window.location.href = 'weixin://';"""

html = html[:idx] + new_func + html[end:]
print(f"Replaced ({len(old_func)} -> {len(new_func)})")

# Upload
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
cmd = "echo '" + encoded + "' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()
ssh.exec_command('nginx -s reload')

with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"File: {len(html)} chars, weixin://: {'weixin://' in html}")

# Also update APK MainActivity.java
ssh.exec_command('nginx -s reload 2>/dev/null; echo done')

ssh.close()
print("Website updated!")
