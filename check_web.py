import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check the handleWechatClick function
stdin, stdout, stderr = ssh.exec_command('grep -A3 "function handleWechatClick" /var/www/frontend/index.html')
func = stdout.read().decode()
print("微信函数:")
print(func)

# Check if products section exists
stdin, stdout, stderr = ssh.exec_command('grep -c "product-card" /var/www/frontend/index.html')
cards = stdout.read().decode().strip()
print(f"\nproduct-card 数量：{cards}")

# Check loadData call
stdin, stdout, stderr = ssh.exec_command('grep "loadData()" /var/www/frontend/index.html')
loadData = stdout.read().decode()
print(f"\nloadData 调用:\n{loadData}")

ssh.close()
