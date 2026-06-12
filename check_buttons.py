import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 检查当前 HTML 的微信和咨询按钮
stdin, stdout, stderr = ssh.exec_command('grep -n "handleWechatClick\\|openWechat\\|consult" /var/www/frontend/index.html | head -20')
buttons = stdout.read().decode()
print("微信/咨询按钮相关:")
print(buttons)

# 检查启动代码
stdin, stdout, stderr = ssh.exec_command('grep -n "loadData\\|loadCases\\|setLang" /var/www/frontend/index.html | tail -10')
startup = stdout.read().decode()
print("\n启动代码:")
print(startup)

ssh.close()
