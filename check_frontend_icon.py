import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(host, port, user, pwd, timeout=10)
    print("=== Connected ===")
    
    # Check frontend directory
    stdin, stdout, stderr = client.exec_command("ls -la /var/www/frontend/")
    print("=== /var/www/frontend/ ===")
    print(stdout.read().decode())
    
    # Find icon/manifest related files
    stdin, stdout, stderr = client.exec_command("find /var/www/frontend -name 'icon*' -o -name 'manifest*' -o -name '*.ico' -o -name 'favicon*' 2>/dev/null")
    print("=== Icon/Manifest files ===")
    print(stdout.read().decode())
    
    # Check if there's an android directory or capacitor config
    stdin, stdout, stderr = client.exec_command("find /var/www/frontend -name 'capacitor*' -o -name 'android' -type d -o -name 'res' -type d 2>/dev/null")
    print("=== Android/Capacitor ===")
    print(stdout.read().decode())
    
    # Check if there's a public or assets directory
    stdin, stdout, stderr = client.exec_command("ls -la /var/www/frontend/src/ 2>/dev/null; ls -la /var/www/frontend/public/ 2>/dev/null; ls -la /var/www/frontend/assets/ 2>/dev/null")
    print("=== Subdirectories ===")
    print(stdout.read().decode())

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
