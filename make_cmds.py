import base64
data = open('D:/tokai/index-fixed2.html','rb').read()
b64 = base64.b64encode(data).decode()
# Split into 3 chunks for Cloud Assistant (limit ~16KB per command)
third = len(b64) // 3
chunks = [
    b64[0:third],
    b64[third:2*third],
    b64[2*third:]
]
for i, c in enumerate(chunks):
    # Create shell command that writes this chunk
    cmd = f'''#!/bin/bash
echo '{c}' >> /tmp/html.b64
echo 'chunk_{i}_done'
'''
    open(f'D:/tokai/cmd_{i}.txt', 'w').write(cmd)
    print(f'Command {i}: {len(cmd)} bytes, chunk size: {len(c)}')
print(f'Total base64: {len(b64)}')
