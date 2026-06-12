import webbrowser, base64

# Read fixed file
with open('D:/tokai/index-fixed2.html', 'r', encoding='utf-8') as f:
    html = f.read()

b64 = base64.b64encode(html.encode('utf-8')).decode('ascii')

# Generate the recovery command
cmd = """echo '%s' | base64 -d > /var/www/frontend/index.html && wc -c /var/www/frontend/index.html && nginx -s reload && echo "DONE" """ % b64

# Save command to file
with open('D:/tokai/recover_command.txt', 'w', encoding='utf-8') as f:
    f.write(cmd)

print("Command length: %d chars" % len(cmd))
print("Saved to D:/tokai/recover_command.txt")

# Open Alibaba Cloud console
webbrowser.open('https://ecs.console.aliyun.com/#/server/detail/region/cn-chengdu/instanceId/iZ7xv9l4awz756t6zatq6rZ/tab/vnc')
print("\nOpened Alibaba Cloud console in browser")
