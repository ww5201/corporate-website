#!/bin/bash
python3 << 'PYEOF'
import re
f = open("/var/www/frontend/index.html", "r")
c = f.read()
f.close()
print("size:", len(c))
if len(c) > 100:
    fixed = re.sub(r"(:\s*'[^']+')(\n\s+[a-z_]+:)", r"\1,\2", c)
    g = open("/var/www/frontend/index.html", "w")
    g.write(fixed)
    g.close()
    print("fixed:", len(fixed))
    import os
    os.system("nginx -s reload")
    print("DONE")
else:
    print("EMPTY - need full upload")
PYEOF
