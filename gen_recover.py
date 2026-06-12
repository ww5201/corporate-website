import base64, sys

with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Base64 encode
b64 = base64.b64encode(html.encode('utf-8')).decode('ascii')

# Write decode command
with open('D:/tokai/recover_cmd.sh', 'w', encoding='utf-8') as f:
    f.write('#!/bin/bash\n')
    f.write('# ===== 卓翌定制网站恢复命令 =====\n')
    f.write('# 在阿里云控制台 Workbench 远程连接中粘贴此命令\n')
    f.write('# 登录后运行: bash recover_cmd.sh\n')
    f.write('\n')
    f.write('echo "正在恢复网站..."\n')
    f.write("echo '%s' | base64 -d > /var/www/frontend/index.html\n" % b64)
    f.write('echo "文件大小: $(wc -c < /var/www/frontend/index.html) bytes"\n')
    f.write('nginx -s reload\n')
    f.write('echo "=== 恢复完成! ==="\n')

print("HTML size: %d bytes" % len(html))
print("Base64 size: %d chars" % len(b64))
print("Command saved to D:/tokai/recover_cmd.sh")
