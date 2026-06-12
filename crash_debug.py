import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Get the nav section
stdin, stdout, stderr = ssh.exec_command("grep -n 'nav-right\\|lang-switch\\|settings' /var/www/frontend/index.html | head -20")
nav_lines = stdout.read().decode()

# Get the full nav HTML
stdin, stdout, stderr = ssh.exec_command("sed -n '/<nav/,/<\\/nav>/p' /var/www/frontend/index.html")
nav_html = stdout.read().decode()

# Check for JS errors
stdin, stdout, stderr = ssh.exec_command('''node -e "
const fs = require('fs');
const html = fs.readFileSync('/var/www/frontend/index.html', 'utf8');
const start = html.indexOf('<script>') + 8;
const end = html.lastIndexOf('</script>');
const js = html.substring(start, end);
try {
    new Function(js);
    console.log('JS syntax: OK');
} catch(e) {
    console.log('JS ERROR:', e.message);
}
// Check for common issues
if (js.includes('undefined')) console.log('WARN: undefined in JS');
if (js.includes('null')) console.log('WARN: null in JS');
console.log('Functions:', (js.match(/function\\s+\\w+/g) || []).length);
"''')
js_check = stdout.read().decode()

with open('D:/tokai/crash_debug.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== NAV LINES ===\n{nav_lines}\n\n")
    f.write(f"=== NAV HTML ===\n{nav_html}\n\n")
    f.write(f"=== JS CHECK ===\n{js_check}\n")

ssh.close()

with open('D:/tokai/crash_debug.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    # Print in chunks to avoid encoding issues
    print(content[:3000])
    if len(content) > 3000:
        print("...")
        print(content[3000:6000])
