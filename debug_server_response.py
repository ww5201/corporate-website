import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Get headers
stdin, stdout, stderr = ssh.exec_command('curl -sI http://127.0.0.1/')
print('Headers:')
print(stdout.read().decode())

# Get body
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1/')
body = stdout.read().decode('utf-8', errors='replace')
print(f'Body size: {len(body)}')
print(f'Has <script>: {"<script>" in body}')
print(f'Has loadData: {"loadData" in body}')
print(f'Has products id: {"id=\"products\"" in body}')
print(f'Has gear icon: {"⚙" in body}')

# Also check nginx config
stdin, stdout, stderr = ssh.exec_command('cat /etc/nginx/conf.d/site.conf')
print(f'\nNginx site.conf:\n{stdout.read().decode()}')

ssh.close()
