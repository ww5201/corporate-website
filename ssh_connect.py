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
    print("=== Connected ===")
    
    # Basic info
    stdin, stdout, stderr = client.exec_command("whoami && hostname && pwd")
    print(stdout.read().decode())
    
    # Find the project
    stdin, stdout, stderr = client.exec_command("find / -name 'admin.html' -o -name 'server.js' -o -name 'app.js' 2>/dev/null | head -20")
    files = stdout.read().decode()
    print("=== Project files ===")
    print(files)
    
    # Check common locations
    stdin, stdout, stderr = client.exec_command("ls -la /root/ /home/ /opt/ /var/www/ 2>/dev/null | head -40")
    print("=== Common dirs ===")
    print(stdout.read().decode())
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
finally:
    client.close()
