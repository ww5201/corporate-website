import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.RunCommandRequest import RunCommandRequest
from aliyunsdkecs.request.v20140526.DescribeInvocationResultsRequest import DescribeInvocationResultsRequest
import time

# These will be set before running
client = None

def run_remote_command(cmd, region='cn-guangzhou', instance_id='i-7xv9l4awz756t6zatq6r'):
    """Execute command on server via Cloud Assistant (no SSH needed)"""
    request = RunCommandRequest()
    request.set_Name('RecoverWebsite')
    request.set_CommandContent(cmd)
    request.set_Type('RunShellScript')
    request.set_WorkerInstanceIds([instance_id])
    
    try:
        response = client.do_action_with_exception(request)
        result = json.loads(response)
        invoke_id = result.get('InvokeId')
        print(f'Command sent! InvokeId: {invoke_id}')
        
        # Wait and check result
        time.sleep(10)
        req = DescribeInvocationResultsRequest()
        req.set_InvokeId(str(invoke_id))
        
        for i in range(12):  # Wait up to 60 seconds
            time.sleep(5)
            resp = client.do_action_with_exception(req)
            res = json.loads(resp)
            invocations = res.get('Invocation', {}).get('InvocationResults', [])
            if invocations:
                output = invocations[0].get('Output', '')
                success = invocations[0].get('ExitCode') == 0
                print(f'Success: {success}')
                print(f'Output: {output}')
                return output
        
        return 'TIMEOUT'
    except ServerException as e:
        print(f'Error: {e.get_code()} - {e.get_message()}')
        return None

if __name__ == '__main__':
    # Step 1: Check current file size
    print("=== Checking server file ===")
    run_remote_command("wc -c /var/www/frontend/index.html && head -c 200 /var/www/frontend/index.html")
    
    # Step 2: Download fixed file from tunnel
    print("\n=== Downloading fixed file ===")
    result = run_remote_command(
        "wget -O /var/www/frontend/index.html 'https://few-melons-grab.loca.lt' --timeout=30 && "
        "wc -c /var/www/frontend/index.html && "
        "nginx -s reload && echo '=== RECOVERY COMPLETE ==='"
    )
    
    print(f"\nFinal result: {result}")
