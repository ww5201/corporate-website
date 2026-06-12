import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

sftp = ssh.open_sftp()
with sftp.open('/var/www/frontend/index.html', 'r') as f:
    html = f.read().decode('utf-8')
sftp.close()

with open('D:/tokai/debug_all.txt', 'w', encoding='utf-8') as out:
    # 1. Find openOrder onclick in product card
    idx = html.find("openOrder")
    while idx > 0:
        out.write(f"\n=== openOrder at {idx} ===\n")
        out.write(html[max(0,idx-100):idx+300])
        out.write('\n')
        idx = html.find("openOrder", idx+10)
    
    # 2. Find orderModal HTML
    out.write("\n\n=== ORDER MODAL HTML ===\n")
    modal_idx = html.find('id="orderModal"')
    if modal_idx > 0:
        out.write(html[modal_idx:modal_idx+2000])
    
    # 3. Find selectPay function
    out.write("\n\n=== SELECTPAY ===\n")
    sp_idx = html.find("function selectPay")
    if sp_idx > 0:
        out.write(html[sp_idx:sp_idx+500])
    
    # 4. Find submitOrder function
    out.write("\n\n=== SUBMITORDER ===\n")
    so_idx = html.find("function submitOrder")
    if so_idx > 0:
        out.write(html[so_idx:so_idx+800])
    
    # 5. Find closeOrder function
    out.write("\n\n=== CLOSEORDER ===\n")
    co_idx = html.find("function closeOrder")
    if co_idx > 0:
        out.write(html[co_idx:co_idx+500])
    
    # 6. Check for nav menu
    out.write("\n\n=== NAV MENU ===\n")
    nav_idx = html.find('class="nav-links"')
    if nav_idx > 0:
        out.write(html[nav_idx:nav_idx+1000])

    # 7. Check for hamburger menu
    out.write("\n\n=== HAMBURGER ===\n")
    ham_idx = html.find('hamburger')
    if ham_idx > 0:
        out.write(html[ham_idx:ham_idx+500])
    ham_idx2 = html.find('menu-toggle')
    if ham_idx2 > 0:
        out.write(html[ham_idx2:ham_idx2+500])

    # 8. Check mobile nav
    out.write("\n\n=== MOBILE NAV ===\n")
    mn_idx = html.find('mobileNav')
    if mn_idx > 0:
        out.write(html[mn_idx:mn_idx+500])

ssh.close()
print("Done")
