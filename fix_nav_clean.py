import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

print(f"Before: {len(html)}")

# Find and replace the entire nav section
nav_start = html.find('<nav class="nav"')
nav_end = html.find('</nav>', nav_start) + 6

old_nav = html[nav_start:nav_end]
print(f"Old nav length: {len(old_nav)}")

# New clean nav structure
new_nav = '''<nav class="nav" id="nav">
    <div class="container">
      <a href="#home" class="logo">卓翌<em>定制</em></a>
      <ul class="menu" id="menu">
        <li><a href="#home" class="active" data-i18n="nav_home">首页</a></li>
        <li><a href="#about" data-i18n="nav_about">关于</a></li>
        <li><a href="#services" data-i18n="nav_services">服务</a></li>
        <li><a href="#products" data-i18n="nav_products">产品</a></li>
        <li><a href="#portfolio" data-i18n="nav_portfolio">案例</a></li>
        <li><a href="#contact" data-i18n="nav_contact">联系</a></li>
      </ul>
      <div style="position:relative;margin-left:8px">
        <button onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.2rem;padding:6px 10px;border-radius:8px;color:#555" title="设置">⚙</button>
        <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:0;top:100%;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:200px;z-index:9999;overflow:hidden">
          <div style="padding:12px 16px;border-bottom:1px solid #f0f0f0">
            <div style="font-size:0.75rem;color:#999;margin-bottom:8px">语言 / Language</div>
            <div style="display:flex;flex-wrap:wrap;gap:4px">
              <button onclick="setLang('zh')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem">🇨🇳 中文</button>
              <button onclick="setLang('en')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem">🇺🇸 EN</button>
              <button onclick="setLang('ja')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem">🇯🇵 日本語</button>
              <button onclick="setLang('ko')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem">🇰🇷 한국어</button>
              <button onclick="setLang('th')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem">🇹🇭 ไทย</button>
              <button onclick="setLang('vi')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem">🇻🇳 Tiếng Việt</button>
              <button onclick="setLang('ms')" style="padding:4px 8px;border:1px solid #e0e0e0;border-radius:6px;background:none;cursor:pointer;font-size:0.8rem">🇲🇾 Melayu</button>
            </div>
          </div>
          <a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🔄</span> 版本更新</a>
          <a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🗑️</span> 清除缓存</a>
        </div>
      </div>
      <button class="menu-toggle" onclick="document.getElementById('menu').classList.toggle('open')">☰</button>
    </div>
  </nav>'''

html = html[:nav_start] + new_nav + html[nav_end:]
print(f"After: {len(html)}")

# Validate JS
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]
print(f"JS braces: {js.count('{')}:{js.count('}')}")

# Save locally
with open(r'D:/tokai/index-fixed.html', 'w', encoding='utf-8', errors='surrogatepass') as f:
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
