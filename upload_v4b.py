import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("8.138.218.146", 22, "root", "ww0987654.", timeout=10)
sftp = ssh.open_sftp()
sftp.put(r"D:\tokai\index-v4.html", "/var/www/frontend/index.html")
sftp.close()
stdin, stdout, stderr = ssh.exec_command("nginx -s reload")
print(stdout.read().decode())
ssh.close()
print("Done")
