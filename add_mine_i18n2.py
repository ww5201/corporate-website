import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

translations = {
    'zh': [
        ("mobile_mine", "我的"), ("mine_title", "个人中心"), ("mine_settings", "系统设置"),
        ("mine_login", "登录/注册"), ("mine_bindwx", "绑定微信"), ("mine_bindphone", "绑定手机号"),
        ("mine_bindwx_hint", "登录后绑定微信和手机号"), ("mine_logout", "退出登录"), ("mine_version", "当前版本"),
    ],
    'en': [
        ("mobile_mine", "Mine"), ("mine_title", "My Account"), ("mine_settings", "Settings"),
        ("mine_login", "Login/Register"), ("mine_bindwx", "Bind WeChat"), ("mine_bindphone", "Bind Phone"),
        ("mine_bindwx_hint", "Login to bind WeChat and phone"), ("mine_logout", "Logout"), ("mine_version", "Version"),
    ],
    'ja': [
        ("mobile_mine", "私"), ("mine_title", "マイページ"), ("mine_settings", "設定"),
        ("mine_login", "ログイン"), ("mine_bindwx", "WeChat連携"), ("mine_bindphone", "電話番号連携"),
        ("mine_bindwx_hint", "ログインしてWeChatと電話を連携"), ("mine_logout", "ログアウト"), ("mine_version", "バージョン"),
    ],
    'ko': [
        ("mobile_mine", "나"), ("mine_title", "내 정보"), ("mine_settings", "설정"),
        ("mine_login", "로그인"), ("mine_bindwx", "위챗 연동"), ("mine_bindphone", "전화번호 연동"),
        ("mine_bindwx_hint", "로그인 후 위챗과 전화번호를 연동하세요"), ("mine_logout", "로그아웃"), ("mine_version", "버전"),
    ],
    'th': [
        ("mobile_mine", "ฉัน"), ("mine_title", "บัญชีของฉัน"), ("mine_settings", "ตั้งค่า"),
        ("mine_login", "เข้าสู่ระบบ"), ("mine_bindwx", "เชื่อมต่อ WeChat"), ("mine_bindphone", "เชื่อมต่อเบอร์โทร"),
        ("mine_bindwx_hint", "เข้าสู่ระบบเพื่อเชื่อมต่อ WeChat และเบอร์โทร"), ("mine_logout", "ออกจากระบบ"), ("mine_version", "เวอร์ชัน"),
    ],
    'vi': [
        ("mobile_mine", "Tôi"), ("mine_title", "Tài khoản"), ("mine_settings", "Cài đặt"),
        ("mine_login", "Đăng nhập"), ("mine_bindwx", "Liên kết WeChat"), ("mine_bindphone", "Liên kết SĐT"),
        ("mine_bindwx_hint", "Đăng nhập để liên kết WeChat và SĐT"), ("mine_logout", "Đăng xuất"), ("mine_version", "Phiên bản"),
    ],
    'ms': [
        ("mobile_mine", "Saya"), ("mine_title", "Akaun Saya"), ("mine_settings", "Tetapan"),
        ("mine_login", "Log Masuk"), ("mine_bindwx", "Sambung WeChat"), ("mine_bindphone", "Sambung Telefon"),
        ("mine_bindwx_hint", "Log masuk untuk sambung WeChat dan Telefon"), ("mine_logout", "Log Keluar"), ("mine_version", "Versi"),
    ],
}

added = 0
for lang, pairs in translations.items():
    for key, value in pairs:
        search = key + ":"
        if search in html:
            continue  # already exists

        # Find "mobile_products:" in this lang section
        # Format: "zh: {" then later "mobile_products: '...'"
        lang_start = html.find(lang + ": {")
        if lang_start < 0:
            lang_start = html.find(lang + ":{")
        if lang_start < 0:
            continue

        mp_idx = html.find("mobile_products:", lang_start)
        if mp_idx < 0:
            continue
        # Find end of line
        line_end = html.find('\n', mp_idx)
        if line_end < 0:
            continue

        # Insert after mobile_products line
        insert = ",\n        %s: '%s'" % (key, value)
        html = html[:line_end] + insert + html[line_end:]
        added += 1

# Upload
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(html)
f.close()
sftp.close()

print("Added %d translations" % added)
print("File: %d bytes" % len(html))
ssh.close()
