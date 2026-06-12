import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

with open('D:/tokai/full_check2.txt', 'w', encoding='utf-8') as out:
    # File info
    out.write(f"Size: {len(html)}\n")
    out.write(f"Ends with </html>: {html.rstrip().endswith('</html>')}\n")
    out.write(f"Has </body>: {'</body>' in html}\n")
    out.write(f"Has </html>: {'</html>' in html}\n\n")

    # Check script section
    script_start = html.rfind('<script>')
    script_end = html.find('</script>', script_start)
    js = html[script_start:script_end] if script_start > 0 else ""
    
    open_b = js.count('{')
    close_b = js.count('}')
    out.write(f"JS braces: {{={open_b} }}={close_b} diff={open_b-close_b}\n\n")
    
    # Check key functions
    for func in ['function loadData', 'function renderProducts', 'function loadCases', 'function handleWechatClick', 'function showWechatGuide', 'selectPay']:
        idx = html.find(func)
        out.write(f"{func}: found at {idx}\n")
    
    # Check payment section
    pay_idx = html.find('payment-config')
    out.write(f"\npayment-config: {pay_idx}\n")
    
    # Check contact form submit
    submit_idx = html.find('contact-form')
    out.write(f"contact-form: {submit_idx}\n")
    
    # Check mobile nav 咨询 button
    consult_idx = html.find('mobile_consult')
    out.write(f"mobile_consult: {consult_idx}\n")
    
    # Find what's after handleWechatClick
    wc_idx = html.find('function handleWechatClick')
    after_wc = html[wc_idx:wc_idx+200]
    out.write(f"\nhandleWechatClick:\n{after_wc}\n")
    
    # Check for any syntax issues near weixin://
    weixin_idx = html.find('weixin://')
    context = html[weixin_idx-50:weixin_idx+100]
    out.write(f"\nweixin:// context:\n{context}\n")

print("Done")
ssh.close()
