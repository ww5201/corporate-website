import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

idx = html.find('function handleWechatClick')
func_text = html[idx:idx+300]
print("Current server function:")
print(func_text)

# Replace with simple weixin:// approach
# Find exact function boundaries
func_start = html.find('function handleWechatClick')
# Find the } that closes this function - look for the pattern after weixin:// call
# The new function should be minimal
new_func = "function handleWechatClick() {\n    window.location.href = 'weixin://';\n}"

# Find where current function ends
after_func = html.find('\n    }\n\n    // =====', func_start)
if after_func < 0:
    after_func = html.find('\n    }\n  </script>', func_start)

old_func = html[func_start:after_func]
html = html[:func_start] + new_func + html[after_func:]

print(f"\nOld: {len(old_func)} chars -> New: {len(new_func)} chars")

# Upload
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
cmd = "echo '" + encoded + "' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()
ssh.exec_command('nginx -s reload')

with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

ssh.close()
print("\nDone: weixin:// approach deployed!")
