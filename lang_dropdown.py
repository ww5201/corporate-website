import paramiko

# 读取前端文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 替换 CSS - 把语言按钮改成下拉菜单
old_css = '''    .lang-switch { display:flex; align-items:center; gap:4px; margin-left:16px; padding-left:16px; border-left:1px solid rgba(0,0,0,0.08); }
    .lang-btn { background:none; border:none; cursor:pointer; font-size:0.85rem; padding:4px 8px; border-radius:6px; transition:all 0.3s; color:var(--text2); }
    .lang-btn.active { background:var(--accent); color:#fff; }
    .lang-btn:hover:not(.active) { background:rgba(0,0,0,0.04); }'''

new_css = '''    .lang-switch { position:relative; margin-left:16px; padding-left:16px; border-left:1px solid rgba(0,0,0,0.08); }
    .lang-toggle { background:none; border:none; cursor:pointer; font-size:0.88rem; padding:6px 12px; border-radius:8px; transition:all 0.3s; color:var(--text2); display:flex; align-items:center; gap:6px; }
    .lang-toggle:hover { background:rgba(0,0,0,0.04); }
    .lang-toggle .arrow { font-size:0.6rem; transition:transform 0.3s; }
    .lang-dropdown { position:absolute; top:100%; right:0; background:#fff; border-radius:12px; box-shadow:0 8px 32px rgba(0,0,0,0.12); min-width:140px; padding:8px 0; opacity:0; visibility:hidden; transform:translateY(-8px); transition:all 0.3s; z-index:100; }
    .lang-dropdown.open { opacity:1; visibility:visible; transform:translateY(4px); }
    .lang-dropdown button { display:block; width:100%; padding:10px 16px; background:none; border:none; cursor:pointer; font-size:0.88rem; text-align:left; transition:all 0.2s; color:var(--text1); }
    .lang-dropdown button:hover { background:rgba(184,149,106,0.08); color:var(--accent-dark); }
    .lang-dropdown button.active { color:var(--accent-dark); font-weight:600; background:rgba(184,149,106,0.1); }'''

html = html.replace(old_css, new_css)

# 2. 替换 HTML - 把按钮改成下拉菜单
old_html = '''      <div class="lang-switch">
        <button class="lang-btn active" onclick="setLang('zh')">中文</button>
        <button class="lang-btn" onclick="setLang('en')">EN</button>
        <button class="lang-btn" onclick="setLang('ja')">日本語</button>
        <button class="lang-btn" onclick="setLang('ko')">한국어</button>
        <button class="lang-btn" onclick="setLang('th')">ไทย</button>
        <button class="lang-btn" onclick="setLang('vi')">Tiếng Việt</button>
        <button class="lang-btn" onclick="setLang('ms')">Melayu</button>
      </div>'''

new_html = '''      <div class="lang-switch">
        <button class="lang-toggle" onclick="toggleLangMenu(event)">
          <span id="currentLangLabel">中文</span>
          <span class="arrow">▼</span>
        </button>
        <div class="lang-dropdown" id="langDropdown">
          <button class="active" onclick="setLang('zh')">🇨🇳 中文</button>
          <button onclick="setLang('en')">🇺🇸 English</button>
          <button onclick="setLang('ja')">🇯🇵 日本語</button>
          <button onclick="setLang('ko')">🇰🇷 한국어</button>
          <button onclick="setLang('th')">🇹🇭 ไทย</button>
          <button onclick="setLang('vi')">🇻🇳 Tiếng Việt</button>
          <button onclick="setLang('ms')">🇲🇾 Melayu</button>
        </div>
      </div>'''

html = html.replace(old_html, new_html)

# 3. 更新 setLang 函数 - 更新下拉菜单状态
old_setlang = '''    function setLang(lang) {
      currentLang = lang;
      localStorage.setItem('lang', lang);
      document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.textContent.toLowerCase().includes(lang === 'zh' ? '中文' : 'en')));'''

new_setlang = '''    function toggleLangMenu(e) {
      e.stopPropagation();
      document.getElementById('langDropdown').classList.toggle('open');
    }
    document.addEventListener('click', () => document.getElementById('langDropdown').classList.remove('open'));

    const langLabels = { zh:'中文', en:'English', ja:'日本語', ko:'한국어', th:'ไทย', vi:'Tiếng Việt', ms:'Melayu' };
    function setLang(lang) {
      currentLang = lang;
      localStorage.setItem('lang', lang);
      document.getElementById('currentLangLabel').textContent = langLabels[lang] || lang;
      document.querySelectorAll('#langDropdown button').forEach(b => b.classList.toggle('active', b.textContent.includes(langLabels[lang])));
      document.getElementById('langDropdown').classList.remove('open');'''

html = html.replace(old_setlang, new_setlang)

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Language menu converted to dropdown!")

# 上传
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
sftp.put(r'D:\tokai\index-v4.html', '/var/www/frontend/index.html')
sftp.close()
ssh.exec_command("nginx -s reload")
ssh.close()
print("Uploaded!")
