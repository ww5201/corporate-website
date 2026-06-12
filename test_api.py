import paramiko
import json

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('8.138.218.146', username='root', password='ww0987654.')

def run(cmd):
    i, o, e = c.exec_command(cmd, timeout=10)
    return o.read().decode('utf-8', 'replace').strip()

# 1. Send SMS
print("=== Send SMS ===")
r1 = run('curl -s -X POST http://localhost:3000/api/auth/sms/send -H "Content-Type: application/json" -d \'{"phone":"13800138000"}\'')
print(r1)
sms_data = json.loads(r1)
code = sms_data.get('_debugCode', '')

# 2. Login
print("\n=== Login ===")
r2 = run(f'curl -s -X POST http://localhost:3000/api/auth/phone/login -H "Content-Type: application/json" -d \'{{"phone":"13800138000","code":"{code}"}}\'')
print(r2[:300])
login_data = json.loads(r2)
token = login_data.get('token', '')

# 3. Get profile
print("\n=== Get Profile ===")
r3 = run(f'curl -s http://localhost:3000/api/auth/me -H "Authorization: Bearer {token}"')
print(r3)

# 4. Create payment
print("\n=== Create Payment ===")
r4 = run('curl -s -X POST http://localhost:3000/api/payment/create -H "Content-Type: application/json" -d \'{"productId":"test","productName":"Test Order","amount":100,"customerName":"Test","customerPhone":"13800138000"}\'')
print(r4)
pay_data = json.loads(r4)
order_id = pay_data.get('orderId', '')

# 5. Check payment status
print("\n=== Payment Status ===")
r5 = run(f'curl -s http://localhost:3000/api/payment/status/{order_id}')
print(r5)

# 6. Mock confirm payment
print("\n=== Mock Confirm ===")
r6 = run(f'curl -s -X POST http://localhost:3000/api/payment/mock-confirm -H "Content-Type: application/json" -d \'{{"orderId":"{order_id}"}}\'')
print(r6)

# 7. Create conversation for chat
print("\n=== Create Conversation ===")
r7 = run('curl -s -X POST http://localhost:3000/api/conversations -H "Content-Type: application/json" -d \'{"visitorId":"test_user_001","name":"Test User"}\'')
print(r7[:300])

# 8. Send chat message
conv_data = json.loads(r7)
conv_id = conv_data.get('_id', '')
print(f"\n=== Send Chat Message (conv: {conv_id}) ===")
r8 = run(f'curl -s -X POST http://localhost:3000/api/conversations/{conv_id}/messages -H "Content-Type: application/json" -d \'{{"sender":"visitor","content":"Hello!","type":"text"}}\'')
print(r8)

# 9. Port check
print("\n=== Port Check ===")
r9 = run('ss -tlnp | grep 3000')
print(r9)

c.close()
print("\n=== All Tests Complete ===")
