import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

files = [
    "/var/www/frontend/index.html",
    "/etc/nginx/conf.d/site.conf"
]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

for filepath in files:
    try:
        stdin, stdout, stderr = client.exec_command(f"cat {filepath}")
        content = stdout.read().decode('utf-8')
        filename = filepath.split('/')[-1]
        with open(f"D:/tokai/{filename}", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Downloaded: {filename} ({len(content)} chars)")
    except Exception as e:
        print(f"Error downloading {filepath}: {e}")

client.close()
