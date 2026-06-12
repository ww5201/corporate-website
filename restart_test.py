import paramiko
import time

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("8.138.218.146", 22, "root", "ww0987654.")

# Kill ALL node processes
print("Killing all node processes...")
stdin, stdout, stderr = c.exec_command("pkill -9 node; sleep 1; ps aux | grep node | grep -v grep")
time.sleep(2)
print("Remaining:", stdout.read().decode().strip() or "none")

# Start fresh
print("Starting server...")
stdin, stdout, stderr = c.exec_command("cd /root/backend && nohup node server-v4.js > server.log 2>&1 &")
time.sleep(4)

# Test
stdin, stdout, stderr = c.exec_command("curl -s http://localhost:3000/api/health")
print("Health:", stdout.read().decode().strip())

stdin, stdout, stderr = c.exec_command("curl -s http://localhost:3000/api/payment/config")
print("Config:", stdout.read().decode('utf-8', 'replace').strip())

stdin, stdout, stderr = c.exec_command("curl -s http://localhost:3000/api/payment/list")
print("List:", stdout.read().decode('utf-8', 'replace').strip())

# Check log for errors
stdin, stdout, stderr = c.exec_command("cat /root/backend/server.log")
print("Log:", stdout.read().decode('utf-8', 'replace').strip())

c.close()
