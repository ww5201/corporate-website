import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 1. Fix server-v4.js - add explicit routes for shop.html and payment.html BEFORE the SPA catch-all
fix_server = r"""
cd /root/backend

# Backup current server-v4.js
cp server-v4.js server-v4.js.bak.$(date +%Y%m%d%H%M%S)

# Add shop.html and payment.html routes before the SPA catch-all
# Insert before line 468 (SPA Catch-all comment)
sed -i '468i\
// ==================== Standalone Pages ====================\
app.get("/shop.html", (req, res) => {\
  const shopPath = path.join(__dirname, "shop.html");\
  if (fs.existsSync(shopPath)) return res.sendFile(shopPath);\
  res.sendFile(path.join(frontendDir, "index.html"));\
});\
app.get("/payment.html", (req, res) => {\
  const payPath = path.join(__dirname, "payment.html");\
  if (fs.existsSync(payPath)) return res.sendFile(payPath);\
  res.sendFile(path.join(frontendDir, "index.html"));\
});\
' server-v4.js

echo "server-v4.js patched"
grep -n "shop\|payment" server-v4.js | tail -20
"""

i, o, e = ssh.exec_command(fix_server, timeout=15)
print("=== Fix server-v4.js ===")
print(o.read().decode('utf-8', 'replace'))
err = e.read().decode('utf-8', 'replace').strip()
if err: print(f"ERR: {err}")

# 2. Fix nginx config - remove the SPA-specific proxy rules that cause 404s
fix_nginx = r"""
cat > /etc/nginx/conf.d/tokai.conf << 'NGINX_EOF'
# Security Headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com 'unsafe-inline' 'unsafe-eval'; img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com data:;" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

# Hide nginx version
server_tokens off;

# Rate limiting
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
limit_conn_zone $binary_remote_addr zone=addr:10m;

server {
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

    location /ws/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location / {
        try_files $uri $uri/ /index.html;
    }
}

server {
    listen 9998;
    location / {
        proxy_pass http://127.0.0.1:9999;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Content-Type "application/json";
    }
}
NGINX_EOF

echo "nginx config written"
nginx -t 2>&1
"""

i, o, e = ssh.exec_command(fix_nginx, timeout=15)
print("\n=== Fix nginx config ===")
print(o.read().decode('utf-8', 'replace'))
err = e.read().decode('utf-8', 'replace').strip()
if err: print(f"ERR: {err}")

# 3. Copy shop.html and payment.html to /var/www/frontend/ so nginx serves them as static files
deploy_pages = """
cp /root/backend/shop.html /var/www/frontend/shop.html 2>/dev/null && echo "shop.html copied" || echo "shop.html not found"
cp /root/backend/payment.html /var/www/frontend/payment.html 2>/dev/null && echo "payment.html copied" || echo "payment.html not found"
"""

i, o, e = ssh.exec_command(deploy_pages, timeout=10)
print("\n=== Deploy shop/payment pages ===")
print(o.read().decode('utf-8', 'replace'))

# 4. Restart everything
restart = """
pm2 restart tokai-backend 2>&1
nginx -s reload 2>&1
sleep 2
echo "=== Verify ==="
curl -sI http://localhost/ 2>/dev/null | head -3
echo ""
curl -sI http://localhost/shop.html 2>/dev/null | head -3
echo ""
curl -sI http://localhost/payment.html 2>/dev/null | head -3
echo ""
curl -s http://localhost:3000/api/health 2>/dev/null
echo ""
echo "=== Frontend files ==="
ls -la /var/www/frontend/
ls -la /var/www/frontend/assets/
"""

i, o, e = ssh.exec_command(restart, timeout=20)
print("\n=== Restart & Verify ===")
print(o.read().decode('utf-8', 'replace'))
err = e.read().decode('utf-8', 'replace').strip()
if err: print(f"ERR: {err}")

ssh.close()
print("\nDone!")
