#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
衣柜CAD图纸生成脚本 v2
根据模型和尺寸生成正立面图、侧立面图、平面图
"""

import ezdxf
from ezdxf import units
from ezdxf.math import Vec2
import os

# ==================== 尺寸参数 ====================
OVERALL_WIDTH = 1590    # 衣柜总宽 mm
OVERALL_DEPTH = 600     # 衣柜深度 mm
OVERALL_HEIGHT = 2800   # 衣柜总高 mm
BASEBOARD_THICKNESS = 15  # 踢脚线厚度 mm
BOARD_THICKNESS = 18    # 板材厚度 mm
GAP = 2                 # 门板间隙 mm

# 踢脚高度
BASEBOARD_HEIGHT = 50   # 踢脚高度 mm

# 柜体结构划分
UPPER_DOOR_HEIGHT = 1900  # 上门高度
LOWER_SECTION_HEIGHT = OVERALL_HEIGHT - BASEBOARD_HEIGHT - UPPER_DOOR_HEIGHT

LOWER_LEFT_WIDTH = 757   # 左侧宽度

UPPER_DOOR_WIDTH = (OVERALL_WIDTH - BOARD_THICKNESS * 2 - GAP * 3) / 4
LOWER_DOOR_WIDTH = (LOWER_LEFT_WIDTH - GAP) / 2
DRAWER_HEIGHT = (LOWER_SECTION_HEIGHT - GAP * 3) / 2

# ==================== 创建DWG文件 ====================
doc = ezdxf.new('R2010')
doc.units = units.MM
msp = doc.modelspace()

# 创建图层
doc.layers.add('OUTLINE', color=7)
doc.layers.add('BOARD', color=7)
doc.layers.add('DOOR', color=1)
doc.layers.add('DRAWER', color=3)
doc.layers.add('DIMENSION', color=2)
doc.layers.add('TEXT', color=5)
doc.layers.add('HATCH', color=8)

# ==================== 绘图函数 ====================
def draw_rect(start, end, layer='OUTLINE'):
    points = [start, (end[0], start[1]), end, (start[0], end[1])]
    return msp.add_lwpolyline(points, close=True, dxfattribs={'layer': layer})

def draw_line(start, end, layer='OUTLINE'):
    return msp.add_line(start, end, dxfattribs={'layer': layer})

def add_dim_linear(p1, p2, distance, layer='DIMENSION'):
    """添加线性标注 - 使用ezdxf 1.4.x API"""
    dim = msp.add_linear_dim(
        base=(p1[0], p1[1] + distance),
        p1=p1,
        p2=p2,
        dimstyle='EZDXF',
        override={'dimtxt': 25, 'dimasz': 15}
    )
    dim.render()
    return dim

def add_text(text, position, height=20, layer='TEXT'):
    t = msp.add_text(text, dxfattribs={'layer': layer, 'height': height})
    t.set_placement(position)
    return t

# ==================== 正立面图 (Front Elevation) ====================
fx, fy = 200, 200  # 起点，留出标注空间

# 外轮廓
draw_rect((fx, fy), (fx + OVERALL_WIDTH, fy + OVERALL_HEIGHT), 'OUTLINE')

# 踢脚线
draw_line((fx, fy + BASEBOARD_HEIGHT), (fx + OVERALL_WIDTH, fy + BASEBOARD_HEIGHT), 'BOARD')

# 上下分界线
draw_line((fx, fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT), 
          (fx + OVERALL_WIDTH, fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT), 'BOARD')

# 左右侧板
draw_line((fx + BOARD_THICKNESS, fy), (fx + BOARD_THICKNESS, fy + OVERALL_HEIGHT), 'BOARD')
draw_line((fx + OVERALL_WIDTH - BOARD_THICKNESS, fy), 
          (fx + OVERALL_WIDTH - BOARD_THICKNESS, fy + OVERALL_HEIGHT), 'BOARD')

# === 上部分：4扇门 ===
upper_left = fx + BOARD_THICKNESS
upper_bottom = fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT
upper_top = fy + OVERALL_HEIGHT - BOARD_THICKNESS

# 第一组对开门（左）
door1_x = upper_left + GAP
door2_x = upper_left + UPPER_DOOR_WIDTH + GAP
draw_rect((door1_x, upper_bottom), (door1_x + UPPER_DOOR_WIDTH, upper_top), 'DOOR')
draw_rect((door2_x, upper_bottom), (door2_x + UPPER_DOOR_WIDTH, upper_top), 'DOOR')

# 第二组对开门（右）
door3_x = door2_x + UPPER_DOOR_WIDTH + GAP
door4_x = door3_x + UPPER_DOOR_WIDTH + GAP
draw_rect((door3_x, upper_bottom), (door3_x + UPPER_DOOR_WIDTH, upper_top), 'DOOR')
draw_rect((door4_x, upper_bottom), (door4_x + UPPER_DOOR_WIDTH, upper_top), 'DOOR')

# 中间竖隔板
mid_x = fx + OVERALL_WIDTH / 2
draw_line((mid_x, upper_bottom), (mid_x, upper_top), 'BOARD')

# === 下部分左侧：2扇门 ===
lower_left_x = fx + BOARD_THICKNESS
lower_left_right = lower_left_x + LOWER_LEFT_WIDTH
lower_top = fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT

# 中间隔板
draw_line((lower_left_right, fy + BASEBOARD_HEIGHT), (lower_left_right, lower_top), 'BOARD')

# 左侧2扇门
ldoor1_x = lower_left_x + GAP
ldoor2_x = lower_left_x + LOWER_DOOR_WIDTH + GAP
draw_rect((ldoor1_x, fy + BASEBOARD_HEIGHT), (ldoor1_x + LOWER_DOOR_WIDTH, lower_top), 'DOOR')
draw_rect((ldoor2_x, fy + BASEBOARD_HEIGHT), (ldoor2_x + LOWER_DOOR_WIDTH, lower_top), 'DOOR')

# === 下部分右侧：2个抽屉 ===
drawer_x = lower_left_right + BOARD_THICKNESS + GAP
drawer_right = fx + OVERALL_WIDTH - BOARD_THICKNESS - GAP

# 上抽屉
draw_rect((drawer_x, lower_top - DRAWER_HEIGHT), (drawer_right, lower_top), 'DRAWER')
# 下抽屉
draw_rect((drawer_x, fy + BASEBOARD_HEIGHT + GAP), (drawer_right, fy + BASEBOARD_HEIGHT + DRAWER_HEIGHT), 'DRAWER')

# === 标注 ===
# 总宽标注
add_dim_linear((fx, fy - 50), (fx + OVERALL_WIDTH, fy - 50), -200, 'DIMENSION')

# 总高标注
add_dim_linear((fx + OVERALL_WIDTH + 50, fy), (fx + OVERALL_WIDTH + 50, fy + OVERALL_HEIGHT), 200, 'DIMENSION')

# 踢脚高度标注
add_dim_linear((fx - 50, fy), (fx - 50, fy + BASEBOARD_HEIGHT), -120, 'DIMENSION')

# 上门高度标注
add_dim_linear((fx - 50, fy + BASEBOARD_HEIGHT), (fx - 50, fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT), -120, 'DIMENSION')

# 上门宽度标注
add_dim_linear((door1_x, upper_top + 50), (door1_x + UPPER_DOOR_WIDTH, upper_top + 50), 150, 'DIMENSION')

# 标题
add_text('正立面图', (fx + OVERALL_WIDTH/2 - 100, fy - 350), 30, 'TEXT')

# ==================== 侧立面图 (Side Elevation) ====================
sx, sy = OVERALL_WIDTH + 600, 200

draw_rect((sx, sy), (sx + OVERALL_DEPTH, sy + OVERALL_HEIGHT), 'OUTLINE')
draw_line((sx, sy + BASEBOARD_HEIGHT), (sx + OVERALL_DEPTH, sy + BASEBOARD_HEIGHT), 'BOARD')

# 标注
add_dim_linear((sx, sy - 50), (sx + OVERALL_DEPTH, sy - 50), -200, 'DIMENSION')
add_dim_linear((sx + OVERALL_DEPTH + 50, sy), (sx + OVERALL_DEPTH + 50, sy + OVERALL_HEIGHT), 200, 'DIMENSION')

add_text('侧立面图', (sx + OVERALL_DEPTH/2 - 100, sy - 350), 30, 'TEXT')

# ==================== 平面图 (Plan View) ====================
px, py = 200, OVERALL_HEIGHT + 600

draw_rect((px, py), (px + OVERALL_WIDTH, py + OVERALL_DEPTH), 'OUTLINE')
draw_line((px + BOARD_THICKNESS, py), (px + BOARD_THICKNESS, py + OVERALL_DEPTH), 'BOARD')
draw_line((px + OVERALL_WIDTH - BOARD_THICKNESS, py), 
          (px + OVERALL_WIDTH - BOARD_THICKNESS, py + OVERALL_DEPTH), 'BOARD')
draw_line((px, py + OVERALL_DEPTH - BOARD_THICKNESS), 
          (px + OVERALL_WIDTH, py + OVERALL_DEPTH - BOARD_THICKNESS), 'BOARD')
draw_line((px + OVERALL_WIDTH/2, py), (px + OVERALL_WIDTH/2, py + OVERALL_DEPTH), 'BOARD')
draw_line((px + BOARD_THICKNESS + LOWER_LEFT_WIDTH, py), 
          (px + BOARD_THICKNESS + LOWER_LEFT_WIDTH, py + OVERALL_DEPTH), 'BOARD')

# 标注
add_dim_linear((px, py - 50), (px + OVERALL_WIDTH, py - 50), -200, 'DIMENSION')
add_dim_linear((px + OVERALL_WIDTH + 50, py), (px + OVERALL_WIDTH + 50, py + OVERALL_DEPTH), 200, 'DIMENSION')

add_text('平面图', (px + OVERALL_WIDTH/2 - 80, py + OVERALL_DEPTH + 200), 30, 'TEXT')

# ==================== 尺寸说明文字 ====================
notes_x = OVERALL_WIDTH + 600
notes_y = OVERALL_HEIGHT + 600

add_text('衣柜设计图 - 尺寸说明', (notes_x, notes_y), 35, 'TEXT')
add_text(f'总宽: {OVERALL_WIDTH}mm', (notes_x, notes_y - 60), 25, 'TEXT')
add_text(f'总深: {OVERALL_DEPTH}mm', (notes_x, notes_y - 100), 25, 'TEXT')
add_text(f'总高: {OVERALL_HEIGHT}mm', (notes_x, notes_y - 140), 25, 'TEXT')
add_text(f'板材厚度: {BOARD_THICKNESS}mm', (notes_x, notes_y - 180), 25, 'TEXT')
add_text(f'踢脚线厚度: {BASEBOARD_THICKNESS}mm', (notes_x, notes_y - 220), 25, 'TEXT')
add_text(f'门板间隙: {GAP}mm', (notes_x, notes_y - 260), 25, 'TEXT')

add_text('结构说明:', (notes_x, notes_y - 340), 25, 'TEXT')
add_text('- 上部分: 4扇长门 (对开两组)', (notes_x, notes_y - 380), 22, 'TEXT')
add_text('- 下部分左侧: 2扇短门', (notes_x, notes_y - 415), 22, 'TEXT')
add_text('- 下部分右侧: 2个抽屉', (notes_x, notes_y - 450), 22, 'TEXT')
add_text('- 踢脚高度: 50mm', (notes_x, notes_y - 485), 22, 'TEXT')

# ==================== 保存文件 ====================
output_file = os.path.join(r'D:\tokai', '衣柜设计图.dxf')
doc.saveas(output_file)
print(f'CAD图纸已生成: {output_file}')
print(f'文件大小: {os.path.getsize(output_file) / 1024:.1f} KB')
