import paramiko, base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

changes = []

# === FIX 1: Remove the incorrectly placed settings-menu div ===
# Find and remove the settings-menu that was inserted before .lang-switch
old_settings = """<div class="settings-menu" style="position:relative;margin-left:8px">
      <button class="settings-toggle" onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.3rem;padding:6px 10px;border-radius:8px;color:var(--text2);transition:all .3s" onmouseover="this.style.background='rgba(0,0,0,0.04)'" onmouseout="this.style.background='none'">☰</button>
      <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:0;top:100%;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:160px;z-index:9999;overflow:hidden">
        <a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🔄</span> 版本更新</a>
        <a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🗑️</span> 清除缓存</a>
      </div>
    </div>
    <div class="lang-switch">"""

new_settings = """<div class="lang-switch">"""

if old_settings in html:
    html = html.replace(old_settings, new_settings)
    changes.append("Removed misplaced settings-menu div")

# === FIX 2: Find the nav bar and add settings menu INSIDE it ===
# Find the actual nav HTML structure
nav_idx = html.find('<nav')
if nav_idx > 0:
    nav_end = html.find('</nav>', nav_idx)
    nav_html = html[nav_idx:nav_end+6]
    
    # Find where the language switcher is in the nav
    # We need to add the ☰ button right before the lang-switch inside nav-right
    lang_in_nav = nav_html.find('lang-switch')
    if lang_in_nav > 0:
        # Add settings button right before lang-switch in the nav
        settings_in_nav = """<button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:6px;color:#555" title="设置">☰</button>
      """
        nav_html_new = nav_html.replace('<div class="lang-switch">', settings_in_nav + '<div class="lang-switch">')
        html = html.replace(nav_html, nav_html_new)
        changes.append("Added ☰ button inside nav before lang-switch")
    else:
        changes.append("WARNING: lang-switch not found in nav")
else:
    changes.append("WARNING: <nav> not found")

# === FIX 3: Also add version update to mobile bottom nav ===
# The mobile nav currently has: 首页, 产品, 咨询
# Add 设置 option
mobile_nav_old = """<a href="#contact"><span class="icon">💬</span>${i18n[lang].mobile_consult}</a>
        
        </div>`;"""

mobile_nav_new = """<a href="#contact"><span class="icon">💬</span>${i18n[lang].mobile_consult}</a>
          <a href="javascript:void(0)" onclick="checkAppUpdate()"><span class="icon">⚙️</span>更新</a>
        </div>`;"""

if mobile_nav_old in html:
    html = html.replace(mobile_nav_old, mobile_nav_new)
    changes.append("Added version update to mobile bottom nav")

# === FIX 4: Check for duplicate submitOrder function ===
import re
func_count = html.count('function submitOrder')
if func_count > 1:
    changes.append(f"WARNING: {func_count} submitOrder functions found!")
    # Find both and remove the second (old) one
    first_idx = html.find('function submitOrder')
    second_idx = html.find('function submitOrder', first_idx + 10)
    if second_idx > first_idx:
        # Find the end of the second function
        # Read the second function
        second_func = html[second_idx:]
        brace_count = 0
        end_idx = 0
        for i, ch in enumerate(second_func):
            if ch == '{': brace_count += 1
            elif ch == '}': 
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break
        if end_idx > 0:
            duplicate = html[second_idx:second_idx+end_idx]
            html = html.replace(duplicate, '')
            changes.append(f"Removed duplicate submitOrder function ({end_idx} chars)")

# === FIX 5: Also fix the old submitOrder that still uses wrong IDs ===
# Check if there's still a reference to orderName, orderPhone, orderAddr
old_refs = ['orderName', 'orderPhone', 'orderAddr', 'orderTitle', 'orderPrice']
for ref in old_refs:
    count = html.count(f"getElementById('{ref}')")
    if count > 0:
        changes.append(f"WARNING: Still has {count} ref to {ref}")

# Validate JS
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

with open('D:/tokai/fix_v2_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"File size: {len(html)}\n")
    f.write(f"Braces: {js.count('{')}:{js.count('}')}\n")
    f.write(f"submitOrder count: {html.count('function submitOrder')}\n")
    for c in changes:
        f.write(f"  {c}\n")

# Upload to server
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
cmd = f"echo '{encoded}' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()

# Save local
with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Validate JS on server
val_cmd = '''node -e "
const fs = require('fs');
const html = fs.readFileSync('/var/www/frontend/index.html', 'utf8');
const start = html.indexOf('<script>') + 8;
const end = html.lastIndexOf('</script>');
const js = html.substring(start, end);
try {
    new Function(js);
    console.log('JS OK, len=' + js.length);
} catch(e) {
    console.log('JS ERROR: ' + e.message);
}
"'''
stdin, stdout, stderr = ssh.exec_command(val_cmd)
js_val = stdout.read().decode()

with open('D:/tokai/fix_v2_result.txt', 'a', encoding='utf-8') as f:
    f.write(f"Server validation: {js_val}\n")

ssh.close()

for c in changes:
    print(f"  {c}")
print(f"JS: {js_val}")
