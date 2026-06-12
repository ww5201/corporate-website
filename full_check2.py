import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check file size and key sections
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode().strip()

# Check for key sections
checks = [
    ('支付', 'payment'),
    ('咨询', 'consult'),
    ('产品', 'products'),
    ('案例', 'cases'),
    ('联系', 'contact'),
    ('loadData', 'startup'),
    ('</body>', 'end body'),
    ('</html>', 'end html'),
]

with open('D:/tokai/full_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"File size: {size}\n\n")
    for label, keyword in checks:
        stdin2, stdout2, stderr2 = ssh.exec_command(f'grep -c "{keyword}" /var/www/frontend/index.html')
        count = stdout2.read().decode().strip()
        f.write(f"{label} ({keyword}): {count}\n")

    # Get last 30 lines
    stdin2, stdout2, stderr2 = ssh.exec_command('tail -30 /var/www/frontend/index.html')
    tail = stdout2.read().decode('utf-8')
    f.write(f"\n=== 页面底部 ===\n{tail}")

    # Check if payment section exists
    stdin2, stdout2, stderr2 = ssh.exec_command('grep -n "payment\\|支付\\|alipay\\|wechat.*pay\\|支付宝" /var/www/frontend/index.html | head -10')
    pay = stdout2.read().decode('utf-8')
    f.write(f"\n=== 支付相关 ===\n{pay}")

ssh.close()
print("Done")
