import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 检查 admin.html 中留言相关部分
stdin, stdout, stderr = ssh.exec_command("grep -n 'messages\\|loadMessages' /root/backend/admin.html")
result = stdout.read().decode('utf-8', errors='replace')

# 写入文件避免 GBK 编码问题
with open(r'D:\tokai\admin_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"Admin messages refs:\n{result}\n")

# 检查留言 API
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/messages")
msgs = stdout.read().decode('utf-8', errors='replace')
with open(r'D:\tokai\admin_check.txt', 'a', encoding='utf-8') as f:
    f.write(f"\nMessages API:\n{msgs[:2000]}\n")

ssh.close()
print("Done")
