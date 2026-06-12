import base64, os

with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

b64 = base64.b64encode(html.encode('utf-8')).decode('ascii')

# Split base64 into 4KB chunks
chunk_size = 4000
chunks = [b64[i:i+chunk_size] for i in range(0, len(b64), chunk_size)]

# Generate a shell script that appends chunks then decodes
lines = ['#!/bin/bash', '# 卓翌定制网站恢复脚本', '', 'B64=""']
for i, chunk in enumerate(chunks):
    lines.append('B64+="%s"' % chunk)

lines.extend([
    '',
    'echo "$B64" | base64 -d > /var/www/frontend/index.html',
    'echo "Written: $(wc -c < /var/www/frontend/index.html) bytes"',
    'nginx -s reload',
    'echo "=== DONE ==="'
])

script = '\n'.join(lines)

with open('D:/tokai/recover.sh', 'w', encoding='utf-8') as f:
    f.write(script)

print("Script: %d bytes, %d chunks" % (len(script), len(chunks)))
print("Saved to D:/tokai/recover.sh")

# Also show first 3 lines as preview
for line in lines[:5]:
    print("  ", line[:80])
