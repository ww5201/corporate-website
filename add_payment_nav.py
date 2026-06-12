import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")

s = c.open_sftp()

# Read current index.html
f = s.open("/var/www/frontend/index.html")
data = f.read().decode("utf-8", "replace")
f.close()

# Add payment link to desktop nav (after "联系" li, before </ul>)
old_nav = '联系</a></li>\r\n      </ul>'
new_nav = '联系</a></li>\r\n        <li><a href="/payment.html" target="_blank">在线支付</a></li>\r\n      </ul>'

if old_nav in data:
    data = data.replace(old_nav, new_nav, 1)
    print("[OK] Desktop nav: added payment link")
else:
    # Try without \r
    old_nav2 = '联系</a></li>\n      </ul>'
    new_nav2 = '联系</a></li>\n        <li><a href="/payment.html" target="_blank">在线支付</a></li>\n      </ul>'
    if old_nav2 in data:
        data = data.replace(old_nav2, new_nav2, 1)
        print("[OK] Desktop nav: added payment link (LF)")
    else:
        print("[FAIL] Could not find desktop nav pattern")

# Add payment link to mobile nav
old_mobile = '联系</a>\r\n    </div>'
new_mobile = '联系</a>\r\n      <a href="/payment.html" target="_blank">在线支付</a>\r\n    </div>'

if old_mobile in data:
    data = data.replace(old_mobile, new_mobile, 1)
    print("[OK] Mobile nav: added payment link")
else:
    old_mobile2 = '联系</a>\n    </div>'
    new_mobile2 = '联系</a>\n      <a href="/payment.html" target="_blank">在线支付</a>\n    </div>'
    if old_mobile2 in data:
        data = data.replace(old_mobile2, new_mobile2, 1)
        print("[OK] Mobile nav: added payment link (LF)")
    else:
        print("[FAIL] Could not find mobile nav pattern")

# Write back
f = s.open("/var/www/frontend/index.html", "w")
f.write(data)
f.close()
print("[OK] index.html updated on server")

# Verify
f = s.open("/var/www/frontend/index.html")
verify = f.read().decode("utf-8", "replace")
f.close()
if "payment.html" in verify:
    print("[OK] Payment link verified in index.html")
else:
    print("[FAIL] Payment link NOT found after update")

s.close()
c.close()
