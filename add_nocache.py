import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

# 1. 给 nginx 加上 no-cache 头
nginx_conf = '''server {
    listen 80;
    server_name _;

    root /var/www/frontend;
    index index.html;

    # 前端静态文件 - 不缓存
    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
    }

    # API 代理到后端
    location /api/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 图片代理到后端
    location /uploads/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
'''

sftp = client.open_sftp()
with sftp.file("/etc/nginx/conf.d/site.conf", "w") as f:
    f.write(nginx_conf)

# 2. 重载 nginx
stdin, stdout, stderr = client.exec_command("nginx -s reload 2>&1")
print("Nginx重载:", stdout.read().decode().strip())

# 3. 给 index.html 加上 meta no-cache 标签
stdin, stdout, stderr = client.exec_command("cat /var/www/frontend/index.html")
html = stdout.read().decode()

# 在 <head> 中插入 no-cache meta
no_cache_meta = '  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">\n  <meta http-equiv="Pragma" content="no-cache">\n  <meta http-equiv="Expires" content="0">\n'
html = html.replace('<head>', '<head>\n' + no_cache_meta, 1)

with sftp.file("/var/www/frontend/index.html", "w") as f:
    f.write(html)

print(f"已更新index.html，加了防缓存标签，大小: {len(html)} 字符")

sftp.close()
client.close()
print("完成!")
