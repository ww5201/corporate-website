import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()
ssh.close()

with open('D:/tokai/deep_result.txt', 'w', encoding='utf-8') as out:
    out.write(f"Size: {len(html)}\n")

    # Count script tags
    script_starts = []
    pos = 0
    while True:
        idx = html.find('<script>', pos)
        if idx == -1: break
        script_starts.append(idx)
        pos = idx + 8

    script_ends = []
    pos = 0
    while True:
        idx = html.find('</script>', pos)
        if idx == -1: break
        script_ends.append(idx)
        pos = idx + 9

    out.write(f"<script> positions: {script_starts}\n")
    out.write(f"</script> positions: {script_ends}\n\n")

    # Check for duplicate handleWechatClick
    wc_count = 0
    pos = 0
    while True:
        idx = html.find('handleWechatClick', pos)
        if idx == -1: break
        wc_count += 1
        context = html[max(0,idx-20):idx+30]
        out.write(f"handleWechatClick #{wc_count} at {idx}: ...{context}...\n")
        pos = idx + 17

    out.write(f"\nTotal handleWechatClick mentions: {wc_count}\n\n")

    # Check for duplicate loadData calls
    ld_count = 0
    pos = 0
    while True:
        idx = html.find('loadData', pos)
        if idx == -1: break
        ld_count += 1
        context = html[max(0,idx-20):idx+30]
        out.write(f"loadData #{ld_count} at {idx}: ...{context}...\n")
        pos = idx + 8

    out.write(f"\nTotal loadData mentions: {ld_count}\n\n")

    # Check for stray script tags or errors near the end
    last_2k = html[-2000:]
    out.write(f"Last 2000 chars:\n{last_2k}\n")

    # Check brace balance in entire file
    out.write(f"\nFile braces: open={html.count('{')} close={html.count('}')}\n")

    # Check if there's HTML content AFTER </script>
    last_script_end = html.rfind('</script>')
    after = html[last_script_end:]
    out.write(f"\nAfter last </script>:\n{after}\n")

print("Done")
