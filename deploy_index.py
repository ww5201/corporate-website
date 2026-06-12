import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")
s = c.open_sftp()

# Upload new index.html
print("[1/2] Uploading new index.html...")
f_local = open("D:/tokai/frontend_index_new.html", "rb")
f_remote = s.open("/var/www/frontend/index.html", "w")
f_remote.write(f_local.read())
f_local.close()
f_remote.close()

stat = s.stat("/var/www/frontend/index.html")
print(f"  [OK] Size: {stat.st_size} bytes")

s.close()

# Verify
def run(cmd):
    stdin, stdout, stderr = c.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', 'replace').strip()

print("[2/2] Verifying...")
print("Index:", run("curl -sI http://localhost/ 2>&1 | head -5"))
print("Has bottom-nav:", "bottom-nav" in run("curl -s http://localhost/ | grep -c bottom-nav"))
print("Has hot-products:", "hot-products" in run("curl -s http://localhost/ | grep -c hot-products"))

c.close()
print("\n[DONE]")
