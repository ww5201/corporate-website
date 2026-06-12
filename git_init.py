import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('8.138.218.146', 22, 'root', 'ww0987654.', timeout=10)

# Git config
cmds = [
    'git config --global user.name "Tokai Admin"',
    'git config --global user.email "admin@tokai.com"',
]
for cmd in cmds:
    stdin, stdout, stderr = client.exec_command(cmd)
    stdout.read()

# Backend repo
print("=== Init backend repo ===")
backend_cmds = [
    'cd /root/backend && git init',
    'cd /root/backend && echo "node_modules/\n*.log\nuploads/\n.env\n.DS_Store" > .gitignore',
    'cd /root/backend && git add -A',
    'cd /root/backend && git commit -m "feat: admin.html with online chat tab + server-v4.js backend"',
    'cd /root/backend && git log --oneline',
]
for cmd in backend_cmds:
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out: print(out)
    if err and 'warning' not in err.lower(): print('  ERR:', err)

# Frontend repo
print("\n=== Init frontend repo ===")
frontend_cmds = [
    'cd /var/www/frontend && git init',
    'cd /var/www/frontend && echo "uploads/\n*.log\n.DS_Store" > .gitignore',
    'cd /var/www/frontend && git add -A',
    'cd /var/www/frontend && git commit -m "feat: frontend with chat.html, admin.html (online chat), index.html"',
    'cd /var/www/frontend && git log --oneline',
]
for cmd in frontend_cmds:
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out: print(out)
    if err and 'warning' not in err.lower(): print('  ERR:', err)

# Status
print("\n=== Backend status ===")
stdin, stdout, stderr = client.exec_command('cd /root/backend && git status --short')
print(stdout.read().decode('utf-8', errors='replace').strip() or "(clean)")

print("\n=== Frontend status ===")
stdin, stdout, stderr = client.exec_command('cd /var/www/frontend && git status --short')
print(stdout.read().decode('utf-8', errors='replace').strip() or "(clean)")

print("\nDone!")
client.close()
