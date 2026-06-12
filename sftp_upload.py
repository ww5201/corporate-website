import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Read local fixed file
with open(r'D:/tokai/index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Local size: {len(html)}")

# Upload via SFTP
sftp = ssh.open_sftp()
# First backup
try:
    sftp.rename('/var/www/frontend/index.html', '/var/www/frontend/index.html.bak2')
except:
    pass

# Write new file
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)

# Verify
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode().strip()

stdin, stdout, stderr = ssh.exec_command('''node -e "const fs=require('fs');const h=fs.readFileSync('/var/www/frontend/index.html','utf8');const s=h.indexOf('<script>')+8;const e=h.lastIndexOf('</script>');const j=h.substring(s,e);try{new Function(j);console.log('JS:OK');}catch(err){console.log('JS:ERR:'+err.message);}"''')
js = stdout.read().decode().strip()

sftp.close()
ssh.close()

print(f"Remote size: {size}")
print(f"JS: {js}")
