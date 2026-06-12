import paramiko, base64

# Read local fixed file
with open(r'D:/tokai/index-clean.html', 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Local: {len(html)} bytes")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Delete remote file first
stdin, stdout, stderr = ssh.exec_command('rm -f /var/www/frontend/index.html')
stdout.read()

# Encode and upload in chunks
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
chunk_size = 500000  # smaller chunks for safety

for i in range(0, len(encoded), chunk_size):
    chunk = encoded[i:i+chunk_size]
    mode = '>' if i == 0 else '>>'
    cmd = f"echo '{chunk}' | base64 -d {mode} /var/www/frontend/index.html"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()

# Verify
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode().strip()

stdin, stdout, stderr = ssh.exec_command("node -e \"const fs=require('fs');const h=fs.readFileSync('/var/www/frontend/index.html','utf8');const s=h.indexOf('<script>')+8;const e=h.lastIndexOf('</script>');const j=h.substring(s,e);try{new Function(j);console.log('JS:OK,len='+j.length);}catch(err){console.log('JS:ERR:'+err.message);}\"")
js_val = stdout.read().decode().strip()

stdin, stdout, stderr = ssh.exec_command("sed -n '/<nav/,/<\\/nav>/p' /var/www/frontend/index.html | head -30")
nav = stdout.read().decode()

ssh.close()

print(f"Remote: {size}")
print(f"JS: {js_val}")
print(f"\nNAV preview:\n{nav[:1000]}")
