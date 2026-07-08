#!/usr/bin/env python3
"""
批量下载封面，容错版。跳过已存在、失败时继续。
"""
import json, os, re, sys, ssl, time, urllib.request, urllib.parse

COVERS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'res', 'covers')
os.makedirs(COVERS_DIR, exist_ok=True)

REGION_SUFFIXES = [
    "(USA)", "(USA, Europe)", "(USA) (En,Fr,De)", "(USA, Europe) (En,Fr,De)",
    "(Europe)", "(Europe) (En,Fr,De)", "(Europe) (En,Fr,De,Es,It,Nl)",
    "(Japan)", "(World)", "(World) (En,Ja)", "(USA) (En,Ja)", "(Japan) (En,Ja)",
]

def sanitize(name):
    safe = re.sub(r'[\\/:*?"<>|]', '_', name)
    return safe if safe else 'cover'

def build_urls(search, system):
    urls = []
    base = search[:-4] if search.lower().endswith('.png') else search
    for suffix in [''] + REGION_SUFFIXES:
        fname = f"{base} {suffix}.png" if suffix else f"{base}.png"
        url = f"https://thumbnails.libretro.com/{urllib.parse.quote(system, safe='')}/Named_Boxarts/{urllib.parse.quote(fname, safe='')}"
        urls.append(url)
    return urls

def download(url, path, timeout=15):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            data = resp.read()
        if len(data) < 2000:
            return False
        with open(path, 'wb') as f:
            f.write(data)
        return True
    except:
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_json', help='JSON 文件')
    parser.add_argument('--workers', type=int, default=5)
    parser.add_argument('--skip-existing', action='store_true', default=True)
    args = parser.parse_args()

    with open(args.input_json, 'r', encoding='utf-8') as f:
        games = json.load(f)

    stats = {'ok': 0, 'exists': 0, 'fail': 0, 'total': len(games)}

    for i, game in enumerate(games, 1):
        name = game['name']
        search = game.get('search', '')
        system = game.get('system', '')
        safe = sanitize(name)
        out = os.path.join(COVERS_DIR, f'{safe}.png')

        if args.skip_existing and os.path.exists(out) and os.path.getsize(out) > 2000:
            stats['exists'] += 1
            if i % 100 == 0:
                print(f"  [{i}/{len(games)}] ok={stats['ok']} exists={stats['exists']} fail={stats['fail']}", flush=True)
            continue

        if not search:
            stats['fail'] += 1
            continue

        ok = False
        for url in build_urls(search, system):
            if download(url, out):
                stats['ok'] += 1
                ok = True
                if stats['ok'] % 50 == 0:
                    print(f"  [{i}/{len(games)}] ok={stats['ok']} exists={stats['exists']} fail={stats['fail']}", flush=True)
                break
            time.sleep(0.05)

        if not ok:
            stats['fail'] += 1

        if i % 500 == 0:
            print(f"  [{i}/{len(games)}] ok={stats['ok']} exists={stats['exists']} fail={stats['fail']}", flush=True)

    print(f"\nDone: ok={stats['ok']}, exists={stats['exists']}, fail={stats['fail']}, total={stats['total']}")

    # Save report
    report_path = os.path.join(os.path.dirname(args.input_json), 'cover_download_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"Report: {report_path}")

if __name__ == '__main__':
    main()
