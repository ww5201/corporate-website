import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check refs
stdin, stdout, stderr = ssh.exec_command("grep -n 'settings' /var/www/frontend/index.html | head -10")
refs = stdout.read().decode('utf-8')

# Size
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode('utf-8').strip()

# JS
stdin, stdout, stderr = ssh.exec_command("node -e \"const fs=require('fs');const h=fs.readFileSync('/var/www/frontend/index.html','utf8');const s=h.indexOf('<script>')+8;const e=h.lastIndexOf('</script>');const j=h.substring(s,e);try{new Function(j);console.log('OK');}catch(err){console.log('ERR:'+err.message);}\"")
js = stdout.read().decode('utf-8').strip()

ssh.close()

print(f"Size: {size}")
print(f"JS: {js}")
print(f"\nSettings refs:\n{refs}")
