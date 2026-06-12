import base64

data = open('D:/tokai/index-fixed2.html', 'rb').read()
b64 = base64.b64encode(data).decode()

# Try larger chunks - Cloud Assistant might accept bigger commands
chunk_size = 20000
chunks = [b64[i:i+chunk_size] for i in range(0, len(b64), chunk_size)]

print(f'Total b64: {len(b64)} chars')
print(f'Chunks: {len(chunks)}')

# Generate commands
cmds = []
# First: clear old file
cmds.append('#!/bin/bash\n> /tmp/html.b64\n> /tmp/html.gz.b64\n')
for i, chunk in enumerate(chunks):
    cmds.append(f"#!/bin/bash\necho '{chunk}' >> /tmp/html.b64\n")

# Final decode command
cmds.append("#!/bin/bash\nbase64 -d /tmp/html.b64 > /var/www/frontend/index.html\nwc -c /var/www/frontend/index.html\nnginx -s reload\necho DONE")

for i, cmd in enumerate(cmds):
    fname = f'D:/tokai/ca_cmd{i}.sh'
    open(fname, 'w').write(cmd)
    print(f'ca_cmd{i}.sh: {len(cmd)} bytes')

print(f'Total commands: {len(cmds)}')
