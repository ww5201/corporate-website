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
    
    # Get the head section of index.html
    stdin, stdout, stderr = client.exec_command("head -50 /var/www/frontend/index.html")
    head_section = stdout.read().decode('utf-8', errors='ignore')
    print("=== Head section of index.html ===")
    print(head_section)
    
    # Check if there's a <link rel="manifest"> already
    stdin, stdout, stderr = client.exec_command("grep -c 'manifest' /var/www/frontend/index.html")
    has_manifest = stdout.read().decode('utf-8', errors='ignore').strip()
    print(f"\n=== Has manifest link: {has_manifest} ===")
    
    # Check assets directory
    stdin, stdout, stderr = client.exec_command("ls -la /var/www/frontend/assets/")
    assets = stdout.read().decode('utf-8', errors='ignore')
    print("\n=== Assets directory ===")
    print(assets)

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
