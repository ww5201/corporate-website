import paramiko
import sys

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

output_file = "D:/tokai/ssh_output.txt"
with open(output_file, "w") as f:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, port, user, pwd, timeout=10)
        f.write("Connected!\n")
        f.flush()
        
        stdin, stdout, stderr = client.exec_command("whoami && hostname && pwd")
        out = stdout.read().decode()
        err = stderr.read().decode()
        f.write(f"Output: {out}\n")
        if err:
            f.write(f"Stderr: {err}\n")
        f.flush()
        
        stdin, stdout, stderr = client.exec_command("ls -la /root/")
        out = stdout.read().decode()
        f.write(f"Root dir:\n{out}\n")
        f.flush()
        
        stdin, stdout, stderr = client.exec_command("find /root /home /opt /var/www -maxdepth 3 -name 'admin.html' -o -name 'server.js' -o -name 'app.js' 2>/dev/null")
        out = stdout.read().decode()
        f.write(f"Project files:\n{out}\n")
        f.flush()
        
    except Exception as e:
        f.write(f"Error: {e}\n")
        f.flush()
        import traceback
        traceback.print_exc(file=f)
    finally:
        client.close()
