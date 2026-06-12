import openpyxl
from openpyxl.worksheet.page import PageMargins

wb = openpyxl.load_workbook(r'C:\Users\w\Desktop\锦绣丽园13栋3203房硬装报价预算.xlsx8(1).xlsx')
ws = wb.active

# 1. 设置横向打印（更适合表格）
ws.page_setup.orientation = 'landscape'

# 2. 设置缩放适应1页宽（确保宽度不超页）
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0  # 0表示高度不限制

# 3. 缩小页边距以最大化打印区域
ws.page_margins = PageMargins(
    left=0.5,
    right=0.5,
    top=0.75,
    bottom=0.75,
    header=0.3,
    footer=0.3
)

# 4. 设置打印区域为所有数据（包括第9列备注）
ws.print_area = 'Sheet1!A1:I227'

# 5. 优化列宽（让内容更紧凑）
column_widths = {'A': 8, 'B': 20, 'C': 12, 'D': 12, 'E': 6, 'F': 6, 'G': 8, 'H': 10, 'I': 30}
for col, width in column_widths.items():
    ws.column_dimensions[col].width = width

# 6. 设置行高为自动（紧凑）
for row in range(1, 228):
    ws.row_dimensions[row].height = None  # 自动行高

# 7. 启用适合页面的选项
ws.sheet_properties.pageSetUpPr.fitToPage = True

# 保存文件
output_path = r'C:\Users\w\Desktop\报价单_打印优化.xlsx'
wb.save(output_path)
print(f'已保存到: {output_path}')
print('优化内容:')
print('- 方向: 横向')
print('- 缩放: 适应1页宽')
print('- 页边距: 缩小至0.5英寸')
print('- 列宽: 已优化')