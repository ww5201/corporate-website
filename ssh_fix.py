import paramiko
import sys

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('8.138.218.146', port=22, username='root', password='ww0987654.', timeout=10)
    
    # Check file size
    stdin, stdout, stderr = ssh.exec_command('wc -c /var/www/frontend/index.html && nginx -s reload && echo RELOADED')
    output = stdout.read().decode('utf-8')
    print(f"File size: {output}")
    
    ssh.close()
    print("SSH SUCCESS")
except Exception as e:
    print(f"SSH FAILED: {e}")
    sys.exit(1)
