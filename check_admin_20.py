import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 找出admin.html中包含20的图片相关行
stdin, stdout, stderr = ssh.exec_command("grep -n '20' /root/backend/admin.html | grep -i 'image\\|img\\|pic\\|photo\\|upload\\|最多\\|max\\|files\\|length'")
lines = stdout.read().decode('utf-8', errors='replace')
with open(r'D:\tokai\admin_20_check.txt', 'w', encoding='utf-8') as f:
    f.write(lines)

ssh.close()
print("Done")
