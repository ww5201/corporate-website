import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Search for payment-related code
with open('D:/tokai/payment_search.txt', 'w', encoding='utf-8') as out:
    # Find payment section HTML
    pay_idx = html.find('payment-section')
    out.write(f"payment-section HTML at: {pay_idx}\n")
    
    # Find selectPay or any payment JS
    for keyword in ['selectPay', 'pay-wechat', 'pay-alipay', 'showPayQr', 'payBtn', 'payment']:
        idx = html.find(keyword)
        out.write(f"{keyword}: {idx}\n")
    
    # Find the payment JS section
    pay_js_start = html.find('payConfig')
    if pay_js_start > 0:
        context = html[pay_js_start:pay_js_start+500]
        out.write(f"\npayConfig context:\n{context}\n")
    else:
        out.write("\npayConfig NOT FOUND\n")
    
    # Check what's between payment HTML and scripts
    pay_html = html.find('id="payment"')
    out.write(f"\npayment id at: {pay_html}\n")

ssh.close()
print("Done")
