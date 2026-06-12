import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")

s = c.open_sftp()
f = s.open("/var/www/frontend/index.html")
data = f.read().decode("utf-8", "replace")
f.close()

# Save local copy for reference
with open("D:/tokai/frontend_index.html", "w", encoding="utf-8") as lf:
    lf.write(data)

# Print key structural elements
for i, line in enumerate(data.split("\n")):
    stripped = line.strip()
    if any(kw in stripped.lower() for kw in ["nav", "menu", "header", "footer", "href", "button", "contact", "order", "cart", "pay"]):
        print(f"{i+1}: {stripped[:150]}")

print(f"\nTotal: {len(data)} bytes, {len(data.split(chr(10)))} lines")

s.close()
c.close()
