import subprocess, sys
try:
    import paramiko
except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'paramiko', '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple'])
    import paramiko

import os

host = '8.138.218.146'
user = 'root'
pwd = 'ww0987654.'

transport = paramiko.Transport((host, 22))
transport.connect(username=user, password=pwd)
sftp = paramiko.SFTPClient.from_transport(transport)

# 上传前端
local = r'D:\tokai\frontend-new.zip'
remote = '/root/frontend-new.zip'
print(f'Uploading {local} -> {remote} ...')
sftp.put(local, remote)
print('Upload done!')

# 上传 admin.html
local2 = r'D:\tokai\backend\admin.html'
remote2 = '/root/backend/admin/admin.html'
sftp.put(local2, remote2)
print('Admin.html uploaded!')

sftp.close()
transport.close()
print('All done!')
