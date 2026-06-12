import paramiko

server = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(server, port, user, pwd, timeout=10)
print("SSH connected")

sftp = ssh.open_sftp()

# Upload v4
sftp.put(r"D:\tokai\index-v4.html", "/var/www/frontend/index.html")
print("Uploaded index.html")

sftp.close()

# Clear nginx cache
stdin, stdout, stderr = ssh.exec_command("nginx -s reload 2>&1")
out = stdout.read().decode()
print(f"nginx reload: {out}")

ssh.close()
print("Done!")
