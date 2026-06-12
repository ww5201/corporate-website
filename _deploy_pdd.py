import paramiko
import os
import time

host = '8.138.218.146'
user = 'root'
pwd = 'ww0987654.'

print('>>> Connecting to server...')
transport = paramiko.Transport((host, 22))
transport.connect(username=user, password=pwd)
sftp = paramiko.SFTPClient.from_transport(transport)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pwd)

# Clear frontend dir
print('>>> Clearing /var/www/frontend/')
stdin, stdout, stderr = ssh.exec_command('rm -rf /var/www/frontend/*')
stdout.read()
time.sleep(0.5)

# Upload dist files
local_dist = r'D:\tokai\dist'
remote_dirs = set()
files_to_upload = []
for root, dirs, files in os.walk(local_dist):
    for f in files:
        local_path = os.path.join(root, f)
        rel = os.path.relpath(local_path, local_dist).replace(os.sep, '/')
        remote_path = f'/var/www/frontend/{rel}'
        remote_dir = os.path.dirname(remote_path).replace(os.sep, '/')
        remote_dirs.add(remote_dir)
        files_to_upload.append((local_path, remote_path))

# Create directories
for d in sorted(remote_dirs):
    try: sftp.mkdir(d)
    except: pass

# Upload files
for local_path, remote_path in files_to_upload:
    size = os.path.getsize(local_path)
    print(f'>>> {os.path.basename(local_path)} ({size} bytes) -> {remote_path}')
    sftp.put(local_path, remote_path)

# Restart nginx
print('>>> Restarting nginx...')
stdin, stdout, stderr = ssh.exec_command('systemctl restart nginx')
stdout.read()
err = stderr.read().decode()
if err: print(f'nginx: {err}')

# Verify
stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost/')
code = stdout.read().decode().strip()
print(f'>>> Server status: {code}')

sftp.close()
transport.close()
ssh.close()
print('>>> Done!')
