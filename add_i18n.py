import paramiko

# 读取文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 添加初始化语言
html = html.replace(
    '// ===== 启动 =====\n    loadData();',
    '// ===== 启动 =====\n    setLang(currentLang);\n    loadData();'
)

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Added language initialization")

# 上传到服务器
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\index-v4.html', '/var/www/frontend/index.html')
sftp.close()

ssh.exec_command("nginx -s reload")
ssh.close()
print("Uploaded!")
