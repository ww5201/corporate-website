import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

with open("D:/tokai/server-v4.js", "w", encoding="utf-8") as f:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, port, user, pwd, timeout=10)
        stdin, stdout, stderr = client.exec_command("cat /root/backend/server-v4.js")
        content = stdout.read().decode('utf-8')
        f.write(content)
        print(f"Downloaded {len(content)} chars")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
