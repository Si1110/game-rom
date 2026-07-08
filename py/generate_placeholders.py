#!/usr/bin/env python3
"""
为缺封面的游戏生成主题占位图。
按平台配色，包含游戏名称居中显示、平台徽章、装饰元素。
"""
import json
import math
import os
import re
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL = os.path.join(ROOT, 'res', 'merged.xlsx')
COVERS = os.path.join(ROOT, 'res', 'covers')

PLATFORM_COLORS = {
    'GBA':      [(0x1a, 0x23, 0x7e), (0x0d, 0x47, 0xa1)],
    'FC/NES':   [(0xb7, 0x1c, 0x1c), (0xc6, 0x28, 0x28)],
    'FC':       [(0xb7, 0x1c, 0x1c), (0xc6, 0x28, 0x28)],
    'SFC/SNES': [(0x4a, 0x14, 0x8c), (0x6a, 0x1b, 0x9a)],
    'SFC':      [(0x4a, 0x14, 0x8c), (0x6a, 0x1b, 0x9a)],
    'NDS':      [(0x00, 0x4d, 0x40), (0x00, 0x69, 0x5c)],
    'N64':      [(0xe6, 0x51, 0x00), (0xef, 0x6c, 0x00)],
    'GBC/GB':   [(0x1b, 0x5e, 0x20), (0x2e, 0x7d, 0x32)],
    '3DS':      [(0x1a, 0x23, 0x7e), (0x28, 0x35, 0x93)],
    'PS1':      [(0x00, 0x4d, 0x40), (0x00, 0x69, 0x5c)],
    'PS2':      [(0x1a, 0x23, 0x7e), (0x0d, 0x47, 0xa1)],
    'PS3':      [(0x1a, 0x23, 0x7e), (0x0d, 0x47, 0xa1)],
    'PSP':      [(0x3e, 0x27, 0x23), (0x4e, 0x34, 0x2e)],
    'WII':      [(0xe6, 0x51, 0x00), (0xef, 0x6c, 0x00)],
    'NGC':      [(0x4a, 0x14, 0x8c), (0x6a, 0x1b, 0x9a)],
    'MD':       [(0x4a, 0x00, 0x00), (0x7f, 0x00, 0x00)],
    'DOS':      [(0x3e, 0x27, 0x23), (0x4e, 0x34, 0x2e)],
    '街机':     [(0xf5, 0x7f, 0x17), (0xf9, 0xa8, 0x25)],
}

PLATFORM_BADGE = {
    'GBA': 'GBA',
    'FC/NES': 'FC / NES',
    'FC': 'FC / NES',
    'SFC/SNES': 'SFC / SNES',
    'SFC': 'SFC / SNES',
    'NDS': 'NINTENDO DS',
    'N64': 'NINTENDO 64',
    'GBC/GB': 'GAME BOY',
    '3DS': 'NINTENDO 3DS',
    'PS1': 'PLAYSTATION',
    'PS2': 'PLAYSTATION 2',
    'PS3': 'PLAYSTATION 3',
    'PSP': 'PSP',
    'WII': 'WII',
    'NGC': 'GAMECUBE',
    'MD': 'MEGA DRIVE',
    'DOS': 'DOS',
    '街机': 'ARCADE',
}

W, H = 400, 560


def get_colors(plat):
    for key, colors in PLATFORM_COLORS.items():
        if key in plat or plat in key:
            return colors
    return [(0x33, 0x33, 0x33), (0x55, 0x55, 0x55)]


def get_badge(plat):
    for key, badge in PLATFORM_BADGE.items():
        if key in plat or plat in key:
            return badge
    return plat.upper()


def find_font(size):
    candidates = [
        'C:/Windows/Fonts/msyh.ttf',
        'C:/Windows/Fonts/msyhbd.ttf',
        'C:/Windows/Fonts/simhei.ttf',
        'C:/Windows/Fonts/arial.ttf',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_gradient(draw, colors):
    c1, c2 = colors
    for y in range(H):
        r = int(c1[0] + (c2[0] - c1[0]) * y / H)
        g = int(c1[1] + (c2[1] - c1[1]) * y / H)
        b = int(c1[2] + (c2[2] - c1[2]) * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))


def draw_stars(draw):
    import random
    random.seed(42)
    for _ in range(60):
        x = random.randint(0, W)
        y = random.randint(0, H)
        s = random.randint(1, 3)
        alpha = random.randint(30, 100)
        draw.ellipse([x, y, x + s, y + s], fill=(255, 255, 255, alpha))


def draw_decorative_bar(draw, colors):
    c1, c2 = colors
    mid_c = ((c1[0] + c2[0]) // 2, (c1[1] + c2[1]) // 2, (c1[2] + c2[2]) // 2)
    bar_h = 8
    bar_y = H - 80
    for x in range(W):
        r = max(0, min(255, mid_c[0] + int(math.sin(x * 0.05) * 20)))
        g = max(0, min(255, mid_c[1] + int(math.sin(x * 0.05 + 1) * 20)))
        b = max(0, min(255, mid_c[2] + int(math.sin(x * 0.05 + 2) * 20)))
        draw.line([(x, bar_y), (x, bar_y + bar_h)], fill=(r, g, b))


def draw_controller_icon(draw):
    cx, cy = W // 2, H // 2 - 40
    outline = (255, 255, 255, 40)
    # Simple controller shape
    draw.rounded_rectangle([cx - 60, cy - 20, cx + 60, cy + 20], radius=30, outline=outline, width=3)
    draw.rounded_rectangle([cx - 80, cy - 12, cx - 55, cy + 12], radius=8, fill=outline)
    draw.rounded_rectangle([cx + 55, cy - 12, cx + 80, cy + 12], radius=8, fill=outline)
    draw.ellipse([cx - 18, cy - 18, cx - 4, cy - 4], fill=outline)
    draw.ellipse([cx + 4, cy - 18, cx + 18, cy - 4], fill=outline)
    draw.ellipse([cx - 18, cy + 4, cx - 4, cy + 18], fill=outline)
    draw.ellipse([cx + 4, cy + 4, cx + 18, cy + 18], fill=outline)


def generate_placeholder(name, plat, output_path):
    colors = get_colors(plat)
    badge = get_badge(plat)

    img = Image.new('RGBA', (W, H))
    draw = ImageDraw.Draw(img)

    # 1. Gradient background
    draw_gradient(draw, colors)

    # 2. Stars decoration
    draw_stars(draw)

    # 3. Controller icon
    draw_controller_icon(draw)

    # 4. Colored decorative bar
    draw_decorative_bar(draw, colors)

    # 5. Platform badge (top)
    font_badge = find_font(24)
    bbox = draw.textbbox((0, 0), badge, font=font_badge)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 30), badge, fill=(255, 255, 255, 60), font=font_badge)

    # 6. Game name (center)
    font_name = find_font(28)
    max_w = W - 40
    # Wrap text manually
    lines = []
    current = ''
    for ch in name:
        test = current + ch
        bbox = draw.textbbox((0, 0), test, font=font_name)
        if bbox[2] - bbox[0] > max_w and current:
            lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)

    if len(lines) > 5:
        lines = lines[:5]
        lines[-1] = lines[-1][:-3] + '...'

    line_h = 40
    start_y = H // 2 - len(lines) * line_h // 2 + 60
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_name)
        tw = bbox[2] - bbox[0]
        # Shadow
        draw.text(((W - tw) // 2 + 2, start_y + i * line_h + 2), line,
                  fill=(0, 0, 0, 100), font=font_name)
        draw.text(((W - tw) // 2, start_y + i * line_h), line,
                  fill=(255, 255, 255, 230), font=font_name)

    # 7. Bottom bar accent
    bar_y = H - 40
    for x in range(W):
        r = max(0, min(255, colors[0][0] + int(math.sin(x * 0.03) * 15)))
        g = max(0, min(255, colors[0][1] + int(math.sin(x * 0.03 + 1) * 15)))
        b = max(0, min(255, colors[0][2] + int(math.sin(x * 0.03 + 2) * 15)))
        draw.line([(x, bar_y), (x, bar_y + 4)], fill=(r, g, b, 120))

    img.save(output_path, 'PNG')


def main():
    from openpyxl import load_workbook
    safe_cache = {}

    def get_safe(name):
        if name not in safe_cache:
            safe_cache[name] = re.sub(r'[\\/:*?"<>|]', '_', name)
        return safe_cache[name]

    print("Reading merged.xlsx...")
    wb = load_workbook(EXCEL, read_only=True)
    to_generate = []

    for sname in wb.sheetnames:
        if sname == '主目录':
            continue
        ws = wb[sname]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row or len(row) < 2:
                continue
            cover = str(row[0] or '').strip() if row[0] else ''
            name = str(row[1] or '').strip() if row[1] else ''
            plat = str(row[4] or '').strip() if len(row) > 4 and row[4] else '未知'
            if not name:
                continue
            if not cover or 'placeholder' in cover:
                safe = get_safe(name)
                fpath = os.path.join(COVERS, f'{safe}.png')
                to_generate.append((name, plat, fpath))

    wb.close()
    print(f"Need placeholders: {len(to_generate)}")

    generated = 0
    for i, (name, plat, fpath) in enumerate(to_generate, 1):
        if os.path.exists(fpath) and os.path.getsize(fpath) > 2000:
            continue
        generate_placeholder(name, plat, fpath)
        generated += 1
        if generated % 100 == 0:
            print(f"  Generated {generated}/{len(to_generate)}...", flush=True)

    print(f"\nDone! Generated {generated} placeholder covers.")
    print(f"Remaining still missing: {len(to_generate) - generated}")


if __name__ == '__main__':
    main()
