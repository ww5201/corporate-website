import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")

# Check what the main frontend looks like
s = c.open_sftp()

# Check admin.html navigation
f = s.open("/root/backend/admin.html")
data = f.read().decode("utf-8", "replace")
f.close()

import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

for i, line in enumerate(data.split("\n")):
    if any(kw in line.lower() for kw in ["nav", "menu", "sidebar", "href", "onclick"]):
        print(f"admin:{i+1}: {line.strip()[:120]}")

print("\n--- admin.html size:", len(data), "bytes")

# Check dist/index.html
try:
    f = s.open("/root/backend/dist/index.html")
    data2 = f.read().decode("utf-8", "replace")
    f.close()
    print("\n--- dist/index.html size:", len(data2), "bytes")
except Exception as e:
    print("dist/index.html error:", e)

# Check /var/www/frontend
try:
    entries = s.listdir("/var/www/frontend")
    print("\n/var/www/frontend:", entries[:20])
except:
    print("\nNo /var/www/frontend")

s.close()
c.close()
