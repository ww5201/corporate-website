import paramiko
import os
import time

host = '8.138.218.146'
user = 'root'
pwd = 'ww0987654.'

transport = paramiko.Transport((host, 22))
transport.connect(username=user, password=pwd)
sftp = paramiko.SFTPClient.from_transport(transport)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pwd)

# 清空前端目录
print('>>> 清空 /var/www/frontend/')
stdin, stdout, stderr = ssh.exec_command('rm -rf /var/www/frontend/*')
stdout.read()
time.sleep(0.5)

# 收集所有需要创建的目录
local_dist = r'D:\tokai\dist'
remote_dirs = set()
files_to_upload = []
for root, dirs, files in os.walk(local_dist):
    for f in files:
        local_path = os.path.join(root, f)
        rel = os.path.relpath(local_path, local_dist).replace(os.sep, '/')
        remote_path = f'/var/www/frontend/{rel}'
        remote_dir = os.path.dirname(remote_path)
        remote_dirs.add(remote_dir)
        files_to_upload.append((local_path, remote_path))

# 先创建所有目录
for d in sorted(remote_dirs):
    ssh.exec_command(f'mkdir -p {d}')
    time.sleep(0.1)

time.sleep(0.5)

# 上传文件
for local_path, remote_path in files_to_upload:
    rel = os.path.relpath(local_path, local_dist).replace(os.sep, '/')
    print(f'  上传: {rel}')
    sftp.put(local_path, remote_path)

# 重载nginx
print('>>> 重载nginx')
stdin, stdout, stderr = ssh.exec_command('nginx -t && systemctl reload nginx')
print(stdout.read().decode())
print(stderr.read().decode())

sftp.close()
ssh.close()
print('[OK] deploy done!')
