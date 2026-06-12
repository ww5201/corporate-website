import paramiko
import os

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."
local_base = r"D:\tokai"
remote_base = "/root/backend"

# Files to upload
files_to_upload = [
    ("server-v4.js", "server-v4.js"),
    ("admin.html", "admin.html"),
    ("package.json", "package.json"),
]

print("Connecting to server...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, user, pwd, timeout=15)
sftp = ssh.open_sftp()

# Ensure remote dir exists
stdin, stdout, stderr = ssh.exec_command(f"mkdir -p {remote_base}")
stdout.read()

# Upload files
for local_name, remote_name in files_to_upload:
    local_path = os.path.join(local_base, local_name)
    remote_path = f"{remote_base}/{remote_name}"
    print(f"Uploading {local_name} -> {remote_path} ...")
    sftp.put(local_path, remote_path)
    print(f"  OK ({os.path.getsize(local_path)} bytes)")

# Upload src/ directory if exists (for frontend assets if needed)
src_dir = os.path.join(local_base, "src")
if os.path.isdir(src_dir):
    try:
        ssh.exec_command(f"mkdir -p {remote_base}/src")
        for f in os.listdir(src_dir):
            local_f = os.path.join(src_dir, f)
            remote_f = f"{remote_base}/src/{f}"
            if os.path.isfile(local_f):
                print(f"Uploading src/{f} ...")
                sftp.put(local_f, remote_f)
                print(f"  OK")
    except Exception as e:
        print(f"  src upload warning: {e}")

# Upload dist/ directory if exists
dist_dir = os.path.join(local_base, "dist")
if os.path.isdir(dist_dir):
    try:
        ssh.exec_command(f"mkdir -p {remote_base}/dist")
        # Upload dist/index.html
        dist_index = os.path.join(dist_dir, "index.html")
        if os.path.isfile(dist_index):
            sftp.put(dist_index, f"{remote_base}/dist/index.html")
            print("Uploaded dist/index.html")
        # Upload dist/assets/
        dist_assets = os.path.join(dist_dir, "assets")
        if os.path.isdir(dist_assets):
            ssh.exec_command(f"mkdir -p {remote_base}/dist/assets")
            for f in os.listdir(dist_assets):
                local_f = os.path.join(dist_assets, f)
                remote_f = f"{remote_base}/dist/assets/{f}"
                if os.path.isfile(local_f):
                    sftp.put(local_f, remote_f)
                    print(f"Uploaded dist/assets/{f}")
    except Exception as e:
        print(f"  dist upload warning: {e}")

sftp.close()

print("\n--- Installing dependencies ---")
stdin, stdout, stderr = ssh.exec_command(f"cd {remote_base} && npm install --production 2>&1")
out = stdout.read().decode()
err = stderr.read().decode()
print(out)
if err:
    print("STDERR:", err[:500])

print("\n--- Restarting backend ---")
# Check if pm2 is available
stdin, stdout, stderr = ssh.exec_command("which pm2 2>/dev/null && echo 'PM2_FOUND' || echo 'NO_PM2'")
pm2_check = stdout.read().decode().strip()

if "PM2_FOUND" in pm2_check:
    stdin, stdout, stderr = ssh.exec_command(f"cd {remote_base} && pm2 restart tokai-backend 2>/dev/null || pm2 start server-v4.js --name tokai-backend 2>&1")
else:
    # Kill existing node process and restart
    ssh.exec_command("pkill -f 'node.*server-v4' 2>/dev/null; sleep 1")
    stdin, stdout, stderr = ssh.exec_command(f"cd {remote_base} && nohup node server-v4.js > /tmp/tokai-backend.log 2>&1 &")
out = stdout.read().decode()
err = stderr.read().decode()
print(out if out else "Restarted")

# Wait and verify
import time
time.sleep(3)

stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:3000/api/health 2>/dev/null || echo 'HEALTH_FAIL'")
health = stdout.read().decode().strip()
print(f"\nHealth check: {health}")

stdin, stdout, stderr = ssh.exec_command("netstat -tlnp 2>/dev/null | grep :3000 || ss -tlnp | grep :3000 || echo 'PORT_CHECK_FAIL'")
port_info = stdout.read().decode().strip()
print(f"Port 3000: {port_info}")

ssh.close()
print("\n=== Deployment complete! ===")
