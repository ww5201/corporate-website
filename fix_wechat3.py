import paramiko
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Replace handleWechatClick function - remove weixin://, use clipboard+guide
old_func = """function handleWechatClick() {
    // Try opening WeChat directly via weixin:// protocol
    var wechatNum = '18977122166';
    
    // Method 1: Try weixin:// URL scheme
    try {
        window.location.href = 'weixin://dl/business/?t=' + wechatNum;
        // If we're still here after 1.5s, WeChat probably didn't open
        setTimeout(function() {
            showWechatGuide(false);
        }, 1500);
        return;
    } catch(e) {
        // Fall through to guide
    }
    
    // Fallback: show guide with number
    showWechatGuide(false);"""

# Wait, the function might have different format. Let me find it first.
idx = html.find('function handleWechatClick')
if idx < 0:
    print("ERROR: handleWechatClick not found!")
else:
    print(f"handleWechatClick at {idx}")
    # Show the full function
    end = html.find('</script>', idx)
    func_text = html[idx:end]
    print(f"Function text ({len(func_text)} chars):")
    print(func_text[:200])
    print("...")
    print(func_text[-200:])

    # We need to find where this function ends and replace it
    # The function should end with showWechatGuide(false); 
    # Find the end of the function body (the } that closes it)
    # Look for the pattern: showWechatGuide(false);\n    }\n    \n    // =====
    func_end_marker = 'showWechatGuide(false);'
    after_func = html.find(func_end_marker, idx)
    if after_func >= 0:
        # The function ends after this - find next } that closes it
        start_of_func = html.find('{', html.find('function', idx))
        # Actually, let's just find the specific pattern to replace
        # Look for exact content from function start to the closing }
        
        print(f"\nFound showWechatGuide at {after_func}")
        context = html[after_func:after_func+300]
        print(f"Context: {repr(context[:100])}")
        print(f"Context end: {repr(context[-100:])}")

ssh.close()
