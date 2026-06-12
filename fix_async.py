import paramiko

# 读取前端文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 修复：去掉 await，用 .then() 替代
old = """        // 复制号码到剪贴板
        var clipOk = false;
        if (navigator.clipboard) {
          try { await navigator.clipboard.writeText('18977122166'); clipOk = true; } catch(e) {}
        }
        showWechatGuide(clipOk);"""

new = """        // 复制号码到剪贴板
        var clipOk = false;
        try {
          if (navigator.clipboard) {
            navigator.clipboard.writeText('18977122166').then(function() { clipOk = true; showWechatGuide(true); }).catch(function() { showWechatGuide(false); });
          } else {
            showWechatGuide(false);
          }
        } catch(e) { showWechatGuide(false); }
        return;"""

html = html.replace(old, new)

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed async issue!")

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
