import paramiko, base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# === FIX 1: openOrder onclick - change 4 params to 1 ===
old_onclick = '''onclick="openOrder('${p._id}','${p.name.replace(/'/g,"\\\\'")}',${p.price},'${imgs[0]||''}')">立即咨询</button>'''
new_onclick = '''onclick="openOrder('${p._id}')">立即咨询</button>'''

if old_onclick in html:
    html = html.replace(old_onclick, new_onclick)
    print("Fixed openOrder onclick (4 params -> 1 param)")
else:
    # Try alternate escaping
    old2 = 'onclick="openOrder'
    idx = html.find(old2)
    if idx > 0:
        # Find the full onclick and replace it
        end = html.find('">立即咨询</button>', idx)
        if end > 0:
            full_old = html[idx:end + len('">立即咨询</button>')]
            # Extract the product ID parameter
            # The onclick is like: onclick="openOrder('${p._id}','${p.name...}',${p.price},'${imgs[0]||''}')"
            new_onclick2 = '''onclick="openOrder('${p._id}')">立即咨询</button>'''
            html = html.replace(full_old, new_onclick2)
            print("Fixed openOrder onclick (alternate method)")
    else:
        print("WARNING: Could not find openOrder onclick")

# === FIX 2: Mobile bottom nav "咨询" - make it scroll to contact or open order ===
# Find mobile_consult in the nav
mobile_consult_idx = html.find('mobile_consult')
if mobile_consult_idx > 0:
    # Check the mobile nav rendering
    nav_context = html[mobile_consult_idx-500:mobile_consult_idx+500]
    print(f"Mobile nav context found")

# === FIX 3: openOrder function - also accept name/price for better UX ===
old_openOrder = """function openOrder(pid) {
      curProd = products.find(p => p._id === pid);
      if (!curProd) return;
      document.getElementById('orderTitle').textContent = curProd.name;
      document.getElementById('orderPrice').textContent = '¥' + curProd.price;
      document.getElementById('orderModal').style.display = 'flex';
      selectPay('wechat');
    }"""

new_openOrder = """function openOrder(pid) {
      curProd = products.find(p => p._id === pid);
      if (!curProd) { alert('Product not found'); return; }
      document.getElementById('orderTitle').textContent = curProd.name;
      document.getElementById('orderPrice').textContent = '¥' + curProd.price;
      document.getElementById('orderModal').style.display = 'flex';
      selectPay('wechat');
    }"""

if old_openOrder in html:
    html = html.replace(old_openOrder, new_openOrder)
    print("Fixed openOrder function (added alert for not found)")
else:
    print("openOrder function already different")

# === FIX 4: Check for modal CSS ===
if '.modal-overlay' not in html:
    print("WARNING: .modal-overlay CSS missing!")
    # Add modal CSS
    modal_css = """
    .modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.6);display:none;align-items:center;justify-content:center;z-index:10000;padding:16px}
    .modal{background:#fff;border-radius:16px;max-width:420px;width:100%;max-height:90vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.3)}
    .modal-header{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;border-bottom:1px solid #eee}
    .modal-header h3{margin:0;font-size:1.1rem}
    .modal-close{background:none;border:none;font-size:1.5rem;cursor:pointer;color:#999;padding:0 4px}
    .modal-body{padding:20px}
    .modal-product{display:flex;gap:12px;align-items:center;margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid #eee}
    .modal-product img{width:80px;height:80px;object-fit:cover;border-radius:8px}
    .modal-product-info h4{margin:0 0 4px}
    .modal-product-info p{margin:0;color:#e67e22;font-weight:700}
    .order-field{margin-bottom:12px}
    .order-field label{display:block;margin-bottom:4px;font-size:.85rem;color:#666}
    .order-field input,.order-field textarea{width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:8px;font-size:.95rem;box-sizing:border-box}
    .order-field textarea{height:60px;resize:none}
    .pay-methods{display:flex;gap:8px}
    .pay-btn{flex:1;padding:8px;border:2px solid #eee;border-radius:8px;text-align:center;cursor:pointer;font-size:.9rem;transition:all .2s}
    .pay-btn.active{border-color:#e67e22;background:#fff8f0}
    .qr-box{text-align:center;margin:16px 0}
    .qr-box img{max-width:200px;max-height:200px;border-radius:8px}
    .qr-box p{font-size:.85rem;color:#777;margin-top:8px}
    .order-btn{width:100%;padding:12px;background:#e67e22;color:#fff;border:none;border-radius:8px;font-size:1rem;cursor:pointer;font-weight:700}
    .order-btn:hover{background:#d35400}
    .order-success{text-align:center;padding:20px}
    .order-success .icon{font-size:3rem;margin-bottom:12px}
    .order-success h3{color:#27ae60;margin:0 0 8px}
    .order-success p{color:#777;font-size:.9rem}
"""
    # Insert before </style>
    html = html.replace('</style>', modal_css + '</style>')
    print("Added modal CSS")
else:
    print("Modal CSS already exists")

# === FIX 5: Check for mobile nav "咨询" button click handler ===
# The mobile bottom nav should have a clickable "咨询" item
mobile_nav_idx = html.find('mobileNav')
if mobile_nav_idx > 0:
    # Find the mobileNav innerHTML template
    inner_idx = html.find('mobileNav.innerHTML', mobile_nav_idx)
    if inner_idx > 0:
        context = html[inner_idx:inner_idx+800]
        print(f"Mobile nav template found")

# Verify JS still valid
import re
js_start = html.find('<script>') + 8
js_end = html.rfind('</script>')
js = html[js_start:js_end]

with open('D:/tokai/fix_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"File size: {len(html)}\n")
    f.write(f"Braces: {js.count('{')}:{js.count('}')}\n")
    onclick_ok = "openOrder('${p._id}')" in html
    f.write(f"openOrder onclick fixed: {onclick_ok}\n")
    f.write(f"modal-overlay CSS: {'.modal-overlay' in html}\n")
    f.write(f"openOrder func: {'function openOrder' in js}\n")

# Upload to server
encoded = base64.b64encode(html.encode('utf-8')).decode('ascii')
cmd = f"echo '{encoded}' | base64 -d > /var/www/frontend/index.html"
stdin, stdout, stderr = ssh.exec_command(cmd)
stdout.read()

# Save local
with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Reload nginx
ssh.exec_command('nginx -s reload')

# Validate JS on server
val_cmd = '''node -e "
const fs = require('fs');
const html = fs.readFileSync('/var/www/frontend/index.html', 'utf8');
const start = html.indexOf('<script>') + 8;
const end = html.lastIndexOf('</script>');
const js = html.substring(start, end);
try {
    new Function(js);
    console.log('JS OK');
} catch(e) {
    console.log('JS ERROR: ' + e.message);
}
"'''
stdin, stdout, stderr = ssh.exec_command(val_cmd)
js_val = stdout.read().decode()

with open('D:/tokai/fix_result.txt', 'a', encoding='utf-8') as f:
    f.write(f"Server JS validation: {js_val}\n")

ssh.close()
print("Done - check fix_result.txt")
