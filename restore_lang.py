import paramiko
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

# Find and replace the nav section
nav_start = html.find('<nav class="nav"')
nav_end = html.find('</nav>', nav_start) + 6

# New nav with standalone language switcher + settings button
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
      <div class="lang-switch">
        <button class="lang-toggle" onclick="toggleLang(event)"><span id="currentLangLabel">中文</span> <span class="arrow">▼</span></button>
        <div class="lang-dropdown" id="langDropdown">
          <button onclick="setLang('zh')">🇨🇳 中文</button>
          <button onclick="setLang('en')">🇺🇸 English</button>
          <button onclick="setLang('ja')">🇯🇵 日本語</button>
          <button onclick="setLang('ko')">🇰🇷 한국어</button>
          <button onclick="setLang('th')">🇹🇭 ไทย</button>
          <button onclick="setLang('vi')">🇻🇳 Tiếng Việt</button>
          <button onclick="setLang('ms')">🇲🇾 Melayu</button>
        </div>
      </div>
      <div style="position:relative">
        <button onclick="toggleSettings(event)" style="background:none;border:none;cursor:pointer;font-size:1.1rem;padding:6px 8px;border-radius:8px;color:#555" title="设置">⚙</button>
        <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:0;top:100%;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:160px;z-index:9999;overflow:hidden">
          <a onclick="checkAppUpdate()" style="display:block;padding:12px 16px;cursor:pointer;font-size:0.88rem;color:#333;text-decoration:none">🔄 版本更新</a>
          <a onclick="clearCache()" style="display:block;padding:12px 16px;cursor:pointer;font-size:0.88rem;color:#333;text-decoration:none">🗑️ 清除缓存</a>
        </div>
      </div>
      <button class="menu-toggle" onclick="toggleMenu()" aria-label="Menu">☰</button>
    </div>
  </nav>'''

html = html[:nav_start] + new_nav + html[nav_end:]

# Fix setLang function - restore currentLangLabel and langDropdown references
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

# Restore the langDropdown active state update
old_active = """      // Update active state on language buttons in settings dropdown
      document.querySelectorAll('#settingsDropdown button[onclick^="setLang"]').forEach(btn => {
        const btnLang = btn.getAttribute('onclick').match(/setLang\\('([a-z]+)'\\)/);
        if (btnLang && btnLang[1] === lang) {
          btn.style.background = '#f5f5f5';
          btn.style.borderColor = '#007bff';
        } else {
          btn.style.background = 'none';
          btn.style.borderColor = '#e0e0e0';
        }
      });"""

new_active = """      // Update lang label
      var langLabel = document.getElementById('currentLangLabel');
      if (langLabel) langLabel.textContent = langLabels[lang] || lang;
      // Update active state on language buttons
      document.querySelectorAll('#langDropdown button').forEach(function(b) {
        b.classList.toggle('active', b.textContent.includes(langLabels[lang]));
      });
      // Close dropdown
      var ld = document.getElementById('langDropdown');
      if (ld) ld.classList.remove('open');"""

if old_active in js:
    js = js.replace(old_active, new_active)
    print("Restored langDropdown active state update")
else:
    print("Active state pattern not found, trying alternative...")
    # Try finding the comment
    idx = js.find('// Update active state on language buttons in settings dropdown')
    if idx >= 0:
        # Find the end of this block
        end_idx = js.find('\n\n', idx)
        if end_idx < 0:
            end_idx = idx + 500
        js = js[:idx] + new_active + js[end_idx:]
        print("Replaced via comment search")

# Add toggleLang function if missing
if 'function toggleLang' not in js:
    toggle_lang = """
    function toggleLang(e) {
      if(e) e.stopPropagation();
      var ld = document.getElementById('langDropdown');
      if(ld) ld.classList.toggle('open');
    }"""
    # Add before toggleSettings
    ts_idx = js.find('function toggleSettings')
    if ts_idx >= 0:
        js = js[:ts_idx] + toggle_lang + '\n' + js[ts_idx:]
        print("Added toggleLang function")

# Add langLabels if missing
if 'var langLabels' not in js and 'langLabels' not in js:
    lang_labels = """
    var langLabels = {zh:'中文',en:'English',ja:'日本語',ko:'한국어',th:'ไทย',vi:'Tiếng Việt',ms:'Melayu'};"""
    # Add after currentLang
    cl_idx = js.find('var currentLang')
    if cl_idx >= 0:
        end_line = js.find('\n', cl_idx)
        js = js[:end_line+1] + lang_labels + js[end_line+1:]
        print("Added langLabels")

# Add click-outside handler for langDropdown if missing
if "getElementById('langDropdown')" not in js:
    # Add after existing click-outside handler
    handler = """
    document.addEventListener('click', function(e) {
      var ld = document.getElementById('langDropdown');
      if(ld && !e.target.closest('.lang-switch')) ld.classList.remove('open');
    });"""
    # Add before startup
    startup_idx = js.find('// ===== 启动')
    if startup_idx >= 0:
        js = js[:startup_idx] + handler + '\n\n' + js[startup_idx:]
        print("Added langDropdown click-outside handler")

# Rebuild HTML
html = html[:js_start] + js + html[js_end:]

# Upload
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(html)
f.close()
sftp.close()

# Save local
with open('D:/tokai/server_nav_restored.html', 'w', encoding='utf-8') as out:
    out.write(html)

# Verify
final_js = html[html.find('<script>')+8:html.rfind('</script>')]
print(f"\nFile: {len(html)} bytes")
print(f"JS braces: {final_js.count(chr(123))}:{final_js.count(chr(125))}")
print(f"lang-switch in HTML: {'lang-switch' in html[:html.find('<script>')]}")
print(f"langDropdown in JS: {'langDropdown' in final_js}")
print(f"currentLangLabel in JS: {'currentLangLabel' in final_js}")
print(f"toggleLang in JS: {'function toggleLang' in final_js}")

ssh.close()
