import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('8.138.218.146', 22, 'root', 'ww0987654.', timeout=10)

cmds = [
    'echo "=== Check git ==="',
    'which git',
    'echo "=== Check existing repos ==="',
    'ls -la /root/backend/.git 2>/dev/null || echo "no backend git"',
    'ls -la /var/www/frontend/.git 2>/dev/null || echo "no frontend git"',
    'echo "=== Check for remote repos ==="',
    'find /root -name "*.git" -o -name "*.git" -type d 2>/dev/null | head -5',
    'echo "=== Check github/ssh config ==="',
    'cat /root/.ssh/config 2>/dev/null || echo "no ssh config"',
    'ls /root/.ssh/ 2>/dev/null',
    'echo "=== Check git global config ==="',
    'git config --global user.name 2>/dev/null || echo "no git user"',
    'git config --global user.email 2>/dev/null || echo "no git email"',
]

stdin, stdout, stderr = client.exec_command(' && '.join(cmds))
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print(out)
if err: print('STDERR:', err)
client.close()
