import paramiko, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")
s = c.open_sftp()

# 1. Upload auth.js
print("[1/5] Uploading auth.js...")
with open("D:/tokai/backend/routes/auth.js", "rb") as fl:
    fr = s.open("/root/backend/routes/auth.js", "w")
    fr.write(fl.read())
    fr.close()
print("  [OK]")

# 2. Upload login.html
print("[2/5] Uploading login.html...")
with open("D:/tokai/backend/login.html", "rb") as fl:
    fr = s.open("/root/backend/login.html", "w")
    fr.write(fl.read())
    fr.close()
print("  [OK]")

# 3. Upload server-v4.js
print("[3/5] Uploading server-v4.js...")
with open("D:/tokai/backend/server-v4.js", "rb") as fl:
    fr = s.open("/root/backend/server-v4.js", "w")
    fr.write(fl.read())
    fr.close()
print("  [OK]")

# 4. Update Nginx config (add /login.html proxy)
print("[4/5] Updating Nginx config...")
nginx_conf = """server {
    listen 80;
    server_name _;
    root /var/www/frontend;
    index index.html;
    location /api/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /uploads/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
    }
    location /file-upload/ {
        proxy_pass http://127.0.0.1:9999/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location = /payment.html {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location = /shop.html {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location = /login.html {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location / {
        try_files $uri $uri/ /index.html;
    }
}
"""
fr = s.open("/etc/nginx/conf.d/site.conf", "w")
fr.write(nginx_conf)
fr.close()
print("  [OK]")

# 5. Update nav links on index.html (change "我的" link to /login.html)
print("[5/5] Updating nav links on index.html...")
f = s.open("/var/www/frontend/index.html")
idx = f.read().decode("utf-8", "replace")
f.close()

# Update bottom nav: 我的 → /login.html
idx = idx.replace('href="#contact">\n      <span class="nav-icon">👤</span>\n      <span class="nav-label">我的</span>', 
                   'href="/login.html">\n      <span class="nav-icon">👤</span>\n      <span class="nav-label">我的</span>')

# Also update quick entry if it links to #contact for 我的
idx = idx.replace('href="#contact">\n      <div class="quick-icon q7">📞</div>\n      <span>联系我们</span>',
                   'href="#contact">\n      <div class="quick-icon q7">📞</div>\n      <span>联系我们</span>')

f = s.open("/var/www/frontend/index.html", "w")
f.write(idx)
f.close()
print("  [OK]")

s.close()

# Restart services
print("\nRestarting services...")
c.exec_command("nginx -t && nginx -s reload")
time.sleep(1)
c.exec_command("pkill -9 node; sleep 2 && cd /root/backend && nohup node server-v4.js > server.log 2>&1 &")
time.sleep(4)

# Verify
def run(cmd):
    stdin, stdout, stderr = c.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', 'replace').strip()

print("\n=== Verification ===")
print("Health:", run("curl -s http://localhost:3000/api/health"))
print("Login page:", run("curl -sI http://localhost/login.html 2>&1 | head -5"))
print("Auth route:", run("curl -s -X POST http://localhost:3000/api/auth/sms/send -H 'Content-Type: application/json' -d '{\"phone\":\"13800138000\"}' 2>&1 | head -c 200"))
print("Login nav:", "/login.html" in idx)

c.close()
print("\n[DONE]")
