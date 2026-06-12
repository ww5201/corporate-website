import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# The missing functions need to be added back
# These are payment/order management functions

missing_js = """
    // ===== 支付/订单 =====
    function selectPay(method) {
      curPay = method;
      document.querySelectorAll('.pay-btn').forEach(b => b.classList.remove('active'));
      if (method === 'wechat') {
        document.querySelector('.pay-btn:first-child').classList.add('active');
      } else {
        document.querySelector('.pay-btn:last-child').classList.add('active');
      }
      if (payConfig[method + 'Qr']) {
        document.getElementById('qrImg').src = payConfig[method + 'Qr'];
        document.getElementById('qrHint').textContent = '请扫码支付';
      } else {
        document.getElementById('qrImg').src = '';
        document.getElementById('qrHint').textContent = '暂未配置支付二维码';
      }
    }

    function openOrder(pid) {
      curProd = products.find(p => p._id === pid);
      if (!curProd) return;
      document.getElementById('orderTitle').textContent = curProd.name;
      document.getElementById('orderPrice').textContent = '¥' + curProd.price;
      document.getElementById('orderModal').style.display = 'flex';
      selectPay('wechat');
    }

    function closeOrder() {
      document.getElementById('orderModal').style.display = 'none';
      document.getElementById('orderSuccess').style.display = 'none';
      document.getElementById('orderForm').style.display = 'block';
    }

    function submitOrder() {
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
          document.getElementById('orderForm').style.display = 'none';
          document.getElementById('orderSuccess').style.display = 'block';
        } else {
          alert('下单失败，请重试');
        }
      }).catch(function() {
        alert('网络错误');
      });
    }
"""

# Insert before the startup code
startup_marker = "    // ===== 启动 ====="
sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

if startup_marker in html:
    new_html = html.replace(startup_marker, missing_js + "\n" + startup_marker)
    
    # Verify
    import re
    js_start = new_html.find('<script>') + 8
    js_end = new_html.rfind('</script>')
    js = new_html[js_start:js_end]
    
    with open('D:/tokai/add_payment_result.txt', 'w', encoding='utf-8') as f:
        f.write(f"Added missing payment functions\n")
        f.write(f"New size: {len(new_html)}\n")
        f.write(f"selectPay defined: {'function selectPay' in js}\n")
        f.write(f"submitOrder defined: {'function submitOrder' in js}\n")
        f.write(f"openOrder defined: {'function openOrder' in js}\n")
        f.write(f"closeOrder defined: {'function closeOrder' in js}\n")
        
        # Check braces
        f.write(f"Braces: {js.count('{') }:{ js.count('}')}\n")
    
    # Upload
    import base64
    encoded = base64.b64encode(new_html.encode('utf-8')).decode('ascii')
    cmd = "echo '" + encoded + "' | base64 -d > /var/www/frontend/index.html"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.read()
    
    # Also save local
    with open(r'D:/tokai/index-v4.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    # Reload nginx
    ssh.exec_command('nginx -s reload')
    
    with open('D:/tokai/add_payment_result.txt', 'a', encoding='utf-8') as f:
        f.write("\nUploaded and nginx reloaded\n")
else:
    with open('D:/tokai/add_payment_result.txt', 'w', encoding='utf-8') as f:
        f.write(f"ERROR: startup marker not found\n")

ssh.close()
print("Done")
