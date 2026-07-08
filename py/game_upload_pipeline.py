#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game ROM Upload Pipeline
=======================
一站式游戏上架流水线：去重 → 找封面 → 写简介 → 查年份 → 验链接 → 追加Excel → 生成站点 → 部署

Usage:
  python py/game_upload_pipeline.py dedup --new <new.xlsx> [--output deduped.json]
  python py/game_upload_pipeline.py list-series [--excel <path>]
  python py/game_upload_pipeline.py append --series <系列名> --games <games.json> [--dry-run]
  python py/game_upload_pipeline.py download-cover --name <游戏名> --url <URL>
  python py/game_upload_pipeline.py verify-links --excel <path> [--series <系列名>]
  python py/game_upload_pipeline.py generate
  python py/game_upload_pipeline.py deploy [--message <msg>]
  python py/game_upload_pipeline.py status
"""

import os, re, sys, json, hashlib, argparse
from datetime import datetime
from openpyxl import load_workbook, Workbook
from openpyxl.utils import get_column_letter
from urllib.parse import urlparse
import subprocess

CHARSET = 'utf-8'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL = os.path.join(ROOT, 'res', 'merged.xlsx')
COVERS_DIR = os.path.join(ROOT, 'res', 'covers')
PLACEHOLDER = '../res/covers/placeholder.png'

# 已知系列（含别名映射）
SERIES_INDEX = {
    '马里奥': '马里奥系列', 'mario': '马里奥系列', '超级马里奥': '马里奥系列',
    '宝可梦': '宝可梦系列', 'pokemon': '宝可梦系列', '口袋妖怪': '宝可梦系列',
    '塞尔达': '塞尔达传说系列', 'zelda': '塞尔达传说系列',
    '最终幻想': '最终幻想系列', 'final fantasy': '最终幻想系列', 'ff': '最终幻想系列',
    '勇者斗恶龙': '勇者斗恶龙系列', 'dragon quest': '勇者斗恶龙系列', 'dq': '勇者斗恶龙系列',
    '魂斗罗': '魂斗罗系列', 'contra': '魂斗罗系列',
    '恶魔城': '恶魔城系列', 'castlevania': '恶魔城系列',
    '洛克人': '洛克人系列', 'rockman': '洛克人系列', 'megaman': '洛克人系列',
    '龙珠': '龙珠系列', 'dragon ball': '龙珠系列',
    '火焰纹章': '火焰纹章系列', 'fire emblem': '火焰纹章系列',
    '高达': '高达系列', 'gundam': '高达系列',
    '拳皇': '拳皇系列', 'kof': '拳皇系列', 'king of fighters': '拳皇系列',
    '合金弹头': '合金弹头系列', 'metal slug': '合金弹头系列',
    '传说': '传说系列', 'tales of': '传说系列',
    '游戏王': '游戏王系列', 'yu-gi-oh': '游戏王系列',
    '星之卡比': '星之卡比系列', 'kirby': '星之卡比系列',
    '牧场物语': '牧场物语系列', 'harvest moon': '牧场物语系列',
    '机战': '超级机器人大战系列', '机器人大战': '超级机器人大战系列',
    '银河战士': '银河战士系列', 'metroid': '银河战士系列',
    '索尼克': '索尼克系列', 'sonic': '索尼克系列',
    '火影': '火影忍者系列', 'naruto': '火影忍者系列',
    '逆转裁判': '逆转裁判系列', 'ace attorney': '逆转裁判系列',
    '黄金太阳': '黄金太阳系列', 'golden sun': '黄金太阳系列',
    '高级战争': '高级战争系列', 'advance wars': '高级战争系列',
    '鬼武者': '鬼武者系列', 'onimusha': '鬼武者系列',
    '光明之魂': '光明之魂系列', 'shining soul': '光明之魂系列',
    '热血': '热血系列', 'river city': '热血系列',
    '蜡笔小新': '蜡笔小新系列',
    '网球王子': '网球王子系列',
    '瓦力欧': '瓦力欧系列', 'wario': '瓦力欧系列',
    '召唤之夜': '召唤之夜系列', 'summon night': '召唤之夜系列',
    '大乱斗': '任天堂明星大乱斗系列', 'smash bros': '任天堂明星大乱斗系列',
    'f-zero': 'F-Zero系列', 'fzero': 'F-Zero系列',
    '星际火狐': '星际火狐系列', 'star fox': '星际火狐系列',
    '耀西': '耀西系列', 'yoshi': '耀西系列',
    '动物森': '动物森林系列', '动物之森': '动物森林系列', 'animal crossing': '动物森林系列',
    '节奏天国': '节奏天国系列', 'rhythm heaven': '节奏天国系列',
    '决战三国': '决战三国系列',
}

# 标准化平台名称
PLATFORM_MAP = {
    'fc': 'FC/NES', 'nes': 'FC/NES', 'fc/nes': 'FC/NES',
    'sfc': 'SFC/SNES', 'snes': 'SFC/SNES', 'sfc/snes': 'SFC/SNES',
    'gba': 'GBA', 'gameboyadvance': 'GBA',
    'gbc': 'GBC', 'gb': 'GB', 'gameboy': 'GB', 'gameboycolor': 'GBC',
    'n64': 'N64', 'nintendo 64': 'N64',
    'nds': 'NDS', '3ds': '3DS',
    'pce': 'PCE', 'pc engine': 'PCE',
    'md': 'MD', 'megadrive': 'MD', 'genesis': 'MD',
    '街机': '街机', 'arcade': '街机',
    'ps': 'PS', 'ps1': 'PS1', 'playstation': 'PS1',
    'ps2': 'PS2', 'playstation2': 'PS2',
    'ps3': 'PS3', 'playstation3': 'PS3',
    'psp': 'PSP',
    'wii': 'WII', 'nintendo wii': 'WII',
    'ngc': 'NGC', 'gamecube': 'NGC',
    'dos': 'DOS',
}


# ============================================================
# Excel 读取/写入
# ============================================================

def load_excel(path):
    """Load all game data from merged.xlsx. Returns dict {series_name: [games]}."""
    if not os.path.exists(path):
        print(f'ERROR: Excel not found at {path}')
        return {}
    wb = load_workbook(path, data_only=True)
    result = {}
    for sname in wb.sheetnames:
        if sname == '主目录':
            continue
        ws = wb[sname]
        games = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            vals = list(row)
            if len(vals) < 2 or vals[1] is None:
                continue
            while len(vals) < 7:
                vals.append('')
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
                'lang': lang, 'plat': plat, 'year': year, 'link': link,
            })
        if games:
            result[sname] = games
    wb.close()
    return result


def load_series_names(path):
    """Return list of series names (sheet names excluding 主目录)."""
    if not os.path.exists(path):
        return []
    wb = load_workbook(path, data_only=True)
    names = [s for s in wb.sheetnames if s != '主目录']
    wb.close()
    return names


def build_known_set(existing_data):
    """Build set of (name, link) tuples for dedup."""
    known = set()
    for series, games in existing_data.items():
        for g in games:
            known.add((g['name'], g['link']))
    return known


def read_new_excel(path):
    """Read user's new game Excel. Returns list of game dicts.
    Auto-detects format:
      - 7-col format: cover, name, desc, lang, plat, year, link
      - 6-col format: 序号, name, category, plat, link, desc
    """
    if not os.path.exists(path):
        print(f'ERROR: File not found: {path}')
        return []
    wb = load_workbook(path, data_only=True)
    games = []
    for sname in wb.sheetnames:
        if sname == '主目录':
            continue
        ws = wb[sname]
        # Detect format from header row
        header = [str(c.value or '').strip() for c in ws[1]]
        is_6col = any('序号' in h for h in header) and any('游戏格式' in h for h in header)

        for row in ws.iter_rows(min_row=2, values_only=True):
            vals = list(row)
            if len(vals) < 2 or vals[1] is None:
                continue
            name = str(vals[1] or '').strip()
            if not name:
                continue

            if is_6col:
                # 序号, 游戏名称, 所属平台, 游戏格式, 下载链接, 游戏简介
                cover = ''
                desc = str(vals[5] or '').strip()
                lang = '中文'
                plat = str(vals[3] or '').strip()
                year = ''
                link = str(vals[4] or '').strip()
            else:
                # Pad to 7 columns
                while len(vals) < 7:
                    vals.append('')
                cover = str(vals[0] or '').strip().replace('\\', '/')
                desc = str(vals[2] or '').strip()
                lang = str(vals[3] or '').strip()
                plat = str(vals[4] or '').strip()
                year = str(vals[5] or '').strip()
                link = str(vals[6] or '').strip()

            games.append({
                'cover': cover,
                'name': name,
                'desc': desc,
                'lang': lang,
                'plat': plat,
                'year': year,
                'link': link,
                '_source_sheet': sname,
            })
    wb.close()
    return games


def platform_normalize(plat):
    """Normalize platform string to standard format."""
    p = plat.strip().lower().replace(' ', '')
    if p in PLATFORM_MAP:
        return PLATFORM_MAP[p]
    # Try partial match
    for key, val in PLATFORM_MAP.items():
        if key in p:
            return val
    return plat.strip()


def guess_series(game):
    """Guess which series a game belongs to."""
    name = game['name']
    name_lower = name.lower()
    plat = game.get('plat', '')
    # Check name for series keywords
    for keyword, series in sorted(SERIES_INDEX.items(), key=lambda x: -len(x[0])):
        if keyword.lower() in name_lower:
            return series
    # Try platform-based guessing for common patterns
    plat_norm = platform_normalize(plat) if plat else ''
    return '其他游戏'


# ============================================================
# 封面操作
# ============================================================

def cover_path(name):
    """Generate cover file path from game name."""
    safe = re.sub(r'[\\/:*?"<>|]', '_', name)
    return os.path.join(COVERS_DIR, f'{safe}.png')


def cover_exists(name):
    """Check if a cover image already exists."""
    return os.path.exists(cover_path(name))


def download_cover(url, name):
    """Download cover image from URL to res/covers/."""
    import requests
    path = cover_path(name)
    if os.path.exists(path):
        print(f'  Cover already exists: {os.path.basename(path)}')
        return f'../res/covers/{os.path.basename(path)}'.replace('\\', '/')
    try:
        r = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        if r.status_code == 200 and len(r.content) > 1000:
            with open(path, 'wb') as f:
                f.write(r.content)
            rel_path = f'../res/covers/{os.path.basename(path)}'.replace('\\', '/')
            print(f'  Downloaded cover: {os.path.basename(path)} ({len(r.content)} bytes)')
            return rel_path
        else:
            print(f'  Failed to download cover (HTTP {r.status_code})')
            return ''
    except Exception as e:
        print(f'  Error downloading cover: {e}')
        return ''


# ============================================================
# 链接验证
# ============================================================

def verify_link(link):
    """Verify a download link is accessible. Returns (ok, message)."""
    if not link or link == 'None':
        return False, 'empty link'
    # Baidu links - can't truly verify without auth, check format
    if 'pan.baidu.com' in link:
        if '?pwd=' in link or '?pwd=' in link:
            return True, 'baidu link format OK'
        return False, 'baidu link missing ?pwd='
    # Quark links
    if 'pan.quark.cn' in link:
        if '?pwd=' in link:
            return True, 'quark link format OK'
        return True, 'quark link (no pwd)'
    # Try generic HTTP check
    try:
        import requests
        r = requests.head(link, timeout=15, allow_redirects=True,
                          headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code < 400:
            return True, f'HTTP {r.status_code}'
        return False, f'HTTP {r.status_code}'
    except Exception as e:
        return False, f'error: {e}'


# ============================================================
# 追加游戏到 Excel
# ============================================================

def append_games_to_excel(path, series_name, games, dry_run=False):
    """Append games to a specific series sheet in merged.xlsx."""
    if not os.path.exists(path):
        print(f'ERROR: Excel not found: {path}')
        return False

    wb = load_workbook(path)
    if series_name not in wb.sheetnames:
        print(f'Creating new sheet: {series_name}')
        ws = wb.create_sheet(title=series_name)
        ws.append(['封面', '游戏名称', '游戏简介', '语言', '平台', '发行年份', '下载链接'])
    else:
        ws = wb[series_name]
        # Find last row
        last_row = ws.max_row
        if last_row < 1:
            last_row = 1

    added = 0
    for g in games:
        cover_val = g.get('cover', '')
        name = g.get('name', '')
        desc = g.get('desc', '')
        lang = g.get('lang', '中文')
        plat = g.get('plat', '')
        year = g.get('year', '未知')
        link = g.get('link', '')

        if not name:
            continue

        ws.append([cover_val, name, desc, lang, plat, year, link])
        added += 1

    if dry_run:
        print(f'[DRY RUN] Would append {added} games to "{series_name}"')
        wb.close()
        return True

    wb.save(path)
    wb.close()
    print(f'Appended {added} games to "{series_name}" in {os.path.basename(path)}')
    return True


# ============================================================
# 系列信息（用于 AI 判断）
# ============================================================

def get_series_info(path):
    """Get info about all series. Returns list of dicts."""
    data = load_excel(path)
    result = []
    for i, (sname, games) in enumerate(sorted(data.items(), key=lambda x: -len(x[1]))):
        # Get sample platforms
        plats = set(g['plat'] for g in games if g['plat'])
        result.append({
            'name': sname,
            'game_count': len(games),
            'sample_platforms': sorted(plats)[:5],
            'has_description': SERIES_DESC_MAP.get(sname, '') != '' if 'SERIES_DESC_MAP' in dir() else False,
        })
    return result

# Include the series description map from generate_game_site
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
    '魔法系列': '魔法系列经典游戏ROM中文版下载合集',
    '逆转裁判系列': '逆转裁判系列游戏ROM中文版下载，包含逆转裁判1-3部法庭推理经典',
    '黄金太阳系列': '黄金太阳系列游戏ROM中文版下载，GBA平台最佳日式RPG系列中文汉化版',
    '我们的太阳系列': '我们的太阳系列游戏ROM中文版下载，结合阳光传感器的独特动作RPG',
    '高级战争系列': '高级战争系列游戏ROM中文版下载，任天堂经典战棋策略游戏中文版',
    '鬼武者系列': '鬼武者系列游戏ROM中文版下载，包含鬼武者战略版等动作策略游戏',
    '光明之魂系列': '光明之魂系列游戏ROM中文版下载，GBA平台经典暗黑Like动作RPG',
    '侦探系列': '侦探系列经典游戏ROM中文版下载合集',
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
    '组合机器人系列': '组合机器人系列游戏ROM中文版下载合集',
    'CT特种部队系列': 'CT特种部队系列游戏ROM中文版下载合集',
    '节奏天国系列': '节奏天国系列游戏ROM中文版下载，任天堂创意音乐节奏游戏',
    '罪与罚系列': '罪与罚系列游戏ROM中文版下载，N64平台经典动作射击游戏',
    '决战三国系列': '决战三国系列游戏ROM中文版下载，三国题材策略战棋游戏合集',
    '其他游戏': '更多经典怀旧游戏ROM合集，包含各平台未分类经典游戏中文汉化版',
}


# ============================================================
# CLI 命令
# ============================================================

def cmd_list_series(args):
    """List all existing series with game counts."""
    data = load_excel(args.excel)
    if not data:
        print('No data found.')
        return
    print(f'\n{"Series":35s} {"Games":>6s}  Platforms')
    print('-' * 60)
    sorted_series = sorted(data.items(), key=lambda x: -len(x[1]))
    for sname, games in sorted_series:
        plats = set(g['plat'] for g in games if g['plat'])
        plat_str = ', '.join(sorted(plats)[:3])
        print(f'{sname:35s} {len(games):>6d}  {plat_str}')
    total = sum(len(g) for _, g in sorted_series)
    print(f'\nTotal: {len(data)} series, {total} games')


def load_json_games(path):
    """Load games from a JSON file (list of game dicts)."""
    with open(path, 'r', encoding=CHARSET) as f:
        return json.load(f)

def cmd_dedup(args):
    """Dedup new games against existing merged.xlsx."""
    print(f'Reading existing: {args.excel}')
    existing = load_excel(args.excel)
    known = build_known_set(existing)
    print(f'Existing: {len(existing)} series, {len(known)} known games')

    print(f'Reading new games: {args.new}')
    if args.new.endswith('.json'):
        new_games = load_json_games(args.new)
    else:
        new_games = read_new_excel(args.new)
    print(f'New games: {len(new_games)}')

    # Dedup
    dupes = []
    unique = []
    for g in new_games:
        key = (g['name'], g['link'])
        if key in known:
            dupes.append(g)
        else:
            unique.append(g)

    print(f'  Duplicates: {len(dupes)}')
    print(f'  Unique: {len(unique)}')

    if dupes:
        print('  Duplicate examples:')
        for d in dupes[:5]:
            print(f'    - {d["name"]}')

    # Classify into series
    for g in unique:
        g['_series'] = guess_series(g)
        g['plat_norm'] = platform_normalize(g.get('plat', ''))

    output = args.output
    if output:
        with open(output, 'w', encoding=CHARSET) as f:
            json.dump(unique, f, ensure_ascii=False, indent=2)
        print(f'Saved deduped games to: {output}')
    else:
        # Print summary by series
        from collections import Counter
        series_count = Counter(g['_series'] for g in unique)
        print(f'\nNew games by series:')
        for sname, cnt in series_count.most_common():
            print(f'  {sname}: {cnt}')


def cmd_append(args):
    """Append games from JSON to merged.xlsx."""
    with open(args.games, 'r', encoding=CHARSET) as f:
        games = json.load(f)
    ok = append_games_to_excel(args.excel, args.series, games, dry_run=args.dry_run)
    if not ok:
        sys.exit(1)


def cmd_download_cover(args):
    """Download a cover image."""
    rel = download_cover(args.url, args.name)
    if rel:
        print(f'Cover saved as: {rel}')
    else:
        print('Failed to download cover')
        sys.exit(1)


def cmd_verify_links(args):
    """Verify download links in the Excel."""
    data = load_excel(args.excel)
    if args.series:
        games = data.get(args.series, [])
        if not games:
            print(f'Series "{args.series}" not found or has no games')
            return
        check_games = [(args.series, games)]
    else:
        check_games = list(data.items())

    total = 0
    failed = 0
    for sname, games in check_games:
        for g in games:
            total += 1
            ok, msg = verify_link(g['link'])
            if not ok:
                failed += 1
                if failed <= 10:
                    print(f'  [{sname}] {g["name"]}: {msg}')
    print(f'\nChecked {total} links, {failed} failed')


def cmd_generate(args):
    """Run the site generator."""
    gen_script = os.path.join(ROOT, 'py', 'generate_game_site.py')
    if not os.path.exists(gen_script):
        print(f'ERROR: Generator not found: {gen_script}')
        return
    print('Running site generator...')
    result = subprocess.run([sys.executable, gen_script], cwd=ROOT,
                            capture_output=False)
    if result.returncode != 0:
        print(f'Generator failed with code {result.returncode}')
        sys.exit(1)


def cmd_deploy(args):
    """Git add, commit, and push to res branch."""
    message = args.message or f'Auto-deploy: site update {datetime.now().strftime("%Y-%m-%d %H:%M")}'

    # Ensure we're on res branch
    result = subprocess.run(['git', 'branch', '--show-current'],
                            cwd=ROOT, capture_output=True, text=True)
    branch = result.stdout.strip()
    if branch != 'res':
        print(f'WARNING: Current branch is "{branch}", not "res"')

    print('Staging all changes...')
    subprocess.run(['git', 'add', '-A'], cwd=ROOT, capture_output=True)

    print('Committing...')
    result = subprocess.run(['git', 'commit', '-m', message],
                            cwd=ROOT, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.returncode != 0 and 'nothing to commit' not in result.stdout:
        print(f'Commit may have failed: {result.stderr.strip()}')

    print('Pushing to origin/res...')
    result = subprocess.run(['git', 'push', 'origin', 'res'],
                            cwd=ROOT, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.returncode != 0:
        print(f'Push may have failed: {result.stderr.strip()}')


def cmd_status(args):
    """Show pipeline status summary."""
    print(f'Project: {ROOT}')
    print(f'Merged Excel: {EXCEL}')
    print(f'  Exists: {os.path.exists(EXCEL)}')
    if os.path.exists(EXCEL):
        data = load_excel(EXCEL)
        total_games = sum(len(g) for g in data.values())
        print(f'  Series: {len(data)}, Games: {total_games}')

    print(f'\nCovers directory: {COVERS_DIR}')
    if os.path.exists(COVERS_DIR):
        covers = [f for f in os.listdir(COVERS_DIR) if f.endswith('.png')]
        print(f'  Cover PNGs: {len(covers)}')

    print(f'\nGenerator: {os.path.join(ROOT, "py", "generate_game_site.py")}')
    print(f'  Exists: {os.path.exists(os.path.join(ROOT, "py", "generate_game_site.py"))}')

    # Git status
    print('\nGit:')
    result = subprocess.run(['git', 'status', '--short'], cwd=ROOT,
                            capture_output=True, text=True)
    modified = result.stdout.strip()
    if modified:
        lines = modified.split('\n')
        print(f'  Uncommitted changes: {len(lines)} files')
        for l in lines[:10]:
            print(f'    {l}')
    else:
        print('  Clean working tree')


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='Game ROM Upload Pipeline - 一站式游戏上架工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest='command', required=True)

    # list-series
    p = sub.add_parser('list-series', help='列出所有系列')
    p.add_argument('--excel', default=EXCEL)

    # dedup
    p = sub.add_parser('dedup', help='去重：对比新游戏和已有游戏')
    p.add_argument('--new', required=True, help='新游戏 Excel 文件')
    p.add_argument('--excel', default=EXCEL, help='现有 merged.xlsx 路径')
    p.add_argument('--output', default='', help='输出去重后的 JSON 文件路径')

    # append
    p = sub.add_parser('append', help='追加游戏到 Excel')
    p.add_argument('--series', required=True, help='系列名称（如 马里奥系列）')
    p.add_argument('--games', required=True, help='游戏 JSON 文件路径')
    p.add_argument('--excel', default=EXCEL)
    p.add_argument('--dry-run', action='store_true', help='仅预览，不实际写入')

    # download-cover
    p = sub.add_parser('download-cover', help='下载游戏封面')
    p.add_argument('--name', required=True, help='游戏名称（用于文件名）')
    p.add_argument('--url', required=True, help='封面图片 URL')

    # verify-links
    p = sub.add_parser('verify-links', help='验证下载链接')
    p.add_argument('--excel', default=EXCEL)
    p.add_argument('--series', default='', help='限定某个系列（不传则检查全部）')

    # generate
    p = sub.add_parser('generate', help='生成网站（运行 generate_game_site.py）')

    # deploy
    p = sub.add_parser('deploy', help='Git 提交并推送')
    p.add_argument('--message', default='', help='提交信息')

    # status
    p = sub.add_parser('status', help='查看流水线状态')

    args = parser.parse_args()

    # Route commands
    if args.command == 'list-series':
        cmd_list_series(args)
    elif args.command == 'dedup':
        cmd_dedup(args)
    elif args.command == 'append':
        cmd_append(args)
    elif args.command == 'download-cover':
        cmd_download_cover(args)
    elif args.command == 'verify-links':
        cmd_verify_links(args)
    elif args.command == 'generate':
        cmd_generate(args)
    elif args.command == 'deploy':
        cmd_deploy(args)
    elif args.command == 'status':
        cmd_status(args)


if __name__ == '__main__':
    main()
