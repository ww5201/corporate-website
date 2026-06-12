import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', errors='replace').strip()

# 检查产品卡片是否有data-product-index
html = run('curl -s http://localhost/')
print('data-product-index count:', html.count('data-product-index'))
print('lightbox-overlay count:', html.count('lightbox-overlay'))
print('closeLightbox count:', html.count('closeLightbox'))
print('product-image img tag count:', html.count('product-image'))

# 检查JS是否正确
js = run('curl -s http://localhost/assets/' + [f for f in run('ls /var/www/frontend/assets/').split('\n') if f.endswith('.js')][0])
print('JS openLightbox defined:', 'openLightbox' in js)
print('JS event delegation:', 'data-product-index' in js)

ssh.close()
