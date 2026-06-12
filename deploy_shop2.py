import paramiko, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")
s = c.open_sftp()

# Upload shop.html
print("[1/2] Uploading shop.html...")
f_local = open("D:/tokai/backend/shop.html", "rb")
f_remote = s.open("/root/backend/shop.html", "w")
f_remote.write(f_local.read())
f_local.close()
f_remote.close()
print("  [OK] Uploaded")

# Verify file size
stat = s.stat("/root/backend/shop.html")
print(f"  Size: {stat.st_size} bytes")

s.close()

# Restart Node
print("[2/2] Restarting Node...")
c.exec_command("pkill -9 node; sleep 2 && cd /root/backend && nohup node server-v4.js > server.log 2>&1 &")
time.sleep(4)

def run(cmd):
    stdin, stdout, stderr = c.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', 'replace').strip()

print("Health:", run("curl -s http://localhost:3000/api/health"))
print("Shop:", run("curl -sI http://localhost/shop.html 2>&1 | head -5"))

c.close()
print("\n[DONE]")
