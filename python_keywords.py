# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 尝试注册中文字体
font_paths = [
    "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
    "C:/Windows/Fonts/simsun.ttc",   # 宋体
    "C:/Windows/Fonts/simhei.ttf",   # 黑体
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

# Python 关键字数据
keywords = [
    # (关键字, 含义, 类型, 示例)
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

# 常用内置函数
builtin_funcs = [
    ("print()", "打印输出", "print('Hello')"),
    ("len()", "获取长度/元素个数", "len([1,2,3])"),
    ("range()", "生成整数序列", "range(10)"),
    ("input()", "获取用户输入", "name = input()"),
    ("int()", "转换为整数", "int('5')"),
    ("float()", "转换为浮点数", "float('3.14')"),
    ("str()", "转换为字符串", "str(100)"),
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
    ("round()", "四舍五入", "round(3.14)"),
    ("sorted()", "排序", "sorted([3,1,2])"),
    ("enumerate()", "枚举，带索引遍历", "enumerate(['a','b'])"),
    ("zip()", "打包多个序列", "zip([1,2], ['a','b'])"),
    ("map()", "映射函数到序列", "map(int, ['1','2'])"),
    ("filter()", "过滤序列", "filter(lambda x:x>0, nums)"),
    ("open()", "打开文件", "open('file.txt')"),
    ("int()/float()/str()", "类型转换", "int('10')"),
    ("bool()", "转换为布尔值", "bool(0)"),
]

# 数据类型
data_types = [
    ("int", "整数", "x = 42"),
    ("float", "浮点数（小数）", "x = 3.14"),
    ("str", "字符串", "x = 'hello'"),
    ("bool", "布尔值（True/False）", "x = True"),
    ("list", "列表（有序可变序列）", "x = [1, 2, 3]"),
    ("tuple", "元组（有序不可变序列）", "x = (1, 2, 3)"),
    ("dict", "字典（键值对集合）", "x = {'a': 1}"),
    ("set", "集合（无序不重复）", "x = {1, 2, 3}"),
    ("NoneType", "空类型（None）", "x = None"),
]

# 运算符
operators = [
    ("+", "加法", "3 + 2 = 5"),
    ("-", "减法", "3 - 2 = 1"),
    ("*", "乘法", "3 * 2 = 6"),
    ("/", "除法", "6 / 2 = 3.0"),
    ("//", "整除（向下取整）", "7 // 2 = 3"),
    ("%", "取模（余数）", "7 % 2 = 1"),
    ("**", "幂运算", "2 ** 3 = 8"),
    ("==", "等于", "3 == 3 → True"),
    ("!=", "不等于", "3 != 2 → True"),
    (">", "大于", "3 > 2 → True"),
    ("<", "小于", "3 < 2 → False"),
    (">=", "大于等于", "3 >= 3 → True"),
    ("<=", "小于等于", "3 <= 2 → False"),
    ("=", "赋值", "x = 5"),
    ("+=", "加后赋值", "x += 3 → x = x + 3"),
    ("-=", "减后赋值", "x -= 3 → x = x - 3"),
    ("*=", "乘后赋值", "x *= 3 → x = x * 3"),
]

def create_pdf():
    doc = SimpleDocTemplate(
        "D:/tokai/Python关键词学习手册.pdf",
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
    )

    styles = getSampleStyleSheet()

    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName=chinese_font,
        fontSize=24,
        spaceAfter=20,
        textColor=colors.HexColor('#1a73e8'),
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontName=chinese_font,
        fontSize=16,
        spaceBefore=15,
        spaceAfter=10,
        textColor=colors.HexColor('#333333'),
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName=chinese_font,
        fontSize=10,
        leading=14,
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#d63384'),
    )

    story = []

    # 标题页
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph("Python 关键词学习手册", title_style))
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph("全面掌握 Python 3.x 核心词汇与语法", normal_style))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph("包含：关键字、内置函数、数据类型、运算符", normal_style))
    story.append(PageBreak())

    # === 第一部分：关键字 ===
    story.append(Paragraph("一、Python 关键字 (Keywords)", subtitle_style))
    story.append(Paragraph("Python 保留的特殊词汇，不能用作变量名。", normal_style))
    story.append(Spacer(1, 5*mm))

    # 关键字表格
    kw_data = [["关键字", "含义", "类型", "示例"]]
    for kw in keywords:
        kw_data.append([kw[0], kw[1], kw[2], kw[3]])

    kw_table = Table(kw_data, colWidths=[60, 180, 70, 130])
    kw_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
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
    story.append(kw_table)
    story.append(PageBreak())

    # === 第二部分：内置函数 ===
    story.append(Paragraph("二、常用内置函数", subtitle_style))
    story.append(Paragraph("Python 自带的函数，无需导入即可使用。", normal_style))
    story.append(Spacer(1, 5*mm))

    fn_data = [["函数", "说明", "示例"]]
    for fn in builtin_funcs:
        fn_data.append([fn[0], fn[1], fn[2]])

    fn_table = Table(fn_data, colWidths=[100, 160, 180])
    fn_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fff4')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(fn_table)
    story.append(PageBreak())

    # === 第三部分：数据类型 ===
    story.append(Paragraph("三、数据类型", subtitle_style))
    story.append(Spacer(1, 5*mm))

    dt_data = [["类型", "说明", "示例"]]
    for dt in data_types:
        dt_data.append([dt[0], dt[1], dt[2]])

    dt_table = Table(dt_data, colWidths=[100, 180, 160])
    dt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fd7e14')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff8f0')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(dt_table)

    # === 第四部分：运算符 ===
    story.append(Spacer(1, 10*mm))
    story.append(Paragraph("四、运算符", subtitle_style))
    story.append(Spacer(1, 5*mm))

    op_data = [["运算符", "含义", "示例"]]
    for op in operators:
        op_data.append([op[0], op[1], op[2]])

    op_table = Table(op_data, colWidths=[80, 160, 190])
    op_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6f42c1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), chinese_font),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f0ff')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(op_table)

    # 生成
    doc.build(story)
    print("PDF 生成完成！")

if __name__ == "__main__":
    create_pdf()
