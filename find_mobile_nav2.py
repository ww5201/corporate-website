import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()
sftp.close()

# Search for mobile-nav div element (not CSS)
import re
# Find <div class="mobile-nav" or similar
matches = list(re.finditer(r'<div[^>]*class="[^"]*mobile-nav[^"]*"', html))

with open('D:/tokai/mobile_nav_html.txt', 'w', encoding='utf-8') as f:
    if matches:
        for m in matches:
            start = m.start()
            # Find matching closing div
            end = html.find('</div>', start + 10)
            while end > 0 and html.count('<div', start, end) > html.count('</div>', start, end):
                end = html.find('</div>', end + 1)
            end += 6
            f.write(f"Found at {start}:\n")
            f.write(html[start:end])
            f.write("\n\n---\n\n")
    else:
        f.write("No mobile-nav div found\n\n")
        # Search in JS for mobileNav template
        js_idx = html.find('mobileNav')
        if js_idx >= 0:
            f.write(f"Found 'mobileNav' in JS at {js_idx}:\n")
            start = max(0, js_idx - 200)
            end = min(len(html), js_idx + 500)
            f.write(html[start:end])
        else:
            f.write("'mobileNav' not found anywhere\n")

            # Search for bottom-nav
            for pattern in ['bottom-nav', 'bottomNav', 'mobile_nav']:
                idx = html.find(pattern)
                if idx >= 0:
                    f.write(f"\nFound '{pattern}' at {idx}:\n")
                    f.write(html[max(0,idx-100):idx+300])

print("Done")
ssh.close()
