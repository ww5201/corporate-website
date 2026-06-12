import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.', timeout=10)

def run(cmd, t=10):
    try:
        stdin, stdout, stderr = ssh.exec_command(cmd, timeout=t)
        return stdout.read().decode('utf-8', errors='replace').strip()
    except:
        return "TIMEOUT"

print("=== 内存情况 ===")
print(run("free -h"))

print("\n=== 进程占用 ===")
print(run("ps aux --sort=-%mem | head -15"))

print("\n=== 系统负载 ===")
print(run("uptime"))

print("\n=== 检查 OOM ===")
print(run("dmesg | grep -i 'oom\\|killed' | tail -5"))

print("\n=== 清理内存缓存 ===")
run("sync; echo 3 > /proc/sys/vm/drop_caches")
print("缓存已清理")

print("\n=== 清理后内存 ===")
print(run("free -h"))

# 杀掉占用内存的进程
print("\n=== 可疑进程 ===")
procs = run("ps aux | grep -E 'node|java|mysql' | grep -v grep")
print(procs)

# 重启后端
print("\n=== 重启后端 ===")
run("pkill -f 'node server' 2>/dev/null")
import time
time.sleep(1)
run("cd /root/backend && nohup node server-v4.js > /tmp/server.log 2>&1 &")
time.sleep(2)
print(run("curl -s http://127.0.0.1:3000/api/health"))

ssh.close()
print("\n✅ Done")
