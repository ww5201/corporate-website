import base64

with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

b64 = base64.b64encode(html.encode('utf-8')).decode('ascii')

# Generate a Python one-liner for Workbench
# Split into chunks to avoid terminal issues
chunk_size = 8000  # 8KB per chunk
chunks = [b64[i:i+chunk_size] for i in range(0, len(b64), chunk_size)]

# Method: Write a small Python script to /tmp, then run it
script_lines = [
    "import base64",
    "d=''",
]
for i, chunk in enumerate(chunks):
    script_lines.append("d+='%s'" % chunk)

script_lines.extend([
    "open('/var/www/frontend/index.html','w').write(base64.b64decode(d).decode())",
    "import os; os.system('nginx -s reload')",
    "print('DONE - %d bytes' % len(d))",
])

full_script = '\n'.join(script_lines)

with open('D:/tokai/recover_script.py', 'w', encoding='utf-8') as f:
    f.write(full_script)

print("Script: %d chars, %d lines" % (len(full_script), len(script_lines)))
print("Chunks: %d" % len(chunks))

# Also create the command to run it
cmd = "python3 -c \"%s\"" % full_script.replace('"', r'\"')
with open('D:/tokai/workbench_cmd.txt', 'w', encoding='utf-8') as f:
    f.write(cmd)
print("Command saved to D:/tokai/workbench_cmd.txt")
print("Command length: %d chars" % len(cmd))
