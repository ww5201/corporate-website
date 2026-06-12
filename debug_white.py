import paramiko
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

stdin, stdout, stderr = ssh.exec_command("cat /var/www/frontend/index.html")
html = stdout.read().decode('utf-8')

# 检查关键部分
sections = ['#services', '#products', '#portfolio', '#contact', '#footer']
for s in sections:
    if s in html:
        idx = html.index(s)
        print(f"Found {s} at position {idx}")
    else:
        print(f"MISSING {s}!")

# 检查JS错误 - 看看有没有语法问题
# 提取script标签内容
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
if scripts:
    for i, s in enumerate(scripts):
        print(f"\nScript {i}: {len(s)} chars")
        # 检查常见的JS错误模式
        if 'Android.callPhone' in s:
            print("  Contains Android.callPhone - OK (browser-safe)")
        # 检查是否有双引号闭合问题
        dq = s.count('"')
        if dq % 2 != 0:
            print(f"  WARNING: Odd number of double quotes ({dq})!")

# 检查i18n部分
print(f"\nTotal HTML size: {len(html)} chars")
print(f"Has langLabels: {'langLabels' in html}")
print(f"Has setLang: {'setLang' in html}")

# 检查最近修改的tel部分
tel_count = html.count('tel:18977122166')
print(f"tel: links: {tel_count}")

# 检查页面底部
last_500 = html[-500:]
print(f"\nLast 500 chars of HTML:")
print(last_500[:200])

ssh.close()
