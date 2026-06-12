import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

print(f"Before: {len(html)}")

# === 1. Remove duplicate ☰ button (keep only one) ===
button = '<button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:4px 8px;border-radius:6px;color:#555;margin-right:8px" title="设置">\u2630</button>'
count = html.count(button)
print(f"Button count: {count}")

# Remove all instances and add back clean one later
html = html.replace(button, '')
print(f"After removing buttons: {len(html)}")

# === 2. Remove old lang-switch div ===
# Find and remove the lang-switch block
lang_block_start = html.find('<div class="lang-switch">')
if lang_block_start >= 0:
    lang_block_end = html.find('</div>', lang_block_start) + 6
    # There might be nested divs, find the right closing
    depth = 0
    for i in range(lang_block_start, len(html)):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                lang_block_end = i + 6
                break
    old_lang = html[lang_block_start:lang_block_end]
    html = html[:lang_block_start] + html[lang_block_end:]
    print(f"Removed lang-switch block ({len(old_lang)} chars)")

# === 3. Remove old settings-dropdown divs ===
while True:
    dd_start = html.find('<div class="settings-dropdown"')
    if dd_start < 0:
        break
    depth = 0
    dd_end = dd_start
    for i in range(dd_start, len(html)):
        if html[i:i+4] == '<div':
            depth += 1
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                dd_end = i + 6
                break
    html = html[:dd_start] + html[dd_end:]
    print(f"Removed settings-dropdown block")

# === 4. Add settings button (gear icon) before </nav> ===
# Clean up any extra whitespace
html = html.replace('\n      \n    </nav>', '\n    </nav>')
html = html.replace('\n    </div>\n\n    </nav>', '\n    </div>\n    </nav>')

# Find the first </nav> (desktop nav)
first_nav_end = html.find('</nav>')
if first_nav_end >= 0:
    # Add settings button and dropdown before </nav>
    settings_block = '''
      <div style="position:relative;margin-left:8px">
        <button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:6px 10px;border-radius:8px;color:#555;transition:all .3s" onmouseover="this.style.background='rgba(0,0,0,0.04)'" onmouseout="this.style.background='none'">\u2699</button>
        <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:0;top:100%;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:200px;z-index:9999;overflow:hidden">
          <div style="padding:12px 16px;border-bottom:1px solid #f0f0f0">
            <div style="font-size:0.75rem;color:#999;margin-bottom:8px">语言 / Language</div>
            <div style="display:flex;flex-wrap:wrap;gap:4px">
              <button onclick="setLang('zh')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem;transition:all .2s" onmouseover="this.style.borderColor='var(--accent)';this.style.color='var(--accent)'" onmouseout="this.style.borderColor='#e0e0e0';this.style.color='#333'">\ud83c\udde8\ud83c\uddf3 中文</button>
              <button onclick="setLang('en')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem;transition:all .2s" onmouseover="this.style.borderColor='var(--accent)';this.style.color='var(--accent)'" onmouseout="this.style.borderColor='#e0e0e0';this.style.color='#333'">\ud83c\uddfa\ud83c\uddf8 EN</button>
              <button onclick="setLang('ja')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem;transition:all .2s" onmouseover="this.style.borderColor='var(--accent)';this.style.color='var(--accent)'" onmouseout="this.style.borderColor='#e0e0e0';this.style.color='#333'">\ud83c\uddef\ud83c\uddf5 \u65e5\u672c\u8a9e</button>
              <button onclick="setLang('ko')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem;transition:all .2s" onmouseover="this.style.borderColor='var(--accent)';this.style.color='var(--accent)'" onmouseout="this.style.borderColor='#e0e0e0';this.style.color='#333'">\ud83c\uddf0\ud83c\uddf7 \ud55c\uad6d\uc5b4</button>
              <button onclick="setLang('th')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem;transition:all .2s" onmouseover="this.style.borderColor='var(--accent)';this.style.color='var(--accent)'" onmouseout="this.style.borderColor='#e0e0e0';this.style.color='#333'">\ud83c\uddf9\ud83c\udded \u0e44\u0e17\u0e22</button>
              <button onclick="setLang('vi')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem;transition:all .2s" onmouseover="this.style.borderColor='var(--accent)';this.style.color='var(--accent)'" onmouseout="this.style.borderColor='#e0e0e0';this.style.color='#333'">\ud83c\uddfb\ud83c\uddf3 Ti\u1ebfng Vi\u1ec7t</button>
              <button onclick="setLang('ms')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem;transition:all .2s" onmouseover="this.style.borderColor='var(--accent)';this.style.color='var(--accent)'" onmouseout="this.style.borderColor='#e0e0e0';this.style.color='#333'">\ud83c\uddf2\ud83c\uddfe Melayu</button>
            </div>
          </div>
          <a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>\U0001f504</span> \u7248\u672c\u66f4\u65b0</a>
          <a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>\U0001f5d1\ufe0f</span> \u6e05\u9664\u7f13\u5b58</a>
        </div>
      </div>
'''
    html = html[:first_nav_end] + settings_block + '    ' + html[first_nav_end:]
    print("Added settings button with gear icon + language + update + cache")

# === 5. Remove old lang CSS (since lang-switch is gone) ===
# Keep lang-toggle and lang-dropdown CSS for now in case mobile nav uses them
# But remove the standalone .lang-switch style
html = html.replace('.lang-switch { position:relative; margin-left:16px; padding-left:16px; border-left:1px solid rgba(0,0,0,0.08); }', '.lang-switch { display:none; }')

# === 6. Fix toggleSettings function ===
# Make sure it works with the new structure
old_toggle = '''function toggleSettings() {
      var dd = document.getElementById('settingsDropdown');
      if (dd) dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
    }'''
new_toggle = '''function toggleSettings(e) {
      if (e) e.stopPropagation();
      var dd = document.getElementById('settingsDropdown');
      if (dd) dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
    }
    document.addEventListener('click', function(e) {
      var dd = document.getElementById('settingsDropdown');
      if (dd && !e.target.closest('.settings-dropdown') && !e.target.closest('[onclick*="toggleSettings"]')) {
        dd.style.display = 'none';
      }
    });'''

if old_toggle in html:
    html = html.replace(old_toggle, new_toggle)
    print("Updated toggleSettings function")
else:
    print("WARNING: toggleSettings pattern not found exactly")

# === 7. Fix setLang to update current language display ===
# The old setLang might reference currentLangLabel
# Add a visual indicator in the settings dropdown

# Validate JS
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]
print(f"\nJS braces: {js.count('{')}:{js.count('}')}")

# Save locally
with open(r'D:/tokai/index-settings.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Upload
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'w') as f:
    f.write(html)
sftp.close()

# Verify
stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html')
size = stdout.read().decode('utf-8').strip()

stdin, stdout, stderr = ssh.exec_command("node -e \"const fs=require('fs');const h=fs.readFileSync('/var/www/frontend/index.html','utf8');const s=h.indexOf('<script>')+8;const e=h.lastIndexOf('</script>');const j=h.substring(s,e);try{new Function(j);console.log('JS:OK');}catch(err){console.log('ERR:'+err.message);}\"")
js_val = stdout.read().decode('utf-8').strip()

ssh.close()

print(f"\nServer: {size}, JS: {js_val}")
print(f"Local: D:/tokai/index-settings.html ({len(html)} bytes)")
