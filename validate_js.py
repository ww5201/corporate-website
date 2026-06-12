import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Extract JS from HTML and validate with Node.js
cmd = """node -e "
const fs = require('fs');
const html = fs.readFileSync('/var/www/frontend/index.html', 'utf8');
const start = html.indexOf('<script>') + 8;
const end = html.lastIndexOf('</script>');
const js = html.substring(start, end);
try {
    new Function(js);
    console.log('JS syntax OK, length:', js.length);
} catch(e) {
    console.log('JS ERROR:', e.message);
    // Find approximate line
    const lines = js.split('\\n');
    console.log('Total lines:', lines.length);
}
" """

stdin, stdout, stderr = ssh.exec_command(cmd)
result = stdout.read().decode()
errors = stderr.read().decode()

with open('D:/tokai/js_validate.txt', 'w', encoding='utf-8') as f:
    f.write(f"Result: {result}\n")
    f.write(f"Errors: {errors}\n")

ssh.close()
print("Done")
