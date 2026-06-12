import paramiko

# 读取前端文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 修改浮动按钮的 HTML - 改成点击两次
old_btn = '    <button class="float-btn float-wechat" onclick="toggleWechat()" title="微信咨询">💬</button>'
new_btn = '    <button class="float-btn float-wechat" onclick="handleWechatClick()" title="微信咨询" id="wechatBtn">💬</button>'
html = html.replace(old_btn, new_btn)

# 2. 替换 toggleWechat 函数 - 改成点击两次跳转
old_func = '''    // ===== 微信弹窗 =====
    function toggleWechat() {
      const popup = document.getElementById('wechatPopup');
      const img = document.getElementById('wechatQrImg');
      if (payConfig.wechatQr) { img.src = IMG + payConfig.wechatQr; img.style.display = 'block'; }'''

new_func = '''    // ===== 微信咨询 - 点击两次跳转 =====
    let wechatClickCount = 0;
    let wechatClickTimer = null;
    function handleWechatClick() {
      wechatClickCount++;
      if (wechatClickCount === 1) {
        const btn = document.getElementById('wechatBtn');
        btn.style.background = '#ff9800';
        btn.innerHTML = '✓';
        btn.title = '再次点击打开微信';
        wechatClickTimer = setTimeout(() => {
          wechatClickCount = 0;
          btn.style.background = '#07c160';
          btn.innerHTML = '💬';
          btn.title = '微信咨询';
        }, 2000);
      } else if (wechatClickCount >= 2) {
        clearTimeout(wechatClickTimer);
        wechatClickCount = 0;
        const btn = document.getElementById('wechatBtn');
        btn.style.background = '#07c160';
        btn.innerHTML = '💬';
        btn.title = '微信咨询';
        // 跳转微信搜索 18977122166
        window.location.href = 'weixin://dl/business/?t=18977122166';
        // 备用方案：复制号码到剪贴板
        navigator.clipboard.writeText('18977122166').then(() => {
          alert('微信号已复制：18977122166\\n请打开微信搜索添加');
        }).catch(() => {
          alert('请手动搜索微信号：18977122166');
        });
      }
    }
    function toggleWechat() {
      const popup = document.getElementById('wechatPopup');
      const img = document.getElementById('wechatQrImg');
      if (payConfig.wechatQr) { img.src = IMG + payConfig.wechatQr; img.style.display = 'block'; }'''

html = html.replace(old_func, new_func)

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Wechat button changed to double-click!")

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
