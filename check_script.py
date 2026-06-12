import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check actual file content
stdin, stdout, stderr = ssh.exec_command('grep -c "<script>" /var/www/frontend/index.html')
count = stdout.read().decode().strip()
print(f"<script> tags: {count}")

stdin, stdout, stderr = ssh.exec_command('grep -c "</script>" /var/www/frontend/index.html')
count2 = stdout.read().decode().strip()
print(f"</script> tags: {count2}")

# Get position of last <script>
stdin, stdout, stderr = ssh.exec_command('grep -ob "<script>" /var/www/frontend/index.html')
positions = stdout.read().decode().strip()
print(f"\nScript positions: {positions}")

# Check what curl returns
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1/ | grep -c "<script>"')
curl_count = stdout.read().decode().strip()
print(f"\nCurl <script> count: {curl_count}")

# Check file size
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode().strip()
print(f"File size: {size}")

ssh.close()
