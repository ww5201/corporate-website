import paramiko, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ===== 1. Update index.html locally =====
print("[1/4] Updating index.html...")
with open("D:/tokai/frontend_index_new.html", "r", encoding="utf-8") as f:
    idx = f.read()

# Red → Blue theme
idx = idx.replace("--red: #e02e24;", "--primary: #1677ff;")
idx = idx.replace("--red-light: #ff4d4f;", "--primary-light: #4096ff;")
idx = idx.replace("--red-bg: #fff1f0;", "--primary-bg: #e6f4ff;")

# Replace all var(--red) references
idx = idx.replace("var(--red)", "var(--primary)")
idx = idx.replace("var(--red-light)", "var(--primary-light)")
idx = idx.replace("var(--red-bg)", "var(--primary-bg)")

# Replace hardcoded red colors in gradients
idx = idx.replace("linear-gradient(135deg, var(--primary) 0%, #ff4444 100%)", "linear-gradient(135deg, var(--primary) 0%, #4096ff 100%)")
idx = idx.replace("linear-gradient(135deg, var(--primary) 0%, #ff6034 100%)", "linear-gradient(135deg, var(--primary) 0%, #69b1ff 100%)")
idx = idx.replace("linear-gradient(135deg, var(--primary) 0%, #ff6034 50%, #ff4444 100%)", "linear-gradient(135deg, var(--primary) 0%, #4096ff 50%, #1677ff 100%)")
idx = idx.replace("#ff4444", "#4096ff")
idx = idx.replace("#ff6034", "#69b1ff")

# Replace .red class color references  
idx = idx.replace("color: var(--primary);", "color: var(--primary);")  # no-op, already changed via var

# Email → Phone in contact form
idx = idx.replace('type="email" placeholder="邮箱地址"', 'type="tel" placeholder="电话号码"')

# Contact section email → phone
idx = idx.replace(
    """<div class="contact-icon email">✉️</div>
      <div>
        <h5>邮箱</h5>
        <p>2841327487@qq.com</p>
      </div>""",
    """<div class="contact-icon email">📱</div>
      <div>
        <h5>电话</h5>
        <p>18977122166</p>
      </div>"""
)

with open("D:/tokai/frontend_index_new.html", "w", encoding="utf-8") as f:
    f.write(idx)
print("  [OK] index.html updated")

# ===== 2. Update shop.html locally =====
print("[2/4] Updating shop.html...")
with open("D:/tokai/backend/shop.html", "r", encoding="utf-8") as f:
    shop = f.read()

# Red → Blue theme
shop = shop.replace("--red: #e02e24;", "--primary: #1677ff;")
shop = shop.replace("--red-light: #ff4d4f;", "--primary-light: #4096ff;")
shop = shop.replace("--red-bg: #fff1f0;", "--primary-bg: #e6f4ff;")

shop = shop.replace("var(--red)", "var(--primary)")
shop = shop.replace("var(--red-light)", "var(--primary-light)")
shop = shop.replace("var(--red-bg)", "var(--primary-bg)")

shop = shop.replace("linear-gradient(135deg, var(--primary) 0%, #ff4444 100%)", "linear-gradient(135deg, var(--primary) 0%, #4096ff 100%)")
shop = shop.replace("linear-gradient(135deg, var(--primary) 0%, #ff6034 100%)", "linear-gradient(135deg, var(--primary) 0%, #69b1ff 100%)")
shop = shop.replace("#ff4444", "#4096ff")
shop = shop.replace("#ff6034", "#69b1ff")

with open("D:/tokai/backend/shop.html", "w", encoding="utf-8") as f:
    f.write(shop)
print("  [OK] shop.html updated")

# ===== 3. Check backend for email/contact references =====
print("[3/4] Checking backend...")
with open("D:/tokai/backend/server-v4.js", "r", encoding="utf-8") as f:
    srv = f.read()

# Check for email-related fields
import re
email_lines = [l.strip() for l in srv.split("\n") if "email" in l.lower() or "2841327487" in l]
print("  Backend email refs:", email_lines[:10] if email_lines else "None found")

# Check payment.js too
with open("D:/tokai/backend/routes/payment.js", "r", encoding="utf-8") as f:
    pay = f.read()
email_lines2 = [l.strip() for l in pay.split("\n") if "email" in l.lower()]
print("  Payment email refs:", email_lines2[:10] if email_lines2 else "None found")

# ===== 4. Deploy all =====
print("[4/4] Deploying...")
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")
s = c.open_sftp()

# Upload index.html to /var/www/frontend/
with open("D:/tokai/frontend_index_new.html", "rb") as f_local:
    f_remote = s.open("/var/www/frontend/index.html", "w")
    f_remote.write(f_local.read())
    f_remote.close()
print("  [OK] index.html deployed")

# Upload shop.html to /root/backend/
with open("D:/tokai/backend/shop.html", "rb") as f_local:
    f_remote = s.open("/root/backend/shop.html", "w")
    f_remote.write(f_local.read())
    f_remote.close()
print("  [OK] shop.html deployed")

s.close()

# Restart Node (shop.html served by backend)
c.exec_command("pkill -9 node; sleep 2 && cd /root/backend && nohup node server-v4.js > server.log 2>&1 &")
time.sleep(4)

# Verify
def run(cmd):
    stdin, stdout, stderr = c.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', 'replace').strip()

# Check colors in served files
idx_served = run("curl -s http://localhost/")
shop_served = run("curl -s http://localhost:3000/shop.html")
print("\n=== Verification ===")
print("Index has blue (#1677ff):", "#1677ff" in idx_served)
print("Index has old red (#e02e24):", "#e02e24" in idx_served)
print("Index has phone (18977122166):", "18977122166" in idx_served)
print("Shop has blue (#1677ff):", "#1677ff" in shop_served)
print("Shop has old red (#e02e24):", "#e02e24" in shop_served)
print("Health:", run("curl -s http://localhost:3000/api/health"))

c.close()
print("\n[DONE]")
