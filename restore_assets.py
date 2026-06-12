import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

cmds = [
    'mkdir -p /root/backend/frontend/assets',
    'cp /root/backend/dist/assets/index-CVahQ6Nl.js /root/backend/frontend/assets/',
    'cp /root/backend/dist/assets/index-BgVLAb6w.css /root/backend/frontend/assets/',
    'ls -la /root/backend/frontend/assets/',
    'ls -la /root/backend/frontend/',
]
for cmd in cmds:
    print(f'>>> {cmd}')
    i, o, e = ssh.exec_command(cmd, timeout=10)
    out = o.read().decode('utf-8', 'replace').strip()
    err = e.read().decode('utf-8', 'replace').strip()
    if out: print(out)
    if err: print(f'ERR: {err}')
    print()

ssh.close()
print('Done!')
