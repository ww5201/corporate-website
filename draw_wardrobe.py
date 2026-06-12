#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
衣柜CAD图纸生成脚本
根据模型和尺寸生成正立面图、侧立面图、平面图
"""

import ezdxf
from ezdxf import units
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
# 上部分门高度（从踢脚线上方到顶部）
UPPER_DOOR_HEIGHT = 1900  # 上门高度
LOWER_SECTION_HEIGHT = OVERALL_HEIGHT - BASEBOARD_HEIGHT - UPPER_DOOR_HEIGHT  # 下部分高度

# 下部分左侧 - 2扇短门
LOWER_LEFT_WIDTH = 757   # 左侧宽度 (约一半)
# 下部分右侧 - 2个抽屉
LOWER_RIGHT_WIDTH = OVERALL_WIDTH - BOARD_THICKNESS * 2 - LOWER_LEFT_WIDTH  # 右侧宽度

# 门板宽度计算（4扇上门，对开两组）
UPPER_DOOR_WIDTH = (OVERALL_WIDTH - BOARD_THICKNESS * 2 - GAP * 3) / 4  # 每扇上门宽度

# 下方门板宽度（2扇，对开）
LOWER_DOOR_WIDTH = (LOWER_LEFT_WIDTH - GAP) / 2

# 抽屉高度
DRAWER_HEIGHT = (LOWER_SECTION_HEIGHT - GAP * 3) / 2  # 两个抽屉

# ==================== 创建DWG文件 ====================
doc = ezdxf.new('R2010')
doc.units = units.MM
msp = doc.modelspace()

# 创建图层
doc.layers.add('OUTLINE', color=7)      # 外轮廓 - 白色
doc.layers.add('BOARD', color=7)        # 板材 - 白色
doc.layers.add('DOOR', color=1)         # 门板 - 红色
doc.layers.add('DRAWER', color=3)       # 抽屉 - 绿色
doc.layers.add('DIMENSION', color=2)    # 标注 - 黄色
doc.layers.add('TEXT', color=5)         # 文字 - 蓝色
doc.layers.add('CENTERLINE', color=6)   # 中心线 - 品红
doc.layers.add('HATCH', color=8)        # 填充 - 灰色

# ==================== 绘图函数 ====================
def draw_rect(doc, msp, start, end, layer='OUTLINE'):
    """绘制矩形"""
    points = [start, (end[0], start[1]), end, (start[0], end[1])]
    return msp.add_lwpolyline(points, close=True, dxfattribs={'layer': layer})

def draw_line(doc, msp, start, end, layer='OUTLINE'):
    """绘制直线"""
    return msp.add_line(start, end, dxfattribs={'layer': layer})

def add_dimension_linear(doc, msp, p1, p2, offset, layer='DIMENSION'):
    """添加线性标注"""
    dim = msp.add_linear_dim(
        base=p1,
        p1=p1,
        p2=p2,
        offset=offset,
        dxfattribs={'layer': layer}
    )
    dim.render()
    return dim

def add_text(doc, msp, text, position, height=20, layer='TEXT'):
    """添加文字"""
    return msp.add_text(text, dxfattribs={'layer': layer}).set_placement(position)

# ==================== 正立面图 (Front Elevation) ====================
# 原点偏移，留出标注空间
fx, fy = 0, 0  # 正立面图起点

# 外轮廓
draw_rect(doc, msp, (fx, fy), (fx + OVERALL_WIDTH, fy + OVERALL_HEIGHT), 'OUTLINE')

# 踢脚线
draw_line(doc, msp, (fx, fy + BASEBOARD_HEIGHT), (fx + OVERALL_WIDTH, fy + BASEBOARD_HEIGHT), 'BOARD')

# 上下分界线
draw_line(doc, msp, (fx, fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT), 
          (fx + OVERALL_WIDTH, fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT), 'BOARD')

# 左右侧板内线
draw_line(doc, msp, (fx + BOARD_THICKNESS, fy), (fx + BOARD_THICKNESS, fy + OVERALL_HEIGHT), 'BOARD')
draw_line(doc, msp, (fx + OVERALL_WIDTH - BOARD_THICKNESS, fy), 
          (fx + OVERALL_WIDTH - BOARD_THICKNESS, fy + OVERALL_HEIGHT), 'BOARD')

# === 上部分：4扇门（对开两组）===
upper_left = fx + BOARD_THICKNESS
upper_bottom = fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT
upper_top = fy + OVERALL_HEIGHT - BOARD_THICKNESS

# 第一组对开门（左）
door1_x = upper_left + GAP
door2_x = upper_left + UPPER_DOOR_WIDTH + GAP
draw_rect(doc, msp, (door1_x, upper_bottom), (door1_x + UPPER_DOOR_WIDTH, upper_top), 'DOOR')
draw_rect(doc, msp, (door2_x, upper_bottom), (door2_x + UPPER_DOOR_WIDTH, upper_top), 'DOOR')

# 第二组对开门（右）
door3_x = door2_x + UPPER_DOOR_WIDTH + GAP
door4_x = door3_x + UPPER_DOOR_WIDTH + GAP
draw_rect(doc, msp, (door3_x, upper_bottom), (door3_x + UPPER_DOOR_WIDTH, upper_top), 'DOOR')
draw_rect(doc, msp, (door4_x, upper_bottom), (door4_x + UPPER_DOOR_WIDTH, upper_top), 'DOOR')

# 中间竖隔板
mid_x = fx + OVERALL_WIDTH / 2
draw_line(doc, msp, (mid_x, upper_bottom), (mid_x, upper_top), 'BOARD')

# === 下部分左侧：2扇门 ===
lower_left_x = fx + BOARD_THICKNESS
lower_left_right = lower_left_x + LOWER_LEFT_WIDTH
lower_top = fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT

# 中间隔板
draw_line(doc, msp, (lower_left_right, fy + BASEBOARD_HEIGHT), (lower_left_right, lower_top), 'BOARD')

# 左侧2扇门
ldoor1_x = lower_left_x + GAP
ldoor2_x = lower_left_x + LOWER_DOOR_WIDTH + GAP
draw_rect(doc, msp, (ldoor1_x, fy + BASEBOARD_HEIGHT), (ldoor1_x + LOWER_DOOR_WIDTH, lower_top), 'DOOR')
draw_rect(doc, msp, (ldoor2_x, fy + BASEBOARD_HEIGHT), (ldoor2_x + LOWER_DOOR_WIDTH, lower_top), 'DOOR')

# === 下部分右侧：2个抽屉 ===
drawer_x = lower_left_right + BOARD_THICKNESS + GAP
drawer_right = fx + OVERALL_WIDTH - BOARD_THICKNESS - GAP

# 上抽屉
draw_rect(doc, msp, (drawer_x, lower_top - DRAWER_HEIGHT), (drawer_right, lower_top), 'DRAWER')
# 下抽屉
draw_rect(doc, msp, (drawer_x, fy + BASEBOARD_HEIGHT + GAP), (drawer_right, fy + BASEBOARD_HEIGHT + DRAWER_HEIGHT), 'DRAWER')

# === 标注 ===
# 宽度标注（底部）
add_dimension_linear(doc, msp, (fx, fy), (fx + OVERALL_WIDTH, fy), -200, 'DIMENSION')

# 高度标注（右侧）
add_dimension_linear(doc, msp, (fx + OVERALL_WIDTH, fy), (fx + OVERALL_WIDTH, fy + OVERALL_HEIGHT), 200, 'DIMENSION')

# 踢脚线高度标注
add_dimension_linear(doc, msp, (fx, fy), (fx, fy + BASEBOARD_HEIGHT), -150, 'DIMENSION')

# 上门高度标注
add_dimension_linear(doc, msp, (fx, fy + BASEBOARD_HEIGHT), 
                     (fx, fy + BASEBOARD_HEIGHT + UPPER_DOOR_HEIGHT), -150, 'DIMENSION')

# 上门宽度标注
add_dimension_linear(doc, msp, (door1_x, upper_top), (door1_x + UPPER_DOOR_WIDTH, upper_top), 150, 'DIMENSION')

# 标题文字
add_text(doc, msp, '正立面图 (Front Elevation)', (fx + OVERALL_WIDTH/2 - 300, fy - 400), 30, 'TEXT')

# ==================== 侧立面图 (Side Elevation) ====================
sx, sy = OVERALL_WIDTH + 500, 0  # 侧立面图起点（在正立面图右侧）

# 外轮廓
draw_rect(doc, msp, (sx, sy), (sx + OVERALL_DEPTH, sy + OVERALL_HEIGHT), 'OUTLINE')

# 踢脚线
draw_line(doc, msp, (sx, sy + BASEBOARD_HEIGHT), (sx + OVERALL_DEPTH, sy + BASEBOARD_HEIGHT), 'BOARD')

# 标注
add_dimension_linear(doc, msp, (sx, sy), (sx + OVERALL_DEPTH, sy), -200, 'DIMENSION')
add_dimension_linear(doc, msp, (sx + OVERALL_DEPTH, sy), (sx + OVERALL_DEPTH, sy + OVERALL_HEIGHT), 200, 'DIMENSION')

# 标题文字
add_text(doc, msp, '侧立面图 (Side Elevation)', (sx + OVERALL_DEPTH/2 - 300, sy - 400), 30, 'TEXT')

# ==================== 平面图 (Plan View) ====================
px, py = 0, OVERALL_HEIGHT + 500  # 平面图起点（在正立面图上方）

# 外轮廓
draw_rect(doc, msp, (px, py), (px + OVERALL_WIDTH, py + OVERALL_DEPTH), 'OUTLINE')

# 左右侧板
draw_line(doc, msp, (px + BOARD_THICKNESS, py), (px + BOARD_THICKNESS, py + OVERALL_DEPTH), 'BOARD')
draw_line(doc, msp, (px + OVERALL_WIDTH - BOARD_THICKNESS, py), 
          (px + OVERALL_WIDTH - BOARD_THICKNESS, py + OVERALL_DEPTH), 'BOARD')

# 背板
draw_line(doc, msp, (px, py + OVERALL_DEPTH - BOARD_THICKNESS), 
          (px + OVERALL_WIDTH, py + OVERALL_DEPTH - BOARD_THICKNESS), 'BOARD')

# 中间隔板（对应正立面图的中间竖隔板）
draw_line(doc, msp, (px + OVERALL_WIDTH/2, py), (px + OVERALL_WIDTH/2, py + OVERALL_DEPTH), 'BOARD')

# 下部分的隔板
draw_line(doc, msp, (px + BOARD_THICKNESS + LOWER_LEFT_WIDTH, py), 
          (px + BOARD_THICKNESS + LOWER_LEFT_WIDTH, py + OVERALL_DEPTH), 'BOARD')

# 标注
add_dimension_linear(doc, msp, (px, py), (px + OVERALL_WIDTH, py), -200, 'DIMENSION')
add_dimension_linear(doc, msp, (px + OVERALL_WIDTH, py), (px + OVERALL_WIDTH, py + OVERALL_DEPTH), 200, 'DIMENSION')

# 标题文字
add_text(doc, msp, '平面图 (Plan View)', (px + OVERALL_WIDTH/2 - 250, py + OVERALL_DEPTH + 200), 30, 'TEXT')

# ==================== 尺寸说明文字 ====================
notes_x = OVERALL_WIDTH + 500
notes_y = OVERALL_HEIGHT + 500

add_text(doc, msp, '衣柜设计图 - 尺寸说明', (notes_x, notes_y), 35, 'TEXT')
add_text(doc, msp, f'总宽: {OVERALL_WIDTH}mm', (notes_x, notes_y - 60), 25, 'TEXT')
add_text(doc, msp, f'总深: {OVERALL_DEPTH}mm', (notes_x, notes_y - 100), 25, 'TEXT')
add_text(doc, msp, f'总高: {OVERALL_HEIGHT}mm', (notes_x, notes_y - 140), 25, 'TEXT')
add_text(doc, msp, f'板材厚度: {BOARD_THICKNESS}mm', (notes_x, notes_y - 180), 25, 'TEXT')
add_text(doc, msp, f'踢脚线厚度: {BASEBOARD_THICKNESS}mm', (notes_x, notes_y - 220), 25, 'TEXT')
add_text(doc, msp, f'门板间隙: {GAP}mm', (notes_x, notes_y - 260), 25, 'TEXT')

add_text(doc, msp, '结构说明:', (notes_x, notes_y - 340), 25, 'TEXT')
add_text(doc, msp, '- 上部分: 4扇长门 (对开两组)', (notes_x, notes_y - 380), 22, 'TEXT')
add_text(doc, msp, '- 下部分左侧: 2扇短门', (notes_x, notes_y - 415), 22, 'TEXT')
add_text(doc, msp, '- 下部分右侧: 2个抽屉', (notes_x, notes_y - 450), 22, 'TEXT')
add_text(doc, msp, '- 踢脚高度: 50mm', (notes_x, notes_y - 485), 22, 'TEXT')

# ==================== 保存文件 ====================
output_dir = r'D:\tokai'
output_file = os.path.join(output_dir, '衣柜设计图.dxf')
doc.saveas(output_file)
print(f'CAD图纸已生成: {output_file}')
print(f'文件大小: {os.path.getsize(output_file) / 1024:.1f} KB')
