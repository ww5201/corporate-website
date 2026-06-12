import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Test URL with query string
stdin, stdout, stderr = ssh.exec_command('curl -s "http://127.0.0.1/?t=12345" | head -5')
result = stdout.read().decode()

# Also verify the API endpoints
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:3000/api/products | head -100')
products = stdout.read().decode()

stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1:3000/api/payment-config')
payment = stdout.read().decode()

with open('D:/tokai/verify_all.txt', 'w', encoding='utf-8') as f:
    f.write(f"Query string test:\n{result}\n\n")
    f.write(f"Products API:\n{products[:200]}\n\n")
    f.write(f"Payment config:\n{payment}\n")

ssh.close()
print("Done")
