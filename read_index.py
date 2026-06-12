import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")
s = c.open_sftp()

f = s.open("/var/www/frontend/index.html")
data = f.read().decode("utf-8", "replace")
f.close()

# Save local copy
with open("D:/tokai/frontend_index_current.html", "w", encoding="utf-8") as lf:
    lf.write(data)

# Print full content
for i, line in enumerate(data.split("\n")):
    print(f"{i+1}: {line.rstrip()[:200]}")

s.close()
c.close()
