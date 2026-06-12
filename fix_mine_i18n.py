import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

# First, remove the bad zh insertions (the extra commas and misplaced keys)
# Find zh section and clean it up
zh_start = html.find('zh: {')
if zh_start >= 0:
    # Find the closing of zh section - look for "en: {"
    en_start = html.find('en: {', zh_start)
    if en_start >= 0:
        # Go back to find the } before "en: {"
        zh_section_end = html.rfind('}', zh_start, en_start)
        if zh_section_end >= 0:
            # Get the zh section
            zh_section = html[zh_start:zh_section_end+1]
            # Find mobile_consult and remove everything after it until the }
            mc_idx = zh_section.find('mobile_consult:')
            if mc_idx >= 0:
                # Find the end of mobile_consult value
                mc_end = zh_section.find('\n', mc_idx)
                if mc_end < 0:
                    mc_end = mc_idx + 50
                # Get the clean part up to mobile_consult line
                clean_zh = zh_section[:mc_end+1]
                # Add the mine_ keys properly
                mine_keys = """
        mobile_mine: '我的', mine_title: '个人中心', mine_settings: '系统设置',
        mine_login: '登录/注册', mine_bindwx: '绑定微信', mine_bindphone: '绑定手机号',
        mine_bindwx_hint: '登录后绑定微信和手机号', mine_logout: '退出登录', mine_version: '当前版本'
      }"""
                clean_zh += mine_keys
                html = html[:zh_start] + clean_zh + html[zh_section_end+1:]
                print("Cleaned zh section")

# Now add mine_ keys to all other languages
translations = {
    'en': "mobile_mine: 'Mine', mine_title: 'My Account', mine_settings: 'Settings', mine_login: 'Login/Register', mine_bindwx: 'Bind WeChat', mine_bindphone: 'Bind Phone', mine_bindwx_hint: 'Login to bind WeChat and phone', mine_logout: 'Logout', mine_version: 'Version'",
    'ja': "mobile_mine: '私', mine_title: 'マイページ', mine_settings: '設定', mine_login: 'ログイン', mine_bindwx: 'WeChat連携', mine_bindphone: '電話番号連携', mine_bindwx_hint: 'ログインしてWeChatと電話を連携', mine_logout: 'ログアウト', mine_version: 'バージョン'",
    'ko': "mobile_mine: '나', mine_title: '내 정보', mine_settings: '설정', mine_login: '로그인', mine_bindwx: '위챗 연동', mine_bindphone: '전화번호 연동', mine_bindwx_hint: '로그인 후 위챗과 전화번호를 연동하세요', mine_logout: '로그아웃', mine_version: '버전'",
    'th': "mobile_mine: 'ฉัน', mine_title: 'บัญชีของฉัน', mine_settings: 'ตั้งค่า', mine_login: 'เข้าสู่ระบบ', mine_bindwx: 'เชื่อมต่อ WeChat', mine_bindphone: 'เชื่อมต่อเบอร์โทร', mine_bindwx_hint: 'เข้าสู่ระบบเพื่อเชื่อมต่อ WeChat และเบอร์โทร', mine_logout: 'ออกจากระบบ', mine_version: 'เวอร์ชัน'",
    'vi': "mobile_mine: 'Tôi', mine_title: 'Tài khoản', mine_settings: 'Cài đặt', mine_login: 'Đăng nhập', mine_bindwx: 'Liên kết WeChat', mine_bindphone: 'Liên kết SĐT', mine_bindwx_hint: 'Đăng nhập để liên kết WeChat và SĐT', mine_logout: 'Đăng xuất', mine_version: 'Phiên bản'",
    'ms': "mobile_mine: 'Saya', mine_title: 'Akaun Saya', mine_settings: 'Tetapan', mine_login: 'Log Masuk', mine_bindwx: 'Sambung WeChat', mine_bindphone: 'Sambung Telefon', mine_bindwx_hint: 'Log masuk untuk sambung WeChat dan Telefon', mine_logout: 'Log Keluar', mine_version: 'Versi'",
}

for lang, keys_str in translations.items():
    if 'mobile_mine' in html and lang + ': {' in html:
        # Check if this lang already has mobile_mine
        lang_start = html.find(lang + ': {')
        if lang_start < 0:
            lang_start = html.find(lang + ":{")
        if lang_start >= 0:
            # Find the next lang or end of i18n
            next_lang_pos = len(html)
            for other_lang in ['en', 'ja', 'ko', 'th', 'vi', 'ms', '}']:
                pos = html.find(other_lang + ': {', lang_start + 5)
                if pos < 0:
                    pos = html.find(other_lang + ':{', lang_start + 5)
                if pos >= 0 and pos < next_lang_pos:
                    next_lang_pos = pos
            # Find the } before the next lang
            close_brace = html.rfind('}', lang_start, next_lang_pos)
            if close_brace >= 0:
                # Check if mobile_mine already exists in this section
                section = html[lang_start:close_brace]
                if 'mobile_mine' not in section:
                    # Insert before the closing }
                    insert = ",\n        " + keys_str + "\n"
                    html = html[:close_brace] + insert + html[close_brace:]
                    print("Added mine_ keys to %s" % lang)

# Upload
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(html)
f.close()
sftp.close()

print("File: %d bytes" % len(html))
ssh.close()
