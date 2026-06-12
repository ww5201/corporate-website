import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 创建systemd服务让后端开机自启
service = """[Unit]
Description=ZhuoYi Backend Server
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/backend
ExecStart=/usr/bin/node server-v4.js
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
"""

# 写入服务文件
stdin, stdout, stderr = ssh.exec_command("cat > /etc/systemd/system/zhuoyi-backend.service << 'EOF'\n" + service + "EOF")
stdout.read()

# 启用服务
ssh.exec_command("systemctl daemon-reload")
ssh.exec_command("systemctl enable zhuoyi-backend.service")
ssh.exec_command("systemctl start zhuoyi-backend.service")

import time
time.sleep(2)

# 验证
stdin, stdout, stderr = ssh.exec_command("systemctl status zhuoyi-backend.service | head -5")
status = stdout.read().decode('utf-8', errors='replace').strip()
print(f"Service status:\n{status}")

ssh.close()
print("Done!")
