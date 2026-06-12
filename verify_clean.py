import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check nav
stdin, stdout, stderr = ssh.exec_command("sed -n '/<nav/,/<\\/nav>/p' /var/www/frontend/index.html | head -35")
nav = stdout.read().decode('utf-8')

# Check JS
stdin, stdout, stderr = ssh.exec_command('''node -e "const fs=require('fs');const h=fs.readFileSync('/var/www/frontend/index.html','utf8');const s=h.indexOf('<script>')+8;const e=h.lastIndexOf('</script>');const j=h.substring(s,e);try{new Function(j);console.log('JS:OK');}catch(err){console.log('JS:ERR:'+err.message);}"''')
js = stdout.read().decode('utf-8').strip()

# Check file size
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode('utf-8').strip()

ssh.close()

with open('D:/tokai/clean_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"Size: {size}\n")
    f.write(f"JS: {js}\n\n")
    f.write(f"NAV:\n{nav}\n")

print("Done - see D:/tokai/clean_result.txt")
