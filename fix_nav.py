import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(host, port, user, pwd, timeout=10)
    print("Connected!")
    
    # Read current index.html
    stdin, stdout, stderr = client.exec_command("cat /var/www/frontend/index.html")
    html = stdout.read().decode('utf-8')
    err = stderr.read().decode()
    if err:
        print(f"Read error: {err}")
    
    print(f"Original size: {len(html)} bytes")
    
    # Check current nav links
    import re
    nav_links = re.findall(r'<a href="([^"]*)"[^>]*data-i18n="nav\.(shop|products)"', html)
    print(f"Current nav links: {nav_links}")
    
    # Fix: change #shop to /shop.html
    html_new = html.replace('href="#shop"', 'href="/shop.html"')
    
    # Verify changes
    nav_links_new = re.findall(r'<a href="([^"]*)"[^>]*data-i18n="nav\.(shop|products)"', html_new)
    print(f"New nav links: {nav_links_new}")
    
    if html_new != html:
        # Backup original
        stdin, stdout, stderr = client.exec_command("cp /var/www/frontend/index.html /var/www/frontend/index.html.bak.nav")
        stdout.read()
        
        # Write modified file
        sftp = client.open_sftp()
        with sftp.open('/var/www/frontend/index.html', 'w') as f:
            f.write(html_new)
        sftp.close()
        print("OK - index.html updated!")
        
        # Also fix mobile nav (same file, already handled by replace_all)
        mobile_count = html_new.count('href="/shop.html"')
        print(f"Total /shop.html links: {mobile_count}")
    else:
        print("No changes needed")
    
    # Verify by curling
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost/ | grep -o 'href=\"[^\"]*\"' | grep -E 'shop|products'")
    result = stdout.read().decode()
    print(f"Verification:\n{result}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    client.close()
