import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('8.138.218.146', username='root', password='ww0987654.')

# 下载前端文件检查
stdin, stdout, stderr = ssh.exec_command("cat /var/www/frontend/index.html")
html = stdout.read().decode('utf-8', errors='replace')

# 检查 JS 语法 - 搜索常见问题
issues = []

# 检查未闭合的引号
lines = html.split('\n')
for i, line in enumerate(lines):
    # 检查单引号未闭合
    if line.count("'") % 2 != 0 and '//' not in line:
        issues.append(f"Line {i+1}: odd single quotes")
    # 检查双引号未闭合
    if line.count('"') % 2 != 0 and '//' not in line and 'data-' not in line:
        issues.append(f"Line {i+1}: odd double quotes")

# 检查 script 标签
script_open = html.count('<script>')
script_close = html.count('</script>')
if script_open != script_close:
    issues.append(f"Script tags mismatch: {script_open} open, {script_close} close")

# 检查函数定义
import re
funcs = re.findall(r'function (\w+)', html)
print(f"Functions found: {len(funcs)}")

# 检查未闭合的花括号
brace_count = html.count('{') - html.count('}')
if brace_count != 0:
    issues.append(f"Brace mismatch: {brace_count} unclosed")

# 写入结果
with open(r'D:\tokai\html_check.txt', 'w', encoding='utf-8') as f:
    f.write(f"File size: {len(html)} chars, {len(lines)} lines\n")
    f.write(f"Script tags: {script_open} open, {script_close} close\n")
    f.write(f"Functions: {len(funcs)}\n")
    f.write(f"Brace balance: {brace_count}\n\n")
    if issues:
        f.write("ISSUES:\n")
        for iss in issues[:20]:
            f.write(f"  - {iss}\n")
    else:
        f.write("No obvious issues found\n")

ssh.close()
print("Done")
