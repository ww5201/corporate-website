import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# Check file size and content
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size1 = stdout.read().decode().strip()

# Check via curl (actual served content)
stdin, stdout, stderr = ssh.exec_command('curl -s http://127.0.0.1/ | wc -c')
size2 = stdout.read().decode().strip()

# Download actual file
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

with open('D:/tokai/verify_upload.txt', 'w', encoding='utf-8') as out:
    out.write(f"File size on disk: {size1}\n")
    out.write(f"Curl size: {size2}\n")
    out.write(f"Actual chars: {len(html)}\n")
    out.write(f"Ends with </html>: {html.rstrip().endswith('</html>')}\n")
    
    # Check for duplicate functions
    import re
    funcs = re.findall(r'function\s+(\w+)', html)
    from collections import Counter
    dupes = {k: v for k, v in Counter(funcs).items() if v > 1}
    if dupes:
        out.write(f"\nDuplicates: {dupes}\n")
    else:
        out.write("\nNo duplicates\n")
    
    # Check handleWechatClick
    if 'window.Android' in html:
        out.write("handleWechatClick: uses Android bridge\n")
    else:
        out.write("handleWechatClick: does NOT use Android bridge\n")
    
    # Check script count
    out.write(f"<script> count: {html.count('<script>')}\n")
    
    # Check last 100 chars
    out.write(f"\nLast 100 chars:\n{html[-100:]}\n")

ssh.close()
print("Done")
