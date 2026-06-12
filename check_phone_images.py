import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 检查电话按钮
stdin, stdout, stderr = ssh.exec_command("grep -nc 'tel:' /var/www/frontend/index.html")
count = stdout.read().decode('utf-8').strip()
print(f"tel: count on server: {count}")

# 检查产品图片渲染 - 读取 product modal 部分
stdin, stdout, stderr = ssh.exec_command("grep -n 'showProduct' /var/www/frontend/index.html")
lines = stdout.read().decode('utf-8')
print(f"showProduct lines:\n{lines}")

# 检查产品 API 
stdin, stdout, stderr = ssh.exec_command("curl -s http://127.0.0.1:3000/api/products | head -c 3000")
api = stdout.read().decode('utf-8')
print(f"Products API:\n{api[:2000]}")

# 检查图片URL格式
stdin, stdout, stderr = ssh.exec_command("ls -la /root/backend/uploads/ | head -10")
uploads = stdout.read().decode('utf-8')
print(f"Uploads dir:\n{uploads}")

# 用write输出避免GBK编码问题
ssh.exec_command("grep -n 'tel:\\|phone' /var/www/frontend/index.html > /tmp/phone_check.txt")
stdin, stdout, stderr = ssh.exec_command("cat /tmp/phone_check.txt")
phone = stdout.read().decode('utf-8', errors='replace')

ssh.exec_command("grep -n 'product-modal\\|showProduct\\|showImages\\|productImage' /var/www/frontend/index.html > /tmp/modal_check.txt")
stdin, stdout, stderr = ssh.exec_command("cat /tmp/modal_check.txt")
modal = stdout.read().decode('utf-8', errors='replace')

# Write results to local file
with open(r'D:\tokai\check_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== PHONE ===\n{phone}\n\n=== MODAL ===\n{modal}\n\n=== API ===\n{api[:3000]}\n\n=== UPLOADS ===\n{uploads}\n")

ssh.close()
print("Results saved to check_result.txt")
