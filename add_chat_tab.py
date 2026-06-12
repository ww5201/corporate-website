import paramiko, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

HOST = '8.138.218.146'
USER = 'root'
PWD = 'ww0987654.'

# The new admin.html with chat tab added
NEW_ADMIN_HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>卓翌定制 - 后台管理</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Microsoft YaHei', sans-serif; background: #f5f5f5; min-height: 100vh; }
    .header { background: linear-gradient(135deg, #8b7355, #6b5a45); color: #fff; padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }
    .header h1 { font-size: 1.4rem; }
    .stats { display: flex; gap: 1rem; max-width: 1200px; margin: 1.5rem auto; padding: 0 1rem; }
    .stat { flex: 1; background: #fff; border-radius: 8px; padding: 1rem; text-align: center; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    .stat h3 { font-size: 2rem; color: #8b7355; }
    .stat p { color: #888; font-size: 0.8rem; margin-top: 0.3rem; }
    .container { max-width: 1200px; margin: 0 auto; padding: 0 1rem 2rem; }
    .tabs { display: flex; background: #fff; border-radius: 8px; overflow: hidden; margin-bottom: 1rem; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    .tab { flex: 1; padding: 0.8rem; border: none; background: none; cursor: pointer; font-size: 0.95rem; color: #666; position: relative; }
    .tab.on { color: #8b7355; font-weight: 600; background: #f9f7f4; border-bottom: 2px solid #8b7355; }
    .tab .unread-badge { position: absolute; top: 6px; right: 12px; background: #ff4d4f; color: #fff; font-size: 0.65rem; padding: 1px 5px; border-radius: 10px; min-width: 16px; text-align: center; }
    .panes > div { display: none; }
    .panes > div.show { display: block; }
    .card { background: #fff; border-radius: 8px; padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    .top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
    .btn { padding: 0.5rem 1rem; background: #8b7355; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 0.85rem; }
    .btn:hover { background: #6b5a45; }
    .btn-d { background: #ff4d4f; }
    .btn-d:hover { background: #e03e3f; }
    .btn-p { background: #1890ff; }
    .btn-s { background: #52c41a; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 0.6rem 0.8rem; text-align: left; border-bottom: 1px solid #f0f0f0; font-size: 0.9rem; }
    th { background: #fafafa; color: #666; font-size: 0.8rem; }
    tr:hover { background: #fafafa; }
    .badge { padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; }
    .badge-y { background: #fff7e6; color: #d48806; }
    .badge-g { background: #f6ffed; color: #52c41a; }
    .empty { text-align: center; padding: 2rem; color: #bbb; }
    .modal { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 999; justify-content: center; align-items: center; }
    .modal.on { display: flex; }
    .box { background: #fff; padding: 1.5rem; border-radius: 8px; width: 90%; max-width: 600px; max-height: 90vh; overflow-y: auto; }
    .box h2 { margin-bottom: 1rem; color: #333; font-size: 1.1rem; }
    .fg { margin-bottom: 0.8rem; }
    .fg label { display: block; margin-bottom: 0.2rem; font-size: 0.85rem; color: #333; }
    .fg input, .fg textarea, .fg select { width: 100%; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; font-size: 0.9rem; }
    .fg input:focus, .fg textarea:focus { border-color: #8b7355; outline: none; }
    .fg textarea { height: 80px; resize: vertical; }
    .acts { text-align: right; margin-top: 1rem; }
    .img-upload-area { border: 2px dashed #ddd; border-radius: 8px; padding: 1rem; text-align: center; cursor: pointer; transition: all 0.3s; }
    .img-upload-area:hover { border-color: #8b7355; background: #faf9f7; }
    .img-upload-area p { color: #999; font-size: 0.85rem; }
    .img-upload-area .icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .img-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 0.8rem; }
    .img-thumb { position: relative; width: 100%; aspect-ratio: 1; border-radius: 4px; overflow: hidden; border: 1px solid #eee; }
    .img-thumb img { width: 100%; height: 100%; object-fit: cover; }
    .img-thumb .del { position: absolute; top: 4px; right: 4px; background: rgba(255,0,0,0.8); color: #fff; border: none; border-radius: 50%; width: 20px; height: 20px; font-size: 12px; cursor: pointer; }
    .img-thumb .cover { position: absolute; bottom: 4px; left: 4px; background: rgba(139,115,85,0.9); color: #fff; border: none; border-radius: 4px; padding: 2px 6px; font-size: 11px; cursor: pointer; }
    .img-thumb.is-cover { border: 2px solid #8b7355; }
    .upload-progress { display: none; margin-top: 0.5rem; }
    .upload-progress.show { display: block; }
    .progress-bar { height: 4px; background: #eee; border-radius: 2px; overflow: hidden; }
    .progress-bar .fill { height: 100%; background: #8b7355; transition: width 0.3s; }

    /* ===== Chat Styles ===== */
    .chat-wrap { display: flex; height: 600px; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }
    .chat-sidebar { width: 300px; border-right: 1px solid #eee; display: flex; flex-direction: column; }
    .chat-sidebar-header { padding: 1rem; border-bottom: 1px solid #eee; font-weight: 600; color: #333; background: #fafafa; }
    .chat-list { flex: 1; overflow-y: auto; }
    .chat-item { padding: 0.8rem 1rem; border-bottom: 1px solid #f5f5f5; cursor: pointer; transition: background 0.2s; }
    .chat-item:hover { background: #f9f7f4; }
    .chat-item.active { background: #f0ebe3; border-left: 3px solid #8b7355; }
    .chat-item-name { font-weight: 600; color: #333; font-size: 0.9rem; display: flex; justify-content: space-between; align-items: center; }
    .chat-item-name .unread { background: #ff4d4f; color: #fff; font-size: 0.65rem; padding: 1px 6px; border-radius: 10px; }
    .chat-item-last { color: #999; font-size: 0.8rem; margin-top: 0.2rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .chat-item-time { color: #bbb; font-size: 0.7rem; margin-top: 0.15rem; }
    .chat-main { flex: 1; display: flex; flex-direction: column; }
    .chat-main-header { padding: 0.8rem 1rem; border-bottom: 1px solid #eee; background: #fafafa; display: flex; justify-content: space-between; align-items: center; }
    .chat-main-header h3 { font-size: 0.95rem; color: #333; }
    .chat-main-header .info { font-size: 0.8rem; color: #999; }
    .chat-messages { flex: 1; overflow-y: auto; padding: 1rem; background: #f5f5f5; }
    .chat-msg { margin-bottom: 0.8rem; display: flex; }
    .chat-msg.visitor { justify-content: flex-start; }
    .chat-msg.admin { justify-content: flex-end; }
    .chat-bubble { max-width: 65%; padding: 0.6rem 0.9rem; border-radius: 12px; font-size: 0.9rem; line-height: 1.5; word-break: break-word; }
    .chat-msg.visitor .chat-bubble { background: #fff; color: #333; border-bottom-left-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.06); }
    .chat-msg.admin .chat-bubble { background: linear-gradient(135deg, #8b7355, #a08a6a); color: #fff; border-bottom-right-radius: 4px; }
    .chat-msg-time { font-size: 0.7rem; color: #bbb; margin-top: 0.2rem; text-align: right; }
    .chat-msg.visitor .chat-msg-time { text-align: left; }
    .chat-input-area { padding: 0.8rem 1rem; border-top: 1px solid #eee; display: flex; gap: 0.5rem; background: #fff; }
    .chat-input-area input { flex: 1; padding: 0.6rem 0.8rem; border: 1px solid #ddd; border-radius: 20px; font-size: 0.9rem; outline: none; }
    .chat-input-area input:focus { border-color: #8b7355; }
    .chat-input-area button { padding: 0.6rem 1.2rem; background: #8b7355; color: #fff; border: none; border-radius: 20px; cursor: pointer; font-size: 0.85rem; }
    .chat-input-area button:hover { background: #6b5a45; }
    .chat-empty { flex: 1; display: flex; align-items: center; justify-content: center; color: #bbb; font-size: 1rem; }
    .chat-no-conv { text-align: center; padding: 3rem; color: #bbb; }
    @media (max-width: 768px) {
      .chat-wrap { flex-direction: column; height: 700px; }
      .chat-sidebar { width: 100%; height: 200px; border-right: none; border-bottom: 1px solid #eee; }
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>🏆 卓翌定制 - 后台管理</h1>
    <span id="status" style="font-size:0.85rem">● 检测中...</span>
  </div>
  <div class="stats">
    <div class="stat"><h3 id="s-p">0</h3><p>📦 产品</p></div>
    <div class="stat"><h3 id="s-m">0</h3><p>💬 留言</p></div>
    <div class="stat"><h3 id="s-o">0</h3><p>🛒 订单</p></div>
    <div class="stat"><h3 id="s-c">0</h3><p>💬 咨询</p></div>
  </div>
  <div class="container">
    <div class="tabs">
      <button class="tab on" onclick="go('p',this)">📦 产品管理</button>
      <button class="tab" onclick="go('m',this)">💬 客户留言</button>
      <button class="tab" onclick="go('c',this)" id="tab-chat">💬 在线客服<span class="unread-badge" id="chat-badge" style="display:none">0</span></button>
      <button class="tab" onclick="go('o',this)">🛒 订单管理</button>
      <button class="tab" onclick="go('pay',this)">💰 支付设置</button>
    </div>
    <div class="panes">
      <!-- Products -->
      <div id="p" class="show">
        <div class="card">
          <div class="top"><h2>产品列表</h2><button class="btn" onclick="addP()">+ 添加产品</button></div>
          <table><thead><tr><th>产品图片</th><th>名称</th><th>类别</th><th>价格</th><th>操作</th></tr></thead><tbody id="tb-p"></tbody></table>
          <div id="ep" class="empty">暂无产品，点击上方按钮添加</div>
        </div>
      </div>
      <!-- Messages -->
      <div id="m">
        <div class="card">
          <div class="top"><h2>客户留言</h2></div>
          <table><thead><tr><th>姓名</th><th>联系方式</th><th>留言</th><th>时间</th><th>操作</th></tr></thead><tbody id="tb-m"></tbody></table>
          <div id="em" class="empty">暂无留言</div>
        </div>
      </div>
      <!-- Online Chat -->
      <div id="c">
        <div class="chat-wrap">
          <div class="chat-sidebar">
            <div class="chat-sidebar-header">📋 对话列表 <span id="conv-count" style="font-weight:normal;color:#999;font-size:0.8rem"></span></div>
            <div class="chat-list" id="conv-list"></div>
          </div>
          <div class="chat-main" id="chat-main">
            <div class="chat-empty">← 选择一个对话开始聊天</div>
          </div>
        </div>
      </div>
      <!-- Orders -->
      <div id="o">
        <div class="card">
          <div class="top"><h2>咨询订单</h2></div>
          <table><thead><tr><th>姓名</th><th>电话</th><th>产品</th><th>金额</th><th>支付方式</th><th>状态</th><th>时间</th><th>操作</th></tr></thead><tbody id="tb-o"></tbody></table>
          <div id="eo" class="empty">暂无订单</div>
        </div>
      </div>
      <!-- Payment -->
      <div id="pay">
        <div class="card">
          <div class="top"><h2>💰 收款码设置</h2></div>
          <p style="color:#888;font-size:0.85rem;margin-bottom:1rem">上传您的微信/支付宝收款二维码，客户下单后可扫码支付。</p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem">
            <div>
              <h3 style="font-size:1rem;margin-bottom:0.8rem">💚 微信收款码</h3>
              <div class="img-upload-area" onclick="uploadQr('wechat')" id="qr-wechat-area">
                <div id="qr-wechat-preview" style="text-align:center">
                  <div class="icon">📱</div>
                  <p>点击上传微信收款码</p>
                </div>
              </div>
            </div>
            <div>
              <h3 style="font-size:1rem;margin-bottom:0.8rem">💙 支付宝收款码</h3>
              <div class="img-upload-area" onclick="uploadQr('alipay')" id="qr-alipay-area">
                <div id="qr-alipay-preview" style="text-align:center">
                  <div class="icon">📱</div>
                  <p>点击上传支付宝收款码</p>
                </div>
              </div>
            </div>
          </div>
          <input type="file" id="qr-input" accept="image/*" style="display:none">
          <div style="margin-top:1.5rem;text-align:right">
            <button class="btn" onclick="savePaymentConfig()">💾 保存设置</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Product Modal -->
  <div id="mp" class="modal">
    <div class="box">
      <h2 id="mt">添加产品</h2>
      <form id="pf">
        <input type="hidden" id="pid">
        <div class="fg"><label>产品名称 *</label><input id="pn" required placeholder="例如：整体衣柜定制"></div>
        <div class="fg"><label>类别</label><select id="pc"><option>整体衣柜</option><option>衣帽间</option><option>橱柜</option><option>全屋定制</option><option>书柜</option><option>鞋柜</option><option>酒柜</option></select></div>
        <div class="fg"><label>价格 (元) *</label><input type="number" id="pp" required placeholder="例如：12999"></div>
        <div class="fg"><label>产品描述</label><textarea id="pd" placeholder="输入产品描述、特点、材质等"></textarea></div>
        <div class="fg">
          <label>产品图片（最多6张，第一张为主图）</label>
          <div class="img-upload-area" id="dropArea" onclick="document.getElementById('fileInput').click()">
            <div class="icon">📁</div>
            <p>点击选择图片或拖拽到这里</p>
            <p style="font-size:0.75rem;color:#bbb">支持 JPG、PNG、GIF、WebP，单张最大 10MB</p>
          </div>
          <input type="file" id="fileInput" accept="image/*" multiple style="display:none" onchange="handleFiles(this.files)">
          <div class="upload-progress" id="uploadProgress">
            <p style="font-size:0.8rem;color:#888" id="uploadText">上传中...</p>
            <div class="progress-bar"><div class="fill" id="progressFill"></div></div>
          </div>
          <div class="img-grid" id="imgGrid"></div>
        </div>
        <div class="acts">
          <button type="button" class="btn" onclick="cls()" style="margin-right:0.5rem;background:#999">取消</button>
          <button type="submit" class="btn">保存</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Message Modal -->
  <div id="mm" class="modal">
    <div class="box">
      <h2>留言详情</h2>
      <div id="md"></div>
      <div class="acts"><button class="btn" onclick="document.getElementById('mm').classList.remove('on')" style="background:#999">关闭</button></div>
    </div>
  </div>

  <script>
    let imgUrls = [];
    let dragCounter = 0;

    function go(id, el) {
      document.querySelectorAll('.panes > div').forEach(e => e.classList.remove('show'));
      document.querySelectorAll('.tab').forEach(e => e.classList.remove('on'));
      document.getElementById(id).classList.add('show');
      el.classList.add('on');
      if (id === 'p') loadP();
      else if (id === 'm') loadM();
      else if (id === 'o') loadO();
      else if (id === 'pay') loadPaymentCfg();
      else if (id === 'c') initChat();
    }

    // Health check
    fetch('/api/health').then(r => r.json()).then(() => {
      document.getElementById('status').innerHTML = '● 服务正常';
      document.getElementById('status').style.color = '#52c41a';
      loadStats();
    }).catch(() => {
      document.getElementById('status').innerHTML = '● 服务异常';
      document.getElementById('status').style.color = '#ff4d4f';
    });

    function loadStats() {
      fetch('/api/products').then(r=>r.json()).then(d=>{document.getElementById('s-p').textContent=d.length});
      fetch('/api/messages').then(r=>r.json()).then(d=>{document.getElementById('s-m').textContent=d.length});
      fetch('/api/orders').then(r=>r.json()).then(d=>{document.getElementById('s-o').textContent=d.length});
      fetch('/api/conversations').then(r=>r.json()).then(d=>{
        document.getElementById('s-c').textContent=d.length;
        const unread = d.reduce((s,c)=>s+(c.unread||0),0);
        const badge = document.getElementById('chat-badge');
        if (unread > 0) { badge.style.display='inline'; badge.textContent=unread; }
        else { badge.style.display='none'; }
      });
    }

    // ===== Products =====
    async function loadP() {
      const d = await (await fetch('/api/products')).json();
      const tb = document.getElementById('tb-p');
      tb.innerHTML = '';
      document.getElementById('ep').style.display = d.length ? 'none' : 'block';
      d.forEach(p => {
        const img = (p.images && p.images.length) ? p.images[0] : (p.image || '');
        const imgHtml = img ? '<img src="'+img+'" style="width:50px;height:50px;object-fit:cover;border-radius:4px">' : '<div style="width:50px;height:50px;background:#f0f0f0;border-radius:4px;display:flex;align-items:center;justify-content:center;color:#ccc">无</div>';
        tb.innerHTML += '<tr><td>'+imgHtml+'</td><td>'+p.name+'</td><td>'+(p.category||'-')+'</td><td>¥'+p.price+'</td><td><button class="btn btn-p" onclick="editP(\''+p._id+'\')">编辑</button> <button class="btn btn-d" onclick="delP(\''+p._id+'\')">删除</button></td></tr>';
      });
    }

    function addP() {
      document.getElementById('mt').textContent = '添加产品';
      document.getElementById('pid').value = '';
      document.getElementById('pn').value = '';
      document.getElementById('pc').value = '整体衣柜';
      document.getElementById('pp').value = '';
      document.getElementById('pd').value = '';
      imgUrls = [];
      renderImgs();
      document.getElementById('mp').classList.add('on');
    }

    async function editP(id) {
      const d = await (await fetch('/api/products')).json();
      const p = d.find(x => x._id === id);
      if (!p) return;
      document.getElementById('mt').textContent = '编辑产品';
      document.getElementById('pid').value = p._id;
      document.getElementById('pn').value = p.name;
      document.getElementById('pc').value = p.category || '整体衣柜';
      document.getElementById('pp').value = p.price;
      document.getElementById('pd').value = p.description || '';
      imgUrls = p.images ? [...p.images] : (p.image ? [p.image] : []);
      renderImgs();
      document.getElementById('mp').classList.add('on');
    }

    async function delP(id) { if (!confirm('确定删除？')) return; await fetch('/api/products/'+id,{method:'DELETE'}); loadP(); loadStats(); }
    function cls() { document.getElementById('mp').classList.remove('on'); }

    function renderImgs() {
      const g = document.getElementById('imgGrid');
      g.innerHTML = '';
      imgUrls.forEach((url, i) => {
        const div = document.createElement('div');
        div.className = 'img-thumb' + (i===0?' is-cover':'');
        div.innerHTML = '<img src="'+url+'"><button class="del" onclick="delImg('+i+')">x</button>'+(i>0?'<button class="cover" onclick="setCover('+i+')">主图</button>':'');
        g.appendChild(div);
      });
    }
    function delImg(i) { imgUrls.splice(i,1); renderImgs(); }
    function setCover(i) { const u=imgUrls.splice(i,1)[0]; imgUrls.unshift(u); renderImgs(); }

    function handleFiles(files) {
      if (!files.length) return;
      const maxFiles = 6 - imgUrls.length;
      const filesToUpload = Array.from(files).slice(0, maxFiles);
      const progressDiv = document.getElementById('uploadProgress');
      const progressFill = document.getElementById('progressFill');
      const uploadText = document.getElementById('uploadText');
      let uploaded = 0;
      progressDiv.classList.add('show');

      filesToUpload.forEach(file => {
        if (file.size > 10*1024*1024) { alert(file.name+' 超过10MB限制'); return; }
        const fd = new FormData();
        fd.append('images', file);
        fetch('/api/upload', { method: 'POST', body: fd })
          .then(r => r.json())
          .then(d => {
            if (d.urls) { imgUrls = imgUrls.concat(d.urls); renderImgs(); }
            uploaded++;
            progressFill.style.width = (uploaded/filesToUpload.length*100)+'%';
            uploadText.textContent = '已上传 '+uploaded+'/'+filesToUpload.length;
            if (uploaded >= filesToUpload.length) { setTimeout(()=>{progressDiv.classList.remove('show');},1000); }
          })
          .catch(e => { alert('上传失败: '+e); uploaded++; if(uploaded>=filesToUpload.length) progressDiv.classList.remove('show'); });
      });
    }

    // Drag and drop
    const dropArea = document.getElementById('dropArea');
    dropArea.addEventListener('dragenter', e => { e.preventDefault(); dragCounter++; dropArea.classList.add('dragover'); });
    dropArea.addEventListener('dragleave', e => { e.preventDefault(); dragCounter--; if(dragCounter===0) dropArea.classList.remove('dragover'); });
    dropArea.addEventListener('dragover', e => e.preventDefault());
    dropArea.addEventListener('drop', e => { e.preventDefault(); dragCounter=0; dropArea.classList.remove('dragover'); handleFiles(e.dataTransfer.files); });

    document.getElementById('pf').onsubmit = async e => {
      e.preventDefault();
      const id = document.getElementById('pid').value;
      const d = { name: document.getElementById('pn').value, category: document.getElementById('pc').value, price: +document.getElementById('pp').value, description: document.getElementById('pd').value, images: imgUrls, image: imgUrls[0]||'' };
      if (id) await fetch('/api/products/'+id,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});
      else await fetch('/api/products',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});
      cls(); loadP(); loadStats();
    };

    // ===== Messages =====
    async function loadM() {
      const d = await (await fetch('/api/messages')).json();
      const tb = document.getElementById('tb-m');
      tb.innerHTML = '';
      document.getElementById('em').style.display = d.length ? 'none' : 'block';
      d.forEach(m => {
        const contact = m.email || m.contact || '-';
        tb.innerHTML += '<tr><td>'+m.name+'</td><td>'+contact+'</td><td>'+(m.message||'-')+'</td><td>'+new Date(m.createdAt).toLocaleString('zh-CN')+'</td><td><button class="btn btn-p" onclick="viewM(\''+m._id+'\')">查看</button> <button class="btn btn-d" onclick="delM(\''+m._id+'\')">删除</button></td></tr>';
      });
    }
    async function viewM(id) {
      const d = await (await fetch('/api/messages')).json();
      const m = d.find(x => x._id === id);
      if (!m) return;
      const contact = m.email || m.contact || '-';
      document.getElementById('md').innerHTML = '<p><b>姓名:</b> '+m.name+'</p><p><b>联系方式:</b> '+contact+'</p><p><b>留言:</b> '+m.message+'</p><p><b>时间:</b> '+new Date(m.createdAt).toLocaleString('zh-CN')+'</p>';
      document.getElementById('mm').classList.add('on');
    }
    async function delM(id) { if (!confirm('确定删除？')) return; await fetch('/api/messages/'+id,{method:'DELETE'}); loadM(); loadStats(); }

    // ===== Orders =====
    async function loadO() {
      const d = await (await fetch('/api/orders')).json();
      const tb = document.getElementById('tb-o');
      tb.innerHTML = '';
      document.getElementById('eo').style.display = d.length ? 'none' : 'block';
      d.forEach(o => {
        const payMethod = o.paymentMethod === 'wechat' ? '💚 微信' : o.paymentMethod === 'alipay' ? '💙 支付宝' : '-';
        const statusBadge = o.status === '已付款' ? '<span class="badge badge-g">已付款</span>' : '<span class="badge badge-y">'+o.status+'</span>';
        const actions = o.status !== '已付款' ? '<button class="btn btn-s" onclick="markPaid(\''+o._id+'\')">确认付款</button>' : '-';
        tb.innerHTML += '<tr><td>'+o.customerName+'</td><td>'+(o.customerPhone||o.phone||'-')+'</td><td>'+o.productName+'</td><td>¥'+o.price+'</td><td>'+payMethod+'</td><td>'+statusBadge+'</td><td>'+new Date(o.createdAt).toLocaleString('zh-CN')+'</td><td>'+actions+'</td></tr>';
      });
    }
    async function markPaid(id) { await fetch('/api/orders/'+id+'/pay',{method:'PUT'}); loadO(); }

    // ===== Payment Config =====
    let paymentCfg = { wechatQr: '', alipayQr: '' };
    async function loadPaymentCfg() {
      try {
        const r = await fetch('/api/payment-config');
        paymentCfg = await r.json();
        if (paymentCfg.wechatQr) {
          document.getElementById('qr-wechat-preview').innerHTML = '<img src="'+paymentCfg.wechatQr+'" style="max-width:100%;max-height:200px;border-radius:8px"><p style="font-size:0.75rem;color:#888;margin-top:0.5rem">点击更换</p>';
        }
        if (paymentCfg.alipayQr) {
          document.getElementById('qr-alipay-preview').innerHTML = '<img src="'+paymentCfg.alipayQr+'" style="max-width:100%;max-height:200px;border-radius:8px"><p style="font-size:0.75rem;color:#888;margin-top:0.5rem">点击更换</p>';
        }
      } catch(e) {}
    }
    function uploadQr(type) {
      const input = document.getElementById('qr-input');
      input.onchange = async () => {
        if (!input.files.length) return;
        const fd = new FormData(); fd.append('images', input.files[0]);
        const r = await fetch('/api/upload', { method:'POST', body: fd });
        const d = await r.json();
        if (d.urls && d.urls.length) { paymentCfg[type+'Qr'] = d.urls[0]; loadPaymentCfg(); }
      };
      input.click();
    }
    async function savePaymentConfig() {
      await fetch('/api/payment-config', { method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(paymentCfg) });
      alert('保存成功！');
    }

    // ===== Online Chat =====
    let conversations = [];
    let activeConvId = null;
    let chatWs = null;
    let chatInited = false;

    function initChat() {
      loadConversations();
      if (!chatInited) {
        chatInited = true;
        connectChatWs();
      }
    }

    async function loadConversations() {
      try {
        conversations = await (await fetch('/api/conversations')).json();
      } catch(e) { conversations = []; }
      renderConvList();
      // Update badge
      const unread = conversations.reduce((s,c)=>s+(c.unread||0),0);
      const badge = document.getElementById('chat-badge');
      if (unread > 0) { badge.style.display='inline'; badge.textContent=unread; }
      else { badge.style.display='none'; }
      document.getElementById('conv-count').textContent = '('+conversations.length+')';
    }

    function renderConvList() {
      const list = document.getElementById('conv-list');
      if (!conversations.length) {
        list.innerHTML = '<div class="chat-no-conv">暂无对话</div>';
        return;
      }
      // Sort by updatedAt desc
      conversations.sort((a,b) => new Date(b.updatedAt) - new Date(a.updatedAt));
      list.innerHTML = '';
      conversations.forEach(c => {
        const lastMsg = c.messages && c.messages.length ? c.messages[c.messages.length-1] : null;
        const lastText = lastMsg ? (lastMsg.content || '[无内容]') : '暂无消息';
        const lastTime = lastMsg ? new Date(lastMsg.createdAt).toLocaleString('zh-CN',{month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'}) : '';
        const unreadBadge = c.unread ? '<span class="unread">'+c.unread+'</span>' : '';
        const activeClass = c._id === activeConvId ? ' active' : '';
        const div = document.createElement('div');
        div.className = 'chat-item' + activeClass;
        div.onclick = () => openChat(c._id);
        div.innerHTML = '<div class="chat-item-name">'+(c.name||'访客')+' '+unreadBadge+'</div><div class="chat-item-last">'+lastText+'</div><div class="chat-item-time">'+lastTime+'</div>';
        list.appendChild(div);
      });
    }

    async function openChat(id) {
      activeConvId = id;
      renderConvList();
      const main = document.getElementById('chat-main');
      main.innerHTML = '<div class="chat-empty">加载中...</div>';

      try {
        const msgs = await (await fetch('/api/conversations/'+id+'/messages')).json();
        const conv = conversations.find(c => c._id === id) || {};
        
        let html = '<div class="chat-main-header"><div><h3>'+(conv.name||'访客')+'</h3><div class="info">'+(conv.phone||'')+'</div></div><button class="btn btn-d" onclick="deleteConv(\''+id+'\')" style="font-size:0.75rem;padding:0.3rem 0.6rem">删除对话</button></div>';
        html += '<div class="chat-messages" id="chat-msgs">';
        if (!msgs.length) {
          html += '<div style="text-align:center;padding:2rem;color:#bbb">暂无消息</div>';
        } else {
          msgs.forEach(m => {
            const cls = m.sender === 'admin' ? 'admin' : 'visitor';
            const time = new Date(m.createdAt).toLocaleTimeString('zh-CN',{hour:'2-digit',minute:'2-digit'});
            html += '<div class="chat-msg '+cls+'"><div><div class="chat-bubble">'+escHtml(m.content)+'</div><div class="chat-msg-time">'+time+'</div></div></div>';
          });
        }
        html += '</div>';
        html += '<div class="chat-input-area"><input type="text" id="chat-input" placeholder="输入回复消息..." onkeydown="if(event.key===\'Enter\')sendMsg()"><button onclick="sendMsg()">发送</button></div>';
        main.innerHTML = html;
        
        // Scroll to bottom
        const msgDiv = document.getElementById('chat-msgs');
        msgDiv.scrollTop = msgDiv.scrollHeight;
        document.getElementById('chat-input').focus();

        // Mark as read
        fetch('/api/conversations/'+id+'/read', { method:'PUT' });
        conv.unread = 0;
        renderConvList();
        const unread = conversations.reduce((s,c)=>s+(c.unread||0),0);
        const badge = document.getElementById('chat-badge');
        if (unread > 0) { badge.style.display='inline'; badge.textContent=unread; }
        else { badge.style.display='none'; }
      } catch(e) {
        main.innerHTML = '<div class="chat-empty">加载失败</div>';
      }
    }

    function escHtml(s) {
      return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');
    }

    async function sendMsg() {
      const input = document.getElementById('chat-input');
      const text = input.value.trim();
      if (!text || !activeConvId) return;
      input.value = '';

      try {
        const r = await fetch('/api/conversations/'+activeConvId+'/messages', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sender: 'admin', content: text })
        });
        const msg = await r.json();
        
        // Add to UI
        const msgDiv = document.getElementById('chat-msgs');
        const time = new Date(msg.createdAt).toLocaleTimeString('zh-CN',{hour:'2-digit',minute:'2-digit'});
        msgDiv.innerHTML += '<div class="chat-msg admin"><div><div class="chat-bubble">'+escHtml(text)+'</div><div class="chat-msg-time">'+time+'</div></div></div>';
        msgDiv.scrollTop = msgDiv.scrollHeight;

        // Update conversation list
        const conv = conversations.find(c => c._id === activeConvId);
        if (conv) {
          if (!conv.messages) conv.messages = [];
          conv.messages.push(msg);
          conv.updatedAt = msg.createdAt;
          renderConvList();
        }
      } catch(e) {
        alert('发送失败: '+e);
      }
    }

    async function deleteConv(id) {
      if (!confirm('确定删除此对话？')) return;
      await fetch('/api/conversations/'+id, { method: 'DELETE' });
      if (activeConvId === id) {
        activeConvId = null;
        document.getElementById('chat-main').innerHTML = '<div class="chat-empty">← 选择一个对话开始聊天</div>';
      }
      loadConversations();
    }

    function connectChatWs() {
      try {
        const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
        chatWs = new WebSocket(proto + '//' + location.host + '/ws/chat?role=admin');
        chatWs.onmessage = (e) => {
          try {
            const data = JSON.parse(e.data);
            if (data.type === 'new_message' || data.type === 'new_conversation') {
              loadConversations();
              if (activeConvId && data.convId === activeConvId) {
                openChat(activeConvId);
              }
            }
          } catch(err) {}
        };
        chatWs.onclose = () => { setTimeout(connectChatWs, 3000); };
        chatWs.onerror = () => {};
      } catch(e) {}
    }

    // Auto-refresh conversations every 10s when on chat tab
    setInterval(() => {
      if (document.getElementById('c').classList.contains('show')) {
        loadConversations();
      }
    }, 10000);

    // Initial load
    loadP();
  </script>
</body>
</html>'''

# Encode and upload
import base64
b64 = base64.b64encode(NEW_ADMIN_HTML.encode('utf-8')).decode('ascii')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USER, PWD, timeout=10)

print("=" * 60)
print("DEPLOYING admin.html WITH CHAT TAB")
print("=" * 60)

# Backup old admin.html
print("\n=== Backup ===")
stdin, stdout, stderr = client.exec_command('cp /root/backend/admin.html /root/backend/admin.html.bak.$(date +%Y%m%d%H%M%S) && echo "backed up"')
print(stdout.read().decode('utf-8', errors='replace').strip())

# Write new admin.html
print("\n=== Write new admin.html ===")
cmd = f'echo "{b64}" | base64 -d > /root/backend/admin.html && wc -c /root/backend/admin.html'
stdin, stdout, stderr = client.exec_command(cmd)
print(stdout.read().decode('utf-8', errors='replace').strip())
err = stderr.read().decode('utf-8', errors='replace').strip()
if err: print("ERR:", err)

# Also copy to frontend dir
stdin, stdout, stderr = client.exec_command('cp /root/backend/admin.html /var/www/frontend/admin.html && echo "copied to frontend"')
print(stdout.read().decode('utf-8', errors='replace').strip())

# Restart backend
print("\n=== Restart backend ===")
stdin, stdout, stderr = client.exec_command('pm2 restart tokai-backend')
print(stdout.read().decode('utf-8', errors='replace').strip())

time.sleep(2)

# Verify
print("\n=== Verify ===")
stdin, stdout, stderr = client.exec_command('curl -s http://localhost/admin | grep -c "chat-wrap"')
print("Chat wrap found:", stdout.read().decode('utf-8', errors='replace').strip())

stdin, stdout, stderr = client.exec_command('curl -s http://localhost/admin | grep -c "在线客服"')
print("Chat tab found:", stdout.read().decode('utf-8', errors='replace').strip())

stdin, stdout, stderr = client.exec_command('curl -s http://localhost/admin | grep -c "connectChatWs"')
print("WebSocket logic found:", stdout.read().decode('utf-8', errors='replace').strip())

# Check conversations API
print("\n=== Test conversations API ===")
stdin, stdout, stderr = client.exec_command('curl -s http://localhost/api/conversations | python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d),\'conversations\')"')
print(stdout.read().decode('utf-8', errors='replace').strip())

print("\n=== Done! ===")
print("Visit http://8.138.218.146/admin and click '在线客服' tab")
client.close()
