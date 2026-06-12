import paramiko
import os

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(host, port, user, pwd, timeout=10)
    print("=== Connected ===")
    
    # Create manifest.json for PWA/APK icon
    manifest = '''{
  "name": "卓翌定制",
  "short_name": "卓翌",
  "description": "高端家居定制",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/icon.png",
      "sizes": "512x512",
      "type": "image/png"
    },
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}'''
    
    # Write manifest.json
    sftp = client.open_sftp()
    with sftp.open('/var/www/frontend/manifest.json', 'w') as f:
        f.write(manifest)
    print("=== Created manifest.json ===")
    
    # Check current index.html for icon references
    stdin, stdout, stderr = client.exec_command("grep -n 'icon\\|manifest\\|favicon' /var/www/frontend/index.html")
    icon_refs = stdout.read().decode()
    print("=== Current icon references in index.html ===")
    print(icon_refs if icon_refs else "None found")
    
    # Get first 30 lines of index.html to see the head section
    stdin, stdout, stderr = client.exec_command("head -50 /var/www/frontend/index.html")
    head_section = stdout.read().decode()
    print("=== Head section of index.html ===")
    print(head_section)
    
    sftp.close()

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
