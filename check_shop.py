import paramiko, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")

def run(cmd):
    stdin, stdout, stderr = c.exec_command(cmd, timeout=15)
    return stdout.read().decode('utf-8', 'replace').strip()

# Check product API
print("=== /api/products ===")
result = run("curl -s http://localhost:3000/api/products | head -c 2000")
print(result)

# Check product categories
print("\n=== /api/products/categories ===")
result = run("curl -s http://localhost:3000/api/products/categories 2>/dev/null | head -c 500")
print(result)

# Check the shop section in the current SPA JS for how it renders products
print("\n=== Shop section HTML in index.html ===")
s = c.open_sftp()
f = s.open("/var/www/frontend/index.html")
data = f.read().decode("utf-8", "replace")
f.close()

# Extract shop section
in_shop = False
for i, line in enumerate(data.split("\n")):
    stripped = line.strip()
    if 'id="shop"' in stripped or 'class="shop' in stripped:
        in_shop = True
    if in_shop:
        print(f"{i+1}: {stripped[:150]}")
    if in_shop and ('</section>' in stripped or 'id="contact"' in stripped):
        in_shop = False

s.close()
c.close()
