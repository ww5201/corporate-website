import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

cmds = [
    'find /root/backend -name "*.js" -path "*/assets/*" 2>/dev/null',
    'find /root/backend -name "*.css" -path "*/assets/*" 2>/dev/null',
    'find /root -maxdepth 4 -name "index-CVahQ6Nl*" 2>/dev/null',
    'find /root -maxdepth 4 -name "index-BgVLAb6w*" 2>/dev/null',
    'ls -la /root/backend/frontend/ 2>/dev/null',
    'find /var/www -name "index-*" 2>/dev/null',
    'find /root -maxdepth 3 -name "dist" -type d 2>/dev/null',
]
for cmd in cmds:
    i, o, e = ssh.exec_command(cmd, timeout=10)
    out = o.read().decode('utf-8', 'replace').strip()
    if out:
        print(f'>>> {cmd}')
        print(out)
        print()
ssh.close()
