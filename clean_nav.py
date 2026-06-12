import paramiko, base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

changes = []

# === STEP 1: Remove ALL settings-menu related HTML ===
# Remove the big misplaced settings-menu div
old_menu1 = """<div class="settings-menu" style="position:relative;margin-left:8px">
      <button class="settings-toggle" onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.3rem;padding:6px 10px;border-radius:8px;color:var(--text2);transition:all .3s" onmouseover="this.style.background='rgba(0,0,0,0.04)'" onmouseout="this.style.background='none'">☰</button>
      <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:0;top:100%;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:160px;z-index:9999;overflow:hidden">
        <a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🔄</span> 版本更新</a>
        <a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🗑️</span> 清除缓存</a>
      </div>
    </div>
    """

if old_menu1 in html:
    html = html.replace(old_menu1, '')
    changes.append("Removed old misplaced settings-menu")

# Remove the inline ☰ button I added
old_menu2 = """<button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:6px;color:#555" title="设置">☰</button>
      """

if old_menu2 in html:
    html = html.replace(old_menu2, '')
    changes.append("Removed inline ☰ button")

# === STEP 2: Add clean settings button inside nav, before lang-switch ===
# Find the nav structure and add it properly
nav_pattern = """<li><a href="#contact" data-i18n="nav_contact">联系</a></li>

      </ul>

      
    <div class="lang-switch">"""

nav_fixed = """<li><a href="#contact" data-i18n="nav_contact">联系</a></li>

      </ul>

      <button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:6px;color:#555;margin-right:8px" title="设置">☰</button>
      <div class="lang-switch">"""

if nav_pattern in html:
    html = html.replace(nav_pattern, nav_fixed)
    changes.append("Added ☰ button in nav before lang-switch")

# === STEP 3: Add the dropdown menu HTML (hidden by default) ===
# Add right after lang-switch div closes, before </nav>
# First find where to insert
dropdown_html = """
      <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:80px;top:60px;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:160px;z-index:9999;overflow:hidden">
        <a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🔄</span> 版本更新</a>
        <a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🗑️</span> 清除缓存</a>
      </div>
"""

# Insert before </nav> but after all nav content
# Find </nav> and insert before it
if '</nav>' in html and '<div class="settings-dropdown"' not in html:
    html = html.replace('</nav>', dropdown_html + '\n    </nav>')
    changes.append("Added settings dropdown")

# === STEP 4: Verify no duplicate content ===
# Check file size
print(f"New size: {len(html)} chars (was 87091)")

# Validate JS
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

# Upload
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
cmd = f"echo '{encoded}' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()

with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Validate on server
val_cmd = '''node -e "
const fs = require('fs');
const html = fs.readFileSync('/var/www/frontend/index.html', 'utf8');
const s = html.indexOf('<script>') + 8;
const e = html.lastIndexOf('</script>');
const js = html.substring(s, e);
try { new Function(js); console.log('JS:OK,len=' + js.length); } catch(err) { console.log('JS:ERR:' + err.message); }
"'''
stdin, stdout, stderr = ssh.exec_command(val_cmd)
js_val = stdout.read().decode()

# Check nav structure
stdin, stdout, stderr = ssh.exec_command("sed -n '/<nav/,/<\\/nav>/p' /var/www/frontend/index.html | head -30")
nav_result = stdout.read().decode()

ssh.close()

for c in changes:
    print(f"  {c}")
print(f"JS: {js_val}")
print(f"\nNAV preview:\n{nav_result[:800]}")
