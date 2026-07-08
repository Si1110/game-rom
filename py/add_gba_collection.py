#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add GBA Pokemon ROM hack collection to the Excel and generate supporting files.
"""
import os
import sys
from openpyxl import load_workbook

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL = os.path.join(ROOT, 'res', 'merged.xlsx')
COVERS_DIR = os.path.join(ROOT, 'res', 'covers')

QUARK_LINK = 'https://pan.quark.cn/s/9db8573476c6'

def get_rom_files():
    """Get all GBA ROM files organized by category."""
    folder = 'G:/游戏/1宝可梦/GBA宝可梦改版合集'
    if not os.path.exists(folder):
        print(f'ERROR: Folder not found: {folder}')
        return None, 0
    
    files = sorted([f for f in os.listdir(folder) if f.endswith('.gba')])
    categories = {}
    for f in files:
        if '红宝石' in f:
            cat = '红宝石系列改版'
        elif '火红' in f:
            cat = '火红系列改版'
        elif '蓝宝石' in f:
            cat = '蓝宝石系列改版'
        elif '绿宝石' in f:
            cat = '绿宝石系列改版'
        elif '叶绿' in f:
            cat = '叶绿系列改版'
        else:
            cat = '其他改版'
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(f)
    
    return categories, len(files)

def generate_modal_html(categories, total):
    """Generate HTML for directory modal."""
    lines = []
    lines.append('<div class="container" style="max-height: 70vh; overflow-y: auto;">')
    lines.append(f'<h5>GBA宝可梦改版合集目录 <span class="badge bg-primary">共{total}款</span></h5>')
    lines.append('<hr>')
    for cat in ['红宝石系列改版', '火红系列改版', '蓝宝石系列改版', '绿宝石系列改版', '叶绿系列改版', '其他改版']:
        flist = categories.get(cat, [])
        if not flist:
            continue
        lines.append(f'<h6 class="mt-3">📁 {cat} <span class="badge bg-secondary">{len(flist)}款</span></h6>')
        lines.append('<div style="max-height: 250px; overflow-y: auto; border: 1px solid #dee2e6; padding: 8px; border-radius: 4px; background: #f8f9fa;">')
        lines.append('<ol style="font-size: 0.85em; margin-bottom: 0; padding-left: 1.5em;">')
        for f in flist:
            # Escape HTML
            safe_f = f.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            lines.append(f'  <li>{safe_f}</li>')
        lines.append('</ol>')
        lines.append('</div>')
    lines.append('</div>')
    return '\n'.join(lines)

def insert_into_excel(description):
    """Insert collection as first row in 宝可梦系列 sheet."""
    print(f'Reading Excel: {EXCEL}')
    wb = load_workbook(EXCEL)
    
    if '宝可梦系列' not in wb.sheetnames:
        print('ERROR: 宝可梦系列 sheet not found')
        return False
    
    ws = wb['宝可梦系列']
    
    # Insert row at position 2 (after header)
    # openpyxl doesn't have direct insert, so we shift down
    ws.insert_rows(2)
    
    # Set the collection data
    ws.cell(row=2, column=1, value='../res/covers/GBA宝可梦改版合集.png')
    ws.cell(row=2, column=2, value='GBA宝可梦改版合集')
    ws.cell(row=2, column=3, value=description)
    ws.cell(row=2, column=4, value='中文/英文')
    ws.cell(row=2, column=5, value='GBA')
    ws.cell(row=2, column=6, value='2024')
    ws.cell(row=2, column=7, value=QUARK_LINK)
    
    wb.save(EXCEL)
    print(f'Inserted collection as first entry in 宝可梦系列 sheet')
    return True

def main():
    print('=' * 60)
    print('Add GBA Pokemon ROM Hack Collection')
    print('=' * 60)
    
    # Step 1: Get ROM files
    print('\n[Step 1] Reading ROM files...')
    categories, total = get_rom_files()
    if categories is None:
        sys.exit(1)
    print(f'  Found {total} ROM files in {len(categories)} categories')
    for cat, flist in categories.items():
        print(f'    {cat}: {len(flist)}')
    
    # Step 2: Generate modal HTML
    print('\n[Step 2] Generating directory modal HTML...')
    modal_html = generate_modal_html(categories, total)
    
    modal_path = os.path.join(ROOT, 'docs', 'gba-collection-dir-modal.html')
    with open(modal_path, 'w', encoding='utf-8') as f:
        f.write(modal_html)
    print(f'  Written to: {modal_path}')
    
    # Step 3: Write ~200 word description
    print('\n[Step 3] Writing description...')
    description = (
        f'本合集收录了多达{total}款GBA平台宝可梦改版游戏，'
        f'涵盖火红、绿宝石、红宝石、蓝宝石、叶绿等五大基础ROM的改版作品。'
        f'包含命运红宝石系列、白金光系列、究极绿宝石系列、'
        f'漆黑的魅影系列、梦的光点系列、'
        f'液体水晶、圣灰、盖亚、激进红、无界等众多经典改版，'
        f'以及剑盾GBA版、融合维度、龙珠Z等跨界改版。'
        f'此外还收录了东方人形剧、萌娘火红、宝可梦女孩猎人等特殊主题改版，'
        f'以及日文、英文、西班牙语、意大利语等多语言版本。'
        f'无论是剧情向、难度向、美化向还是恶搞向的改版，'
        f'本合集都一网打尽，是宝可梦GBA改版爱好者不可错过的收藏宝库。'
        f'所有ROM均为.gba格式，下载后可直接在GBA模拟器上运行。'
    )
    print(f'  Description ({len(description)} chars):')
    print(f'  {description}')
    
    # Step 4: Insert into Excel
    print('\n[Step 4] Inserting into Excel...')
    if insert_into_excel(description):
        print('  Success!')
    else:
        print('  Failed!')
        sys.exit(1)
    
    # Step 5: Generate directory text file
    print('\n[Step 5] Generating directory text file...')
    dir_lines = []
    dir_lines.append(f'GBA宝可梦改版合集目录 (共{total}款)')
    dir_lines.append('=' * 50)
    for cat in ['红宝石系列改版', '火红系列改版', '蓝宝石系列改版', '绿宝石系列改版', '叶绿系列改版', '其他改版']:
        flist = categories.get(cat, [])
        if not flist:
            continue
        dir_lines.append(f'\n【{cat}】共{len(flist)}款')
        for f in flist:
            dir_lines.append(f'  {f}')
    
    dir_path = os.path.join(ROOT, 'docs', 'gba-collection-directory.txt')
    with open(dir_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(dir_lines))
    print(f'  Written to: {dir_path}')
    
    print('\n' + '=' * 60)
    print('Done! Now:')
    print('  1. Find/download a cover image as res/covers/GBA宝可梦改版合集.png')
    print('  2. Modify generate_game_site.py to add directory button')
    print('  3. Run python py/generate_game_site.py')
    print('=' * 60)

if __name__ == '__main__':
    main()
