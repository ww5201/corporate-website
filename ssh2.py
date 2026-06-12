import paramiko
import sys

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(host, port, user, pwd, timeout=10)
    sys.stdout.write("Connected!\n")
    sys.stdout.flush()
    
    stdin, stdout, stderr = client.exec_command("whoami && hostname && pwd")
    out = stdout.read().decode()
    err = stderr.read().decode()
    sys.stdout.write(f"Output: {out}\n")
    if err:
        sys.stdout.write(f"Stderr: {err}\n")
    sys.stdout.flush()
    
    stdin, stdout, stderr = client.exec_command("find /root /home /opt /var/www -maxdepth 3 -name 'admin.html' -o -name 'server.js' -o -name 'app.js' 2>/dev/null")
    out = stdout.read().decode()
    sys.stdout.write(f"Files: {out}\n")
    sys.stdout.flush()
    
    stdin, stdout, stderr = client.exec_command("ls -la /root/")
    out = stdout.read().decode()
    sys.stdout.write(f"Root dir:\n{out}\n")
    sys.stdout.flush()
    
except Exception as e:
    sys.stdout.write(f"Error: {e}\n")
    sys.stdout.flush()
    import traceback
    traceback.print_exc()
finally:
    client.close()
