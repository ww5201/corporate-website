import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# The file ends with: showWechatGuide(false);\n</script>\n</body>\n</html>
# Missing: the startup section that calls loadCases(), setLang(), loadData()

old_end = "showWechatGuide(false);\n</script>\n</body>\n</html>"
new_end = """showWechatGuide(false);
    }

    // ===== 启动 =====
    loadCases();
    setLang(currentLang);
    loadData();
  </script>
</body>
</html>"""

if old_end in html:
    html = html.replace(old_end, new_end)
    print("Added missing startup code")
else:
    print("Pattern not found, trying alternative...")
    # Try without \n variations
    if html.endswith('</html>\n'):
        print("File ends with </html>")
        # Find last </script> and replace from there
        last_script = html.rfind('</script>')
        if last_script > 0:
            print(f"Last </script> at {last_script}")
            print(f"Context: {repr(html[last_script-30:last_script+20])}")

# Verify balance
js_start = html.find('<script>', html.find('<head>') + 100)
rest = html[js_start:]
open_b = rest.count('{')
close_b = rest.count('}')
print(f"\nBraces: open={open_b}, close={close_b}, diff={open_b-close_b}")
print(f"loadCases(): {'loadCases()' in html}")
print(f"setLang(currentLang): {'setLang(currentLang)' in html}")
print(f"loadData(): {'loadData()' in html}")
print(f"Total size: {len(html)}")

# Upload
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
cmd = "echo '" + encoded + "' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()

ssh.exec_command('nginx -s reload')

# Save local
with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

ssh.close()
print("Done!")
