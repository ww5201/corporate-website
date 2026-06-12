import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 读取当前文件
stdin, stdout, stderr = ssh.exec_command("cat /var/www/frontend/index.html")
html = stdout.read().decode('utf-8')

# 1. 把 tel: 链接改回普通文本，加上 onclick 事件
old = '<a href="tel:18977122166" style="color:inherit;text-decoration:none">18977122166</a>'
new = '<span style="color:inherit;cursor:pointer" onclick="callPhone()">18977122166</span>'

html = html.replace(old, new)
count = html.count(new)
print(f"Replaced tel links: {count}")

# 2. 在 </body> 前添加 callPhone 函数（如果还没有的话）
js_func = '''
function callPhone() {
    var num = "18977122166";
    if (navigator.clipboard) {
        navigator.clipboard.writeText(num).then(function() {
            alert("电话号码已复制：\\n" + num + "\\n\\n请打开电话应用拨打");
        }).catch(function() {
            alert("请拨打电话：" + num);
        });
    } else {
        alert("请拨打电话：" + num);
    }
}
'''

if 'function callPhone' not in html:
    html = html.replace('</body>', '<script>' + js_func + '</script></body>')
    print("Added callPhone function")
else:
    print("callPhone already exists")

# 写回服务器
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

# 重载nginx
ssh.exec_command("nginx -s reload")

# 同步到本地
with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 验证
stdin, stdout, stderr = ssh.exec_command("grep -c 'callPhone' /var/www/frontend/index.html")
c = stdout.read().decode().strip()
print(f"callPhone refs: {c}")
stdin, stdout, stderr = ssh.exec_command("grep -c 'tel:' /var/www/frontend/index.html")
t = stdout.read().decode().strip()
print(f"tel: links remaining: {t}")

ssh.close()
print("Done!")
