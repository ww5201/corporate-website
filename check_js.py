import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

# 下载JS文件看看原版是怎么写的
stdin, stdout, stderr = client.exec_command("cat /var/www/frontend/assets/index-D_o_inZM.js")
js_content = stdout.read().decode('utf-8')
with open("D:/tokai/original_js.js", "w", encoding="utf-8") as f:
    f.write(js_content)
print(f"JS文件: {len(js_content)} 字符")
print(js_content[:3000])

client.close()
