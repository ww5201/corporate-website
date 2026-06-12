import paramiko, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")
s = c.open_sftp()

# 1. Upload shop.html
print("[1/5] Uploading shop.html...")
f_local = open("D:/tokai/backend/shop.html", "rb")
f_remote = s.open("/root/backend/shop.html", "w")
f_remote.write(f_local.read())
f_local.close()
f_remote.close()
print("  [OK] shop.html uploaded")

# 2. Upload updated server-v4.js
print("[2/5] Uploading server-v4.js...")
f_local = open("D:/tokai/backend/server-v4.js", "rb")
f_remote = s.open("/root/backend/server-v4.js", "w")
f_remote.write(f_local.read())
f_local.close()
f_remote.close()
print("  [OK] server-v4.js uploaded")

# 3. Update Nginx config (add /shop.html proxy)
print("[3/5] Updating Nginx config...")
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
    location / {
        try_files $uri $uri/ /index.html;
    }
}
"""
f_remote = s.open("/etc/nginx/conf.d/site.conf", "w")
f_remote.write(nginx_conf)
f_remote.close()
print("  [OK] Nginx config updated")

# 4. Update index.html nav (change shop link to /shop.html)
print("[4/5] Updating index.html nav...")
f = s.open("/var/www/frontend/index.html")
data = f.read().decode("utf-8", "replace")
f.close()

# Desktop nav: change #shop to /shop.html
data = data.replace(
    '<a href="#shop" data-i18n="nav.shop">商品</a>',
    '<a href="/shop.html" target="_blank">商品</a>'
)
# Mobile nav
data = data.replace(
    '<a href="#shop" data-i18n="nav.shop">商品</a>',
    '<a href="/shop.html" target="_blank">商品</a>'
)

f = s.open("/var/www/frontend/index.html", "w")
f.write(data)
f.close()
print("  [OK] Nav links updated")

s.close()

# 5. Restart services
print("[5/5] Restarting services...")
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
print("Shop page:", run("curl -sI http://localhost/shop.html 2>&1 | head -5"))
print("Payment page:", run("curl -sI http://localhost/payment.html 2>&1 | head -5"))
print("Nav updated:", "shop.html" in data)

c.close()
print("\n[DONE] All deployed!")
