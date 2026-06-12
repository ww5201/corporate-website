import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'r')
html = f.read().decode('utf-8')
f.close()

original_len = len(html)

# 1. Remove mine panel HTML
mine_start = html.find('<!-- 我的面板 -->')
if mine_start >= 0:
    # Find closing of overlay
    overlay_id = html.find('minePanelOverlay', mine_start)
    if overlay_id >= 0:
        div_close = html.rfind('</div>', overlay_id)
        if div_close >= 0:
            end = div_close + 6
            # Also remove trailing newlines
            while end < len(html) and html[end] in ' \t\n\r':
                end += 1
            html = html[:mine_start] + html[end:]
            print("Removed mine panel HTML")

# 2. Remove mine panel CSS
css_marker = "/* ===== 我的面板 ===== */"
if css_marker in html:
    idx = html.find(css_marker)
    # Find the style end before it
    style_start = html.rfind('<style>', 0, idx)
    style_end_tag = html.find('</style>', idx)
    # Remove just the mine CSS block
    next_line = html.find('\n', idx)
    while next_line < style_end_tag and html[next_line+1] in ' \t\n\r':
        next_line = html.find('\n', next_line+1)
    html = html[:idx] + html[next_line+1:]
    print("Removed mine panel CSS")

# 3. Remove mine panel JS functions
js_markers = ['// ===== 我的面板 =====']
for marker in js_markers:
    if marker in html:
        idx = html.find(marker)
        # Find the start of this comment line
        line_start = html.rfind('\n', 0, idx)
        if line_start < 0:
            line_start = 0
        else:
            line_start += 1
        # Find where the next section starts
        next_section = html.find('\n    // =====', idx + len(marker))
        if next_section < 0:
            next_section = html.find('\n    function ', idx + 100)
        if next_section >= 0:
            html = html[:line_start] + html[next_section+1:]
            print("Removed mine panel JS")

# 4. Remove showContact function (was added for mine panel)
sc_start = html.find('function showContact()')
if sc_start >= 0:
    # Find start of function
    line_start = html.rfind('\n', 0, sc_start)
    if line_start < 0:
        line_start = 0
    else:
        line_start += 1
    # Find end of function - next function
    next_func = html.find('\n    function ', sc_start + 10)
    if next_func >= 0:
        html = html[:line_start] + html[next_func+1:]
        print("Removed showContact function")

# 5. Remove mine_ i18n keys from all languages
for lang in ['zh', 'en', 'ja', 'ko', 'th', 'vi', 'ms']:
    for key in ['mobile_mine', 'mine_title', 'mine_settings', 'mine_login', 
                'mine_bindwx', 'mine_bindphone', 'mine_bindwx_hint', 'mine_logout', 'mine_version']:
        # Find and remove the key from each lang section
        search = "%s: '%s'" % (key, '')  # just find the key
        idx = html.find(key + ":")
        while idx >= 0:
            # Make sure it's in a JS context (not in HTML)
            line_start = html.rfind('\n', 0, idx)
            line = html[line_start:idx+len(key)+50]
            if key + ":" in line and ",'" not in html[idx-5:idx]:
                # Find end of this key-value pair
                val_start = html.find("'", idx + len(key) + 1)
                if val_start >= 0:
                    val_end = html.find("'", val_start + 1)
                    if val_end >= 0:
                        # Check if there's a comma after
                        after = val_end + 1
                        if after < len(html) and html[after] == ',':
                            val_end += 1
                        # Remove from newline before to the value end
                        remove_start = html.rfind('\n', 0, idx)
                        if remove_start >= 0:
                            html = html[:remove_start+1] + html[val_end+1:]
                            break
            idx = html.find(key + ":", idx + 1)

# 6. Restore mobile nav to 3 tabs (remove 👤 我的)
old_mine_tab = '<a href="javascript:void(0)" onclick="showMinePanel()"><span class="icon">👤</span>${i18n[lang].mobile_mine}</a>'
if old_mine_tab in html:
    html = html.replace(old_mine_tab, '')
    print("Removed Mine tab from mobile nav")

# 7. Remove mobile_mine i18n from nav template
# Check if there's a leftover comma
import re
html = re.sub(r',\s*\n\s*\n', '\n', html)  # Remove double newlines with commas

# Upload
sftp = ssh.open_sftp()
f = sftp.open('/var/www/frontend/index.html', 'w')
f.write(html)
f.close()
sftp.close()

# Verify
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

print("\n=== Result ===")
print("Original: %d bytes" % original_len)
print("Restored: %d bytes" % len(html))
print("JS: %d chars, braces: %d:%d" % (len(js), js.count('{'), js.count('}')))
print("showMinePanel: %s" % ('showMinePanel' in js))
print("showContact: %s" % ('function showContact' in js))
print("minePanel in HTML: %s" % ('id="minePanel"' in html))

ssh.close()
