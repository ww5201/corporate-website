import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")

def run(cmd):
    stdin, stdout, stderr = c.exec_command(cmd, timeout=15)
    return stdout.read().decode('utf-8', 'replace').strip()

# Check nginx config
print("=== Nginx config ===")
print(run("cat /etc/nginx/conf.d/site.conf 2>/dev/null || echo NO_SITE_CONF"))

# Test if payment.html is accessible from outside
print("\n=== curl /payment.html (via nginx) ===")
print(run("curl -sI http://localhost/payment.html 2>&1 | head -10"))

# Test via port 3000 directly
print("\n=== curl :3000/payment.html ===")
print(run("curl -sI http://localhost:3000/payment.html 2>&1 | head -10"))

c.close()
