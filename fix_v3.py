import paramiko, base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

changes = []

# === Update checkAppUpdate to use Android bridge for download ===
old_check = """function checkAppUpdate() {
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
    }"""

new_check = """function checkAppUpdate() {
      toggleSettings();
      fetch(API + '/app-version').then(function(r){return r.json()}).then(function(d){
        var curVer = (window.Android && window.Android.getVersionCode) ? window.Android.getVersionCode() : 0;
        if (d.versionCode > curVer) {
          if (confirm('发现新版本 v' + d.versionName + '\\n' + d.updateMessage + '\\n\\n是否立即更新？')) {
            if (window.Android && window.Android.downloadUpdate) {
              window.Android.downloadUpdate(d.downloadUrl);
            } else {
              window.open(d.downloadUrl);
            }
          }
        } else {
          alert('当前已是最新版本 v' + d.versionName);
        }
      }).catch(function(){ alert('检查更新失败，请稍后再试'); });
    }"""

if old_check in html:
    html = html.replace(old_check, new_check)
    changes.append("Updated checkAppUpdate to use Android.downloadUpdate bridge")
else:
    changes.append("WARNING: checkAppUpdate not found")

# Validate
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

# Upload
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
cmd = f"echo '{encoded}' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()

with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Validate on server
val_cmd = '''node -e "
const fs = require('fs');
const html = fs.readFileSync('/var/www/frontend/index.html', 'utf8');
const start = html.indexOf('<script>') + 8;
const end = html.lastIndexOf('</script>');
const js = html.substring(start, end);
try { new Function(js); console.log('JS OK, len=' + js.length); } catch(e) { console.log('JS ERROR: ' + e.message); }
"'''
stdin, stdout, stderr = ssh.exec_command(val_cmd)
js_val = stdout.read().decode()

ssh.close()

for c in changes:
    print(c)
print(f"JS: {js_val}")
