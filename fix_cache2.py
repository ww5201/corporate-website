import paramiko

# 读取本地前端文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 添加缓存清除 meta 标签
cache_meta = '  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate, max-age=0">\n  <meta http-equiv="Pragma" content="no-cache">\n  <meta http-equiv="Expires" content="0">\n'

if 'no-cache, no-store' not in html:
    html = html.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n' + cache_meta)
    print("Added cache busting meta tags")
else:
    print("Cache meta already exists")

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 上传
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\index-v4.html', '/var/www/frontend/index.html')
sftp.close()

ssh.exec_command("nginx -s reload")
ssh.close()
print("Uploaded!")
