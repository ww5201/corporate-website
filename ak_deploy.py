import sys
import json
import base64

# Will be filled with user's credentials
ACCESS_KEY_ID = sys.argv[1] if len(sys.argv) > 1 else "YOUR_AK_ID"
ACCESS_KEY_SECRET = sys.argv[2] if len(sys.argv) > 2 else "YOUR_AK_SECRET"

# Read the fixed HTML file
html_path = "D:/tokai/index-fixed2.html"
with open(html_path, "rb") as f:
    html_data = f.read()

b64_data = base64.b64encode(html_data).decode()
print(f"HTML file size: {len(html_data)} bytes")
print(f"Base64 size: {len(b64_data)} chars")

# Split into chunks of 10000 chars
chunk_size = 10000
chunks = [b64_data[i:i+chunk_size] for i in range(0, len(b64_data), chunk_size)]
print(f"Chunks needed: {len(chunks)}")

try:
    from aliyunsdkecs.request.v20140526.RunCommandRequest import RunCommandRequest
    from aliyunsdkcore.client import AcsClient
    
    client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, "cn-guangzhou")
    instance_id = "i-7xv9l4awz756t6zatq6r"
    
    # Step 1: Clear old file
    print("\n[1/4] Clearing old file...")
    request = RunCommandRequest()
    request.set_accept_format("json")
    request.set_Type("RunShellScript")
    request.set_CommandContent(base64.b64encode(b"#!/bin/bash\n> /tmp/html.b64\n> /tmp/html.gz.b64\necho 'cleared'\n").decode())
    request.set_InstanceIds(json.dumps([instance_id]))
    request.set_Timeout(60)
    response = client.do_action_with_exception(request)
    result = json.loads(response)
    invoke_id = result.get("InvokeId", "")
    print(f"  InvokeId: {invoke_id}")
    
    import time
    time.sleep(5)
    
    # Step 2: Send chunks
    for i, chunk in enumerate(chunks):
        print(f"\n[{i+2}/{len(chunks)+3}] Sending chunk {i} ({len(chunk)} chars)...")
        cmd = f"#!/bin/bash\necho '{chunk}' >> /tmp/html.b64\n"
        request = RunCommandRequest()
        request.set_accept_format("json")
        request.set_Type("RunShellScript")
        request.set_CommandContent(base64.b64encode(cmd.encode()).decode())
        request.set_InstanceIds(json.dumps([instance_id]))
        request.set_Timeout(60)
        response = client.do_action_with_exception(request)
        result = json.loads(response)
        invoke_id = result.get("InvokeId", "")
        print(f"  InvokeId: {invoke_id}")
        time.sleep(3)
    
    # Step 3: Decode and deploy
    print(f"\n[{len(chunks)+3}/{len(chunks)+3}] Decoding and deploying...")
    decode_cmd = b"""#!/bin/bash
base64 -d /tmp/html.b64 > /var/www/frontend/index.html
sz=$(wc -c < /var/www/frontend/index.html)
echo "Deployed: $sz bytes"
nginx -s reload
echo "DONE"
"""
    request = RunCommandRequest()
    request.set_accept_format("json")
    request.set_Type("RunShellScript")
    request.set_CommandContent(base64.b64encode(decode_cmd).decode())
    request.set_InstanceIds(json.dumps([instance_id]))
    request.set_Timeout(120)
    response = client.do_action_with_exception(request)
    result = json.loads(response)
    invoke_id = result.get("InvokeId", "")
    print(f"  InvokeId: {invoke_id}")
    print(f"\nAll commands sent! Check results at:")
    print(f"https://ecs.console.aliyun.com/cloud-assistant/region/cn-guangzhou/result?InvokeId={invoke_id}")
    
except ImportError as e:
    print(f"\nSDK not installed: {e}")
    print("Run: pip install aliyun-python-sdk-ecs aliyunsdkcore")
except Exception as e:
    print(f"\nError: {e}")
