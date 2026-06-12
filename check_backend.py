import paramiko, sys  
  
sys.stdout.reconfigure(encoding='utf-8', errors='replace')  
sys.stderr.reconfigure(encoding='utf-8', errors='replace')  
  
client = paramiko.SSHClient()  
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
client.connect('8.138.218.146', 22, 'root', 'ww0987654.', timeout=10) 
