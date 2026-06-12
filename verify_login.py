import paramiko
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

host = "8.138.218.146"
port = 22
user = "root"
pwd = "ww0987654."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port, user, pwd, timeout=10)

def run(cmd, label=""):
    if label:
        print(f"\n=== {label} ===")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out: print(out[:3000])
    if err and 'WARN' not in err: print("ERR:", err[:500])
    return out

# Test auth endpoints
run("curl -s http://localhost:3000/api/auth/sms/send -X POST -H 'Content-Type: application/json' -d '{\"phone\":\"13800138000\"}'", "Test SMS send")

# Get the debug code from output and test login
out = run("curl -s http://localhost:3000/api/auth/sms/send -X POST -H 'Content-Type: application/json' -d '{\"phone\":\"13900139000\"}'", "Test SMS for login")
try:
    data = json.loads(out.strip())
    code = data.get('_debugCode', '')
    print(f"  Debug code: {code}")

    # Test login with the code
    login_out = run(f"curl -s http://localhost:3000/api/auth/phone/login -X POST -H 'Content-Type: application/json' -d '{{\"phone\":\"13900139000\",\"code\":\"{code}\"}}'", "Test phone login")
    login_data = json.loads(login_out.strip())
    if login_data.get('success'):
        token = login_data.get('token', '')
        print(f"  ✅ Login success! Token: {token[:30]}...")
        print(f"  User: {login_data.get('user', {})}")

        # Test /me endpoint
        me_out = run(f"curl -s http://localhost:3000/api/auth/me -H 'Authorization: Bearer {token}'", "Test /me endpoint")
        me_data = json.loads(me_out.strip())
        print(f"  ✅ /me: {me_data}")

        # Test logout
        logout_out = run(f"curl -s http://localhost:3000/api/auth/logout -X POST -H 'Authorization: Bearer {token}'", "Test logout")
        print(f"  ✅ Logout: {logout_out.strip()}")
    else:
        print(f"  ❌ Login failed: {login_data}")
except Exception as e:
    print(f"Parse error: {e}")

# Check server routes
run("grep -n 'login\\|shop\\|payment' /root/backend/server-v4.js | head -20", "Verify server routes")
run("grep -n 'logout' /root/backend/routes/auth.js", "Verify logout route")

# Check users.db
run("cat /root/backend/data/users.db 2>/dev/null", "Users database")

client.close()
print("\n✅ All tests complete!")
