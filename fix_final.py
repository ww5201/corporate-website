import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

dup_start = html.find('DOCTYPE html>', 100)
clean = html[:dup_start].rstrip()

if not clean.endswith('</html>'):
    clean += '\n</script>\n</body>\n</html>'

print(f"Clean: {len(clean)} chars, reveal: {'opacity: 1 !important' in clean}, weixin: {'weixin://' in clean}")

encoded = base64.b64encode(clean.encode('utf-8')).decode('ascii')
cmd = "echo '" + encoded + "' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()

stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html && tail -3 /var/www/frontend/index.html')
print("Server:", stdout.read().decode().strip())

ssh.exec_command('nginx -s reload')

with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(clean)

ssh.close()
print("Done!")
