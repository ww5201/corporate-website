import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Get the nav section
stdin, stdout, stderr = ssh.exec_command("sed -n '/<nav/,/<\\/nav>/p' /var/www/frontend/index.html | head -50")
nav_html = stdout.read().decode('utf-8')

# Check JS
stdin, stdout, stderr = ssh.exec_command('''node -e "
const fs = require('fs');
const html = fs.readFileSync('/var/www/frontend/index.html', 'utf8');
const s = html.indexOf('<script>') + 8;
const e = html.lastIndexOf('</script>');
const js = html.substring(s, e);
try { new Function(js); console.log('JS:OK'); } catch(err) { console.log('JS:ERR:' + err.message); }
"''')
js_status = stdout.read().decode('utf-8').strip()

# Check file size
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
file_size = stdout.read().decode('utf-8').strip()

ssh.close()

# Write result
with open('D:/tokai/nav_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"File: {file_size}\n")
    f.write(f"JS: {js_status}\n\n")
    f.write(f"NAV HTML:\n{nav_html}\n")

print("Check D:/tokai/nav_check.txt")
