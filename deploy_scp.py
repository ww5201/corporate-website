"""
部署脚本：通过 SFTP 将支付系统文件上传到服务器并重启服务
"""
import paramiko
import os
import sys

# ========== 服务器配置 ==========
HOST = "8.138.218.146"
PORT = 22
USER = "root"
# 从命令行参数或环境变量获取密码
PASS = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SERVER_PASS", "")

if not PASS:
    print("ERROR: 请提供服务器密码")
    print("用法: python deploy_scp.py <密码>")
    sys.exit(1)

# ========== 要上传的文件 ==========
FILES = [
    ("D:\\tokai\\backend\\routes\\payment.js", "/root/backend/routes/payment.js"),
    ("D:\\tokai\\backend\\payment.html",       "/root/backend/payment.html"),
    ("D:\\tokai\\backend\\server-v4.js",        "/root/backend/server-v4.js"),
]

# ========== 执行部署 ==========
def deploy():
    print(f"连接服务器 {HOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(HOST, port=PORT, username=USER, password=PASS, timeout=15)
        print("[OK] SSH connected")
    except Exception as e:
        print(f"[FAIL] Connection error: {e}")
        sys.exit(1)

    sftp = client.open_sftp()
    
    # 确保目录存在
    print("\n确保远程目录存在...")
    for local, remote in FILES:
        dirname = os.path.dirname(remote)
        try:
            sftp.stat(dirname)
        except FileNotFoundError:
            stdin, stdout, stderr = client.exec_command(f"mkdir -p {dirname}")
            stdout.read()
            print(f"  创建目录: {dirname}")

    # 上传文件
    print("\n上传文件...")
    for local, remote in FILES:
        if not os.path.exists(local):
            print(f"  [SKIP] Local file not found: {local}")
            continue
        try:
            sftp.put(local, remote)
            size = sftp.stat(remote).st_size
            print(f"  [OK] {os.path.basename(local)} -> {remote} ({size} bytes)")
        except Exception as e:
            print(f"  [FAIL] Upload error {os.path.basename(local)}: {e}")

    sftp.close()
    
    # 重启服务
    print("\n重启后端服务...")
    restart_cmd = "pkill -9 node; sleep 2 && cd /root/backend && nohup node server-v4.js > server.log 2>&1 &"
    stdin, stdout, stderr = client.exec_command(restart_cmd)
    stdout.read()
    
    # 等待启动并测试
    print("等待服务启动...")
    import time
    time.sleep(3)
    
    stdin, stdout, stderr = client.exec_command("curl -s http://localhost:3000/api/payment/config")
    result = stdout.read().decode()
    print(f"\n服务测试结果:\n{result}")
    
    client.close()
    print("\n[OK] Deploy done!")

if __name__ == "__main__":
    deploy()
