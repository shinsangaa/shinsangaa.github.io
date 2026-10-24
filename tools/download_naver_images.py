#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""네이버 글 검토용 Markdown의 네이버 외부 이미지를 내려받고 원래 위치의 링크를 교체.

원본 블로그 글은 공개/변경하지 않으며, 검토 폴더 안에서만 작동합니다.
실행 (GitHub 저장소 루트에서):
  py tools/download_naver_images.py
그 다음 변환된 글과 이미지 확인 후에만:
  py tools/naver_backup_to_md.py --publish
"""
from __future__ import annotations

import csv
import re
import shutil
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from html import unescape

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT.parent / 'naver_blog_review'
POSTS = REVIEW / 'posts'
IMAGES = REVIEW / 'images'
BACKUPS = REVIEW / 'backup_posts_before_images'
REPORT = REVIEW / '이미지처리결과.csv'
LIMIT = 20 * 1024 * 1024

# 사용자 작성 Markdown 이미지와 <img src="..."> 모두 대응.
MD_IMAGE = re.compile(r'!\[[^\]]*\]\(\s*<?(https?://[^\s)<>]+)>?(?:\s+[^)]*)?\)', re.I)
HTML_IMAGE = re.compile(r'(?is)<img\b[^>]*?\bsrc\s*=\s*[\'\"](https?://[^\'\"]+)[\'\"][^>]*>')
UID = re.compile(r'-naver-([0-9a-f]{12})\.md$', re.I)
KNOWN_TYPES = {'image/png': '.png', 'image/jpeg': '.jpg', 'image/jpg': '.jpg',
               'image/gif': '.gif', 'image/webp': '.webp', 'image/bmp': '.bmp',
               'image/svg+xml': '.svg'}


def from_naver(url: str) -> bool:
    parts = urlsplit(unescape(url))
    host = (parts.hostname or '').lower()
    return parts.scheme == 'https' and (host == 'pstatic.net' or host.endswith('.pstatic.net'))


def identify(data: bytes, header_type: str) -> str | None:
    """서버 응답을 이미지로 검증하고 안전한 확장자 반환."""
    if data.startswith(b'\x89PNG\r\n\x1a\n'): return '.png'
    if data.startswith(b'\xff\xd8\xff'): return '.jpg'
    if data[:6] in (b'GIF87a', b'GIF89a'): return '.gif'
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP': return '.webp'
    if data.startswith(b'BM'): return '.bmp'
    if (b'<svg' in data[:2000]) and (data.lstrip().startswith((b'<svg', b'<?xml'))): return '.svg'
    return None


def fetch(url: str) -> tuple[bytes, str]:
    request = Request(unescape(url), headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36',
        'Referer': 'https://blog.naver.com/',
        'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
    })
    with urlopen(request, timeout=25) as res:
        data = res.read(LIMIT + 1)
        if len(data) > LIMIT:
            raise ValueError('이미지 20MB 초과')
        kind = res.headers.get('Content-Type', '').split(';')[0].lower().strip()
        ext = identify(data, kind)
        if not ext:
            raise ValueError(f'이미지가 아닌 응답 또는 지원하지 않는 형식: {kind or "unknown"}')
        return data, ext


def transform_post(post: Path, records: list[dict]):
    m = UID.search(post.name)
    if not m: return (0, 0, 0)
    uid = m.group(1)
    source = post.read_text(encoding='utf-8')
    folder = IMAGES / uid
    existing = [int(x.group(1)) for f in folder.glob('img-*.*')
                if (x := re.match(r'img-(\d+)\.', f.name))]
    number = max(existing, default=0) + 1
    results: dict[str, str | None] = {}
    success = failure = skip = 0

    def replace(match: re.Match) -> str:
        nonlocal number, success, failure, skip
        url = match.group(1)
        if not from_naver(url):
            if url not in results:
                results[url] = None
                records.append({'post':post.name,'status':'SKIP_NOT_NAVER', 'saved_file':'', 'url':url,'note':'네이버 이미지 호스트가 아니거나 HTTPS 아님'})
                skip += 1
            return match.group(0)
        if url not in results:
            try:
                data, ext = fetch(url)
                folder.mkdir(parents=True, exist_ok=True)
                target = folder / f'img-{number:03d}{ext}'
                while target.exists():
                    number += 1
                    target = folder / f'img-{number:03d}{ext}'
                target.write_bytes(data)
                newref = f'../images/{uid}/{target.name}'
                results[url] = newref
                records.append({'post':post.name, 'status':'SAVED','saved_file':str(target),'url':url,'note':''})
                success += 1
                number += 1
            except (OSError, HTTPError, URLError, ValueError) as e:
                results[url] = None
                records.append({'post':post.name, 'status':'FAILED','saved_file':'','url':url,'note':str(e)[:200]})
                failure += 1
        newref = results[url]
        return match.group(0).replace(url, newref, 1) if newref else match.group(0)

    newtext = MD_IMAGE.sub(replace, source)
    newtext = HTML_IMAGE.sub(replace, newtext)
    if newtext != source:
        BACKUPS.mkdir(parents=True, exist_ok=True)
        backup = BACKUPS / post.name
        if not backup.exists(): shutil.copy2(post, backup)
        post.write_text(newtext, encoding='utf-8')
    return success, failure, skip


def main():
    if not (ROOT / '_config.yml').exists() or not POSTS.is_dir():
        raise SystemExit('블로그 저장소의 tools 폴더에 스크립트를 넣고, 검토용 posts 폴더도 있는지 확인하세요.')
    all_results = []
    total = [0, 0, 0]
    for post in sorted(POSTS.glob('*.md')):
        numbers = transform_post(post, all_results)
        for i in range(3): total[i] += numbers[i]
        if sum(numbers): print(f'{post.name}: 저장 {numbers[0]} / 실패 {numbers[1]} / 기타 외부 {numbers[2]}')
    with REPORT.open('w', encoding='utf-8-sig', newline='') as fp:
        writer = csv.DictWriter(fp, fieldnames=['post','status','saved_file','url','note'])
        writer.writeheader(); writer.writerows(all_results)
    print(f'\n합계: 이미지 저장 {total[0]}개 / 실패 {total[1]}개 / 네이버 외부가 아닌 이미지 {total[2]}개')
    print(f'이미지 저장 위치: {IMAGES}')
    print(f'상태표: {REPORT}')
    print('검토용 Markdown과 이미지에만 반영되었습니다. GitHub 공개는 아직 아닙니다.')
    if total[1] or total[2]:
        print('실패/기타 외부 이미지 URL은 그대로 유지했습니다. 보고서 확인 후 수동 처리하세요.')
    print('검토 후 기존 변환 프로그램의 --publish로 이미지와 글을 게시용으로 복사할 수 있습니다.')


if __name__ == '__main__':
    main()
