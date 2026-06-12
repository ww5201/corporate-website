import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Extract first copy (before duplicate)
second_head = html.find('<head>', 50)
clean = html[:second_head]

print(f"Clean: {len(clean)} chars, has weixin://: {'weixin://' in clean}, .reveal fixed: {'opacity: 1 !important' in clean}")

# Write via exec (base64 encode to avoid issues)
import base64
encoded = base64.b64encode(clean.encode('utf-8')).decode('ascii')
print(f"Base64 length: {len(encoded)}")

# Use heredoc approach - write base64 then decode
cmd = f'''echo '{encoded}' | base64 -d > /var/www/frontend/index.html'''
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()

# Verify
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode().strip()
print(f"Server file size: {size}")

# Reload nginx
ssh.exec_command('nginx -s reload')

# Save local
with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(clean)

ssh.close()
print("Done!")
