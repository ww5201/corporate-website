# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 注册中文字体
font_paths = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/simhei.ttf",
]
chinese_font = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont('ChineseFont', fp))
            chinese_font = 'ChineseFont'
            break
        except:
            continue
if not chinese_font:
    chinese_font = 'Helvetica'

# ============================================================
# Shell 命令数据
# ============================================================

# 文件操作
file_cmds = [
    ("ls", "列出目录内容", "ls -la"),
    ("cd", "切换目录", "cd /home"),
    ("pwd", "显示当前工作目录", "pwd"),
    ("cp", "复制文件/目录", "cp -r src/ dest/"),
    ("mv", "移动/重命名文件", "mv old.txt new.txt"),
    ("rm", "删除文件/目录", "rm -rf dir/"),
    ("mkdir", "创建目录", "mkdir -p a/b/c"),
    ("rmdir", "删除空目录", "rmdir empty_dir"),
    ("touch", "创建空文件/更新时间戳", "touch file.txt"),
    ("ln", "创建链接", "ln -s target link"),
    ("find", "查找文件", "find . -name '*.txt'"),
    ("locate", "快速定位文件", "locate filename"),
    ("which", "查找命令位置", "which python"),
    ("whereis", "查找命令相关文件", "whereis nginx"),
    ("stat", "显示文件详细信息", "stat file.txt"),
    ("file", "检测文件类型", "file image.png"),
    ("readlink", "查看链接指向", "readlink -f link"),
    ("basename", "提取文件名", "basename /path/file.txt"),
    ("dirname", "提取目录路径", "dirname /path/file.txt"),
    ("realpath", "显示绝对路径", "realpath ../file"),
    ("tree", "树状显示目录结构", "tree -L 2"),
    ("du", "查看目录/文件大小", "du -sh *"),
    ("df", "查看磁盘使用情况", "df -h"),
    ("mount", "挂载文件系统", "mount /dev/sda1 /mnt"),
    ("umount", "卸载文件系统", "umount /mnt"),
]

# 文件内容
content_cmds = [
    ("cat", "查看文件内容", "cat file.txt"),
    ("less", "分页查看文件", "less big_file.log"),
    ("more", "分页查看（简单版）", "more file.txt"),
    ("head", "查看文件开头", "head -n 20 file.txt"),
    ("tail", "查看文件末尾", "tail -f log.txt"),
    ("grep", "搜索文本内容", "grep 'error' log.txt"),
    ("egrep", "扩展正则搜索", "egrep 'err|warn' log.txt"),
    ("fgrep", "固定字符串搜索", "fgrep 'exact text' file"),
    ("awk", "文本处理/列操作", "awk '{print $1}' file"),
    ("sed", "流编辑器（替换/删除）", "sed 's/old/new/g' file"),
    ("sort", "排序", "sort -n numbers.txt"),
    ("uniq", "去除重复行", "sort file | uniq"),
    ("wc", "统计行数/单词数", "wc -l file.txt"),
    ("tr", "字符转换/删除", "tr 'a-z' 'A-Z'"),
    ("cut", "按列截取", "cut -d':' -f1 /etc/passwd"),
    ("paste", "按行合并文件", "paste file1 file2"),
    ("join", "按行连接文件", "join file1 file2"),
    ("diff", "比较文件差异", "diff file1 file2"),
    ("cmp", "逐字节比较", "cmp file1 file2"),
    ("comm", "比较已排序文件", "comm sorted1 sorted2"),
    ("tee", "输出同时写入文件", "cmd | tee output.txt"),
    ("xargs", "将输入转换为命令参数", "find . -name '*.txt' | xargs rm"),
    ("strings", "提取二进制文件中的字符串", "strings binary_file"),
    ("iconv", "字符编码转换", "iconv -f GBK -t UTF-8 file"),
    ("fmt", "文本格式化", "fmt -w 80 file.txt"),
    ("nl", "显示行号", "nl file.txt"),
    ("rev", "反转每一行", "rev file.txt"),
    ("column", "格式化为表格", "column -t file"),
]

# 系统信息
system_cmds = [
    ("uname", "系统信息", "uname -a"),
    ("hostname", "主机名", "hostname"),
    ("uptime", "运行时间和负载", "uptime"),
    ("whoami", "当前用户名", "whoami"),
    ("id", "用户/组 ID 信息", "id"),
    ("w", "当前登录用户", "w"),
    ("who", "登录用户列表", "who"),
    ("last", "登录历史记录", "last"),
    ("date", "显示/设置日期", "date '+%Y-%m-%d'"),
    ("cal", "显示日历", "cal 2026"),
    ("time", "计时", "time ls"),
    ("free", "查看内存使用", "free -h"),
    ("top", "实时进程监控", "top"),
    ("htop", "增强版 top", "htop"),
    ("ps", "查看进程", "ps aux"),
    ("pstree", "进程树", "pstree"),
    ("pgrep", "按名称查找进程", "pgrep nginx"),
    ("pidof", "获取进程 ID", "pidof python"),
    ("nice", "以低优先级运行", "nice -n 10 cmd"),
    ("renice", "修改进程优先级", "renice -5 -p PID"),
    ("kill", "终止进程", "kill -9 PID"),
    ("killall", "按名称终止进程", "killall firefox"),
    ("pkill", "按模式终止进程", "pkill python"),
    ("lsof", "查看打开的文件", "lsof -i :80"),
    ("fuser", "查找占用端口的进程", "fuser 80/tcp"),
    ("strace", "跟踪系统调用", "strace ls"),
    ("ltrace", "跟踪库调用", "ltrace ls"),
    ("dmesg", "内核日志", "dmesg | tail"),
    ("lsmod", "已加载内核模块", "lsmod"),
    ("modinfo", "模块信息", "modinfo e1000"),
    ("lscpu", "CPU 信息", "lscpu"),
    ("lsblk", "块设备信息", "lsblk"),
    ("lsusb", "USB 设备信息", "lsusb"),
    ("lspci", "PCI 设备信息", "lspci"),
    ("dmidecode", "硬件详细信息", "dmidecode"),
    ("nproc", "CPU 核心数", "nproc"),
    ("getconf", "系统配置参数", "getconf PAGE_SIZE"),
    ("ulimit", "资源限制", "ulimit -a"),
    ("sysctl", "内核参数", "sysctl -a"),
    ("ulimit", "用户资源限制", "ulimit -n"),
]

# 网络相关
network_cmds = [
    ("ping", "测试网络连通性", "ping google.com"),
    ("traceroute", "追踪路由", "traceroute google.com"),
    ("mtr", "网络诊断工具", "mtr google.com"),
    ("curl", "HTTP 请求/下载", "curl -O url/file"),
    ("wget", "下载文件", "wget url/file"),
    ("ifconfig", "网络接口配置", "ifconfig"),
    ("ip", "网络配置（新版）", "ip addr show"),
    ("route", "路由表", "route -n"),
    ("ip route", "路由表（新版）", "ip route"),
    ("netstat", "网络连接信息", "netstat -tuln"),
    ("ss", "Socket 统计（新版）", "ss -tuln"),
    ("nslookup", "DNS 查询", "nslookup domain.com"),
    ("dig", "详细 DNS 查询", "dig domain.com"),
    ("host", "DNS 查询（简单）", "host domain.com"),
    ("arp", "ARP 缓存", "arp -a"),
    ("ip neigh", "邻居表（新版）", "ip neigh"),
    ("scp", "安全复制文件", "scp file user@host:/path"),
    ("rsync", "远程同步", "rsync -avz src/ dest/"),
    ("ssh", "远程登录", "ssh user@host"),
    ("telnet", "Telnet 连接", "telnet host port"),
    ("nc", "网络瑞士军刀", "nc -zv host port"),
    ("nmap", "端口扫描", "nmap -sV host"),
    ("ip link", "网络接口状态", "ip link show"),
    ("ethtool", "网卡信息", "ethtool eth0"),
    ("tcpdump", "抓包工具", "tcpdump -i eth0"),
    ("iptables", "防火墙规则", "iptables -L"),
    ("firewall-cmd", "firewalld 管理", "firewall-cmd --list-all"),
    ("ufw", "简易防火墙", "ufw status"),
    ("nft", "新一代防火墙", "nft list ruleset"),
    ("speedtest", "网速测试", "speedtest-cli"),
    ("ipconfig", "Windows 网络配置", "ipconfig /all"),
    ("tracert", "Windows 路由追踪", "tracert google.com"),
    ("nslookup", "DNS 查询", "nslookup google.com"),
    ("pathping", "Windows 路由诊断", "pathping google.com"),
]

# 包管理
package_cmds = [
    ("apt", "Debian/Ubuntu 包管理", "apt install nginx"),
    ("apt-get", "APT 旧版命令", "apt-get update"),
    ("dpkg", "Debian 包管理", "dpkg -i package.deb"),
    ("yum", "CentOS/RHEL 包管理", "yum install nginx"),
    ("dnf", "Fedora 包管理", "dnf install nginx"),
    ("rpm", "RPM 包管理", "rpm -ivh package.rpm"),
    ("pip", "Python 包管理", "pip install numpy"),
    ("pip3", "Python3 包管理", "pip3 install requests"),
    ("npm", "Node.js 包管理", "npm install express"),
    ("yarn", "Yarn 包管理", "yarn add lodash"),
    ("pnpm", "pnpm 包管理", "pnpm install"),
    ("gem", "Ruby 包管理", "gem install rails"),
    ("cargo", "Rust 包管理", "cargo install ripgrep"),
    ("brew", "macOS 包管理", "brew install wget"),
    ("snap", "Snap 包管理", "snap install code"),
    ("flatpak", "Flatpak 包管理", "flatpak install firefox"),
    ("pacman", "Arch Linux 包管理", "pacman -S nginx"),
    ("zypper", "openSUSE 包管理", "zypper install nginx"),
    ("composer", "PHP 依赖管理", "composer install"),
    ("nuget", "NuGet 包管理", "nuget install Newtonsoft.Json"),
]

# 压缩解压
archive_cmds = [
    ("tar", "打包/解包", "tar -xvf archive.tar.gz"),
    ("gzip", "gzip 压缩", "gzip file.txt"),
    ("gunzip", "gzip 解压", "gunzip file.gz"),
    ("bzip2", "bzip2 压缩", "bzip2 file.txt"),
    ("bunzip2", "bzip2 解压", "bunzip2 file.bz2"),
    ("xz", "xz 压缩", "xz file.txt"),
    ("unxz", "xz 解压", "unxz file.xz"),
    ("zip", "zip 压缩", "zip -r archive.zip dir/"),
    ("unzip", "zip 解压", "unzip archive.zip"),
    ("7z", "7-Zip 压缩/解压", "7z x archive.7z"),
    ("rar", "RAR 解压", "unrar x archive.rar"),
    ("zcat", "查看 gzip 内容", "zcat file.gz"),
    ("zmore", "分页查看 gzip", "zmore file.gz"),
    ("tar -czvf", "打包并 gzip 压缩", "tar -czvf archive.tar.gz dir/"),
    ("tar -xzvf", "解压 gzip 包", "tar -xzvf archive.tar.gz"),
    ("tar -cjvf", "打包并 bzip2 压缩", "tar -cjvf archive.tar.bz2 dir/"),
    ("tar -xjvf", "解压 bzip2 包", "tar -xjvf archive.tar.bz2"),
    ("tar -cJvf", "打包并 xz 压缩", "tar -cJvf archive.tar.xz dir/"),
    ("tar -xJvf", "解压 xz 包", "tar -xJvf archive.tar.xz"),
]

# 用户管理
user_cmds = [
    ("useradd", "创建用户", "useradd -m username"),
    ("usermod", "修改用户", "usermod -aG sudo user"),
    ("userdel", "删除用户", "userdel -r username"),
    ("passwd", "修改密码", "passwd username"),
    ("groupadd", "创建用户组", "groupadd groupname"),
    ("groupdel", "删除用户组", "groupdel groupname"),
    ("groups", "查看用户所属组", "groups username"),
    ("chown", "修改文件所有者", "chown user:group file"),
    ("chmod", "修改文件权限", "chmod 755 file"),
    ("chgrp", "修改文件所属组", "chgrp group file"),
    ("su", "切换用户", "su - username"),
    ("sudo", "以管理员执行", "sudo command"),
    ("visudo", "编辑 sudoers", "visudo"),
    ("w", "查看当前用户", "w"),
    ("who", "当前登录用户", "who"),
    ("whoami", "当前用户名", "whoami"),
    ("id", "用户 ID 信息", "id username"),
    ("finger", "用户信息查询", "finger username"),
    ("pkill", "按用户名终止进程", "pkill -u username"),
    ("lastlog", "最后登录时间", "lastlog"),
]

# 进程管理
process_cmds = [
    ("ps", "查看进程", "ps aux | grep nginx"),
    ("top", "实时进程监控", "top"),
    ("htop", "增强版 top", "htop"),
    ("pgrep", "按名称查找进程", "pgrep nginx"),
    ("pkill", "按名称终止进程", "pkill nginx"),
    ("kill", "终止进程", "kill -9 PID"),
    ("killall", "终止所有同名进程", "killall chrome"),
    ("nohup", "后台运行（不挂断）", "nohup cmd &"),
    ("&", "后台运行", "cmd &"),
    ("jobs", "查看后台任务", "jobs"),
    ("fg", "调回前台", "fg %1"),
    ("bg", "继续后台运行", "bg %1"),
    ("disown", "脱离终端", "disown %1"),
    ("screen", "终端复用器", "screen -S session"),
    ("tmux", "终端复用器（新版）", "tmux new -s session"),
    ("crontab", "定时任务", "crontab -e"),
    ("at", "一次性定时任务", "at now + 5 minutes"),
    ("sleep", "休眠", "sleep 5"),
    ("timeout", "限时执行", "timeout 10s cmd"),
    ("watch", "重复执行命令", "watch -n 2 cmd"),
    ("xargs", "参数传递", "cat file | xargs cmd"),
    ("eval", "执行参数中的命令", "eval 'echo hello'"),
    ("exec", "执行命令（替换当前进程）", "exec cmd"),
    ("trap", "信号捕获", "trap 'echo done' EXIT"),
    ("wait", "等待子进程完成", "wait"),
]

# 服务管理
service_cmds = [
    ("systemctl", "systemd 服务管理", "systemctl start nginx"),
    ("service", "SysVinit 服务管理", "service nginx start"),
    ("systemctl start", "启动服务", "systemctl start nginx"),
    ("systemctl stop", "停止服务", "systemctl stop nginx"),
    ("systemctl restart", "重启服务", "systemctl restart nginx"),
    ("systemctl reload", "重载配置", "systemctl reload nginx"),
    ("systemctl status", "查看服务状态", "systemctl status nginx"),
    ("systemctl enable", "开机自启", "systemctl enable nginx"),
    ("systemctl disable", "禁止开机自启", "systemctl disable nginx"),
    ("systemctl list-units", "列出所有服务", "systemctl list-units"),
    ("journalctl", "查看日志", "journalctl -u nginx"),
    ("dmesg", "内核日志", "dmesg | tail -20"),
    ("logwatch", "日志摘要", "logwatch --detail high"),
]

# 磁盘/存储
disk_cmds = [
    ("df", "磁盘使用情况", "df -h"),
    ("du", "目录/文件大小", "du -sh *"),
    ("fdisk", "磁盘分区", "fdisk -l"),
    ("parted", "高级分区工具", "parted /dev/sda"),
    ("mkfs", "格式化文件系统", "mkfs.ext4 /dev/sda1"),
    ("fsck", "文件系统检查", "fsck /dev/sda1"),
    ("mount", "挂载", "mount /dev/sda1 /mnt"),
    ("umount", "卸载", "umount /mnt"),
    ("blkid", "块设备 UUID", "blkid"),
    ("lsblk", "块设备列表", "lsblk"),
    ("lvm", "逻辑卷管理", "lvdisplay"),
    ("resize2fs", "调整 ext4 大小", "resize2fs /dev/sda1"),
    ("iostat", "IO 统计", "iostat -x 1"),
    ("iotop", "IO 实时监控", "iotop"),
    ("smartctl", "硬盘健康检查", "smartctl -a /dev/sda"),
    ("dd", "磁盘复制/备份", "dd if=/dev/sda of=backup.img"),
]

# 文本处理高级
text_cmds = [
    ("awk", "列处理/文本分析", "awk -F: '{print $1}' /etc/passwd"),
    ("sed", "流编辑器", "sed -i 's/old/new/g' file"),
    ("grep", "正则搜索", "grep -E 'err|warn' log"),
    ("egrep", "扩展正则", "egrep 'pattern1|pattern2' file"),
    ("fgrep", "固定字符串", "fgrep 'exact' file"),
    ("sort", "排序", "sort -t: -k3 -n file"),
    ("uniq", "去重", "sort file | uniq -c"),
    ("cut", "截取列", "cut -d' ' -f1,3 file"),
    ("paste", "按行合并", "paste -d',' f1 f2"),
    ("join", "按行连接", "join -t: f1 f2"),
    ("column", "格式化表格", "column -t -s: file"),
    ("tr", "字符转换", "tr '[:lower:]' '[:upper:]'"),
    ("fold", "文本折行", "fold -w 80 file"),
    ("fmt", "文本格式化", "fmt -u -w 72 file"),
    ("par", "段落格式化", "par 72 file"),
    ("pr", "打印格式化", "pr -2 file"),
    ("expand", "制表符转空格", "expand -t 4 file"),
    ("unexpand", "空格转制表符", "unexpand --first-only file"),
    ("nl", "加行号", "nl -ba file"),
    ("cat", "显示/连接文件", "cat -n file"),
    ("tac", "反向显示行", "tac file"),
    ("rev", "反转每行字符", "rev file"),
    ("strings", "提取可打印字符串", "strings binary_file"),
    ("od", "八进制转储", "od -c file"),
    ("hexdump", "十六进制转储", "hexdump -C file"),
    ("xxd", "十六进制转储", "xxd file"),
    ("base64", "Base64 编解码", "base64 file"),
    ("uuencode", "UU 编码", "uuencode file file.uu"),
]

# 环境变量/Shell配置
env_cmds = [
    ("echo", "输出文本/变量", "echo $HOME"),
    ("export", "设置环境变量", "export PATH=$PATH:/new"),
    ("env", "显示所有环境变量", "env"),
    ("printenv", "打印环境变量", "printenv HOME"),
    ("set", "设置 Shell 变量", "set -x"),
    ("unset", "删除变量", "unset MY_VAR"),
    ("alias", "命令别名", "alias ll='ls -la'"),
    ("unalias", "删除别名", "unalias ll"),
    ("history", "命令历史", "history | grep 'python'"),
    ("source", "执行脚本（当前环境）", "source ~/.bashrc"),
    (".", "同 source", ". ~/.profile"),
    ("type", "查看命令类型", "type ls"),
    ("hash", "命令路径缓存", "hash -r"),
    ("hash", "查看缓存", "hash"),
    ("shopt", "Shell 选项", "shopt -s globstar"),
    ("bind", "键盘绑定", "bind -x '\"\\C-r\": __fzf_history__'"),
    ("readonly", "只读变量", "readonly MY_VAR=1"),
    ("declare", "声明变量", "declare -i NUM=42"),
    ("local", "局部变量", "local var=value"),
    ("getopts", "选项解析", "getopts 'abc:' opt"),
    ("printf", "格式化输出", "printf '%-10s %d\\n' name age"),
    ("read", "读取输入", "read -p 'Name: ' name"),
    ("test", "条件判断", "test -f file && echo exists"),
    ("[ ]", "同 test", "[ -f file ]"),
    ("[[ ]]", "增强条件判断", "[[ $str == pattern ]]"),
    ("(( ))", "算术运算", "(( num++ ))"),
    ("$(( ))", "算术展开", "echo $(( 2 + 3 ))"),
    ("$(( ))", "算术运算", "echo $(( 10 % 3 ))"),
    ("$(( ))", "算术运算", "echo $(( 2 ** 8 ))"),
    ("$(( ))", "算术运算", "echo $(( 10 / 3 ))"),
]

# Windows CMD 常用
windows_cmds = [
    ("dir", "列出目录内容（Windows）", "dir C:\\"),
    ("cd", "切换目录", "cd C:\\Users"),
    ("copy", "复制文件", "copy file.txt dest\\"),
    ("xcopy", "增强复制", "xcopy src dest /E"),
    ("robocopy", "可靠复制（高级）", "robocopy src dest /MIR"),
    ("move", "移动/重命名", "move file.txt new.txt"),
    ("del", "删除文件", "del *.tmp"),
    ("rd /rmdir", "删除目录", "rd /s /q dir"),
    ("mkdir / md", "创建目录", "mkdir new_dir"),
    ("type", "查看文件内容", "type file.txt"),
    ("find", "搜索文件内容", "find \"text\" file.txt"),
    ("findstr", "增强搜索", "findstr /i \"text\" *.txt"),
    ("ren / rename", "重命名", "ren old.txt new.txt"),
    ("cls", "清屏", "cls"),
    ("echo", "输出", "echo Hello"),
    ("pause", "暂停", "pause"),
    ("tasklist", "进程列表", "tasklist"),
    ("taskkill", "终止进程", "taskkill /PID 1234"),
    ("netstat", "网络连接", "netstat -ano"),
    ("ipconfig", "网络配置", "ipconfig /all"),
    ("ping", "网络测试", "ping google.com"),
    ("tracert", "路由追踪", "tracert google.com"),
    ("nslookup", "DNS 查询", "nslookup google.com"),
    ("systeminfo", "系统信息", "systeminfo"),
    ("hostname", "主机名", "hostname"),
    ("whoami", "当前用户", "whoami"),
    ("net user", "用户管理", "net user"),
    ("shutdown", "关机", "shutdown /s /t 60"),
    ("shutdown /a", "取消关机", "shutdown /a"),
    ("sfc /scannow", "系统文件检查", "sfc /scannow"),
    ("chkdsk", "磁盘检查", "chkdsk C: /f"),
    ("diskpart", "磁盘管理", "diskpart"),
    ("format", "格式化", "format D: /FS:NTFS"),
    ("attrib", "文件属性", "attrib +h file.txt"),
    ("assoc", "文件关联", "assoc .txt=txtfile"),
    ("ftype", "文件类型", "ftype txtfile=notepad.exe"),
    ("reg", "注册表操作", "reg query HKLM"),
    ("gpupdate", "更新组策略", "gpupdate /force"),
    ("msconfig", "系统配置", "msconfig"),
    ("services.msc", "服务管理", "services.msc"),
    ("compmgmt.msc", "计算机管理", "compmgmt.msc"),
    ("devmgmt.msc", "设备管理器", "devmgmt.msc"),
    ("diskmgmt.msc", "磁盘管理", "diskmgmt.msc"),
    ("secpol.msc", "本地安全策略", "secpol.msc"),
    ("wf.msc", "防火墙", "wf.msc"),
    ("eventvwr.msc", "事件查看器", "eventvwr.msc"),
    ("certmgr.msc", "证书管理", "certmgr.msc"),
    ("mmc", "管理控制台", "mmc"),
    ("mspaint", "画图", "mspaint"),
    ("notepad", "记事本", "notepad file.txt"),
    ("calc", "计算器", "calc"),
    ("explorer", "文件管理器", "explorer"),
    ("cmd", "命令提示符", "cmd"),
    ("powershell", "PowerShell", "powershell"),
    ("wsl", "Linux 子系统", "wsl"),
]

# 实用技巧
tips = [
    ("!!", "执行上一条命令"),
    ("!$", "上一条命令的最后一个参数"),
    ("!n", "执行第 n 条历史命令"),
    ("Ctrl+C", "终止当前命令"),
    ("Ctrl+Z", "暂停当前命令"),
    ("Ctrl+D", "退出当前 Shell"),
    ("Ctrl+R", "反向搜索历史"),
    ("Ctrl+A", "光标移到行首"),
    ("Ctrl+E", "光标移到行尾"),
    ("Ctrl+W", "删除光标前一个词"),
    ("Ctrl+U", "删除光标到行首"),
    ("Ctrl+K", "删除光标到行尾"),
    ("Ctrl+L", "清屏"),
    ("Tab", "自动补全"),
    ("Tab Tab", "显示所有补全选项"),
    ("&&", "前一个成功才执行下一个"),
    ("||", "前一个失败才执行下一个"),
    (";", "依次执行命令"),
    ("|", "管道（前一个输出作为后一个输入）"),
    (">", "输出重定向（覆盖）"),
    (">>", "输出重定向（追加）"),
    ("<", "输入重定向"),
    ("2>", "错误输出重定向"),
    ("&>", "所有输出重定向"),
    ("2>&1", "错误输出合并到标准输出"),
    ("|&", "同时捕获标准和错误输出"),
    ("`cmd`", "命令替换（旧式）"),
    ("$(cmd)", "命令替换（推荐）"),
    ("$((expr))", "算术展开"),
    ("${var}", "变量展开"),
    ("${var:-default}", "变量为空时用默认值"),
    ("${var:=default}", "变量为空时设默认值"),
    ("${var:+value}", "变量非空时用指定值"),
    ("${var:?error}", "变量为空时报错"),
    ("${#var}", "变量长度"),
    ("${var%pattern}", "从末尾删除最短匹配"),
    ("${var%%pattern}", "从末尾删除最长匹配"),
    ("${var#pattern}", "从开头删除最短匹配"),
    ("${var##pattern}", "从开头删除最长匹配"),
    ("${var/pattern/string}", "替换第一个匹配"),
    ("${var//pattern/string}", "替换所有匹配"),
    ("${var:offset:length}", "字符串切片"),
    ("${!prefix*}", "以 prefix 开头的所有变量"),
    ("${var,,}", "转小写（Bash 4+）"),
    ("${var^^}", "转大写（Bash 4+）"),
    ("seq 1 10", "生成序列 1 到 10"),
    ("seq 1 2 10", "生成序列 1,3,5,7,9"),
    ("yes | cmd", "自动确认 y"),
    ("cmd 2>/dev/null", "忽略错误输出"),
    ("cmd > /dev/null 2>&1", "完全静默"),
    ("cmd &", "后台运行"),
    ("cmd & disown", "后台运行并脱离终端"),
    ("tee file | cmd", "同时显示和保存"),
    ("cmd1 | cmd2 | cmd3", "链式管道"),
]

def create_pdf():
    doc = SimpleDocTemplate(
        "D:/tokai/Shell命令学习手册.pdf",
        pagesize=A4,
        rightMargin=18*mm,
        leftMargin=18*mm,
        topMargin=18*mm,
        bottomMargin=18*mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Title'],
        fontName=chinese_font, fontSize=26, spaceAfter=15,
        textColor=colors.HexColor('#0d6efd'),
    )
    subtitle_style = ParagraphStyle(
        'CustomSubtitle', parent=styles['Heading2'],
        fontName=chinese_font, fontSize=16, spaceBefore=12, spaceAfter=8,
        textColor=colors.HexColor('#333333'),
    )
    normal_style = ParagraphStyle(
        'CustomNormal', parent=styles['Normal'],
        fontName=chinese_font, fontSize=10, leading=14,
    )

    story = []

    def make_table(data, col_widths, header_color):
        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(header_color)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), chinese_font),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        return t

    # 标题页
    story.append(Spacer(1, 50*mm))
    story.append(Paragraph("Shell 命令学习手册", title_style))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("Linux / Windows / macOS 命令行完全指南", normal_style))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("包含：文件操作 · 文本处理 · 系统信息 · 网络 · 包管理 · 压缩 · 用户 · 进程 · 服务 · 磁盘 · 环境变量 · 快捷键 · 实用技巧", normal_style))
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph("生成日期：2026-06-02", normal_style))
    story.append(PageBreak())

    # 目录
    story.append(Paragraph("目 录", subtitle_style))
    story.append(Spacer(1, 5*mm))
    toc = [
        "一、文件操作命令（25个）",
        "二、文件内容处理（28个）",
        "三、系统信息命令（36个）",
        "四、网络相关命令（34个）",
        "五、包管理命令（20个）",
        "六、压缩解压命令（19个）",
        "七、用户管理命令（20个）",
        "八、进程管理命令（24个）",
        "九、服务管理命令（13个）",
        "十、磁盘/存储命令（16个）",
        "十一、文本处理高级（27个）",
        "十二、环境变量/Shell配置（29个）",
        "十三、Windows CMD 常用（60个）",
        "十四、Shell 快捷键与技巧（60个）",
    ]
    for item in toc:
        story.append(Paragraph(item, normal_style))
        story.append(Spacer(1, 3*mm))
    story.append(PageBreak())

    # 一、文件操作
    story.append(Paragraph("一、文件操作命令", subtitle_style))
    story.append(Paragraph("文件和目录的基本操作。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(file_cmds)
    story.append(make_table(data, [100, 160, 170], '#0d6efd'))
    story.append(PageBreak())

    # 二、文件内容
    story.append(Paragraph("二、文件内容处理", subtitle_style))
    story.append(Paragraph("查看、搜索、处理文件内容。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(content_cmds)
    story.append(make_table(data, [100, 160, 170], '#198754'))
    story.append(PageBreak())

    # 三、系统信息
    story.append(Paragraph("三、系统信息命令", subtitle_style))
    story.append(Paragraph("查看系统状态、进程、硬件信息。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(system_cmds)
    story.append(make_table(data, [100, 160, 170], '#ffc107'))
    story.append(PageBreak())

    # 四、网络
    story.append(Paragraph("四、网络相关命令", subtitle_style))
    story.append(Paragraph("网络诊断、连接、远程操作。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(network_cmds)
    story.append(make_table(data, [100, 160, 170], '#dc3545'))
    story.append(PageBreak())

    # 五、包管理
    story.append(Paragraph("五、包管理命令", subtitle_style))
    story.append(Paragraph("各平台的软件包安装和管理。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(package_cmds)
    story.append(make_table(data, [100, 160, 170], '#6f42c1'))
    story.append(PageBreak())

    # 六、压缩解压
    story.append(Paragraph("六、压缩解压命令", subtitle_style))
    story.append(Paragraph("常见压缩格式的处理。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(archive_cmds)
    story.append(make_table(data, [100, 160, 170], '#0dcaf0'))
    story.append(PageBreak())

    # 七、用户管理
    story.append(Paragraph("七、用户管理命令", subtitle_style))
    story.append(Paragraph("用户、组、权限管理。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(user_cmds)
    story.append(make_table(data, [100, 160, 170], '#fd7e14'))
    story.append(PageBreak())

    # 八、进程管理
    story.append(Paragraph("八、进程管理命令", subtitle_style))
    story.append(Paragraph("进程查看、控制、后台任务。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(process_cmds)
    story.append(make_table(data, [100, 160, 170], '#20c997'))
    story.append(PageBreak())

    # 九、服务管理
    story.append(Paragraph("九、服务管理命令", subtitle_style))
    story.append(Paragraph("系统服务的启动、停止、配置。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(service_cmds)
    story.append(make_table(data, [120, 150, 160], '#6610f2'))
    story.append(PageBreak())

    # 十、磁盘
    story.append(Paragraph("十、磁盘/存储命令", subtitle_style))
    story.append(Paragraph("磁盘查看、分区、格式化。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(disk_cmds)
    story.append(make_table(data, [100, 160, 170], '#198754'))
    story.append(PageBreak())

    # 十一、文本处理高级
    story.append(Paragraph("十一、文本处理高级", subtitle_style))
    story.append(Paragraph("awk、sed、grep 等强大文本工具。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(text_cmds)
    story.append(make_table(data, [100, 160, 170], '#e83e8c'))
    story.append(PageBreak())

    # 十二、环境变量
    story.append(Paragraph("十二、环境变量/Shell 配置", subtitle_style))
    story.append(Paragraph("Shell 环境配置和变量操作。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(env_cmds)
    story.append(make_table(data, [100, 160, 170], '#0dcaf0'))
    story.append(PageBreak())

    # 十三、Windows CMD
    story.append(Paragraph("十三、Windows CMD 常用命令", subtitle_style))
    story.append(Paragraph("Windows 命令提示符和系统工具。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["命令", "说明", "示例"]] + list(windows_cmds)
    story.append(make_table(data, [110, 160, 160], '#0d6efd'))
    story.append(PageBreak())

    # 十四、快捷键与技巧
    story.append(Paragraph("十四、Shell 快捷键与实用技巧", subtitle_style))
    story.append(Paragraph("提高命令行效率的快捷键和技巧。", normal_style))
    story.append(Spacer(1, 3*mm))
    data = [["快捷键/技巧", "说明"]] + list(tips)
    story.append(make_table(data, [160, 270], '#198754'))

    doc.build(story)
    print("Shell 命令学习手册 PDF 生成完成！共 14 个章节。")

if __name__ == "__main__":
    create_pdf()
