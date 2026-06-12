#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
衣柜CAD图纸生成脚本 v3
补充：顶封板、左侧收口、内部结构图
"""

import ezdxf
from ezdxf import units
import os

# ==================== 尺寸参数 ====================
OVERALL_WIDTH = 1590    # 衣柜总宽 mm
OVERALL_DEPTH = 600     # 衣柜深度 mm
OVERALL_HEIGHT = 2800   # 衣柜总高 mm
BOARD_THICKNESS = 18    # 板材厚度 mm
GAP = 2                 # 门板间隙 mm

# 顶封板和收口
TOP_BOARD_HEIGHT = 50   # 顶封板高度 mm
LEFT_TRIM_WIDTH = 50    # 左侧收口宽度 mm
BASEBOARD_HEIGHT = 50   # 踢脚高度 mm

# 柜体实际高度（扣除顶封板）
CABINET_HEIGHT = OVERALL_HEIGHT - TOP_BOARD_HEIGHT

# 柜体实际宽度（扣除左侧收口）
CABINET_WIDTH = OVERALL_WIDTH - LEFT_TRIM_WIDTH

# 门板划分
UPPER_DOOR_HEIGHT = 1850  # 上门高度
LOWER_SECTION_HEIGHT = CABINET_HEIGHT - BASEBOARD_HEIGHT - UPPER_DOOR_HEIGHT

# 下部分左侧 - 2扇短门
LOWER_LEFT_WIDTH = (CABINET_WIDTH - BOARD_THICKNESS * 2) / 2
# 下部分右侧 - 2个抽屉
LOWER_RIGHT_WIDTH = CABINET_WIDTH - BOARD_THICKNESS * 2 - LOWER_LEFT_WIDTH

# 门板宽度计算（4扇上门，对开两组）
UPPER_DOOR_WIDTH = (CABINET_WIDTH - BOARD_THICKNESS * 2 - GAP * 3) / 4

# 下方门板宽度（2扇，对开）
LOWER_DOOR_WIDTH = (LOWER_LEFT_WIDTH - GAP) / 2

# 抽屉高度
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
doc.layers.add('TRIM', color=4)       # 收口/封板 - 青色
doc.layers.add('DIMENSION', color=2)
doc.layers.add('TEXT', color=5)
doc.layers.add('INNER', color=6)      # 内部结构 - 品红

# ==================== 绘图函数 ====================
def draw_rect(start, end, layer='OUTLINE'):
    points = [start, (end[0], start[1]), end, (start[0], end[1])]
    return msp.add_lwpolyline(points, close=True, dxfattribs={'layer': layer})

def draw_line(start, end, layer='OUTLINE'):
    return msp.add_line(start, end, dxfattribs={'layer': layer})

def add_dim_linear(p1, p2, distance, layer='DIMENSION'):
    dim = msp.add_linear_dim(
        base=(p1[0], p1[1] + distance),
        p1=p1,
        p2=p2,
        dimstyle='EZDXF',
        override={'dimtxt': 20, 'dimasz': 12}
    )
    dim.render()
    return dim

def add_text(text, position, height=18, layer='TEXT'):
    t = msp.add_text(text, dxfattribs={'layer': layer, 'height': height})
    t.set_placement(position)
    return t

# ==================== 正立面图 (Front Elevation) ====================
fx, fy = 300, 300

# === 顶封板 ===
draw_rect((fx, fy + CABINET_HEIGHT), (fx + OVERALL_WIDTH, fy + OVERALL_HEIGHT), 'TRIM')
# 顶封板斜线填充表示
draw_line((fx, fy + CABINET_HEIGHT), (fx + OVERALL_WIDTH, fy + OVERALL_HEIGHT), 'TRIM')
draw_line((fx + OVERALL_WIDTH, fy + CABINET_HEIGHT), (fx, fy + OVERALL_HEIGHT), 'TRIM')

# === 左侧收口板 ===
draw_rect((fx, fy), (fx + LEFT_TRIM_WIDTH, fy + CABINET_HEIGHT), 'TRIM')
# 收口板斜线填充
draw_line((fx, fy), (fx + LEFT_TRIM_WIDTH, fy + CABINET_HEIGHT), 'TRIM')
draw_line((fx + LEFT_TRIM_WIDTH, fy), (fx, fy + CABINET_HEIGHT), 'TRIM')

# === 柜体外轮廓 ===
cabinet_left = fx + LEFT_TRIM_WIDTH
draw_rect((cabinet_left, fy), (fx + OVERALL_WIDTH, fy + CABINET_HEIGHT), 'OUTLINE')

# 踢脚线
draw_line((cabinet_left, fy + BASEBOARD_HEIGHT), (fx + OVERALL_WIDTH, fy + BASEBOARD_HEIGHT), 'BOARD')

# 上下分界线
draw_line((cabinet_left, fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT), 
          (fx + OVERALL_WIDTH, fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT), 'BOARD')

# 左右侧板
draw_line((cabinet_left + BOARD_THICKNESS, fy), 
          (cabinet_left + BOARD_THICKNESS, fy + CABINET_HEIGHT), 'BOARD')
draw_line((fx + OVERALL_WIDTH - BOARD_THICKNESS, fy), 
          (fx + OVERALL_WIDTH - BOARD_THICKNESS, fy + CABINET_HEIGHT), 'BOARD')

# === 上部分：4扇门 ===
upper_left = cabinet_left + BOARD_THICKNESS
upper_bottom = fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT
upper_top = fy + CABINET_HEIGHT - BOARD_THICKNESS

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
mid_x = cabinet_left + (CABINET_WIDTH - BOARD_THICKNESS * 2) / 2 + BOARD_THICKNESS
draw_line((mid_x, upper_bottom), (mid_x, upper_top), 'BOARD')

# === 下部分左侧：2扇门 ===
lower_left_x = cabinet_left + BOARD_THICKNESS
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

draw_rect((drawer_x, lower_top - DRAWER_HEIGHT), (drawer_right, lower_top), 'DRAWER')
draw_rect((drawer_x, fy + BASEBOARD_HEIGHT + GAP), (drawer_right, fy + BASEBOARD_HEIGHT + DRAWER_HEIGHT), 'DRAWER')

# === 标注 ===
# 总宽（含收口）
add_dim_linear((fx, fy - 80), (fx + OVERALL_WIDTH, fy - 80), -200, 'DIMENSION')

# 柜体宽度
add_dim_linear((cabinet_left, fy - 30), (fx + OVERALL_WIDTH, fy - 30), -150, 'DIMENSION')

# 左侧收口宽度
add_dim_linear((fx, fy - 30), (cabinet_left, fy - 30), -100, 'DIMENSION')

# 总高（含顶封板）
add_dim_linear((fx + OVERALL_WIDTH + 80, fy), (fx + OVERALL_WIDTH + 80, fy + OVERALL_HEIGHT), 200, 'DIMENSION')

# 顶封板高度
add_dim_linear((fx + OVERALL_WIDTH + 30, fy + CABINET_HEIGHT), 
               (fx + OVERALL_WIDTH + 30, fy + OVERALL_HEIGHT), 100, 'DIMENSION')

# 柜体高度
add_dim_linear((fx + OVERALL_WIDTH + 30, fy), 
               (fx + OVERALL_WIDTH + 30, fy + CABINET_HEIGHT), 150, 'DIMENSION')

# 踢脚高度
add_dim_linear((cabinet_left - 50, fy), (cabinet_left - 50, fy + BASEBOARD_HEIGHT), -100, 'DIMENSION')

# 上门高度
add_dim_linear((cabinet_left - 50, fy + BASEBOARD_HEIGHT), 
               (cabinet_left - 50, fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT), -100, 'DIMENSION')

# 上门宽度
add_dim_linear((door1_x, upper_top + 40), (door1_x + UPPER_DOOR_WIDTH, upper_top + 40), 120, 'DIMENSION')

# 标题
add_text('正立面图 (Front Elevation)', (fx + OVERALL_WIDTH/2 - 150, fy - 350), 25, 'TEXT')

# ==================== 侧立面图 (Side Elevation) ====================
sx, sy = OVERALL_WIDTH + 800, 300

# 顶封板
draw_rect((sx, sy + CABINET_HEIGHT), (sx + OVERALL_DEPTH, sy + OVERALL_HEIGHT), 'TRIM')
draw_line((sx, sy + CABINET_HEIGHT), (sx + OVERALL_DEPTH, sy + OVERALL_HEIGHT), 'TRIM')
draw_line((sx + OVERALL_DEPTH, sy + CABINET_HEIGHT), (sx, sy + OVERALL_HEIGHT), 'TRIM')

# 柜体
draw_rect((sx, sy), (sx + OVERALL_DEPTH, sy + CABINET_HEIGHT), 'OUTLINE')
draw_line((sx, sy + BASEBOARD_HEIGHT), (sx + OVERALL_DEPTH, sy + BASEBOARD_HEIGHT), 'BOARD')

# 背板
draw_line((sx + BOARD_THICKNESS, sy), (sx + BOARD_THICKNESS, sy + CABINET_HEIGHT), 'BOARD')

# 标注
add_dim_linear((sx, sy - 80), (sx + OVERALL_DEPTH, sy - 80), -200, 'DIMENSION')
add_dim_linear((sx + OVERALL_DEPTH + 50, sy), (sx + OVERALL_DEPTH + 50, sy + OVERALL_HEIGHT), 200, 'DIMENSION')
add_dim_linear((sx + OVERALL_DEPTH + 30, sy + CABINET_HEIGHT), 
               (sx + OVERALL_DEPTH + 30, sy + OVERALL_HEIGHT), 80, 'DIMENSION')

add_text('侧立面图 (Side Elevation)', (sx + OVERALL_DEPTH/2 - 150, sy - 350), 25, 'TEXT')

# ==================== 平面图 (Plan View) ====================
px, py = 300, OVERALL_HEIGHT + 600

# 左侧收口
draw_rect((px, py), (px + LEFT_TRIM_WIDTH, py + OVERALL_DEPTH), 'TRIM')
draw_line((px, py), (px + LEFT_TRIM_WIDTH, py + OVERALL_DEPTH), 'TRIM')
draw_line((px + LEFT_TRIM_WIDTH, py), (px, py + OVERALL_DEPTH), 'TRIM')

# 柜体
cabinet_plan_left = px + LEFT_TRIM_WIDTH
draw_rect((cabinet_plan_left, py), (px + OVERALL_WIDTH, py + OVERALL_DEPTH), 'OUTLINE')

# 左右侧板
draw_line((cabinet_plan_left + BOARD_THICKNESS, py), 
          (cabinet_plan_left + BOARD_THICKNESS, py + OVERALL_DEPTH), 'BOARD')
draw_line((px + OVERALL_WIDTH - BOARD_THICKNESS, py), 
          (px + OVERALL_WIDTH - BOARD_THICKNESS, py + OVERALL_DEPTH), 'BOARD')

# 背板
draw_line((cabinet_plan_left, py + OVERALL_DEPTH - BOARD_THICKNESS), 
          (px + OVERALL_WIDTH, py + OVERALL_DEPTH - BOARD_THICKNESS), 'BOARD')

# 中间隔板
mid_plan_x = cabinet_plan_left + (CABINET_WIDTH - BOARD_THICKNESS * 2) / 2 + BOARD_THICKNESS
draw_line((mid_plan_x, py), (mid_plan_x, py + OVERALL_DEPTH), 'BOARD')

# 下部分隔板
lower_plan_x = cabinet_plan_left + BOARD_THICKNESS + LOWER_LEFT_WIDTH
draw_line((lower_plan_x, py), (lower_plan_x, py + OVERALL_DEPTH), 'BOARD')

# 标注
add_dim_linear((px, py - 80), (px + OVERALL_WIDTH, py - 80), -200, 'DIMENSION')
add_dim_linear((px + OVERALL_WIDTH + 50, py), (px + OVERALL_WIDTH + 50, py + OVERALL_DEPTH), 200, 'DIMENSION')

add_text('平面图 (Plan View)', (px + OVERALL_WIDTH/2 - 120, py + OVERALL_DEPTH + 200), 25, 'TEXT')

# ==================== 内部结构图 (Internal Structure) ====================
ix, iy = OVERALL_WIDTH + 800, OVERALL_HEIGHT + 600

# 柜体外框
draw_rect((ix, iy), (ix + CABINET_WIDTH, iy + CABINET_HEIGHT), 'INNER')

# 踢脚线
draw_line((ix, iy + BASEBOARD_HEIGHT), (ix + CABINET_WIDTH, iy + BASEBOARD_HEIGHT), 'INNER')

# 左右侧板
draw_line((ix + BOARD_THICKNESS, iy), (ix + BOARD_THICKNESS, iy + CABINET_HEIGHT), 'INNER')
draw_line((ix + CABINET_WIDTH - BOARD_THICKNESS, iy), 
          (ix + CABINET_WIDTH - BOARD_THICKNESS, iy + CABINET_HEIGHT), 'INNER')

# 中间竖隔板
mid_inner_x = ix + (CABINET_WIDTH - BOARD_THICKNESS * 2) / 2 + BOARD_THICKNESS
draw_line((mid_inner_x, iy + BASEBOARD_HEIGHT), (mid_inner_x, iy + CABINET_HEIGHT - BOARD_THICKNESS), 'INNER')

# 上部分横隔板（挂衣杆位置）
hanging_height = 1200  # 挂衣区高度
draw_line((ix + BOARD_THICKNESS, iy + CABINET_HEIGHT - BOARD_THICKNESS - hanging_height), 
          (mid_inner_x, iy + CABINET_HEIGHT - BOARD_THICKNESS - hanging_height), 'INNER')
draw_line((mid_inner_x, iy + CABINET_HEIGHT - BOARD_THICKNESS - hanging_height), 
          (ix + CABINET_WIDTH - BOARD_THICKNESS, iy + CABINET_HEIGHT - BOARD_THICKNESS - hanging_height), 'INNER')

# 挂衣杆（用虚线表示）
draw_line((ix + BOARD_THICKNESS + 50, iy + CABINET_HEIGHT - BOARD_THICKNESS - hanging_height + 80), 
          (mid_inner_x - 50, iy + CABINET_HEIGHT - BOARD_THICKNESS - hanging_height + 80), 'INNER')
draw_line((mid_inner_x + 50, iy + CABINET_HEIGHT - BOARD_THICKNESS - hanging_height + 80), 
          (ix + CABINET_WIDTH - BOARD_THICKNESS - 50, iy + CABINET_HEIGHT - BOARD_THICKNESS - hanging_height + 80), 'INNER')

# 下部分横隔板
lower_top_inner = iy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT
draw_line((ix + BOARD_THICKNESS, lower_top_inner), (mid_inner_x, lower_top_inner), 'INNER')

# 抽屉分隔
draw_line((mid_inner_x + BOARD_THICKNESS, lower_top_inner - DRAWER_HEIGHT), 
          (ix + CABINET_WIDTH - BOARD_THICKNESS, lower_top_inner - DRAWER_HEIGHT), 'INNER')

# 层板
shelf_y1 = iy + BASEBOARD_HEIGHT + 300
shelf_y2 = iy + BASEBOARD_HEIGHT + 600
draw_line((ix + BOARD_THICKNESS, shelf_y1), (mid_inner_x, shelf_y1), 'INNER')
draw_line((ix + BOARD_THICKNESS, shelf_y2), (mid_inner_x, shelf_y2), 'INNER')

# 标注
add_dim_linear((ix, iy - 80), (ix + CABINET_WIDTH, iy - 80), -200, 'DIMENSION')
add_dim_linear((ix + CABINET_WIDTH + 50, iy), (ix + CABINET_WIDTH + 50, iy + CABINET_HEIGHT), 200, 'DIMENSION')

# 挂衣区标注
add_dim_linear((ix + BOARD_THICKNESS - 50, iy + CABINET_HEIGHT - BOARD_THICKNESS - hanging_height), 
               (ix + BOARD_THICKNESS - 50, iy + CABINET_HEIGHT - BOARD_THICKNESS), -120, 'DIMENSION')

add_text('内部结构图 (Internal Structure)', (ix + CABINET_WIDTH/2 - 150, iy - 350), 25, 'TEXT')
add_text('挂衣区', (ix + BOARD_THICKNESS + 100, iy + CABINET_HEIGHT - BOARD_THICKNESS - hanging_height/2), 20, 'INNER')
add_text('层板区', (ix + BOARD_THICKNESS + 100, iy + BASEBOARD_HEIGHT + 150), 20, 'INNER')
add_text('抽屉', (mid_inner_x + BOARD_THICKNESS + 50, lower_top_inner - DRAWER_HEIGHT/2), 20, 'INNER')

# ==================== 尺寸说明文字 ====================
notes_x = CABINET_WIDTH + 1200
notes_y = OVERALL_HEIGHT + 600

add_text('衣柜设计图 - 尺寸说明', (notes_x, notes_y), 30, 'TEXT')
add_text(f'总宽: {OVERALL_WIDTH}mm (含收口{LEFT_TRIM_WIDTH}mm)', (notes_x, notes_y - 50), 22, 'TEXT')
add_text(f'总深: {OVERALL_DEPTH}mm', (notes_x, notes_y - 85), 22, 'TEXT')
add_text(f'总高: {OVERALL_HEIGHT}mm (含顶封板{TOP_BOARD_HEIGHT}mm)', (notes_x, notes_y - 120), 22, 'TEXT')
add_text(f'柜体尺寸: {CABINET_WIDTH}×{OVERALL_DEPTH}×{CABINET_HEIGHT}mm', (notes_x, notes_y - 155), 22, 'TEXT')
add_text(f'板材厚度: {BOARD_THICKNESS}mm', (notes_x, notes_y - 190), 22, 'TEXT')
add_text(f'门板间隙: {GAP}mm', (notes_x, notes_y - 225), 22, 'TEXT')

add_text('结构说明:', (notes_x, notes_y - 290), 22, 'TEXT')
add_text(f'- 顶封板: {TOP_BOARD_HEIGHT}mm (斜线填充)', (notes_x, notes_y - 325), 20, 'TEXT')
add_text(f'- 左侧收口: {LEFT_TRIM_WIDTH}mm (斜线填充)', (notes_x, notes_y - 355), 20, 'TEXT')
add_text('- 上部分: 4扇长门 (对开两组)', (notes_x, notes_y - 385), 20, 'TEXT')
add_text('- 下部分左侧: 2扇短门 + 层板', (notes_x, notes_y - 415), 20, 'TEXT')
add_text('- 下部分右侧: 2个抽屉', (notes_x, notes_y - 445), 20, 'TEXT')
add_text('- 上部挂衣区: 配挂衣杆', (notes_x, notes_y - 475), 20, 'TEXT')

# ==================== 保存文件 ====================
output_file = os.path.join(r'D:\tokai', '衣柜设计图_完整版.dxf')
doc.saveas(output_file)
print(f'CAD图纸已生成: {output_file}')
print(f'文件大小: {os.path.getsize(output_file) / 1024:.1f} KB')
