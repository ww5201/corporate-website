import paramiko

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

output_file = "D:/tokai/project_info.txt"
with open(output_file, "w", encoding="utf-8") as f:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(host, port, user, pwd, timeout=10)
        f.write("=== 服务器项目信息 ===\n\n")
        
        # 查看 backend 目录结构
        stdin, stdout, stderr = client.exec_command("ls -la /root/backend/")
        f.write("Backend 目录:\n")
        f.write(stdout.read().decode())
        f.write("\n")
        
        # 查看 server.js 内容
        stdin, stdout, stderr = client.exec_command("cat /root/backend/server.js")
        f.write("=== server.js 内容 ===\n")
        f.write(stdout.read().decode())
        f.write("\n")
        
        # 查看 admin.html 前200行
        stdin, stdout, stderr = client.exec_command("head -200 /root/backend/admin.html")
        f.write("=== admin.html (前200行) ===\n")
        f.write(stdout.read().decode())
        f.write("\n")
        
        # 查看 varwwwfrontend 目录
        stdin, stdout, stderr = client.exec_command("ls -la /root/varwwwfrontend/")
        f.write("=== varwwwfrontend 目录 ===\n")
        f.write(stdout.read().decode())
        f.write("\n")
        
        # 查看进程
        stdin, stdout, stderr = client.exec_command("ps aux | grep node")
        f.write("=== 运行中的 Node 进程 ===\n")
        f.write(stdout.read().decode())
        f.write("\n")
        
        # 查看 package.json
        stdin, stdout, stderr = client.exec_command("cat /root/backend/package.json")
        f.write("=== package.json ===\n")
        f.write(stdout.read().decode())
        f.write("\n")
        
    except Exception as e:
        f.write(f"Error: {e}\n")
        import traceback
        traceback.print_exc(file=f)
    finally:
        client.close()

print("Done")
