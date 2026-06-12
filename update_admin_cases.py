import paramiko

# 读取 admin.html
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

stdin, stdout, stderr = ssh.exec_command("cat /root/backend/admin.html")
admin = stdout.read().decode('utf-8')

# 添加案例管理标签
old_tabs = '''<div class="tabs"><button class="tab active" data-tab="products">产品</button><button class="tab" data-tab="orders">订单</button><button class="tab" data-tab="messages">留言</button><button class="tab" data-tab="payment">支付</button></div>'''
new_tabs = '''<div class="tabs"><button class="tab active" data-tab="products">产品</button><button class="tab" data-tab="cases">案例</button><button class="tab" data-tab="orders">订单</button><button class="tab" data-tab="messages">留言</button><button class="tab" data-tab="payment">支付</button></div>'''
admin = admin.replace(old_tabs, new_tabs)

# 添加案例管理面板
old_orders = '<div class="panel" id="orders">'
new_orders = '''<div class="panel" id="cases">
    <h2>案例管理</h2>
    <div class="form-group">
      <label>案例名称</label>
      <input type="text" id="caseName" placeholder="如：南宁别墅衣帽间">
    </div>
    <div class="form-group">
      <label>案例描述</label>
      <textarea id="caseDesc" placeholder="案例描述..." rows="3"></textarea>
    </div>
    <div class="form-group">
      <label>案例图片（最多 20 张，第一张为主图）</label>
      <div class="image-preview" id="casePreview"></div>
      <input type="file" id="caseImages" multiple accept="image/*" style="display:none" onchange="handleCaseImages(event)">
      <button class="btn" onclick="document.getElementById('caseImages').click()">选择图片</button>
      <button class="btn btn-danger" onclick="clearCaseImages()">清空</button>
    </div>
    <button class="btn btn-primary" onclick="saveCase()">保存案例</button>
    <div class="data-list" id="caseList"></div>
  </div>
  <div class="panel" id="orders">'''
admin = admin.replace(old_orders, new_orders)

# 添加 JS 函数
old_js = "let editingId = null;"
new_js = "let editingId = null; let caseImages = [];"
admin = admin.replace(old_js, new_js)

# 添加案例处理函数
old_switch = '''function switchTab(tab) {
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  document.querySelectorAll('.panel').forEach(p => p.style.display = (p.id === tab ? 'block' : 'none'));
  if (tab === 'products') loadProducts();
  if (tab === 'orders') loadOrders();
  if (tab === 'messages') loadMessages();
  if (tab === 'payment') loadPaymentConfig();
}'''

new_switch = '''function switchTab(tab) {
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  document.querySelectorAll('.panel').forEach(p => p.style.display = (p.id === tab ? 'block' : 'none'));
  if (tab === 'products') loadProducts();
  if (tab === 'cases') loadCases();
  if (tab === 'orders') loadOrders();
  if (tab === 'messages') loadMessages();
  if (tab === 'payment') loadPaymentConfig();
}

async function loadCases() {
  const r = await fetch(API + '/cases');
  const cases = await r.json();
  const list = document.getElementById('caseList');
  list.innerHTML = cases.map(c => {
    const img = c.images && c.images[0] ? IMG + c.images[0] : '';
    return `<div class="data-item">
      <img src="${img}" style="width:80px;height:60px;object-fit:cover;border-radius:8px;margin-right:16px">
      <div style="flex:1">
        <div style="font-weight:600">${c.name || '未命名'}</div>
        <div style="color:#777;font-size:0.9rem">${c.description || ''}</div>
        <div style="color:#999;font-size:0.85rem;margin-top:4px">${(c.images || []).length} 张图片 · ${new Date(c.createdAt).toLocaleString('zh-CN')}</div>
      </div>
      <button class="btn btn-sm" onclick="editCase('${c._id}')">编辑</button>
      <button class="btn btn-sm btn-danger" onclick="deleteCase('${c._id}')">删除</button>
    </div>`;
  }).join('') || '<div style="color:#999;text-align:center;padding:40px">暂无案例</div>';
}

function handleCaseImages(e) {
  const files = Array.from(e.target.files);
  if (caseImages.length + files.length > 20) {
    alert('最多只能上传 20 张图片！');
    return;
  }
  caseImages = [...caseImages, ...files];
  renderCasePreview();
}

function renderCasePreview() {
  const preview = document.getElementById('casePreview');
  preview.innerHTML = caseImages.map((f, i) => {
    const url = URL.createObjectURL(f);
    return `<div style="position:relative;display:inline-block;margin:8px">
      <img src="${url}" style="width:100px;height:100px;object-fit:cover;border-radius:8px">
      <button onclick="removeCaseImage(${i})" style="position:absolute;top:-8px;right:-8px;background:#f44;width:24px;height:24px;border-radius:50%;border:none;color:#fff;cursor:pointer">×</button>
    </div>`;
  }).join('');
}

function removeCaseImage(i) {
  caseImages.splice(i, 1);
  renderCasePreview();
}

function clearCaseImages() {
  caseImages = [];
  document.getElementById('caseImages').value = '';
  renderCasePreview();
}

async function saveCase() {
  const name = document.getElementById('caseName').value.trim();
  const desc = document.getElementById('caseDesc').value.trim();
  if (!name) { alert('请输入案例名称'); return; }
  
  let images = [];
  if (caseImages.length > 0) {
    const formData = new FormData();
    caseImages.forEach(f => formData.append('images', f));
    const r = await fetch(API + '/upload', { method: 'POST', body: formData });
    const res = await r.json();
    images = res.urls || [];
  }
  
  const body = { name, description: desc, images };
  const method = editingId ? 'PUT' : 'POST';
  const url = editingId ? `${API}/cases/${editingId}` : `${API}/cases`;
  
  const r = await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  
  if (r.ok) {
    alert('保存成功');
    editingId = null;
    document.getElementById('caseName').value = '';
    document.getElementById('caseDesc').value = '';
    clearCaseImages();
    loadCases();
  } else {
    const err = await r.json();
    alert('保存失败：' + (err.error || '未知错误'));
  }
}

function editCase(id) {
  // TODO: 加载案例详情进行编辑
  alert('编辑功能待实现');
}

async function deleteCase(id) {
  if (!confirm('确定删除此案例？')) return;
  const r = await fetch(`${API}/cases/${id}`, { method: 'DELETE' });
  if (r.ok) {
    alert('删除成功');
    loadCases();
  } else {
    alert('删除失败');
  }
}'''

admin = admin.replace(old_switch, new_switch)

# 保存回服务器
with open('/tmp/admin-new.html', 'w', encoding='utf-8') as f:
    f.write(admin)

sftp = ssh.open_sftp()
sftp.put('/tmp/admin-new.html', '/root/backend/admin.html')
sftp.put('/tmp/admin-new.html', '/var/www/frontend/admin.html')
sftp.close()
ssh.close()
print("Admin updated!")
