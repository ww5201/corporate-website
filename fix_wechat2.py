import paramiko

# 读取前端文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 替换 weixin:// 那段
old = """        // 跳转微信搜索 18977122166
        window.location.href = 'weixin://dl/business/?t=18977122166';
        // 备用方案：复制号码到剪贴板
        navigator.clipboard.writeText('18977122166').then(() => {
          alert('微信号已复制：18977122166\\n请打开微信搜索添加');
        }).catch(() => {
          alert('请手动搜索微信号：18977122166');
        });"""

new = """        // 复制号码到剪贴板
        var clipOk = false;
        if (navigator.clipboard) {
          try { await navigator.clipboard.writeText('18977122166'); clipOk = true; } catch(e) {}
        }
        showWechatGuide(clipOk);"""

html = html.replace(old, new)

# 在 handleWechatClick 函数后面添加 showWechatGuide
old2 = """    let wechatClickCount = 0;"""

new2 = """    function showWechatGuide(clipOk) {
      var existing = document.getElementById('wechatGuide');
      if (existing) existing.remove();
      var overlay = document.createElement('div');
      overlay.id = 'wechatGuide';
      overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:99999;display:flex;align-items:center;justify-content:center;';
      overlay.onclick = function(e) { if (e.target === overlay) overlay.remove(); };
      var box = document.createElement('div');
      box.style.cssText = 'background:#fff;border-radius:16px;padding:32px 28px;max-width:320px;width:90%;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.3);';
      box.innerHTML = '<div style="font-size:2.5rem;margin-bottom:12px">💬</div>' +
        '<div style="font-size:1.1rem;font-weight:600;margin-bottom:8px">' + (clipOk ? '号码已复制！' : '请手动复制') + '</div>' +
        '<div style="font-size:0.9rem;color:#666;margin-bottom:16px">打开微信 → 搜索 → 粘贴号码</div>' +
        '<div style="background:#f5f5f5;border-radius:10px;padding:14px;margin-bottom:16px;font-size:1.3rem;font-weight:700;color:#07c160;letter-spacing:2px;user-select:all">18977122166</div>' +
        '<div style="font-size:0.8rem;color:#999;margin-bottom:16px">长按上方号码可复制</div>' +
        '<button onclick="this.closest(\\'div[id=wechatGuide]\\').remove()" style="background:#07c160;color:#fff;border:none;padding:12px 40px;border-radius:8px;font-size:1rem;cursor:pointer">知道了</button>';
      overlay.appendChild(box);
      document.body.appendChild(overlay);
    }
    let wechatClickCount = 0;"""

html = html.replace(old2, new2)

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed wechat button - no more weixin:// URL")

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
