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
# 数据
# ============================================================

keywords = [
    ("False", "布尔假值，表示逻辑假", "布尔值", "x = False"),
    ("None", "表示空值或没有值", "空值", "x = None"),
    ("True", "布尔真值，表示逻辑真", "布尔值", "x = True"),
    ("and", "逻辑与运算符", "运算符", "if a and b:"),
    ("as", "用于别名或上下文管理器", "关键字", "import os as o"),
    ("assert", "断言，用于调试检查条件", "语句", "assert x > 0"),
    ("async", "定义异步函数", "关键字", "async def func():"),
    ("await", "等待异步操作完成", "关键字", "await result()"),
    ("break", "跳出循环", "循环控制", "while True: break"),
    ("class", "定义类", "面向对象", "class Dog:"),
    ("continue", "跳过当前循环迭代", "循环控制", "continue"),
    ("def", "定义函数", "函数", "def hello():"),
    ("del", "删除对象引用", "操作", "del x"),
    ("elif", "else if 的缩写，条件分支", "条件", "elif x > 0:"),
    ("else", "else 分支，条件不满足时执行", "条件", "else:"),
    ("except", "捕获异常", "异常处理", "except ValueError:"),
    ("finally", "异常处理中无论如何都执行", "异常处理", "finally:"),
    ("for", "for 循环，遍历可迭代对象", "循环", "for i in range(10):"),
    ("from", "从模块导入指定部分", "导入", "from os import path"),
    ("global", "声明全局变量", "作用域", "global x"),
    ("if", "条件判断", "条件", "if x > 0:"),
    ("import", "导入模块", "导入", "import math"),
    ("in", "成员运算符，判断是否在序列中", "运算符", "if x in list:"),
    ("is", "身份运算符，判断是否为同一对象", "运算符", "if x is None:"),
    ("lambda", "创建匿名函数", "函数", "f = lambda x: x*2"),
    ("nonlocal", "声明外层非全局变量", "作用域", "nonlocal x"),
    ("not", "逻辑非运算符", "运算符", "if not x:"),
    ("or", "逻辑或运算符", "运算符", "if a or b:"),
    ("pass", "空语句，占位符", "语句", "pass"),
    ("raise", "引发异常", "异常处理", "raise Error('msg')"),
    ("return", "函数返回值", "函数", "return x"),
    ("try", "尝试执行代码块，捕获异常", "异常处理", "try:"),
    ("while", "while 循环，条件循环", "循环", "while x < 10:"),
    ("with", "上下文管理器，自动管理资源", "语句", "with open('f'):"),
    ("yield", "生成器函数，返回值并暂停", "函数", "yield x"),
]

builtin_funcs = [
    ("print()", "打印输出到控制台", "print('Hello')"),
    ("len()", "获取长度/元素个数", "len([1,2,3])"),
    ("range()", "生成整数序列", "range(10)"),
    ("input()", "获取用户输入（返回字符串）", "name = input()"),
    ("int()", "转换为整数", "int('5')"),
    ("float()", "转换为浮点数", "float('3.14')"),
    ("str()", "转换为字符串", "str(100)"),
    ("bool()", "转换为布尔值", "bool(0)"),
    ("list()", "创建列表", "list((1,2,3))"),
    ("dict()", "创建字典", "dict(a=1, b=2)"),
    ("set()", "创建集合", "set([1,2,3])"),
    ("tuple()", "创建元组", "tuple([1,2,3])"),
    ("type()", "查看对象类型", "type(42)"),
    ("isinstance()", "判断类型", "isinstance(x, int)"),
    ("id()", "获取对象唯一标识", "id(x)"),
    ("max()", "获取最大值", "max([1,5,3])"),
    ("min()", "获取最小值", "min([1,5,3])"),
    ("sum()", "求和", "sum([1,2,3])"),
    ("abs()", "取绝对值", "abs(-5)"),
    ("round()", "四舍五入", "round(3.14, 1)"),
    ("sorted()", "排序（返回新列表）", "sorted([3,1,2])"),
    ("reversed()", "反转迭代器", "list(reversed([1,2,3]))"),
    ("enumerate()", "枚举，带索引遍历", "enumerate(['a','b'])"),
    ("zip()", "打包多个序列", "zip([1,2], ['a','b'])"),
    ("map()", "映射函数到序列", "map(int, ['1','2'])"),
    ("filter()", "过滤序列", "filter(lambda x:x>0, nums)"),
    ("open()", "打开文件", "open('file.txt')"),
    ("chr()", "整数转字符", "chr(65) → 'A'"),
    ("ord()", "字符转整数", "ord('A') → 65"),
    ("hex()", "转十六进制字符串", "hex(255) → '0xff'"),
    ("bin()", "转二进制字符串", "bin(10) → '0b1010'"),
    ("oct()", "转八进制字符串", "oct(8) → '0o10'"),
    ("hash()", "获取对象哈希值", "hash('hello')"),
    ("format()", "格式化字符串", "format(3.14, '.1f')"),
    ("any()", "可迭代对象中有任一True则True", "any([0,1,0])"),
    ("all()", "可迭代对象中全True则True", "all([1,1,1])"),
    ("dir()", "列出对象所有属性和方法", "dir([])"),
    ("vars()", "返回对象的 __dict__", "vars()"),
    ("help()", "查看帮助文档", "help(print)"),
    ("callable()", "判断是否可调用", "callable(lambda: 1)"),
    ("slice()", "创建切片对象", "slice(0, 5, 2)"),
    ("memoryview()", "创建内存视图", "memoryview(b'abc')"),
    ("property()", "创建属性描述符", "property(fget, fset)"),
    ("staticmethod()", "静态方法装饰器", "staticmethod(func)"),
    ("classmethod()", "类方法装饰器", "classmethod(func)"),
    ("super()", "调用父类方法", "super().__init__()"),
    ("object()", "所有类的基类", "object()"),
]

data_types = [
    ("int", "整数（任意精度）", "x = 42 / x = -100 / x = 10**100"),
    ("float", "浮点数（双精度）", "x = 3.14 / x = 2.5e10"),
    ("str", "字符串（不可变序列）", "x = 'hello' / x = \"world\""),
    ("bool", "布尔值（int子类）", "x = True / x = False"),
    ("list", "列表（有序可变序列）", "x = [1, 2, 3, 'a']"),
    ("tuple", "元组（有序不可变序列）", "x = (1, 2, 3)"),
    ("dict", "字典（键值对映射）", "x = {'name': 'Tom', 'age': 18}"),
    ("set", "集合（无序不重复）", "x = {1, 2, 3}"),
    ("frozenset", "不可变集合", "x = frozenset([1, 2])"),
    ("NoneType", "空类型", "x = None"),
    ("bytes", "字节序列（不可变）", "x = b'hello'"),
    ("bytearray", "字节数组（可变）", "x = bytearray(b'hi')"),
    ("complex", "复数", "x = 3 + 4j"),
]

operators = [
    ("+", "加法", "3 + 2 → 5"),
    ("-", "减法", "3 - 2 → 1"),
    ("*", "乘法", "3 * 2 → 6"),
    ("/", "除法（返回浮点数）", "7 / 2 → 3.5"),
    ("//", "整除（向下取整）", "7 // 2 → 3"),
    ("%", "取模（余数）", "7 % 2 → 1"),
    ("**", "幂运算", "2 ** 3 → 8"),
    ("==", "等于", "3 == 3 → True"),
    ("!=", "不等于", "3 != 2 → True"),
    (">", "大于", "3 > 2 → True"),
    ("<", "小于", "3 < 2 → False"),
    (">=", "大于等于", "3 >= 3 → True"),
    ("<=", "小于等于", "3 <= 2 → False"),
    ("&", "按位与", "0b1010 & 0b1100 → 0b1000"),
    ("|", "按位或", "0b1010 | 0b1100 → 0b1110"),
    ("^", "按位异或", "0b1010 ^ 0b1100 → 0b0110"),
    ("~", "按位取反", "~0 → -1"),
    ("<<", "左移", "1 << 3 → 8"),
    (">>", "右移", "8 >> 2 → 2"),
    ("=", "赋值", "x = 5"),
    ("+=", "加后赋值", "x += 3"),
    ("-=", "减后赋值", "x -= 3"),
    ("*=", "乘后赋值", "x *= 3"),
    ("/=", "除后赋值", "x /= 3"),
    ("//=", "整除后赋值", "x //= 3"),
    ("%=", "取模后赋值", "x %= 3"),
    ("**=", "幂后赋值", "x **= 3"),
    ("&=", "按位与后赋值", "x &= 3"),
    ("|=", "按位或后赋值", "x |= 3"),
    ("^=", "按位异或后赋值", "x ^= 3"),
    ("@", "矩阵乘法运算符", "A @ B（NumPy中使用）"),
    (":=", "海象运算符（赋值表达式）", "if (n := len(a)) > 10:"),
]

# 字符串方法
str_methods = [
    ("upper()", "全部转大写", "'hello'.upper() → 'HELLO'"),
    ("lower()", "全部转小写", "'HELLO'.lower() → 'hello'"),
    ("title()", "每个单词首字母大写", "'hello world'.title() → 'Hello World'"),
    ("capitalize()", "首字母大写，其余小写", "'hello'.capitalize() → 'Hello'"),
    ("strip()", "去除两端空白字符", "' hi '.strip() → 'hi'"),
    ("lstrip()", "去除左端空白", "' hi '.lstrip() → 'hi '"),
    ("rstrip()", "去除右端空白", "' hi '.rstrip() → ' hi'"),
    ("split()", "按分隔符切割为列表", "'a,b,c'.split(',') → ['a','b','c']"),
    ("join()", "用字符串连接可迭代对象", "','.join(['a','b']) → 'a,b'"),
    ("replace()", "替换子字符串", "'hello'.replace('l','L') → 'heLLo'"),
    ("find()", "查找子串位置（-1表示没找到）", "'hello'.find('ll') → 2"),
    ("rfind()", "从右边查找子串位置", "'hello'.rfind('l') → 3"),
    ("index()", "查找子串位置（找不到会报错）", "'hello'.index('ll') → 2"),
    ("count()", "统计子串出现次数", "'hello'.count('l') → 2"),
    ("startswith()", "判断是否以指定字符串开头", "'hello'.startswith('he') → True"),
    ("endswith()", "判断是否以指定字符串结尾", "'hello'.endswith('lo') → True"),
    ("isdigit()", "判断是否全为数字", "'123'.isdigit() → True"),
    ("isalpha()", "判断是否全为字母", "'abc'.isalpha() → True"),
    ("isalnum()", "判断是否为字母或数字", "'abc1'.isalnum() → True"),
    ("isspace()", "判断是否全为空白", "' '.isspace() → True"),
    ("isupper()", "判断是否全为大写", "'HELLO'.isupper() → True"),
    ("islower()", "判断是否全为小写", "'hello'.islower() → True"),
    ("splitlines()", "按行分割", "'a\\nb'.splitlines() → ['a','b']"),
    ("zfill()", "用0填充到指定宽度", "'42'.zfill(5) → '00042'"),
    ("center()", "居中对齐", "'hi'.center(10) → '    hi    '"),
    ("ljust()", "左对齐", "'hi'.ljust(10) → 'hi        '"),
    ("rjust()", "右对齐", "'hi'.rjust(10) → '        hi'"),
    ("encode()", "编码为字节", "'你好'.encode('utf-8')"),
    ("format()", "格式化字符串", "'{} is {}'.format('It', 'OK')"),
    ("maketrans()", "创建映射表", "str.maketrans('aeiou', '12345')"),
    ("translate()", "按映射表替换", "'hello'.translate(table)"),
]

# 列表方法
list_methods = [
    ("append()", "在末尾添加元素", "lst.append(4)"),
    ("extend()", "用另一个列表扩展", "lst.extend([4,5])"),
    ("insert()", "在指定位置插入元素", "lst.insert(0, 'a')"),
    ("remove()", "删除第一个匹配的元素", "lst.remove(3)"),
    ("pop()", "删除并返回指定位置元素", "lst.pop() / lst.pop(0)"),
    ("clear()", "清空列表", "lst.clear()"),
    ("index()", "查找元素的索引", "lst.index(3)"),
    ("count()", "统计元素出现次数", "lst.count(3)"),
    ("sort()", "原地排序", "lst.sort() / lst.sort(reverse=True)"),
    ("reverse()", "原地反转", "lst.reverse()"),
    ("copy()", "浅拷贝", "lst.copy()"),
]

# 字典方法
dict_methods = [
    ("get()", "获取值（可设默认值）", "d.get('key', 'default')"),
    ("keys()", "获取所有键", "d.keys()"),
    ("values()", "获取所有值", "d.values()"),
    ("items()", "获取所有键值对", "d.items()"),
    ("update()", "用另一个字典更新", "d.update({'a': 1})"),
    ("pop()", "删除并返回指定键的值", "d.pop('key')"),
    ("popitem()", "删除并返回最后插入的键值对", "d.popitem()"),
    ("setdefault()", "获取值，不存在则设置默认值", "d.setdefault('k', 'v')"),
    ("clear()", "清空字典", "d.clear()"),
    ("copy()", "浅拷贝", "d.copy()"),
    ("fromkeys()", "用相同值创建新字典", "dict.fromkeys(['a','b'], 0)"),
]

# 集合方法
set_methods = [
    ("add()", "添加元素", "s.add(4)"),
    ("remove()", "删除元素（不存在报错）", "s.remove(3)"),
    ("discard()", "删除元素（不存在不报错）", "s.discard(3)"),
    ("pop()", "随机删除并返回一个元素", "s.pop()"),
    ("clear()", "清空集合", "s.clear()"),
    ("union()", "并集", "s1.union(s2) / s1 | s2"),
    ("intersection()", "交集", "s1.intersection(s2) / s1 & s2"),
    ("difference()", "差集", "s1.difference(s2) / s1 - s2"),
    ("symmetric_difference()", "对称差集", "s1.symmetric_difference(s2) / s1 ^ s2"),
    ("issubset()", "是否为子集", "s1.issubset(s2)"),
    ("issuperset()", "是否为超集", "s1.issuperset(s2)"),
    ("isdisjoint()", "是否无交集", "s1.isdisjoint(s2)"),
    ("copy()", "浅拷贝", "s.copy()"),
    ("update()", "更新集合", "s.update([4,5])"),
]

# 异常类型
exceptions = [
    ("Exception", "所有异常的基类", "捕获大多数错误"),
    ("SyntaxError", "语法错误", "代码不符合Python语法规则"),
    ("IndentationError", "缩进错误", "缩进不正确"),
    ("NameError", "名称错误", "变量未定义"),
    ("TypeError", "类型错误", "操作/函数应用于不适当类型"),
    ("ValueError", "值错误", "函数参数类型正确但值不合适"),
    ("IndexError", "索引错误", "序列下标越界"),
    ("KeyError", "键错误", "字典中找不到指定的键"),
    ("AttributeError", "属性错误", "对象没有该属性或方法"),
    ("ModuleNotFoundError", "模块未找到", "导入的模块不存在"),
    ("ImportError", "导入错误", "导入语句失败"),
    ("FileNotFoundError", "文件未找到", "文件或目录不存在"),
    ("ZeroDivisionError", "零除错误", "除以零"),
    ("OverflowError", "溢出错误", "数值运算超出范围"),
    ("MemoryError", "内存错误", "内存不足"),
    ("RecursionError", "递归错误", "递归深度超限"),
    ("StopIteration", "迭代停止", "迭代器耗尽"),
    ("RuntimeError", "运行时错误", "不属于其他类型的运行时错误"),
    ("IOError", "输入输出错误", "文件操作相关错误（Python3即OSError）"),
    ("OSError", "操作系统错误", "系统相关错误"),
    ("PermissionError", "权限错误", "权限不足"),
    ("TimeoutError", "超时错误", "操作超时"),
    ("ConnectionError", "连接错误", "网络连接相关错误"),
    ("UnicodeError", "Unicode错误", "Unicode相关错误"),
    ("AssertionError", "断言错误", "assert语句失败"),
    ("NotImplementedError", "未实现错误", "抽象方法未实现"),
    ("ArithmeticError", "算术错误", "算术运算错误的基类"),
    ("LookupError", "查找错误", "索引/键查找失败的基类"),
    ("BufferError", "缓冲区错误", "缓冲区相关错误"),
    ("EOFError", "输入结束错误", "input()读到EOF"),
]

# 常用模块
common_modules = [
    ("os", "操作系统相关功能", "文件路径、目录操作、环境变量"),
    ("sys", "系统相关功能", "命令行参数、Python路径、退出"),
    ("math", "数学函数", "sin, cos, sqrt, pi, log"),
    ("random", "随机数生成", "randint, choice, shuffle, random"),
    ("datetime", "日期和时间", "datetime, timedelta, strftime"),
    ("time", "时间相关", "sleep, time, perf_counter"),
    ("re", "正则表达式", "match, search, findall, sub"),
    ("json", "JSON处理", "loads, dumps, load, dump"),
    ("csv", "CSV文件处理", "reader, writer, DictReader"),
    ("collections", "高级数据结构", "Counter, defaultdict, deque"),
    ("itertools", "迭代器工具", "chain, product, combinations"),
    ("functools", "函数工具", "reduce, lru_cache, partial"),
    ("string", "字符串常量和工具", "ascii_letters, digits, Template"),
    ("io", "IO操作", "StringIO, BytesIO"),
    ("pathlib", "面向对象的路径操作", "Path, cwd, home"),
    ("urllib", "URL处理", "request, parse, error"),
    ("http", "HTTP协议", "client, server"),
    ("socket", "网络编程", "低层网络接口"),
    ("threading", "多线程", "Thread, Lock, Event"),
    ("multiprocessing", "多进程", "Process, Pool, Queue"),
    ("subprocess", "子进程管理", "run, Popen, check_output"),
    ("logging", "日志记录", "debug, info, warning, error"),
    ("unittest", "单元测试", "TestCase, assertEqual"),
    ("argparse", "命令行参数解析", "ArgumentParser, add_argument"),
    ("hashlib", "哈希/摘要算法", "md5, sha256"),
    ("base64", "Base64编解码", "b64encode, b64decode"),
    ("struct", "二进制数据打包", "pack, unpack"),
    ("shutil", "高级文件操作", "copy, move, rmtree"),
    ("glob", "文件名匹配", "glob, iglob"),
    ("tempfile", "临时文件/目录", "NamedTemporaryFile, mkdtemp"),
    ("pickle", "对象序列化", "dumps, loads（不安全，勿加载不可信数据）"),
    ("copy", "对象拷贝", "copy, deepcopy"),
    ("pprint", "美观打印", "pprint, pformat"),
    ("typing", "类型提示", "List, Dict, Optional, Union"),
    ("abc", "抽象基类", "ABC, abstractmethod"),
    ("enum", "枚举类型", "Enum, IntEnum"),
    ("dataclasses", "数据类（Python3.7+）", "@dataclass装饰器"),
    ("asyncio", "异步IO框架", "run, gather, sleep"),
    ("socketserver", "简单服务器", "TCPServer, ThreadingMixin"),
    ("email", "邮件处理", "MIMEText, Header"),
    ("html", "HTML相关", "escape, unescape"),
    ("xml", "XML处理", "ElementTree, minidom"),
    ("ssl", "SSL/TLS加密", "SSLContext, wrap_socket"),
    ("statistics", "统计函数", "mean, median, stdev"),
    ("decimal", "高精度十进制", "Decimal, getcontext"),
    ("fractions", "分数", "Fraction(1, 2)"),
    ("array", "高效数值数组", "array('i', [1,2,3])"),
    ("types", "类型工具", "FunctionType, ModuleType"),
    ("weakref", "弱引用", "ref, proxy"),
    ("contextlib", "上下文管理器工具", "contextmanager, suppress"),
    ("textwrap", "文本包装/对齐", "wrap, indent, dedent"),
    ("difflib", "差异比较", "unified_diff, SequenceMatcher"),
    ("dis", "字节码反汇编", "dis"),
    ("inspect", "检查活动对象", "getmembers, signature"),
    ("code", "交互式解释器", "InteractiveConsole"),
    ("codecs", "编解码器", "open, register"),
    ("calendar", "日历", "calendar, month, weekday"),
    ("locale", "本地化", "getlocale, setlocale"),
]

# 编程常用英语
english_words = [
    ("variable", "变量"),
    ("constant", "常量"),
    ("function", "函数"),
    ("method", "方法"),
    ("class", "类"),
    ("object", "对象"),
    ("instance", "实例"),
    ("parameter", "参数"),
    ("argument", "实参"),
    ("return value", "返回值"),
    ("loop", "循环"),
    ("iteration", "迭代"),
    ("array", "数组"),
    ("list", "列表"),
    ("dictionary", "字典"),
    ("tuple", "元组"),
    ("set", "集合"),
    ("string", "字符串"),
    ("integer", "整数"),
    ("float", "浮点数"),
    ("boolean", "布尔值"),
    ("operator", "运算符"),
    ("expression", "表达式"),
    ("statement", "语句"),
    ("block", "代码块"),
    ("indentation", "缩进"),
    ("syntax", "语法"),
    ("error", "错误"),
    ("exception", "异常"),
    ("debug", "调试"),
    ("compile", "编译"),
    ("interpret", "解释"),
    ("import", "导入"),
    ("module", "模块"),
    ("package", "包"),
    ("library", "库"),
    ("framework", "框架"),
    ("file", "文件"),
    ("directory", "目录"),
    ("path", "路径"),
    ("input", "输入"),
    ("output", "输出"),
    ("console", "控制台"),
    ("terminal", "终端"),
    ("command", "命令"),
    ("script", "脚本"),
    ("algorithm", "算法"),
    ("data structure", "数据结构"),
    ("recursion", "递归"),
    ("inheritance", "继承"),
    ("polymorphism", "多态"),
    ("encapsulation", "封装"),
    ("abstraction", "抽象"),
    ("interface", "接口"),
    ("implementation", "实现"),
    ("dependency", "依赖"),
    ("repository", "仓库"),
    ("version", "版本"),
    ("update", "更新"),
    ("upgrade", "升级"),
    ("install", "安装"),
    ("uninstall", "卸载"),
    ("configure", "配置"),
    ("deploy", "部署"),
    ("execute", "执行"),
    ("runtime", "运行时"),
    ("compile time", "编译时"),
    ("environment", "环境"),
    ("virtual environment", "虚拟环境"),
    ("global", "全局的"),
    ("local", "局部的"),
    ("scope", "作用域"),
    ("namespace", "命名空间"),
    ("stack", "栈"),
    ("queue", "队列"),
    ("heap", "堆"),
    ("tree", "树"),
    ("graph", "图"),
    ("node", "节点"),
    ("edge", "边"),
    ("pointer", "指针"),
    ("reference", "引用"),
    ("memory", "内存"),
    ("address", "地址"),
    ("buffer", "缓冲区"),
    ("cache", "缓存"),
    ("token", "标记/令牌"),
    ("parser", "解析器"),
    ("lexer", "词法分析器"),
    ("compiler", "编译器"),
    ("interpreter", "解释器"),
    ("IDE", "集成开发环境"),
    ("API", "应用程序接口"),
    ("SDK", "软件开发工具包"),
    ("GUI", "图形用户界面"),
    ("CLI", "命令行界面"),
    ("HTTP", "超文本传输协议"),
    ("URL", "统一资源定位符"),
    ("JSON", "JavaScript对象表示法"),
    ("XML", "可扩展标记语言"),
    ("HTML", "超文本标记语言"),
    ("CSS", "层叠样式表"),
    ("SQL", "结构化查询语言"),
    ("database", "数据库"),
    ("query", "查询"),
    ("transaction", "事务"),
    ("thread", "线程"),
    ("process", "进程"),
    ("concurrency", "并发"),
    ("parallelism", "并行"),
    ("synchronization", "同步"),
    ("asynchronous", "异步的"),
    ("callback", "回调"),
    ("event", "事件"),
    ("listener", "监听器"),
    ("handler", "处理器"),
    ("middleware", "中间件"),
    ("server", "服务器"),
    ("client", "客户端"),
    ("request", "请求"),
    ("response", "响应"),
    ("authentication", "认证"),
    ("authorization", "授权"),
    ("encryption", "加密"),
    ("decryption", "解密"),
    ("serialization", "序列化"),
    ("deserialization", "反序列化"),
    ("marshalling", "编组"),
    ("unit test", "单元测试"),
    ("integration test", "集成测试"),
    ("regression", "回归"),
    ("refactor", "重构"),
    ("code review", "代码审查"),
    ("documentation", "文档"),
    ("bug", "缺陷/虫子"),
    ("fix", "修复"),
    ("patch", "补丁"),
    ("release", "发布"),
    ("branch", "分支"),
    ("merge", "合并"),
    ("commit", "提交"),
    ("push", "推送"),
    ("pull", "拉取"),
]

def create_pdf():
    doc = SimpleDocTemplate(
        "D:/tokai/Python关键词学习手册_完整版.pdf",
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
        textColor=colors.HexColor('#1a73e8'),
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

    small_style = ParagraphStyle(
        'SmallStyle', parent=styles['Normal'],
        fontName=chinese_font, fontSize=8, leading=11,
    )

    story = []

    # 标题页
    story.append(Spacer(1, 50*mm))
    story.append(Paragraph("Python 关键词学习手册", title_style))
    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("全面掌握 Python 3.x 核心词汇与语法（完整版）", normal_style))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("包含：关键字 · 内置函数 · 数据类型 · 运算符 · 字符串方法 · 列表方法 · 字典方法 · 集合方法 · 异常类型 · 常用模块 · 编程英语词汇", normal_style))
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph("生成日期：2026-06-02", normal_style))
    story.append(PageBreak())

    # === 目录 ===
    story.append(Paragraph("目 录", subtitle_style))
    story.append(Spacer(1, 5*mm))
    toc_items = [
        "一、Python 关键字（35个）",
        "二、常用内置函数（45个）",
        "三、数据类型（13种）",
        "四、运算符（31个）",
        "五、字符串方法（31个）",
        "六、列表方法（11个）",
        "七、字典方法（11个）",
        "八、集合方法（14个）",
        "九、异常类型（29个）",
        "十、常用模块（55个）",
        "十一、编程常用英语词汇（120个）",
    ]
    for item in toc_items:
        story.append(Paragraph(item, normal_style))
        story.append(Spacer(1, 3*mm))
    story.append(PageBreak())

    def make_table(data, headers, col_widths, header_color):
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

    # === 一、关键字 ===
    story.append(Paragraph("一、Python 关键字 (Keywords)", subtitle_style))
    story.append(Paragraph("Python 保留的特殊词汇，不能用作变量名。", normal_style))
    story.append(Spacer(1, 3*mm))

    kw_data = [["关键字", "含义", "类型", "示例"]]
    for kw in keywords:
        kw_data.append(kw)
    story.append(make_table(kw_data, [], [55, 175, 65, 145], '#1a73e8'))
    story.append(PageBreak())

    # === 二、内置函数 ===
    story.append(Paragraph("二、常用内置函数", subtitle_style))
    story.append(Paragraph("Python 自带的函数，无需导入即可使用。", normal_style))
    story.append(Spacer(1, 3*mm))

    fn_data = [["函数", "说明", "示例"]]
    for fn in builtin_funcs:
        fn_data.append(fn)
    story.append(make_table(fn_data, [], [90, 170, 170], '#28a745'))
    story.append(PageBreak())

    # === 三、数据类型 ===
    story.append(Paragraph("三、数据类型", subtitle_style))
    story.append(Spacer(1, 3*mm))

    dt_data = [["类型", "说明", "示例"]]
    for dt in data_types:
        dt_data.append(dt)
    story.append(make_table(dt_data, [], [90, 170, 170], '#fd7e14'))
    story.append(PageBreak())

    # === 四、运算符 ===
    story.append(Paragraph("四、运算符", subtitle_style))
    story.append(Spacer(1, 3*mm))

    op_data = [["运算符", "含义", "示例"]]
    for op in operators:
        op_data.append(op)
    story.append(make_table(op_data, [], [75, 165, 190], '#6f42c1'))
    story.append(PageBreak())

    # === 五、字符串方法 ===
    story.append(Paragraph("五、字符串方法", subtitle_style))
    story.append(Paragraph("字符串是不可变对象，这些方法返回新字符串。", normal_style))
    story.append(Spacer(1, 3*mm))

    sm_data = [["方法", "说明", "示例"]]
    for sm in str_methods:
        sm_data.append(sm)
    story.append(make_table(sm_data, [], [95, 170, 165], '#e83e8c'))
    story.append(PageBreak())

    # === 六、列表方法 ===
    story.append(Paragraph("六、列表方法", subtitle_style))
    story.append(Paragraph("列表是可变序列，方法会原地修改列表。", normal_style))
    story.append(Spacer(1, 3*mm))

    lm_data = [["方法", "说明", "示例"]]
    for lm in list_methods:
        lm_data.append(lm)
    story.append(make_table(lm_data, [], [95, 170, 165], '#20c997'))
    story.append(PageBreak())

    # === 七、字典方法 ===
    story.append(Paragraph("七、字典方法", subtitle_style))
    story.append(Spacer(1, 3*mm))

    dm_data = [["方法", "说明", "示例"]]
    for dm in dict_methods:
        dm_data.append(dm)
    story.append(make_table(dm_data, [], [110, 160, 160], '#17a2b8'))
    story.append(PageBreak())

    # === 八、集合方法 ===
    story.append(Paragraph("八、集合方法", subtitle_style))
    story.append(Paragraph("集合是无序不重复的元素集，支持数学集合运算。", normal_style))
    story.append(Spacer(1, 3*mm))

    stm_data = [["方法", "说明", "示例"]]
    for stm in set_methods:
        stm_data.append(stm)
    story.append(make_table(stm_data, [], [130, 160, 140], '#6610f2'))
    story.append(PageBreak())

    # === 九、异常类型 ===
    story.append(Paragraph("九、异常类型", subtitle_style))
    story.append(Paragraph("Python 内置的异常类，用于错误处理。", normal_style))
    story.append(Spacer(1, 3*mm))

    ex_data = [["异常类型", "含义", "常见原因"]]
    for ex in exceptions:
        ex_data.append(ex)
    story.append(make_table(ex_data, [], [120, 155, 155], '#dc3545'))
    story.append(PageBreak())

    # === 十、常用模块 ===
    story.append(Paragraph("十、常用模块", subtitle_style))
    story.append(Paragraph("Python 标准库中常用的模块。", normal_style))
    story.append(Spacer(1, 3*mm))

    mo_data = [["模块", "用途", "主要功能"]]
    for mo in common_modules:
        mo_data.append(mo)
    story.append(make_table(mo_data, [], [90, 170, 170], '#007bff'))
    story.append(PageBreak())

    # === 十一、编程常用英语 ===
    story.append(Paragraph("十一、编程常用英语词汇", subtitle_style))
    story.append(Paragraph("编程中高频出现的英文单词及其中文含义。", normal_style))
    story.append(Spacer(1, 3*mm))

    en_data = [["英文", "中文含义"]]
    for ew in english_words:
        en_data.append(ew)
    story.append(make_table(en_data, [], [160, 270], '#343a40'))

    doc.build(story)
    print("PDF 生成完成！共包含 11 个章节。")

if __name__ == "__main__":
    create_pdf()
