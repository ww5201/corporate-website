import paramiko

# 读取前端文件
with open(r'D:\tokai\index-v4.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 修复1: 删除 JS 模板中的电话按钮
html = html.replace(
    '''<a href="tel:18977122166"><span class="icon">📞</span>${i18n[lang].mobile_call}</a>''',
    ''
)

# 修复2: 删除 mobile_call 翻译
html = html.replace(
    "mobile_home: '首页', mobile_products: '产品', mobile_consult: '咨询', mobile_call: '电话'",
    "mobile_home: '首页', mobile_products: '产品', mobile_consult: '咨询'"
)
html = html.replace(
    "mobile_home: 'Home', mobile_products: 'Products', mobile_consult: 'Consult', mobile_call: 'Call'",
    "mobile_home: 'Home', mobile_products: 'Products', mobile_consult: 'Consult'"
)

# 修复3: 给产品卡片图片添加点击放大功能
# 找到 renderProducts 函数中卡片创建部分，在 product-img 上添加 onclick
old_card = '''<div class="product-img" data-idx="0" data-total="${imgs.length}" data-pid="${p._id}">
            <div class="product-img-track">${track}</div>'''
new_card = '''<div class="product-img" data-idx="0" data-total="${imgs.length}" data-pid="${p._id}" onclick="openProductLb('${p._id}')" style="cursor:pointer">
            <div class="product-img-track">${track}</div>'''

html = html.replace(old_card, new_card)

# 修复4: 添加 openProductLb 函数 (在 imgNavAuto 函数后面)
old_func = '''    // ===== 案例 ====='''
new_func = '''    // ===== 产品灯箱 =====
    function openProductLb(pid) {
      const p = products.find(x => x._id === pid);
      if (!p) return;
      openLb(p);
    }

    // ===== 案例 ====='''

html = html.replace(old_func, new_func)

# 保存
with open(r'D:\tokai\index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed: phone removed, product lightbox added")

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
