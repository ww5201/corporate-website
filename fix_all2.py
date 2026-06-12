import paramiko, base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

changes = []

# === FIX 1: openOrder function - fix ID references ===
old1 = """function openOrder(pid) {
      curProd = products.find(p => p._id === pid);
      if (!curProd) { alert('Product not found'); return; }
      document.getElementById('orderTitle').textContent = curProd.name;
      document.getElementById('orderPrice').textContent = '¥' + curProd.price;
      document.getElementById('orderModal').style.display = 'flex';
      selectPay('wechat');
    }"""

new1 = """function openOrder(pid) {
      curProd = products.find(p => p._id === pid);
      if (!curProd) { alert('Product not found'); return; }
      document.getElementById('oName').textContent = curProd.name;
      document.getElementById('oPrice').textContent = '¥' + curProd.price;
      if (curProd.images && curProd.images.length > 0) {
        document.getElementById('oImg').src = curProd.images[0];
      }
      document.getElementById('orderModal').style.display = 'flex';
      selectPay('wechat');
    }"""

if old1 in html:
    html = html.replace(old1, new1)
    changes.append("Fixed openOrder ID refs (orderTitle->oName, orderPrice->oPrice)")
else:
    changes.append("WARNING: openOrder not found for fix")

# === FIX 2: submitOrder function - fix ID references ===
old2 = """function submitOrder() {
      var name = document.getElementById('orderName').value.trim();
      var phone = document.getElementById('orderPhone').value.trim();
      var addr = document.getElementById('orderAddr').value.trim();
      if (!name || !phone || !addr) {
        alert('请填写完整信息');
        return;
      }
      fetch(API + '/orders', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          product: curProd ? curProd.name : '',
          price: curProd ? curProd.price : 0,
          name: name,
          phone: phone,
          address: addr,
          payMethod: curPay
        })
      }).then(function(r) { return r.json(); }).then(function(d) {
        if (d.ok) {
          document.getElementById('orderForm').st"""

new2 = """function submitOrder() {
      var name = document.getElementById('oName2').value.trim();
      var phone = document.getElementById('oPhone').value.trim();
      var note = document.getElementById('oNote').value.trim();
      if (!name || !phone) {
        alert('请填写姓名和电话');
        return;
      }
      fetch(API + '/orders', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          product: curProd ? curProd.name : '',
          price: curProd ? curProd.price : 0,
          name: name,
          phone: phone,
          address: note,
          payMethod: curPay
        })
      }).then(function(r) { return r.json(); }).then(function(d) {
        if (d.ok) {
          document.getElementById('orderForm').st"""

if old2 in html:
    html = html.replace(old2, new2)
    changes.append("Fixed submitOrder ID refs (orderName->oName2, orderPhone->oPhone, orderAddr->oNote)")
else:
    changes.append("WARNING: submitOrder not found for fix")

# === FIX 3: Add version update to nav menu ===
# Find the nav area and add a settings dropdown
# First check if there's already a version-update link
if '版本更新' not in html and 'app-version' not in html:
    # Add settings menu HTML - find the nav-right area (language switcher)
    # Add a settings gear icon next to the language switcher
    settings_btn = """
    <div class="settings-menu" style="position:relative;margin-left:8px">
      <button class="settings-toggle" onclick="toggleSettings()" style="background:none;border:none;cursor:pointer;font-size:1.3rem;padding:6px 10px;border-radius:8px;color:var(--text2);transition:all .3s" onmouseover="this.style.background='rgba(0,0,0,0.04)'" onmouseout="this.style.background='none'">☰</button>
      <div class="settings-dropdown" id="settingsDropdown" style="display:none;position:absolute;right:0;top:100%;background:#fff;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,0.12);min-width:160px;z-index:9999;overflow:hidden">
        <a href="javascript:void(0)" onclick="checkAppUpdate()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem;border-bottom:1px solid #f0f0f0" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🔄</span> 版本更新</a>
        <a href="javascript:void(0)" onclick="clearCache()" style="display:flex;align-items:center;gap:8px;padding:12px 16px;color:#333;text-decoration:none;font-size:0.9rem" onmouseover="this.style.background='#f8f8f8'" onmouseout="this.style.background='transparent'"><span>🗑️</span> 清除缓存</a>
      </div>
    </div>
"""
    # Insert before .lang-switch
    if '.lang-switch' in html:
        html = html.replace('<div class="lang-switch">', settings_btn + '\n    <div class="lang-switch">')
        changes.append("Added settings menu (version update + clear cache)")
    
    # Add toggleSettings and checkAppUpdate functions
    new_funcs = """
    function toggleSettings() {
      var dd = document.getElementById('settingsDropdown');
      dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
    }
    function checkAppUpdate() {
      toggleSettings();
      if (window.Android && window.Android.getVersionCode) {
        var curVer = window.Android.getVersionCode();
        fetch(API + '/app-version').then(function(r){return r.json()}).then(function(d){
          if (d.versionCode > curVer) {
            if (confirm('发现新版本 v' + d.versionName + '\\n' + d.updateMessage + '\\n\\n是否立即更新？')) {
              window.location.href = d.downloadUrl;
            }
          } else {
            alert('当前已是最新版本 v' + d.versionName);
          }
        }).catch(function(){ alert('检查更新失败，请稍后再试'); });
      } else {
        fetch(API + '/app-version').then(function(r){return r.json()}).then(function(d){
          alert('当前版本: v' + (d.versionName || '1.0.0') + '\\n最新版本: v' + d.versionName);
        }).catch(function(){ alert('检查更新失败'); });
      }
    }
    function clearCache() {
      toggleSettings();
      if ('caches' in window) {
        caches.keys().then(function(names){ for(var i=0;i<names.length;i++) caches.delete(names[i]); });
      }
      location.reload(true);
    }
    // Close settings dropdown when clicking outside
    document.addEventListener('click', function(e) {
      var dd = document.getElementById('settingsDropdown');
      if (dd && !e.target.closest('.settings-menu')) {
        dd.style.display = 'none';
      }
    });
"""
    # Insert before startup marker
    if '// ===== 启动 =====' in html:
        html = html.replace('// ===== 启动 =====', new_funcs + '\n    // ===== 启动 =====')
        changes.append("Added toggleSettings/checkAppUpdate/clearCache functions")

# Validate JS
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

with open('D:/tokai/fix_all2_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"File size: {len(html)}\n")
    f.write(f"Braces: {js.count('{')}:{js.count('}')}\n")
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

with open('D:/tokai/fix_all2_result.txt', 'a', encoding='utf-8') as f:
    f.write(f"Server validation: {js_val}\n")

ssh.close()

for c in changes:
    print(f"  {c}")
print(f"JS: {js_val}")
