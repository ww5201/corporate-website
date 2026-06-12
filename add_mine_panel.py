import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

changes = []

# 1. Add mobile_mine translations to all 7 languages
lang_translations = {
    'zh': {'mobile_mine': '我的', 'mine_title': '个人中心', 'mine_settings': '系统设置', 'mine_login': '登录/注册', 'mine_bindwx': '绑定微信', 'mine_bindphone': '绑定手机号', 'mine_logout': '退出登录', 'mine_version': '当前版本'},
    'en': {'mobile_mine': 'Mine', 'mine_title': 'My Account', 'mine_settings': 'Settings', 'mine_login': 'Login/Register', 'mine_bindwx': 'Bind WeChat', 'mine_bindphone': 'Bind Phone', 'mine_logout': 'Logout', 'mine_version': 'Version'},
    'ja': {'mobile_mine': '私', 'mine_title': 'マイページ', 'mine_settings': '設定', 'mine_login': 'ログイン', 'mine_bindwx': 'WeChat連携', 'mine_bindphone': '電話番号連携', 'mine_logout': 'ログアウト', 'mine_version': 'バージョン'},
    'ko': {'mobile_mine': '나', 'mine_title': '내 정보', 'mine_settings': '설정', 'mine_login': '로그인', 'mine_bindwx': '위챗 연동', 'mine_bindphone': '전화번호 연동', 'mine_logout': '로그아웃', 'mine_version': '버전'},
    'th': {'mobile_mine': 'ฉัน', 'mine_title': 'บัญชีของฉัน', 'mine_settings': 'ตั้งค่า', 'mine_login': 'เข้าสู่ระบบ', 'mine_bindwx': 'เชื่อมต่อ WeChat', 'mine_bindphone': 'เชื่อมต่อเบอร์โทร', 'mine_logout': 'ออกจากระบบ', 'mine_version': 'เวอร์ชัน'},
    'vi': {'mobile_mine': 'Tôi', 'mine_title': 'Tài khoản', 'mine_settings': 'Cài đặt', 'mine_login': 'Đăng nhập', 'mine_bindwx': 'Liên kết WeChat', 'mine_bindphone': 'Liên kết SĐT', 'mine_logout': 'Đăng xuất', 'mine_version': 'Phiên bản'},
    'ms': {'mobile_mine': 'Saya', 'mine_title': 'Akaun Saya', 'mine_settings': 'Tetapan', 'mine_login': 'Log Masuk', 'mine_bindwx': 'Sambung WeChat', 'mine_bindphone': 'Sambung Telefon', 'mine_logout': 'Log Keluar', 'mine_version': 'Versi'},
}

for lang, translations in lang_translations.items():
    for key, value in translations.items():
        # Find the key in the i18n section for this language
        marker = f"mobile_products"
        idx = html.find(f"'{marker}':")
        if idx < 0:
            idx = html.find(f'"{marker}":')
        if idx >= 0:
            # Find the end of this line
            line_end = html.find('\n', idx)
            if line_end >= 0:
                # Check if this key already exists
                check_key = f"'{key}'"
                if check_key not in html[idx:idx+200]:
                    new_line = f",\n          '{key}': '{value}'"
                    html = html[:line_end] + new_line + html[line_end:]
                    changes.append(f"Added i18n {lang}.{key}")

# 2. Update mobile nav JS template to add 4th tab
old_mobile_nav = """          <a href="#contact"><span class="icon">💬</span>${i18n[lang].mobile_consult}</a>

          """

new_mobile_nav = """          <a href="#contact"><span class="icon">💬</span>${i18n[lang].mobile_consult}</a>
          <a href="javascript:void(0)" onclick="showMinePanel()"><span class="icon">👤</span>${i18n[lang].mobile_mine}</a>
          """

if old_mobile_nav in html:
    html = html.replace(old_mobile_nav, new_mobile_nav)
    changes.append("Updated mobile nav template - added Mine tab")
else:
    # Try alternative pattern
    old_alt = '<a href="#contact"><span class="icon">💬</span>${i18n[lang].mobile_consult}</a>'
    if old_alt in html:
        html = html.replace(old_alt, old_alt + '\n          <a href="javascript:void(0)" onclick="showMinePanel()"><span class="icon">👤</span>${i18n[lang].mobile_mine}</a>')
        changes.append("Updated mobile nav template (alt pattern)")

# 3. Add user panel HTML before </body>
panel_html = """
    <!-- 我的面板 -->
    <div id="minePanel" style="display:none;position:fixed;bottom:0;left:0;right:0;z-index:200;background:#fff;border-radius:20px 20px 0 0;box-shadow:0 -8px 40px rgba(0,0,0,0.15);padding:0;max-height:70vh;overflow:hidden;transform:translateY(100%);transition:transform 0.35s cubic-bezier(0.4,0,0.2,1)">
      <div style="padding:20px 24px 0;text-align:center">
        <div style="width:40px;height:4px;background:#ddd;border-radius:2px;margin:0 auto 16px"></div>
        <div style="width:64px;height:64px;border-radius:50%;background:linear-gradient(135deg,var(--accent),#d4a574);margin:0 auto 12px;display:flex;align-items:center;justify-content:center;font-size:1.8rem">👤</div>
        <p style="font-size:0.95rem;color:var(--text1);margin:0 0 4px" data-i18n="mine_login">登录/注册</p>
        <p style="font-size:0.75rem;color:var(--text2);margin:0 0 16px" data-i18n="mine_bindwx_hint">登录后绑定微信和手机号</p>
      </div>
      <div style="padding:0 24px 20px">
        <a href="javascript:void(0)" onclick="showLoginPanel()" style="display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:12px;background:var(--accent);color:#fff;text-decoration:none;font-size:0.92rem;margin-bottom:8px">
          <span>🔑</span><span data-i18n="mine_login">登录/注册</span>
        </a>
        <a href="javascript:void(0)" onclick="showSettingsPanel()" style="display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:12px;background:var(--bg2);color:var(--text1);text-decoration:none;font-size:0.92rem;margin-bottom:8px">
          <span>⚙</span><span data-i18n="mine_settings">系统设置</span>
        </a>
        <div style="display:flex;gap:8px;margin-bottom:8px">
          <a href="javascript:void(0)" onclick="bindWechat()" style="flex:1;display:flex;align-items:center;justify-content:center;gap:8px;padding:12px;border-radius:12px;background:#f0fdf4;color:#16a34a;text-decoration:none;font-size:0.85rem">
            <span>💬</span><span data-i18n="mine_bindwx">绑定微信</span>
          </a>
          <a href="javascript:void(0)" onclick="bindPhone()" style="flex:1;display:flex;align-items:center;justify-content:center;gap:8px;padding:12px;border-radius:12px;background:#eff6ff;color:#2563eb;text-decoration:none;font-size:0.85rem">
            <span>📱</span><span data-i18n="mine_bindphone">绑定手机号</span>
          </a>
        </div>
        <div style="text-align:center;padding:8px 0;font-size:0.75rem;color:var(--text2)" data-i18n="mine_version">当前版本 v1.0</div>
      </div>
    </div>
    <div id="minePanelOverlay" onclick="hideMinePanel()" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.4);z-index:199"></div>
"""

body_close = html.rfind('</body>')
if body_close >= 0:
    html = html[:body_close] + panel_html + html[body_close:]
    changes.append("Added user panel HTML")

# 4. Add CSS for mine panel
mine_css = """
    /* ===== 我的面板 ===== */
    #minePanel.show { transform:translateY(0) !important; }
"""
style_end = html.find('</style>')
if style_end >= 0:
    html = html[:style_end] + mine_css + html[style_end:]
    changes.append("Added mine panel CSS")

# 5. Add JS functions
mine_js = """
    // ===== 我的面板 =====
    function showMinePanel() {
      var panel = document.getElementById('minePanel');
      var overlay = document.getElementById('minePanelOverlay');
      if (panel && overlay) {
        overlay.style.display = 'block';
        panel.style.display = 'block';
        setTimeout(function() { panel.classList.add('show'); }, 10);
      }
    }

    function hideMinePanel() {
      var panel = document.getElementById('minePanel');
      var overlay = document.getElementById('minePanelOverlay');
      if (panel && overlay) {
        panel.classList.remove('show');
        setTimeout(function() { panel.style.display = 'none'; overlay.style.display = 'none'; }, 350);
      }
    }

    function showLoginPanel() {
      hideMinePanel();
      showContact();
      alert(i18n[currentLang].mine_login || '请登录');
    }

    function showSettingsPanel() {
      hideMinePanel();
      alert(i18n[currentLang].mine_settings || '系统设置');
    }

    function bindWechat() {
      hideMinePanel();
      handleWechatClick();
    }

    function bindPhone() {
      hideMinePanel();
      showContact();
    }

"""

# Add before startup code
startup_idx = html.find('// ===== 启动')
if startup_idx >= 0:
    html = html[:startup_idx] + mine_js + html[startup_idx:]
    changes.append("Added mine panel JS functions")

# 6. Add mine_bindwx_hint to i18n
hint_translations = {
    'zh': '登录后绑定微信和手机号',
    'en': 'Login to bind WeChat and phone',
    'ja': 'ログインしてWeChatと電話を連携',
    'ko': '로그인 후 위챗과 전화번호를 연동하세요',
    'th': 'เข้าสู่ระบบเพื่อเชื่อมต่อ WeChat และเบอร์โทร',
    'vi': 'Đăng nhập để liên kết WeChat và SĐT',
    'ms': 'Log masuk untuk sambung WeChat dan Telefon',
}

for lang, value in hint_translations.items():
    marker = "'mine_version':"
    idx = html.find(f"'{marker}'") if "'" in marker else html.find(marker)
    if idx >= 0:
        line_end = html.find('\n', idx)
        if line_end >= 0 and "'mine_bindwx_hint'" not in html[idx:idx+300]:
            new_line = f",\n          'mine_bindwx_hint': '{value}'"
            html = html[:line_end] + new_line + html[line_end:]
            changes.append(f"Added i18n {lang}.mine_bindwx_hint")

# Upload
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(html)
f.close()
sftp.close()

with open('D:/tokai/mine_changes.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(changes))

print(f"File: {len(html)} bytes")
print(f"Changes: {len(changes)}")
for c in changes:
    print(f"  {c}")

ssh.close()
