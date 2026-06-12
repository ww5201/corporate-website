import paramiko

# 读取本地前端文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 在 head 中添加缓存清除 meta 标签
cache_bust = '''  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate, max-age=0">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <meta http-equiv="refresh" content="0;url=http://8.138.218.146/?v=''' + str(hash(html)) + '''">'''

# 检查是否已有这些标签
if 'no-cache, no-store' not in html:
    html = html.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n' + cache_bust)

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Added cache busting meta tags")

# 上传
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\index-v4.html', '/var/www/frontend/index.html')
sftp.close()

# 清除 nginx 缓存
ssh.exec_command("nginx -s reload")

# 验证
stdin, stdout, stderr = ssh.exec_command("head -15 /var/www/frontend/index.html")
content = stdout.read().decode('utf-8', errors='replace')
print(content[:500])

ssh.close()
print("Done!")
