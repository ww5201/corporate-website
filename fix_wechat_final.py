import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Find the handleWechatClick function
idx = html.find('function handleWechatClick')
if idx < 0:
    print("ERROR: function not found!")
    exit(1)

print(f"Function at {idx}")

# Find the full function: from "function handleWechatClick()" to after the closing "}"
# After the function ends, the next line starts with "// =====" (startup section)
# Find the last "}" in the function that is followed by newline+newline+// =====
start_marker = "function handleWechatClick()"
end_marker = "\n    }\n    \n    // ====="

func_start = html.find(start_marker)
func_end = html.find(end_marker, func_start)

if func_end < 0:
    print("End marker not found, trying alternatives...")
    # Look for the pattern after showWechatGuide
    after_func = html.find('showWechatGuide(false);', idx)
    if after_func >= 0:
        # Find the closing } after this
        rest = html[after_func:]
        context = rest[:300]
        print(f"Context after showWechatGuide:\n{repr(context)}")
        
        # The function should end with showWechatGuide(false);\n    }
        # Find the } that closes it
        close_pos = html.find('\n    }\n    \n    // =====', after_func)
        if close_pos > 0:
            func_end = close_pos
            print(f"Found end at {close_pos}")
        else:
            # Try just after the } right after showWechatGuide
            close_pos = html.find('\n    }', after_func)
            if close_pos > 0:
                func_end = close_pos + 6  # include the }
                print(f"Found end at {func_end} via close bracket")

old_func = html[func_start:func_end]
print(f"\nOld function ({len(old_func)} chars):")
print(old_func[:150])
print("...")
print(old_func[-150:])

# New simple function: copy to clipboard + guide overlay
new_func = """function handleWechatClick() {
    var wechatNum = '18977122166';
    var copied = false;
    
    // Copy to clipboard
    try {
        var ta = document.createElement('textarea');
        ta.value = wechatNum;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        copied = true;
    } catch(e) {}
    
    // Show guide overlay
    showWechatGuide(copied);"""

if old_func != new_func:
    html = html[:func_start] + new_func + html[func_end:]
    print(f"\nReplaced! New size: {len(html)} chars")
else:
    print("\nAlready matching, no change needed")

# Upload
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
cmd = "echo '" + encoded + "' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()

ssh.exec_command('nginx -s reload')

with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

ssh.close()
print("Done!")
