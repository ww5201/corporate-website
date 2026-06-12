import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

# Add CSS for .menu.show inside the @media (max-width:768px) block
# Find the @media block that has .menu { display:none }
media_marker = '@media (max-width:768px)'
media_idx = html.find(media_marker)
if media_idx >= 0:
    # Find the .menu { display:none } inside this media block
    menu_hide = '.menu { display:none; }'
    menu_idx = html.find(menu_hide, media_idx)
    if menu_idx >= 0:
        # Add .menu.show style right after .menu { display:none }
        insert_after = menu_idx + len(menu_hide)
        show_css = "\n      .menu.show { display:block; position:absolute; top:100%; left:0; right:0; background:#fff; box-shadow:0 8px 30px rgba(0,0,0,0.12); border-radius:0 0 16px 16px; z-index:999; padding:16px 24px; }"
        html = html[:insert_after] + show_css + html[insert_after:]
        print("Added .menu.show CSS")
    else:
        print(".menu { display:none } not found in media query")
else:
    print("Media query not found")

# Upload
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(html)
f.close()
sftp.close()

# Verify
with open('D:/tokai/verify_show.txt', 'w', encoding='utf-8') as f:
    f.write(f"File: {len(html)} bytes\n")
    f.write(f".menu.show in CSS: {'.menu.show' in html}\n")
    f.write(f"toggleMenu in JS: {'function toggleMenu' in html}\n")
    f.write(f"toggleMenu in HTML: {'toggleMenu' in html}\n")

print(f"File: {len(html)} bytes")
print("Done")
ssh.close()
