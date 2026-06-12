import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

for f in ['security.conf', 'site.conf', 'site.conf.bak', 'upload.conf']:
    i, o, e = ssh.exec_command(f'cat /etc/nginx/conf.d/{f}', timeout=10)
    out = o.read().decode('utf-8', 'replace').strip()
    print(f'=== {f} ===')
    if out: print(out)
    print()

ssh.close()
