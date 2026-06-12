import paramiko

host = '8.138.218.146'
user = 'root'
pwd = 'ww0987654.'

transport = paramiko.Transport((host, 22))
transport.connect(username=user, password=pwd)
sftp = paramiko.SFTPClient.from_transport(transport)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=user, password=pwd)

# 上传前端文件
print('=== 上传前端文件 ===')
import os
dist_dir = r'D:\tokai\dist'

for root, dirs, files in os.walk(dist_dir):
    for f in files:
        local_path = os.path.join(root, f)
        rel_path = os.path.relpath(local_path, dist_dir)
        remote_path = '/var/www/frontend/' + rel_path.replace('\\', '/')
        
        # 创建目录
        remote_dir = os.path.dirname(remote_path)
        ssh.exec_command(f'mkdir -p {remote_dir}')
        
        print(f'Uploading: {rel_path}')
        sftp.put(local_path, remote_path)

# 重载 nginx
print('\n=== 重载 nginx ===')
stdin, stdout, stderr = ssh.exec_command('systemctl reload nginx')
stdout.read()
print('Done!')

sftp.close()
ssh.close()
