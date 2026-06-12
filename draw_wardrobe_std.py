#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
衣柜CAD图纸 - 标准格式
俯视图、外观图、结构图、侧视图
尺寸: 1590×600×2800mm
"""

import ezdxf
from ezdxf import units
import os

# ==================== 尺寸参数 ====================
TOTAL_WIDTH = 1590      # 总宽 mm
TOTAL_DEPTH = 600       # 总深 mm
TOTAL_HEIGHT = 2800     # 总高 mm
BOARD_THICK = 18        # 板材厚度 mm
GAP = 2                 # 间隙 mm

# 内部划分比例（参考标准图）
# 左区（挂衣+层板）: 约40%
# 中区（挂衣）: 约35%
# 右区（抽屉+层板）: 约25%

LEFT_ZONE = int(TOTAL_WIDTH * 0.40)   # 左区宽度 636mm
MID_ZONE = int(TOTAL_WIDTH * 0.35)    # 中区宽度 557mm
RIGHT_ZONE = TOTAL_WIDTH - LEFT_ZONE - MID_ZONE - BOARD_THICK * 2  # 右区宽度

# 高度划分
TOP_ZONE = 450         # 顶部被褥区
HANG_ZONE = 1200       # 挂衣区
DRAWER_ZONE = 500      # 抽屉区
BOTTOM_ZONE = TOTAL_HEIGHT - TOP_ZONE - HANG_ZONE - DRAWER_ZONE - BOARD_THICK * 3  # 底部层板区

# ==================== 创建DWG ====================
doc = ezdxf.new('R2010')
doc.units = units.MM
msp = doc.modelspace()

# 图层
doc.layers.add('OUTLINE', color=7)      # 白色-外框
doc.layers.add('BOARD', color=7)        # 白色-板材
doc.layers.add('DOOR', color=1)         # 红色-门板
doc.layers.add('INNER', color=3)        # 绿色-内部结构
doc.layers.add('HANGER', color=5)       # 蓝色-挂衣杆
doc.layers.add('DIM', color=2)          # 黄色-标注
doc.layers.add('TEXT', color=1)         # 红色-文字
doc.layers.add('PATTERN', color=8)      # 灰色-门板花纹
doc.layers.add('NOTE', color=1)         # 红色-备注

def draw_rect(start, end, layer='OUTLINE'):
    pts = [start, (end[0], start[1]), end, (start[0], end[1])]
    return msp.add_lwpolyline(pts, close=True, dxfattribs={'layer': layer})

def draw_line(start, end, layer='OUTLINE'):
    return msp.add_line(start, end, dxfattribs={'layer': layer})

def add_dim(p1, p2, offset, layer='DIM'):
    dim = msp.add_linear_dim(
        base=(p1[0], p1[1] + offset),
        p1=p1, p2=p2,
        dimstyle='EZDXF',
        override={'dimtxt': 20, 'dimasz': 12, 'dimclrd': 2, 'dimclre': 2, 'dimclrt': 2}
    )
    dim.render()
    return dim

def add_text(text, pos, height=25, layer='TEXT', color=None):
    attribs = {'layer': layer, 'height': height}
    if color:
        attribs['color'] = color
    t = msp.add_text(text, dxfattribs=attribs)
    t.set_placement(pos)
    return t

# ==================== 俯视图 (Top View) ====================
# 位置：左上
tx, ty = 200, TOTAL_HEIGHT + 800

# 外框
draw_rect((tx, ty), (tx + TOTAL_WIDTH, ty + TOTAL_DEPTH), 'OUTLINE')

# 左右侧板
draw_line((tx + BOARD_THICK, ty), (tx + BOARD_THICK, ty + TOTAL_DEPTH), 'BOARD')
draw_line((tx + TOTAL_WIDTH - BOARD_THICK, ty), (tx + TOTAL_WIDTH - BOARD_THICK, ty + TOTAL_DEPTH), 'BOARD')

# 背板
draw_line((tx, ty + TOTAL_DEPTH - BOARD_THICK), (tx + TOTAL_WIDTH, ty + TOTAL_DEPTH - BOARD_THICK), 'BOARD')

# 竖隔板（分三区）
left_x = tx + BOARD_THICK + LEFT_ZONE
mid_x = left_x + BOARD_THICK + MID_ZONE
draw_line((left_x, ty), (left_x, ty + TOTAL_DEPTH - BOARD_THICK), 'BOARD')
draw_line((mid_x, ty), (mid_x, ty + TOTAL_DEPTH - BOARD_THICK), 'BOARD')

# 门板线（俯视图显示门板厚度）
draw_line((tx, ty - 5), (tx + TOTAL_WIDTH, ty - 5), 'DOOR')
draw_line((tx, ty), (tx + TOTAL_WIDTH, ty), 'DOOR')

# 标注
add_dim((tx, ty), (tx + TOTAL_WIDTH, ty), -150, 'DIM')
add_dim((tx + TOTAL_WIDTH, ty), (tx + TOTAL_WIDTH, ty + TOTAL_DEPTH), 150, 'DIM')
add_dim((tx, ty - 5), (tx + LEFT_ZONE, ty - 5), -100, 'DIM')
add_dim((left_x + BOARD_THICK, ty - 5), (left_x + BOARD_THICK + MID_ZONE, ty - 5), -100, 'DIM')
add_dim((mid_x + BOARD_THICK, ty - 5), (tx + TOTAL_WIDTH - BOARD_THICK, ty - 5), -100, 'DIM')

add_text('俯视图', (tx + TOTAL_WIDTH/2 - 60, ty + TOTAL_DEPTH + 250), 30, 'TEXT')

# ==================== 外观图 (Front View - Exterior) ====================
# 位置：左下
fx, fy = 200, 200

# 外框
draw_rect((fx, fy), (fx + TOTAL_WIDTH, fy + TOTAL_HEIGHT), 'OUTLINE')

# 顶封板
draw_rect((fx, fy + TOTAL_HEIGHT - 50), (fx + TOTAL_WIDTH, fy + TOTAL_HEIGHT), 'BOARD')
# 顶封板斜线填充
for i in range(0, TOTAL_WIDTH, 80):
    draw_line((fx + i, fy + TOTAL_HEIGHT - 50), (fx + i + 50, fy + TOTAL_HEIGHT), 'PATTERN')

# 踢脚线
draw_rect((fx, fy), (fx + TOTAL_WIDTH, fy + 50), 'BOARD')

# 四扇门的分隔线
door_width = (TOTAL_WIDTH - BOARD_THICK * 2 - GAP * 3) / 4
door_left = fx + BOARD_THICK

# 竖向门缝
x1 = door_left + GAP + door_width
x2 = x1 + GAP + door_width
x3 = x2 + GAP + door_width

# 门板外框
draw_line((fx, fy + 50), (fx, fy + TOTAL_HEIGHT - 50), 'DOOR')
draw_line((fx + TOTAL_WIDTH, fy + 50), (fx + TOTAL_WIDTH, fy + TOTAL_HEIGHT - 50), 'DOOR')
draw_line((fx, fy + TOTAL_HEIGHT - 50), (fx + TOTAL_WIDTH, fy + TOTAL_HEIGHT - 50), 'DOOR')
draw_line((fx, fy + 50), (fx + TOTAL_WIDTH, fy + 50), 'DOOR')

# 四扇门竖缝
draw_line((x1, fy + 50), (x1, fy + TOTAL_HEIGHT - 50), 'DOOR')
draw_line((x2, fy + 50), (x2, fy + TOTAL_HEIGHT - 50), 'DOOR')
draw_line((x3, fy + 50), (x3, fy + TOTAL_HEIGHT - 50), 'DOOR')

# 门板花纹（菱形几何图案）- 每扇门
def draw_door_pattern(dx, dy, w, h, layer='PATTERN'):
    """绘制门板菱形花纹"""
    cx = dx + w/2
    cy = dy + h/2
    # 菱形
    draw_line((cx, dy + 20), (dx + w - 20, cy), layer)
    draw_line((dx + w - 20, cy), (cx, dy + h - 20), layer)
    draw_line((cx, dy + h - 20), (dx + 20, cy), layer)
    draw_line((dx + 20, cy), (cx, dy + 20), layer)
    # 内菱形
    margin = 80
    draw_line((cx, dy + margin), (dx + w - margin, cy), layer)
    draw_line((dx + w - margin, cy), (cx, dy + h - margin), layer)
    draw_line((cx, dy + h - margin), (dx + margin, cy), layer)
    draw_line((dx + margin, cy), (cx, dy + margin), layer)

# 为每扇门绘制花纹
for i in range(4):
    dx = door_left + i * (door_width + GAP)
    draw_door_pattern(dx, fy + 50, door_width, TOTAL_HEIGHT - 100)

# 拉手位置（小圆点）
for i in range(4):
    hx = door_left + i * (door_width + GAP) + door_width - 30
    hy = fy + TOTAL_HEIGHT/2
    msp.add_circle((hx, hy), 8, dxfattribs={'layer': 'DOOR'})

# 标注
add_dim((fx, fy), (fx + TOTAL_WIDTH, fy), -150, 'DIM')
add_dim((fx + TOTAL_WIDTH, fy), (fx + TOTAL_WIDTH, fy + TOTAL_HEIGHT), 150, 'DIM')
add_dim((fx, fy + TOTAL_HEIGHT + 5), (fx + TOTAL_WIDTH, fy + TOTAL_HEIGHT + 5), 150, 'DIM')

# 门宽标注
for i in range(4):
    dx = door_left + i * (door_width + GAP)
    add_dim((dx, fy + TOTAL_HEIGHT + 80), (dx + door_width, fy + TOTAL_HEIGHT + 80), 60, 'DIM')

# 顶封板标注
add_dim((fx + TOTAL_WIDTH + 80, fy + TOTAL_HEIGHT - 50), (fx + TOTAL_WIDTH + 80, fy + TOTAL_HEIGHT), 80, 'DIM')

# 踢脚标注
add_dim((fx + TOTAL_WIDTH + 80, fy), (fx + TOTAL_WIDTH + 80, fy + 50), 80, 'DIM')

add_text('外观图', (fx + TOTAL_WIDTH/2 - 60, fy - 250), 30, 'TEXT')

# ==================== 结构图 (Internal Structure View) ====================
# 位置：中下
ix, iy = TOTAL_WIDTH + 600, 200

# 外框
draw_rect((ix, iy), (ix + TOTAL_WIDTH, iy + TOTAL_HEIGHT), 'OUTLINE')

# 顶封板
draw_rect((ix, iy + TOTAL_HEIGHT - 50), (ix + TOTAL_WIDTH, iy + TOTAL_HEIGHT), 'BOARD')
for i in range(0, TOTAL_WIDTH, 80):
    draw_line((ix + i, iy + TOTAL_HEIGHT - 50), (ix + i + 50, iy + TOTAL_HEIGHT), 'PATTERN')

# 踢脚线
draw_rect((ix, iy), (ix + TOTAL_WIDTH, iy + 50), 'BOARD')

# 左右侧板
draw_line((ix + BOARD_THICK, iy), (ix + BOARD_THICK, iy + TOTAL_HEIGHT - 50), 'BOARD')
draw_line((ix + TOTAL_WIDTH - BOARD_THICK, iy), (ix + TOTAL_WIDTH - BOARD_THICK, iy + TOTAL_HEIGHT - 50), 'BOARD')

# 竖隔板（分三区）
inner_left = ix + BOARD_THICK + LEFT_ZONE
inner_mid = inner_left + BOARD_THICK + MID_ZONE
draw_line((inner_left, iy + 50), (inner_left, iy + TOTAL_HEIGHT - 50), 'BOARD')
draw_line((inner_mid, iy + 50), (inner_mid, iy + TOTAL_HEIGHT - 50), 'BOARD')

# === 左区：上部挂衣 + 下部层板 ===
# 顶部被褥区横板
y_top = iy + TOTAL_HEIGHT - 50 - TOP_ZONE
draw_line((ix + BOARD_THICK, y_top), (inner_left, y_top), 'BOARD')

# 挂衣区横板
y_hang = y_top - HANG_ZONE
draw_line((ix + BOARD_THICK, y_hang), (inner_left, y_hang), 'BOARD')

# 挂衣杆
hang_x1 = ix + BOARD_THICK + 40
hang_x2 = inner_left - 40
draw_line((hang_x1, y_top - 80), (hang_x2, y_top - 80), 'HANGER')
# 挂衣杆端头
draw_line((hang_x1, y_top - 60), (hang_x1, y_top - 100), 'HANGER')
draw_line((hang_x2, y_top - 60), (hang_x2, y_top - 100), 'HANGER')

# 挂的衣服（简化表示）
for j in range(3):
    cx = ix + BOARD_THICK + 100 + j * 150
    draw_line((cx, y_top - 100), (cx, y_top - 350), 'INNER')
    draw_line((cx - 30, y_top - 350), (cx + 30, y_top - 350), 'INNER')

# 层板区
y_shelf1 = y_hang - 300
y_shelf2 = y_hang - 600
draw_line((ix + BOARD_THICK, y_shelf1), (inner_left, y_shelf1), 'BOARD')
draw_line((ix + BOARD_THICK, y_shelf2), (inner_left, y_shelf2), 'BOARD')

# 层板上的物品（简化）
for j in range(2):
    cy = y_hang - 150 - j * 300
    draw_line((ix + BOARD_THICK + 50, cy), (ix + BOARD_THICK + 200, cy), 'INNER')

# === 中区：上下挂衣 ===
# 顶部被褥区
draw_line((inner_left + BOARD_THICK, y_top), (inner_mid, y_top), 'BOARD')

# 中间横板（分上下挂衣区）
y_mid_hang = y_top - int(HANG_ZONE * 0.6)
draw_line((inner_left + BOARD_THICK, y_mid_hang), (inner_mid, y_mid_hang), 'BOARD')

# 上挂衣杆
hang2_x1 = inner_left + BOARD_THICK + 40
hang2_x2 = inner_mid - 40
draw_line((hang2_x1, y_top - 80), (hang2_x2, y_top - 80), 'HANGER')
draw_line((hang2_x1, y_top - 60), (hang2_x1, y_top - 100), 'HANGER')
draw_line((hang2_x2, y_top - 60), (hang2_x2, y_top - 100), 'HANGER')

# 上区衣服
for j in range(2):
    cx = inner_left + BOARD_THICK + 100 + j * 150
    draw_line((cx, y_top - 100), (cx, y_top - 350), 'INNER')
    draw_line((cx - 30, y_top - 350), (cx + 30, y_top - 350), 'INNER')

# 下挂衣杆
hang3_y = y_mid_hang - 80
draw_line((hang2_x1, hang3_y), (hang2_x2, hang3_y), 'HANGER')
draw_line((hang2_x1, hang3_y - 20), (hang2_x1, hang3_y + 20), 'HANGER')
draw_line((hang2_x2, hang3_y - 20), (hang2_x2, hang3_y + 20), 'HANGER')

# 下区衣服
for j in range(3):
    cx = inner_left + BOARD_THICK + 80 + j * 120
    draw_line((cx, hang3_y - 20), (cx, y_hang + 100), 'INNER')
    draw_line((cx - 25, y_hang + 100), (cx + 25, y_hang + 100), 'INNER')

# === 右区：抽屉 + 层板 ===
right_x1 = inner_mid + BOARD_THICK
right_x2 = ix + TOTAL_WIDTH - BOARD_THICK

# 顶部被褥区
draw_line((right_x1, y_top), (right_x2, y_top), 'BOARD')

# 三个抽屉
drawer_h = (y_top - 50 - iy - 50) / 3
for j in range(3):
    y_d = y_top - (j + 1) * drawer_h
    draw_line((right_x1, y_d), (right_x2, y_d), 'BOARD')
    # 把手
    handle_x = (right_x1 + right_x2) / 2
    handle_y = y_d + drawer_h / 2
    draw_line((handle_x - 20, handle_y), (handle_x + 20, handle_y), 'INNER')

# 标注
add_dim((ix, iy), (ix + TOTAL_WIDTH, iy), -150, 'DIM')
add_dim((ix + TOTAL_WIDTH, iy), (ix + TOTAL_WIDTH, iy + TOTAL_HEIGHT), 150, 'DIM')

# 各区宽度标注
add_dim((ix, iy + TOTAL_HEIGHT + 80), (ix + BOARD_THICK + LEFT_ZONE, iy + TOTAL_HEIGHT + 80), 60, 'DIM')
add_dim((inner_left, iy + TOTAL_HEIGHT + 80), (inner_mid, iy + TOTAL_HEIGHT + 80), 60, 'DIM')
add_dim((inner_mid, iy + TOTAL_HEIGHT + 80), (ix + TOTAL_WIDTH - BOARD_THICK, iy + TOTAL_HEIGHT + 80), 60, 'DIM')

# 高度分区标注
add_dim((ix - 80, y_top), (ix - 80, iy + TOTAL_HEIGHT - 50), -120, 'DIM')
add_dim((ix - 80, y_hang), (ix - 80, y_top), -120, 'DIM')

add_text('结构图', (ix + TOTAL_WIDTH/2 - 60, iy - 250), 30, 'TEXT')

# ==================== 侧视图 (Side View) ====================
# 位置：右侧
sx, sy = TOTAL_WIDTH * 2 + 1000, 200

# 外框
draw_rect((sx, sy), (sx + TOTAL_DEPTH, sy + TOTAL_HEIGHT), 'OUTLINE')

# 顶封板
draw_rect((sx, sy + TOTAL_HEIGHT - 50), (sx + TOTAL_DEPTH, sy + TOTAL_HEIGHT), 'BOARD')
for i in range(0, TOTAL_DEPTH, 60):
    draw_line((sx + i, sy + TOTAL_HEIGHT - 50), (sx + i + 40, sy + TOTAL_HEIGHT), 'PATTERN')

# 踢脚线
draw_rect((sx, sy), (sx + TOTAL_DEPTH, sy + 50), 'BOARD')

# 背板
draw_line((sx + BOARD_THICK, sy), (sx + BOARD_THICK, sy + TOTAL_HEIGHT - 50), 'BOARD')

# 层板线（侧视图显示）
for y_offset in [TOP_ZONE, TOP_ZONE + HANG_ZONE, TOP_ZONE + HANG_ZONE + 300]:
    y_line = sy + TOTAL_HEIGHT - 50 - y_offset
    draw_line((sx + BOARD_THICK, y_line), (sx + TOTAL_DEPTH - BOARD_THICK, y_line), 'BOARD')

# 标注
add_dim((sx, sy), (sx + TOTAL_DEPTH, sy), -150, 'DIM')
add_dim((sx + TOTAL_DEPTH, sy), (sx + TOTAL_DEPTH, sy + TOTAL_HEIGHT), 150, 'DIM')
add_dim((sx + TOTAL_DEPTH + 50, sy + TOTAL_HEIGHT - 50), (sx + TOTAL_DEPTH + 50, sy + TOTAL_HEIGHT), 80, 'DIM')

add_text('侧视图', (sx + TOTAL_DEPTH/2 - 60, sy - 250), 30, 'TEXT')

# ==================== 备注文字 ====================
note_x = TOTAL_WIDTH * 2 + 1000 + TOTAL_DEPTH + 400
note_y = TOTAL_HEIGHT + 800

add_text('备注：主卧衣柜', (note_x, note_y), 35, 'NOTE')
add_text(f'柜体颜色：派阳山 博兰灰 欧松板 49尺', (note_x, note_y - 60), 22, 'NOTE')
add_text(f'柜体颜色：福庆 福月胡桃 多层实木 48尺', (note_x, note_y - 100), 22, 'NOTE')
add_text(f'木制免拉手', (note_x, note_y - 140), 22, 'NOTE')
add_text(f'文件配效果图', (note_x, note_y - 180), 22, 'NOTE')

add_text(f'尺寸参数:', (note_x, note_y - 260), 25, 'TEXT')
add_text(f'总宽: {TOTAL_WIDTH}mm', (note_x, note_y - 300), 22, 'TEXT')
add_text(f'总深: {TOTAL_DEPTH}mm', (note_x, note_y - 335), 22, 'TEXT')
add_text(f'总高: {TOTAL_HEIGHT}mm', (note_x, note_y - 370), 22, 'TEXT')
add_text(f'板材: {BOARD_THICK}mm', (note_x, note_y - 405), 22, 'TEXT')

# ==================== 保存 ====================
output = os.path.join(r'D:\tokai', '衣柜设计图_标准版.dxf')
doc.saveas(output)
print(f'完成: {output}')
print(f'大小: {os.path.getsize(output) / 1024:.1f} KB')
