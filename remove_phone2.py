import paramiko

# 读取前端文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 删除移动端导航的电话按钮
html = html.replace(
    '<a href="tel:18977122166"><span class="icon">📞</span>电话</a>',
    ''
)

# 同时更新 JS 中的移动端导航模板
html = html.replace(
    'mobile_home: \'首页\', mobile_products: \'产品\', mobile_consult: \'咨询\', mobile_call: \'电话\'',
    'mobile_home: \'首页\', mobile_products: \'产品\', mobile_consult: \'咨询\''
)

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Removed phone button from mobile nav")

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
