import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    return stdout.read().decode('utf-8', errors='replace').strip()

# 检查nginx配置
print('=== nginx配置 ===')
print(run('cat /etc/nginx/conf.d/site.conf'))

# 检查图片通过nginx访问的完整header
print('\n=== 图片请求header ===')
print(run('curl -sI http://localhost/uploads/1779850816993-ql0rh1icf.png'))

# 检查API返回的数据格式
print('\n=== API产品数据 ===')
print(run('curl -s http://localhost/api/products'))

# 检查前端HTML是否有正确的JS引用
print('\n=== 前端HTML ===')
print(run('cat /var/www/frontend/index.html | grep -E "(script|assets)"'))

# 检查JS文件中图片处理逻辑
print('\n=== JS中图片处理 ===')
js = run('curl -s http://localhost/assets/index-DnyHXUWK.js')
# 找到图片处理部分
idx = js.find('images')
if idx > -1:
    print(js[max(0,idx-100):idx+300])

# 直接用浏览器模拟访问
print('\n=== 测试完整页面 ===')
print(run('curl -s http://localhost/ | grep -o "products-grid.*</section>" | head -1')[:500])

ssh.close()
