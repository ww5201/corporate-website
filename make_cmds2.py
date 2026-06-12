import base64
data = open('D:/tokai/index-fixed2.html','rb').read()
b64 = base64.b64encode(data).decode()
# Split into chunks of ~12000 chars (under 16KB limit with overhead)
chunk_size = 12000
chunks = [b64[i:i+chunk_size] for i in range(0, len(b64), chunk_size)]
print(f'Total base64: {len(b64)}')
print(f'Number of chunks: {len(chunks)}')
for i, c in enumerate(chunks):
    cmd = "#!/bin/bash\necho '" + c + "' >> /tmp/html.b64\necho 'chunk_" + str(i) + "_done'"
    open(f'D:/tokai/cmd_{i}.txt', 'w').write(cmd)
    print(f'Command {i}: {len(cmd)} bytes')
# Final decode command
final_cmd = '''#!/bin/bash
base64 -d /tmp/html.b64 > /var/www/frontend/index.html
nginx -s reload
echo 'RECOVERY_COMPLETE'
wc -c /var/www/frontend/index.html
'''
open('D:/tokai/cmd_final.txt', 'w').write(final_cmd)
print(f'Final command: {len(final_cmd)} bytes')
print(f'Total commands: {len(chunks) + 1}')
