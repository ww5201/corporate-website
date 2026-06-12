import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 检查微信按钮
stdin, stdout, stderr = ssh.exec_command('grep -n "handleWechatClick" /var/www/frontend/index.html')
result = stdout.read().decode('utf-8')
with open('D:/tokai/check_result.txt', 'w', encoding='utf-8') as f:
    f.write("微信按钮:\n" + result + "\n\n")

# 检查咨询按钮
stdin, stdout, stderr = ssh.exec_command('grep -n "consult\\|咨询" /var/www/frontend/index.html | head -10')
result = stdout.read().decode('utf-8')
with open('D:/tokai/check_result.txt', 'a', encoding='utf-8') as f:
    f.write("咨询按钮:\n" + result + "\n\n")

# 检查启动代码
stdin, stdout, stderr = ssh.exec_command('tail -20 /var/www/frontend/index.html')
result = stdout.read().decode('utf-8')
with open('D:/tokai/check_result.txt', 'a', encoding='utf-8') as f:
    f.write("页面底部:\n" + result)

ssh.close()
print("检查完成，查看 D:/tokai/check_result.txt")
