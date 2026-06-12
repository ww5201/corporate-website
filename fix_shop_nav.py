import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Fix shop.html locally
with open("D:/tokai/backend/shop.html", "rb") as f:
    data = f.read()

# Replace the nav link
old = b'href="/">\r\n      <span class="nav-icon">\xf0\x9f\x91\xa4</span>\r\n      <span class="nav-label">\xe6\x88\x91\xe7\x9a\x84</span>'
new = b'href="/login.html">\r\n      <span class="nav-icon">\xf0\x9f\x91\xa4</span>\r\n      <span class="nav-label">\xe6\x88\x91\xe7\x9a\x84</span>'

if old in data:
    data = data.replace(old, new, 1)
    with open("D:/tokai/backend/shop.html", "wb") as f:
        f.write(data)
    print("[OK] shop.html fixed locally")
else:
    print("[FAIL] Pattern not found")

# Now upload
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")
s = c.open_sftp()

with open("D:/tokai/backend/shop.html", "rb") as fl:
    fr = s.open("/root/backend/shop.html", "w")
    fr.write(fl.read())
    fr.close()

# Verify
f = s.open("/root/backend/shop.html")
v = f.read().decode("utf-8", "replace")
f.close()
print("Shop has /login.html:", "/login.html" in v)

s.close()
c.close()
