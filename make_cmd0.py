data = open('D:/tokai/b0.txt', 'r').read()
cmd = '#!/bin/bash\necho \'' + data + '\' >> /tmp/html.b64\necho chunk_0_done'
open('D:/tokai/cmd0.sh', 'w').write(cmd)
print(f'Command size: {len(cmd)}')
