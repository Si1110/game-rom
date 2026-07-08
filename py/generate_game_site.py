#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate game ROM website from merged Excel.
Output: index.html, sections/section-XX.html, sitemap.xml
Updates: docs/js/seo-meta.js, docs/js/global-search.js, docs/js/count-badges.js, res/README.md
"""

import os, re, random, string, shutil
from datetime import datetime
from openpyxl import load_workbook
from jinja2 import Template

CHARSET = 'utf-8'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL = os.path.join(ROOT, 'res', 'merged.xlsx')
for alt in [os.path.join(ROOT, r'..\游戏文件夹\游戏合集整理_整合版.xlsx'), r'G:\游戏文件夹\游戏合集整理_整合版.xlsx']:
    if not os.path.exists(EXCEL) and os.path.exists(alt):
        EXCEL = alt

TEMPLATE_SECTION = os.path.join(ROOT, 'templates', 'section-tpl.html')
TEMPLATE_PLATFORM = os.path.join(ROOT, 'templates', 'platform-tpl.html')
TEMPLATE_CARD = os.path.join(ROOT, 'templates', 'card-tpl.html')
TEMPLATE_INDEX = os.path.join(ROOT, 'templates', 'index-tpl.html')
TEMPLATE_COVER = os.path.join(ROOT, 'templates', 'cover-tpl.html')
TEMPLATE_SITEMAP = os.path.join(ROOT, 'templates', 'sitemap-tpl.html')
TEMPLATE_LINK = os.path.join(ROOT, 'templates', 'link-tpl.html')
OUTPUT_SECTIONS = os.path.join(ROOT, 'sections')
OUTPUT_PLATFORMS = os.path.join(ROOT, 'platforms')
OUTPUT_INDEX = os.path.join(ROOT, 'index.html')
OUTPUT_SITEMAP = os.path.join(ROOT, 'sitemap.xml')
RES_COVERS = os.path.join(ROOT, 'res', 'covers')

INDEX_TITLE = '🎮 经典怀旧游戏 ROM 合集 🎮'
SITE_TITLE = '26000+款怀旧游戏ROM合集 - GBA/FC/SFC/N64/NDS/PS中文版下载'

SEO_TITLE = '26000+款怀旧游戏ROM合集 - GBA/FC/SFC/N64/NDS/PS中文版下载'
SEO_DESCRIPTION = '26000+款经典怀旧游戏ROM中文版合集，涵盖GBA/FC/SFC/N64/NDS/PS1/PS2/PS3/WII等全平台，含宝可梦、马里奥、塞尔达传说、最终幻想等系列中文汉化版，支持模拟器运行。'
SEO_KEYWORDS = '怀旧游戏,经典游戏,ROM下载,中文ROM,中文汉化版,GBA游戏,FC游戏,SFC游戏,GBC游戏,N64游戏,NDS游戏,3DS游戏,PS2游戏,PS3游戏,PS1游戏,PSP游戏,WII游戏,宝可梦,精灵宝可梦,超级马里奥,马里奥,塞尔达传说,塞尔达,最终幻想,洛克人,热血系列,魂斗罗,龙珠,火焰纹章,恶魔城,高达,游戏王,牧场物语,星之卡比,逆转裁判,合金弹头,索尼克,高级战争,火影忍者,拳皇,超级机器人大战,黄金太阳,银河战士,节奏天国,F-Zero,任天堂,红白机,GameBoy,GameBoyAdvance,超级任天堂,GBA模拟器,FC模拟器,SFC模拟器,童年游戏,80后游戏,90后游戏,老游戏,复古游戏,模拟器游戏,汉化游戏,游戏ROM合集,怀旧游戏大全,模拟器中文版ROM'
SEO_AUTHOR = 'Game ROM Collection'
SEO_SITE_NAME = '经典怀旧游戏 ROM 合集'
SEO_DOMAIN = 'https://si1110.github.io/game-rom/'
SEO_IMAGE = 'https://si1110.github.io/game-rom/docs/logo.png'

# Platform categories for 热门游戏模拟器
PLATFORM_CATEGORIES = [
    # (key_in_excel, label, icon_emoji, slug)
    ('FC/NES', 'FC红白机', '🎮', 'fc'),
    ('SFC/SNES', 'SFC超任', '🕹️', 'sfc'),
    ('GBA', 'GBA掌机', '📟', 'gba'),
    ('街机', '街机', '💰', 'arcade'),
    ('GBC/GB', 'Game Boy', '🎯', 'gb'),
    ('3DS', '3DS掌机', '📱', '3ds'),
    ('N64', 'N64主机', '🔷', 'n64'),
    ('MD', '世嘉MD', '⚡', 'md'),
    ('PCE', 'PC Engine', '💿', 'pce'),
    ('NGP', 'Neo Geo Pocket', '🕹️', 'ngp'),
    ('WS+WSC', 'WonderSwan', '📱', 'ws'),
    ('NDS', 'NDS掌机', '📱', 'nds'),
    ('HAK', 'Hack合集', '🔧', 'hack'),
    ('PS2', 'PS2游戏', '🎮', 'ps2'),
    ('PS3', 'PS3游戏', '🎮', 'ps3'),
    ('PS1', 'PS1游戏', '🎮', 'ps1'),
    ('PSP', 'PSP游戏', '🎮', 'psp'),
    ('WII', 'WII游戏', '🎮', 'wii'),
    ('NGC', 'NGC游戏', '🎮', 'ngc'),
    ('DOS', 'DOS游戏', '💻', 'dos'),
]

# Platform -> slug mapping for sidebar links
PLATFORM_SLUG_MAP = {key: slug for key, _, _, slug in PLATFORM_CATEGORIES}

SERIES_DESC_MAP = {
    '马里奥系列': '马里奥系列经典游戏ROM中文版下载，包含超级马里奥、马里奥赛车等全系列作品，支持GBA/FC/SFC模拟器运行',
    '宝可梦系列': '宝可梦系列经典游戏ROM中文版下载，包含宝可梦红宝石、蓝宝石、火红、叶绿、心金、魂银等全系列中文汉化版',
    '塞尔达传说系列': '塞尔达传说系列游戏ROM中文版下载，包含缩小帽、时之笛、梦见岛、众神的三角力量等经典作品，支持GBA/N64/SFC/Wii模拟器',
    '最终幻想系列': '最终幻想系列游戏ROM中文版下载，包含FF1-6代等经典日式RPG作品，支持GBA/FC/SFC模拟器',
    '勇者斗恶龙系列': '勇者斗恶龙系列游戏ROM中文版下载，包含DQ1-9代经典日式RPG中文汉化版',
    '魂斗罗系列': '魂斗罗系列游戏ROM中文版下载，包含经典FC魂斗罗、超级魂斗罗等横版射击游戏',
    '恶魔城系列': '恶魔城系列游戏ROM中文版下载，包含月下夜想曲、晓月圆舞曲等动作冒险经典',
    '洛克人系列': '洛克人系列游戏ROM中文版下载，包含洛克人X、EXE、Zero等全系列动作游戏',
    '龙珠系列': '龙珠系列游戏ROM中文版下载，包含龙珠Z、龙珠大冒险等动漫改编格斗游戏',
    '火焰纹章系列': '火焰纹章系列游戏ROM中文版下载，包含烈火之剑、圣魔之光石等经典战棋RPG',
    '高达系列': '高达系列游戏ROM中文版下载，包含SD高达、机动战士高达等机器人战棋游戏',
    '拳皇系列': '拳皇系列游戏ROM中文版下载，包含拳皇97、98、99等经典格斗游戏ROM',
    '合金弹头系列': '合金弹头系列游戏ROM中文版下载，包含合金弹头1-6代经典横版射击游戏',
    '传说系列': '传说系列游戏ROM中文版下载，包含幻想传说、永恒传说等经典日式RPG',
    '游戏王系列': '游戏王系列游戏ROM中文版下载，包含游戏王决斗怪兽等经典卡牌对战游戏',
    '星之卡比系列': '星之卡比系列游戏ROM中文版下载，包含星之卡比梦之泉等可爱风格动作游戏',
    '牧场物语系列': '牧场物语系列游戏ROM中文版下载，包含矿石镇、双子村等模拟经营经典',
    '超级机器人大战系列': '超级机器人大战系列ROM中文版下载，包含机战A/R/D/J/OG等战棋游戏',
    '银河战士系列': '银河战士系列游戏ROM中文版下载，包含融合、零点任务等经典动作冒险游戏',
    '索尼克系列': '索尼克系列游戏ROM中文版下载，蓝色刺猬的高速平台跳跃动作游戏',
    '火影忍者系列': '火影忍者系列游戏ROM中文版下载，火影忍者动漫改编格斗动作游戏',
    '真女神转生系列': '真女神转生系列游戏ROM中文版下载，包含真女神转生、恶魔召唤师等RPG',
    '魔法系列': '魔法系列经典游戏ROM中文版下载合集，包含魔法气泡、魔法门等经典魔法题材游戏',
    '逆转裁判系列': '逆转裁判系列游戏ROM中文版下载，包含逆转裁判1-3部法庭推理经典',
    '黄金太阳系列': '黄金太阳系列游戏ROM中文版下载，GBA平台最佳日式RPG系列中文汉化版',
    '我们的太阳系列': '我们的太阳系列游戏ROM中文版下载，结合阳光传感器的独特动作RPG',
    '高级战争系列': '高级战争系列游戏ROM中文版下载，任天堂经典战棋策略游戏中文版',
    '鬼武者系列': '鬼武者系列游戏ROM中文版下载，包含鬼武者战略版等动作策略游戏',
    '光明之魂系列': '光明之魂系列游戏ROM中文版下载，GBA平台经典暗黑Like动作RPG',
    '侦探系列': '侦探系列经典游戏ROM中文版下载合集，包含侦探解密、悬疑推理等经典侦探题材游戏',
    '热血系列': '热血系列游戏ROM中文版下载，包含热血足球、篮球、格斗等热血硬派经典',
    '蜡笔小新系列': '蜡笔小新系列游戏ROM中文版下载，动漫改编休闲游戏合集',
    '网球王子系列': '网球王子系列游戏ROM中文版下载，动漫改编网球竞技游戏',
    '瓦力欧系列': '瓦力欧系列游戏ROM中文版下载，包含瓦力欧制造等创意动作游戏',
    '马力欧系列': '马力欧系列游戏ROM中文版下载，包含超级马里奥世界等经典平台跳跃游戏',
    '召唤之夜系列': '召唤之夜系列游戏ROM中文版下载，包含铸剑物语等经典日式RPG',
    '任天堂明星大乱斗系列': '任天堂明星大乱斗游戏ROM下载，任天堂全明星跨平台格斗游戏',
    'F-Zero系列': 'F-Zero系列游戏ROM中文版下载，任天堂经典高速赛车游戏',
    '星际火狐系列': '星际火狐系列游戏ROM中文版下载，任天堂经典空战射击游戏',
    '耀西系列': '耀西系列游戏ROM中文版下载，包含耀西岛等可爱风格平台跳跃游戏',
    '动物森林系列': '动物森友会系列游戏ROM中文版下载，任天堂治愈系模拟经营游戏',
    '水上摩托系列': '水上摩托系列游戏ROM中文版下载，任天堂经典水上竞速游戏',
    '越野摩托系列': '越野摩托系列游戏ROM中文版下载，经典摩托车竞速游戏合集',
    '组合机器人系列': '组合机器人系列游戏ROM中文版下载合集，创意合体机器人动作游戏',
    'CT特种部队系列': 'CT特种部队系列游戏ROM中文版下载合集，经典战术动作游戏',
    'FC红白机系列': 'FC红白机系列经典怀旧游戏ROM中文版下载，包含2700+款经典FC/NES游戏中文汉化版',
    'GBA系列': 'GBA系列经典游戏ROM中文版下载，包含4400+款GBA掌机游戏中文汉化版',
    'N64系列': 'N64系列经典游戏ROM中文版下载，包含400款N64主机游戏中文汉化版',
    'NDS系列': 'NDS系列经典游戏ROM中文版下载，包含5200款NDS掌机游戏中文汉化版',
    'SFC超任系列': 'SFC超任系列经典游戏ROM中文版下载，包含3000+款SFC超任游戏中文汉化版',
    '其他游戏精选': '其他游戏精选经典游戏ROM合集，包含各平台精选怀旧游戏中文版',
    '节奏天国系列': '节奏天国系列游戏ROM中文版下载，任天堂创意音乐节奏游戏',
    '罪与罚系列': '罪与罚系列游戏ROM中文版下载，N64平台经典动作射击游戏',
    '决战三国系列': '决战三国系列游戏ROM中文版下载，三国题材策略战棋游戏合集',
    '街机系列': '街机系列经典游戏ROM中文版下载，包含街机、CPS1、CPS2、NEOGEO等经典街机游戏中文汉化版',
    '其他游戏': '更多经典怀旧游戏ROM合集，包含各平台未分类经典游戏中文汉化版',
}

def badge_for_platform(pf):
    """Generate format badge for a platform string."""
    pf_clean = pf.strip().upper().replace('/', '_').replace(' ', '_')
    color_map = {
        'GBA': 'blue', 'GBC': 'green', 'GB': 'green',
        'FC': 'red', 'NES': 'red', 'SFC': 'purple', 'SNES': 'purple',
        'N64': 'orange', 'PS2': 'blue', 'PS3': 'blue',
        'PS1': 'blue', 'PSP': 'yellow', 'WII': 'red',
        'NGC': 'purple', 'DOS': 'gray'
    }
    color = 'gray'
    for k, v in color_map.items():
        if k in pf_clean:
            color = v
            break
    return f'<img src="https://img.shields.io/badge/{pf_clean}-Yes-{color}.svg" data-bs-toggle="tooltip" title="{pf.strip()} 平台 ROM 文件">'

def load_excel(path):
    """Load Excel, return list of (sheet_name, [game_dict, ...])."""
    wb = load_workbook(path, data_only=True)
    result = []
    for sname in wb.sheetnames:
        if sname == '主目录':
            continue
        ws = wb[sname]
        games = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            vals = list(row)
            if vals[1] is None:
                continue
            cover = str(vals[0] or '').strip().replace('\\', '/')
            name = str(vals[1] or '').strip()
            desc = str(vals[2] or '').strip()
            lang = str(vals[3] or '').strip()
            plat = str(vals[4] or '').strip()
            year = str(vals[5] or '').strip()
            link = str(vals[6] or '').strip()
            if not name:
                continue
            games.append({
                'cover': cover, 'name': name, 'desc': desc,
                'lang': lang, 'plat': plat, 'year': year, 'link': link
            })
        if games:
            # Dedup within series: remove exact duplicates (same name + link + desc)
            seen = set()
            deduped = []
            for g in games:
                key = (g['name'], g['link'], g['desc'][:50])
                if key not in seen:
                    seen.add(key)
                    deduped.append(g)
            if len(deduped) < len(games):
                print(f'  Dedup {sname}: removed {len(games) - len(deduped)} duplicates')
            result.append((sname, deduped))
    return result

PLACEHOLDER = '../res/covers/placeholder.png'
COVER_DIR = os.path.join(ROOT, 'res', 'covers')

def resolve_cover(rel_path):
    """Return the cover path if file exists, else placeholder."""
    if not rel_path or rel_path == 'None':
        return PLACEHOLDER
    fname = os.path.basename(rel_path.replace('\\', '/'))
    full = os.path.join(COVER_DIR, fname)
    if os.path.exists(full):
        return rel_path.replace('\\', '/')
    return PLACEHOLDER

def extract_pwd(link):
    """Extract pwd parameter from Baidu link."""
    if '?pwd=' in link:
        return link.split('?pwd=')[-1].split('&')[0]
    return '0000'

def label_source(link):
    """Label the download source: 百度网盘 / 夸克网盘 / 直链"""
    if not link:
        return ''
    if 'pan.baidu.com' in link:
        return '百度网盘'
    if 'pan.quark.cn' in link:
        return '夸克网盘'
    return '直链'

def make_card_html(game, dup_label=''):
    """Generate a single game card HTML."""
    cover = resolve_cover(game['cover'])
    pwd = extract_pwd(game['link'])
    badges = badge_for_platform(game['plat'])
    year = game['year'] if game['year'] and game['year'] != '未知' else '未知'
    is_collection = (game['name'] == 'GBA宝可梦改版合集')
    btn_label = '[点此下载]'
    download_btn = f'<button type="button" class="btn button-link" data-bs-toggle="modal" data-bs-target="#downloadModal" data-bs-download="{game["link"]}" data-uuid="{pwd}">{btn_label}</button>'
    if is_collection:
        download_btn += ' <button type="button" class="btn button-link" data-bs-toggle="modal" data-bs-target="#collectionDirModal">[📋 目录]</button>'
    desc = game['desc']
    desc_btn = ''
    if len(desc) > 100:
        desc_btn = '<button class="btn btn-sm btn-link desc-toggle p-0" onclick="toggleDesc(this)">展开 ▾</button>'
    label_html = f'<span class="badge bg-info ms-2">{dup_label}</span>' if dup_label else ''
    source = label_source(game['link'])
    source_html = f'<span class="badge bg-secondary ms-1">{source}</span>' if source else ''
    return f'''        <div class="col-sm-12 col-md-6 col-lg-4">
          <div class="card mb-3 bold-border" style="max-width: 540px;">
            <div class="row g-0">
              <div class="col-md-4">
                <a href="{cover}" target="_blank">
                  <img src="{cover}" class="card-img" alt="{game['name']} ROM 中文汉化版 封面">
                </a>
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h4 class="card-title">{game['name']}{label_html}{source_html}</h4>
                  <ul class="list-group">
                    <li class="list-group-item list-group-item-primary"><div class="desc-collapse">{desc}</div>{desc_btn}</li>
                    <li class="list-group-item list-group-item-success">语言：{game['lang']}</li>
                    <li class="list-group-item list-group-item-info">平台：{game['plat']}</li>
                    <li class="list-group-item list-group-item-danger">下载：
                      {download_btn}
                    </li>
                    <li class="list-group-item list-group-item-warning">
                      {badges}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <small class="text-muted">发行年份：{year}</small>
            </div>
          </div>
        </div>'''

def make_cover_card(sname, idx, game_count, first_cover, platforms=None):
    """Generate a series cover card for the index page."""
    if platforms is None:
        platforms = []
    desc_map = {
        '宝可梦系列': '精灵宝可梦全系列中文版，包含GBA/GBC等多平台作品',
        '马力欧系列': '超级马力欧全系列中文版，横版跳跃经典',
        '传说系列': '包含塞尔达传说、火焰之纹章等经典RPG系列',
        '格斗系列': '热血系列、拳皇等经典格斗游戏',
        '其他游戏': '其他未分类的经典怀旧游戏合集',
    }
    desc = desc_map.get(sname, f'{sname}经典游戏合集')
    cover = resolve_cover(first_cover) if first_cover else PLACEHOLDER
    tags_html = ''
    if platforms:
        badges = ' '.join(f'<span class="badge bg-secondary me-1">{p}</span>' for p in platforms[:3])
        tags_html = f'<div class="text-muted small">{badges}</div>'
    return f'''              <div class="col-sm-12 col-md-6 col-lg-4 mb-4">
                  <a href="./sections/section-{idx:02d}.html" class="section-card">
                      <div class="card h-100">
                          <img src="{cover}" class="card-img-top" alt="{sname} 经典怀旧游戏 ROM 合集封面" style="height: 200px; object-fit: cover;">
                          <div class="card-body">
                              <span class="section-badge">{game_count} 款</span>
                              <h4 class="card-title">{sname}</h4>
                              <p class="card-text">{desc}</p>
                              {tags_html}
                          </div>
                      </div>
                  </a>
              </div>'''

def make_quick_nav(sections_info, current_idx=None):
    """Generate floating sidebar directory HTML. current_idx=None for index."""
    links_html = ''
    for sname, idx, cnt, _ in sections_info:
        active = ' class="nav-link-item active"' if current_idx == idx else ' class="nav-link-item"'
        href = f'../sections/section-{idx:02d}.html' if current_idx else f'./sections/section-{idx:02d}.html'
        safe_name = sname.replace("'", "&#39;")
        links_html += f'            <a{active} href="{href}"><span>{safe_name}</span><span class="nav-count-badge">{cnt}</span></a>\n'
    return f'''    <!-- 系列目录悬浮侧栏 -->
    <div class="quick-nav" id="quickNav">
        <div class="quick-nav-title">📂 系列目录</div>
        <div class="nav-links" id="navLinks">
{links_html}        </div>
    </div>'''

EMULATOR_MAP = [
    ('FC/NES', '红白机', '🎮'),
    ('SFC/SNES', '超任', '🕹️'),
    ('GBA', 'GBA掌机', '📟'),
    ('街机', '街机', '💰'),
    ('GBC/GB', 'Game Boy', '🎯'),
    ('N64', 'N64主机', '🔷'),
    ('MD', '世嘉MD', '⚡'),
    ('PCE', 'PC Engine', '💿'),
    ('NGP', 'Neo Geo Pocket', '🕹️'),
    ('WS+WSC', 'WonderSwan', '📱'),
    ('HAK', 'Hack合集', '🔧'),
    ('NDS', 'NDS掌机', '📱'),
    ('3DS', '3DS掌机', '📱'),
    ('PS2', 'PS2游戏', '🎮'),
    ('PS3', 'PS3游戏', '🎮'),
    ('PS1', 'PS1游戏', '🎮'),
    ('PSP', 'PSP游戏', '🎮'),
    ('WII', 'WII游戏', '🎮'),
    ('NGC', 'NGC游戏', '🎮'),
    ('DOS', 'DOS游戏', '💻'),
]

def make_emulator_sidebar(all_games, prefix='.'):
    """Generate 热门游戏模拟器 sidebar HTML from all games list."""
    from collections import Counter
    emu_counts = Counter()
    for g in all_games:
        pf = g['plat'].strip()
        if pf:
            emu_counts[pf] += 1
    links_html = ''
    for key, label, icon in EMULATOR_MAP:
        cnt = emu_counts.get(key, 0)
        if cnt > 0:
            slug = PLATFORM_SLUG_MAP.get(key, '')
            if slug:
                href = f'{prefix}/platforms/{slug}.html'
            else:
                href = f'{prefix}/index.html'
            links_html += f'''            <a href="{href}" class="emu-item emu-link">
                <span class="emu-icon">{icon}</span>
                <span class="emu-name">{label}</span>
                <span class="emu-count">{cnt}</span>
            </a>\n'''
    return f'''    <!-- 热门游戏模拟器悬浮侧栏 -->
    <div class="emu-sidebar" id="emuSidebar">
        <div class="emu-sidebar-title">热门游戏模拟器</div>
        <div class="emu-links">
{links_html}        </div>
    </div>'''


def make_platform_grid_html(all_games):
    """Generate the 热门游戏模拟器 grid section for the index page."""
    from collections import Counter
    emu_counts = Counter()
    for g in all_games:
        pf = g['plat'].strip()
        if pf:
            emu_counts[pf] += 1
    cards = []
    for key, label, icon, slug in PLATFORM_CATEGORIES:
        cnt = emu_counts.get(key, 0)
        if cnt > 0:
            cards.append(f'''          <a href="./platforms/{slug}.html" class="platform-card-link">
            <div class="platform-card">
              <div class="platform-card-icon">{icon}</div>
              <div class="platform-card-info">
                <div class="platform-card-name">{label}</div>
                <div class="platform-card-count">{cnt:,} 款游戏</div>
              </div>
            </div>
          </a>''')
    return '\n'.join(cards)


def generate_platform_pages(series, sections_info, all_games):
    """Generate platform-category pages (FC红白机, GBA掌机, etc)."""
    from collections import Counter, defaultdict
    emu_games = defaultdict(list)
    for _, games in series:
        for g in games:
            pf = g['plat'].strip()
            if pf:
                emu_games[pf].append(g)

    quick_nav = make_quick_nav(sections_info, current_idx=None)
    emu_sidebar = make_emulator_sidebar(all_games, prefix='..')

    generated = []
    for key, label, icon, slug in PLATFORM_CATEGORIES:
        games = emu_games.get(key, [])
        if not games:
            continue
        count = len(games)
        cards_html = '\n\n'.join(make_card_html(g) for g in games)
        desc = f'{label}经典怀旧游戏ROM中文版合集，共{count}款游戏，包含宝可梦、马里奥、塞尔达等经典系列，全部中文汉化版，支持模拟器运行。'
        keywords = f'{label}游戏,{label}ROM合集,{label}ROM下载,{label}中文版,{count}款游戏,怀旧游戏下载,经典游戏ROM,{label}模拟器游戏,汉化游戏合集'
        title_full = f'{label}游戏 - 经典怀旧游戏ROM中文版下载'

        breadcrumb_ld = make_breadcrumb_jsonld([
            ('经典怀旧游戏 ROM 合集', SEO_DOMAIN),
            (f'{label}游戏', f'{SEO_DOMAIN}platforms/{slug}.html'),
        ])
        page_url = f'{SEO_DOMAIN}platforms/{slug}.html'
        itemlist_ld = make_itemlist_jsonld(games, label, page_url)
        ctx = {
            'platform_label': label,
            'platform_slug': slug,
            'platform_title_full': title_full,
            'platform_desc': desc,
            'platform_keywords': keywords,
            'platform_count': count,
            'cards': cards_html,
            'quick_nav': quick_nav,
            'emu_sidebar': emu_sidebar,
            'jsonld_breadcrumb': breadcrumb_ld,
            'jsonld_itemlist': itemlist_ld,
        }
        html = render_template(TEMPLATE_PLATFORM, ctx)
        outpath = os.path.join(ROOT, 'platforms', f'{slug}.html')
        with open(outpath, 'w', encoding=CHARSET) as f:
            f.write(html)
        generated.append((slug, label, count))
        print(f'  [{slug}] {label} ({count} games) -> platforms/{slug}.html')
    return generated


def render_template(path, ctx):
    with open(path, 'r', encoding=CHARSET) as f:
        return Template(f.read()).render(**ctx)

def make_index_jsonld(sections_info):
    """Generate JSON-LD for index page (WebSite + ItemList)."""
    def esc(s):
        return s.replace("'", "\\'").replace('"', '\\"')
    from datetime import date
    today_str = date.today().isoformat()
    # WebSite schema
    website = f'''    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "{esc(SEO_SITE_NAME)}",
      "description": "{esc(SEO_DESCRIPTION)}",
      "url": "{esc(SEO_DOMAIN)}",
      "inLanguage": "zh-CN",
      "dateModified": "{today_str}",
      "potentialAction": {{
        "@type": "SearchAction",
        "target": {{ "@type": "EntryPoint", "urlTemplate": "{esc(SEO_DOMAIN)}?search={{search_term_string}}" }},
        "query-input": "required name=search_term_string"
      }}
    }}'''
    # ItemList with game series
    filtered = [(sname, idx, cnt) for sname, idx, cnt, _ in sections_info
                if sname not in ('马力欧系列', '传说系列')]
    items = ',\n'.join(
        f'''      {{
        "@type": "ListItem",
        "position": {i+1},
        "item": {{
          "@type": "VideoGameSeries",
          "name": "{esc(name)}",
          "description": "{esc(SERIES_DESC_MAP.get(name, name + '经典游戏ROM合集'))}"
        }}
      }}'''
        for i, (name, _, _) in enumerate(filtered)
    )
    itemlist = f'''    {{
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "经典怀旧游戏系列",
      "description": "包含GBA/GBC/FC/SFC/N64全平台经典怀旧游戏系列合集",
      "inLanguage": "zh-CN",
      "itemListElement": [
{items}
      ]
    }}'''
    return website, itemlist

def make_itemlist_jsonld(games, name, url_prefix):
    """Generate ItemList JSON-LD for a list of games."""
    def esc(s):
        return s.replace("'", "\\'").replace('"', '\\"')
    items = ',\n'.join(
        f'''      {{
        "@type": "ListItem",
        "position": {i+1},
        "item": {{
          "@type": "VideoGame",
          "name": "{esc(g['name'])}",
          "description": "{esc(g['name'] + ' ROM中文版下载')}",
          "applicationCategory": "Game",
          "operatingSystem": "{esc(g.get('plat', '模拟器'))}"
        }}
      }}'''
        for i, g in enumerate(games[:100])
    )
    return f'''    {{
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "{esc(name + '游戏ROM合集')}",
      "description": "{esc(name + '经典怀旧游戏ROM中文版合集，共' + str(len(games)) + '款游戏')}",
      "inLanguage": "zh-CN",
      "numberOfItems": {len(games)},
      "itemListElement": [
{items}
      ]
    }}'''

def make_breadcrumb_jsonld(items):
    """Generate BreadcrumbList JSON-LD from list of (name, url) tuples."""
    def esc(s):
        return s.replace("'", "\\'").replace('"', '\\"')
    elements = ',\n'.join(
        f'''      {{
        "@type": "ListItem",
        "position": {i+1},
        "name": "{esc(name)}",
        "item": "{esc(url)}"
      }}'''
        for i, (name, url) in enumerate(items)
    )
    return f'''    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "inLanguage": "zh-CN",
      "itemListElement": [
{elements}
      ]
    }}'''

def generate_section_page(sname, games, idx, sections_info, all_games):
    """Generate a full section HTML page."""
    # Group same-name games and add labels to distinguish duplicates
    from collections import Counter, defaultdict
    import re as _re
    name_counts = Counter(g['name'] for g in games)
    # For dupes, collect unique descriptions per name
    name_descs = defaultdict(set)
    for g in games:
        n = g['name']
        if name_counts[n] > 1:
            d = g.get('desc', '')[:60]
            name_descs[n].add(d)
    name_idx = {}
    labeled_games = []
    for g in games:
        n = g['name']
        if name_counts[n] > 1:
            name_idx[n] = name_idx.get(n, 0) + 1
            d = g.get('desc', '')
            if len(name_descs[n]) > 1:
                # Descriptions differ — find a short version/distinction tag
                tag = ''
                # Priority 1: extract text inside last () or [] in desc
                parens = _re.findall(r'[（\(]([^）\)]{1,30})[）\)]', d)
                if parens:
                    tag = parens[-1]
                else:
                    brackets = _re.findall(r'[\[【]([^\]】]{1,30})[\]】]', d)
                    if brackets:
                        tag = brackets[-1]
                # Priority 2: first 15 chars of desc if non-generic
                if not tag or len(tag) < 2:
                    short = d.strip()[:20]
                    if short and not any(kw in short for kw in ['是', '的', '了', '在', '有', '为', '以', '与', 'FC/NES', 'GBA', 'NDS', 'PS']):
                        tag = short
                if not tag or len(tag) < 2:
                    tag = f'版本 {name_idx[n]}'
                labeled_games.append((g, tag))
            else:
                labeled_games.append((g, f'副本 {name_idx[n]}'))
        else:
            labeled_games.append((g, ''))
    cards_html = '\n\n'.join(make_card_html(g, lbl) for g, lbl in labeled_games)
    quick_nav = make_quick_nav(sections_info, current_idx=idx)
    emu_sidebar = make_emulator_sidebar(all_games, prefix='..')
    section_desc = SERIES_DESC_MAP.get(sname, f'{sname}经典怀旧游戏ROM中文版合集')
    # Collect unique platforms and languages for richer meta
    platforms = sorted(set(g['plat'] for g in games if g['plat']))
    plats_str = '/'.join(platforms[:4])
    if len(platforms) > 4:
        plats_str += '等'
    section_keywords = f'{sname},{sname}ROM下载,{sname}中文版,{plats_str},{plats_str}模拟器,怀旧游戏,经典游戏,ROM下载,中文汉化版,{len(games)}款游戏'
    section_title_full = f'{sname} - 经典怀旧游戏ROM中文版下载'
    dir_script = ''
    if sname == '宝可梦系列':
        dir_script = '''
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        var modal = document.getElementById('collectionDirModal');
        if (modal) {
            modal.addEventListener('show.bs.modal', function () {
                var body = document.getElementById('collectionDirModalBody');
                if (!body.dataset.loaded) {
                    fetch('../docs/gba-collection-dir-modal.html')
                        .then(function(r) { return r.text(); })
                        .then(function(html) {
                            body.innerHTML = html;
                            body.dataset.loaded = '1';
                        })
                        .catch(function() {
                            body.innerHTML = '<div class="text-center text-muted"><p>加载目录失败，请刷新后重试</p></div>';
                        });
                }
            });
        }
    });
    </script>'''
    breadcrumb_ld = make_breadcrumb_jsonld([
        ('经典怀旧游戏 ROM 合集', SEO_DOMAIN),
        (sname, f'{SEO_DOMAIN}sections/section-{idx:02d}.html'),
    ])
    page_url = f'{SEO_DOMAIN}sections/section-{idx:02d}.html'
    itemlist_ld = make_itemlist_jsonld(games, sname, page_url)
    ctx = {
        'section_title': sname,
        'section_title_full': section_title_full,
        'section_desc': section_desc,
        'section_keywords': section_keywords,
        'section_number': idx,
        'cards': cards_html,
        'quick_nav': quick_nav,
        'emu_sidebar': emu_sidebar,
        'collection_dir_script': dir_script,
        'jsonld_breadcrumb': breadcrumb_ld,
        'jsonld_itemlist': itemlist_ld,
    }
    html = render_template(TEMPLATE_SECTION, ctx)
    return html

def generate_index_page(sections_info, all_games, section_platforms=None):
    """Generate index.html."""
    if section_platforms is None:
        section_platforms = {}
    covers_html = '\n\n'.join(
        make_cover_card(sname, idx, cnt, first_cover, section_platforms.get(sname, []))
        for sname, idx, cnt, first_cover in sections_info
    )
    platform_grid = make_platform_grid_html(all_games)
    quick_nav = make_quick_nav(sections_info)
    emu_sidebar = make_emulator_sidebar(all_games, prefix='.')
    website_ld, itemlist_ld = make_index_jsonld(sections_info)
    ctx = {
        'covers': covers_html,
        'platform_grid': platform_grid,
        'INDEX_TITLE': INDEX_TITLE,
        'SITE_TITLE': SITE_TITLE,
        'quick_nav': quick_nav,
        'emu_sidebar': emu_sidebar,
        'jsonld_website': website_ld,
        'jsonld_itemlist': itemlist_ld,
    }
    html = render_template(TEMPLATE_INDEX, ctx)
    html = html.replace('{{ SITE_TITLE | safe }}', SITE_TITLE)
    return html

def update_seo_js(sections_info):
    """Update docs/js/seo-meta.js."""
    path = os.path.join(ROOT, 'docs', 'js', 'seo-meta.js')
    with open(path, 'r', encoding=CHARSET) as f:
        content = f.read()
    replacements = {
        r"title:.*?'.*?',": f"title: '{SEO_TITLE}',",
        r"description:.*?'.*?',": f"description: '{SEO_DESCRIPTION}',",
        r"keywords:.*?'.*?',": f"keywords: '{SEO_KEYWORDS}',",
        r"author:.*?'.*?',": f"author: '{SEO_AUTHOR}',",
        r"siteName:.*?'.*?',": f"siteName: '{SEO_SITE_NAME}',",
        r"domain:.*?'.*?',": f"domain: '{SEO_DOMAIN}',",
        r"image:.*?'.*?',": f"image: '{SEO_IMAGE}',",
    }
    for pattern, repl in replacements.items():
        content = re.sub(pattern, repl, content)
    # Update gameSeries with real descriptions
    series_list = []
    for sname, _, cnt, _ in sections_info:
        safe_name = sname.replace("'", "\\'")
        safe_desc = SERIES_DESC_MAP.get(sname, f'{sname}经典游戏ROM合集').replace("'", "\\'")
        series_list.append(f"            {{ name: '{safe_name}', description: '{safe_desc}' }}")
    series_js = ',\n'.join(series_list)
    content = re.sub(
        r"gameSeries:\s*\[[\s\S]*?\]",
        f"gameSeries: [\n{series_js}\n        ]",
        content
    )
    with open(path, 'w', encoding=CHARSET) as f:
        f.write(content)
    print(f'  Updated seo-meta.js ({len(sections_info)} series)')

def update_global_search_js(sections_info):
    """Update docs/js/global-search.js SECTIONS config."""
    path = os.path.join(ROOT, 'docs', 'js', 'global-search.js')
    with open(path, 'r', encoding=CHARSET) as f:
        content = f.read()
    sections_js = ',\n'.join(
        f"        {{ file: 'section-{idx:02d}.html', name: '{sname.replace(chr(39), chr(92) + chr(39))}' }}"
        for sname, idx, _, _ in sections_info
    )
    content = re.sub(
        r"const SECTIONS = \[[\s\S]*?\];",
        f"const SECTIONS = [\n{sections_js}\n    ];",
        content
    )
    with open(path, 'w', encoding=CHARSET) as f:
        f.write(content)
    print(f'  Updated global-search.js ({len(sections_info)} sections)')

def update_count_badges_js(sections_info):
    """Update docs/js/count-badges.js SECTIONS config."""
    path = os.path.join(ROOT, 'docs', 'js', 'count-badges.js')
    with open(path, 'r', encoding=CHARSET) as f:
        content = f.read()
    sections_js = ',\n'.join(
        f"        {{ file: 'section-{idx:02d}.html', index: {i} }}"
        for i, (_, idx, _, _) in enumerate(sections_info)
    )
    content = re.sub(
        r"const SECTIONS = \[[\s\S]*?\];",
        f"const SECTIONS = [\n{sections_js}\n    ];",
        content
    )
    with open(path, 'w', encoding=CHARSET) as f:
        f.write(content)
    print(f'  Updated count-badges.js ({len(sections_info)} sections)')

def update_readme():
    """Update res/README.md config."""
    path = os.path.join(ROOT, 'res', 'README.md')
    lines = f"""## 说明

修改下面的变量值，运行 `python py/generate_game_site.py` 脚本时会自动读取这些变量，在 python 生成网站源码的同时，自动填充 html 模板中。


### html 页面标题和提示

> 影响 `index.html`, `sections/*`

```
SITE_TITLE={SITE_TITLE}

INDEX_TITLE={INDEX_TITLE}
```



### SEO 配置（用于优化搜索引擎推荐排名）

> 影响 `docs/js/seo-meta.js`


```
SEO_TITLE={SEO_TITLE}

SEO_DESCRIPTION={SEO_DESCRIPTION}

SEO_KEYWORDS={SEO_KEYWORDS}

SEO_AUTHOR={SEO_AUTHOR}

SEO_SITE_NAME={SEO_SITE_NAME}

SEO_DOMAIN={SEO_DOMAIN}

SEO_IMAGE={SEO_IMAGE}
```
"""
    with open(path, 'w', encoding=CHARSET) as f:
        f.write(lines)
    print('  Updated res/README.md')

def generate_sitemap(sections_info, platform_pages=None):
    """Generate sitemap.xml."""
    today = datetime.now().strftime('%Y-%m-%d')
    links = []
    # Index
    ctx = {'loc': f'{SEO_DOMAIN}', 'lastmod': today, 'changefreq': 'weekly', 'priority': '1.0'}
    links.append(render_template(TEMPLATE_LINK, ctx))
    # Sections with priority by popularity rank
    total = len(sections_info)
    for i, (sname, idx, _, _) in enumerate(sections_info):
        p = max(0.5, 1.0 - (i / max(total, 1)) * 0.5)
        priority = f'{p:.1f}'
        ctx = {
            'loc': f'{SEO_DOMAIN}sections/section-{idx:02d}.html',
            'lastmod': today, 'changefreq': 'monthly', 'priority': priority
        }
        links.append(render_template(TEMPLATE_LINK, ctx))
    # Platform pages
    if platform_pages:
        for slug, label, cnt in platform_pages:
            ctx = {
                'loc': f'{SEO_DOMAIN}platforms/{slug}.html',
                'lastmod': today,
                'changefreq': 'weekly', 'priority': '0.8'
            }
            links.append(render_template(TEMPLATE_LINK, ctx))
    sitemap = render_template(TEMPLATE_SITEMAP, {'item_links': '\n'.join(links)})
    with open(OUTPUT_SITEMAP, 'w', encoding=CHARSET) as f:
        f.write(sitemap)
    print(f'  Generated sitemap.xml ({len(links)} URLs)')

def main():
    print('='*60)
    print('Game ROM Site Generator')
    print('='*60)
    
    # Load Excel
    print(f'\nReading Excel: {EXCEL}')
    series = load_excel(EXCEL)
    print(f'Found {len(series)} series, {sum(len(g) for _, g in series)} total games')
    
    # Clear old sections
    if os.path.exists(OUTPUT_SECTIONS):
        for f in os.listdir(OUTPUT_SECTIONS):
            if f.startswith('section-') and f.endswith('.html'):
                os.remove(os.path.join(OUTPUT_SECTIONS, f))
        print(f'Cleared old section files')
    os.makedirs(OUTPUT_SECTIONS, exist_ok=True)
    
    # Build sections info list with first real cover found
    sections_info = []
    for i, (sname, games) in enumerate(series, 1):
        real_cover = ''
        for g in games:
            path = resolve_cover(g['cover'])
            if path != PLACEHOLDER:
                real_cover = path
                break
        sections_info.append((sname, i, len(games), real_cover))
    
    # Sort by network popularity (品牌知名度/网络热度), 其他游戏 last
    POPULARITY = {
        '马里奥系列': 1, '宝可梦系列': 2, '塞尔达传说系列': 3,
        '最终幻想系列': 4, '勇者斗恶龙系列': 5, '魂斗罗系列': 6, '恶魔城系列': 7,
        '洛克人系列': 8, '龙珠系列': 9, '火焰纹章系列': 10, '高达系列': 11,
        '拳皇系列': 12, '合金弹头系列': 13, '街霸系列': 14, '传说系列': 15,
        '游戏王系列': 16, '星之卡比系列': 17, '牧场物语系列': 18, '超级机器人大战系列': 19,
        '银河战士系列': 20, '索尼克系列': 21, '火影忍者系列': 22, '真女神转生系列': 23,
        '魔法系列': 24, '逆转裁判系列': 25, '黄金太阳系列': 26, '我们的太阳系列': 27,
        '高级战争系列': 28, '鬼武者系列': 29, '光明之魂系列': 30, '侦探系列': 31,
        '热血系列': 32, '蜡笔小新系列': 33, '网球王子系列': 34, '瓦力欧系列': 35,
        '马力欧系列': 36, '召唤之夜系列': 37, '任天堂明星大乱斗系列': 38,
        'F-Zero系列': 39, '星际火狐系列': 40, '耀西系列': 41, '动物森林系列': 42,
        '水上摩托系列': 43, '越野摩托系列': 44, '组合机器人系列': 45,
        'CT特种部队系列': 46, '节奏天国系列': 47, '罪与罚系列': 48, '决战三国系列': 49,
    }
    sections_info.sort(key=lambda x: (x[0] == '其他游戏', POPULARITY.get(x[0], 99)))
    # Re-assign indices after sort
    for i, item in enumerate(sections_info, 1):
        sections_info[i-1] = (item[0], i, item[2], item[3])
    # Reorder series to match sections_info order
    sections_map = {sname: games for sname, games in series}
    series = [(sname, sections_map[sname]) for sname, _, _, _ in sections_info]
    
    # Collect all games for emulator sidebar
    all_games = []
    for _, games in series:
        all_games.extend(games)
    
    # Generate section pages
    print(f'\nGenerating {len(series)} section pages...')
    for (sname, games), (_, idx, _, _) in zip(series, sections_info):
        html = generate_section_page(sname, games, idx, sections_info, all_games)
        outpath = os.path.join(OUTPUT_SECTIONS, f'section-{idx:02d}.html')
        with open(outpath, 'w', encoding=CHARSET) as f:
            f.write(html)
        print(f'  [{idx:02d}] {sname} ({len(games)} games) -> section-{idx:02d}.html')
    
    # Generate platform pages
    print(f'\nGenerating platform pages...')
    os.makedirs(os.path.join(ROOT, 'platforms'), exist_ok=True)
    platform_pages = generate_platform_pages(series, sections_info, all_games)
    
    # Build platform tags per section for index cover cards
    section_platforms = {}
    for sname, games in series:
        plats = sorted(set(g['plat'] for g in games if g['plat']))
        section_platforms[sname] = plats[:3]
    
    # Generate index page
    print(f'\nGenerating index.html...')
    index_html = generate_index_page(sections_info, all_games, section_platforms)
    with open(OUTPUT_INDEX, 'w', encoding=CHARSET) as f:
        f.write(index_html)
    print(f'  index.html written')
    
    # Update JS configs
    print(f'\nUpdating JS configs...')
    update_seo_js(sections_info)
    update_global_search_js(sections_info)
    update_count_badges_js(sections_info)
    update_readme()
    
    # Generate sitemap
    print(f'\nGenerating sitemap...')
    generate_sitemap(sections_info, platform_pages)
    
    print(f'\n{"="*60}')
    print(f'Done! Generated {len(series)} sections + {len(platform_pages)} platform pages + index.html')
    print(f'Total games: {sum(len(g) for _, g in series)}')
    print(f'{"="*60}')

if __name__ == '__main__':
    main()
