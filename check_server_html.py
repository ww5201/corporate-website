import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 下载前端文件检查
stdin, stdout, stderr = ssh.exec_command("cat /var/www/frontend/index.html")
html = stdout.read().decode('utf-8', errors='replace')

# 检查关键内容
checks = []
if '卓翌定制' in html:
    checks.append("OK: 卓翌定制 exists")
else:
    checks.append("MISSING: 卓翌定制 not found!")

if '抖音' in html or 'tiktok' in html.lower() or 'douyin' in html.lower():
    checks.append("FOUND: 抖音/tiktok content!")
else:
    checks.append("OK: No 抖音 content")

# 写入前500字符
with open(r'D:\tokai\server_html_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"File size: {len(html)} chars\n\n")
    for c in checks:
        f.write(c + "\n")
    f.write(f"\nFirst 1000 chars:\n{html[:1000]}")

ssh.close()
print("Done")
