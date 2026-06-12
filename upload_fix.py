import paramiko
import sys

print("正在连接服务器...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect('8.138.218.146', username='root', password='ww0987654.', timeout=30)
    print("SSH 连接成功！")
except Exception as e:
    print("SSH 失败：%s" % e)
    print("\n请检查：")
    print("1. 服务器是否开机")
    print("2. 防火墙是否允许 SSH (端口 22)")
    print("3. 密码是否正确")
    sys.exit(1)

# 读取修复后的文件
with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("上传文件 (%d 字节)..." % len(html))

# 上传
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(html)
f.close()
sftp.close()

print("上传成功！")

# 重载 nginx
print("重载 nginx...")
stdin, stdout, stderr = ssh.exec_command("nginx -s reload", timeout=10)
err = stderr.read().decode()
if err:
    print("nginx 重载可能有问题：%s" % err)
else:
    print("nginx 重载成功！")

# 验证
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost/ | head -c 200", timeout=10)
result = stdout.read().decode()
print("\n验证 - 页面开头：%s..." % result[:100])

ssh.close()
print("\n✅ 完成！请刷新浏览器测试。")
