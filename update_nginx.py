import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")

# Update nginx config to proxy payment.html to backend
new_config = """server {
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
    location / {
        try_files $uri $uri/ /index.html;
    }
}
"""

# Write new config
s = c.open_sftp()
f = s.open("/etc/nginx/conf.d/site.conf", "w")
f.write(new_config)
f.close()
s.close()
print("[OK] Nginx config updated")

# Test nginx config
stdin, stdout, stderr = c.exec_command("nginx -t 2>&1")
result = stdout.read().decode('utf-8', 'replace')
print("nginx -t:", result)

# Reload nginx
stdin, stdout, stderr = c.exec_command("nginx -s reload 2>&1")
result = stdout.read().decode('utf-8', 'replace')
print("nginx -s reload:", result or "OK")

import time
time.sleep(2)

# Verify payment.html is now proxied correctly
stdin, stdout, stderr = c.exec_command("curl -sI http://localhost/payment.html 2>&1 | head -10")
print("\ncurl /payment.html after update:")
print(stdout.read().decode('utf-8', 'replace'))

# Also verify index.html still works
stdin, stdout, stderr = c.exec_command("curl -sI http://localhost/ 2>&1 | head -5")
print("curl / (index.html):")
print(stdout.read().decode('utf-8', 'replace'))

c.close()
