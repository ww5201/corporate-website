import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

# Get the openOrder function and the onclick call
import re

with open('D:/tokai/check_consult2.txt', 'w', encoding='utf-8') as out:
    # Find the onclick call in detail
    idx = html.find("onclick=\"openOrder")
    if idx > 0:
        out.write(f"onclick call:\n{html[idx:idx+200]}\n\n")
    
    # Find the openOrder function definition
    idx2 = html.find("function openOrder")
    if idx2 > 0:
        out.write(f"openOrder function:\n{html[idx2:idx2+500]}\n\n")
    
    # Find orderModal HTML
    idx3 = html.find("orderModal")
    if idx3 > 0:
        out.write(f"orderModal HTML:\n{html[max(0,idx3-100):idx3+300]}\n\n")
    
    # Find mobile_consult button
    idx4 = html.find("mobile_consult")
    if idx4 > 0:
        out.write(f"mobile_consult context:\n{html[max(0,idx4-200):idx4+200]}\n\n")

ssh.close()
print("Done")
