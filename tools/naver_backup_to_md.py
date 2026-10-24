#!/usr/bin/env python3
"""네이버 공식 콘텐츠 백업(HTML/첨부 이미지) -> Jekyll 검토용 Markdown.

사용법(저장소 루트에서):
  py tools/naver_backup_to_md.py "C:\\Users\\...\\Downloads\\네이버백업압축해제폴더"
  py tools/naver_backup_to_md.py --publish
준비 단계는 tools/naver_review 내에만 씁니다. --publish 전에는 게시하지 않습니다.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
from hashlib import sha1
import html as htmlmod
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
import zipfile

try:
    from bs4 import BeautifulSoup
    from markdownify import markdownify as html_to_md
except ImportError:
    raise SystemExit("필수 라이브러리가 없습니다. 실행: py -m pip install beautifulsoup4 markdownify")

ROOT = Path(__file__).resolve().parent.parent
REVIEW = ROOT.parent / 'naver_blog_review'
REVIEW_POSTS = REVIEW / 'posts'
REVIEW_IMAGES = REVIEW / 'images'
PUBLIC_POSTS = ROOT / '_posts'
PUBLIC_IMAGES = ROOT / 'assets' / 'images' / 'naver-import'
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'}
DATE_PATTERN = re.compile(r'(?<!\d)(20\d{2})[.\-/년_ ]+\s*(0?[1-9]|1[0-2])[.\-/월_ ]+\s*(0?[1-9]|[12]\d|3[01])(?!\d)')
DATE_COMPACT = re.compile(r'(?<!\d)(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(?!\d)')


def normalize_date(text: str) -> str | None:
    for pattern in (DATE_PATTERN, DATE_COMPACT):
        m = pattern.search(str(text or ''))
        if m:
            date = f'{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}'
            try:
                datetime.strptime(date, '%Y-%m-%d')
                return date
            except ValueError:
                pass
    return None


def slug(s: str, limit: int = 72) -> str:
    s = re.sub(r'[^\w\uac00-\ud7a3-]+', '-', s, flags=re.UNICODE).strip('-_')
    return (s[:limit].rstrip('-_') or 'untitled')


def yaml_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ') + '"'


def classify(title: str) -> str:
    s = title.lower()
    if any(k in s for k in ['streamlit','이상거래','프로젝트','프로토타입','팀 프로젝트']): return 'projects'
    if any(k in s for k in ['llm','mcp','agent','에이전트','프롬프트','langchain','langgraph','rag','transformer','gpt','bert','파인튜닝','파인 튜닝']): return 'llm-agent'
    if any(k in s for k in ['cnn','rnn','lstm','keras','tensorflow','딥러닝','신경망','dropout','softmax','mnist','batch normalization']): return 'deep-learning'
    if any(k in s for k in ['lightgbm','xgboost','random forest','decision tree','머신러닝','회귀','분류 모델','scikit','앙상블','과적합']): return 'machine-learning'
    if any(k in s for k in ['matplotlib','seaborn','시각화','그래프','pyplot']): return 'data-visualization'
    if any(k in s for k in ['pandas','numpy','데이터 분석','통계','상관분석','데이터프레임']): return 'data-analysis'
    if any(k in s for k in ['python','파이썬','리스트','함수','튜플','딕셔너리','클래스']): return 'python'
    return 'class-notes'


def source_url(soup: BeautifulSoup) -> str:
    for tag in soup.find_all('meta', attrs={'property': 'og:url'}):
        url = tag.get('content', '')
        if 'blog.naver.com/' in url:
            return url.strip()
    for a in soup.find_all('a', href=True):
        href = a['href']
        if re.search(r'blog\.naver\.com/[^/]+/\d+', href): return href
    return ''


def extract_date(soup: BeautifulSoup, relative_path: Path) -> str | None:
    # 게시 날짜가 명시된 필드를 먼저 사용. 본문 학습일은 게시일과 다를 수 있음.
    for selector in ('meta[property="article:published_time"]', 'meta[itemprop="datePublished"]',
                     'meta[name="date"]', 'meta[name="pubdate"]', 'time[datetime]'):
        tag = soup.select_one(selector)
        if tag:
            val = tag.get('content') or tag.get('datetime') or ''
            date = normalize_date(val)
            if date: return date
    for script in soup.select('script[type="application/ld+json"]'):
        m = re.search(r'"datePublished"\s*:\s*"([^"]+)', script.get_text())
        if m:
            date = normalize_date(m.group(1))
            if date: return date
    # 파일명/폴더명에 표기된 날짜 사용.
    for part in [relative_path.stem, *reversed(relative_path.parts[:-1])]:
        date = normalize_date(part)
        if date: return date
    # '작성일/등록일/발행일'로 명시된 경우에만 문서 텍스트에서 추출.
    text = soup.get_text(' ', strip=True)
    for m in re.finditer(r'(작성일|발행일|등록일|published|created)\s*[:：]?\s*.{0,12}', text, re.I):
        date = normalize_date(m.group())
        if date: return date
    return None


def folder_title(filepath: Path) -> str | None:
    # 네이버 공식 백업 예: 20260929_224425870048_1. LLM으로 어떤 일을 할 수 있을까/index.html
    # index.html 자체가 글이므로 상위 폴더 이름의 제목 부분도 참고합니다.
    parent = filepath.parent.name
    m = re.match(r'^20\d{6}[_\-]\d{5,}[_\-](.+)$', parent)
    if m and m.group(1).strip():
        return m.group(1).strip()
    return None


def extract_title(soup: BeautifulSoup, filepath: Path) -> str:
    for q in ('meta[property="og:title"]', 'meta[name="title"]'):
        tag = soup.select_one(q)
        if tag and tag.get('content', '').strip():
            return htmlmod.unescape(tag['content'].strip())[:200]
    for q in ('h1', 'h2', 'title'):
        tag = soup.select_one(q)
        if tag and tag.get_text(' ', strip=True):
            val = tag.get_text(' ', strip=True)
            if val.lower() not in ('naver', 'blog', '네이버 블로그') and 'naver' not in val.lower():
                return htmlmod.unescape(val)[:200]
    return (folder_title(filepath) or filepath.stem)[:200]


def extract_body(soup: BeautifulSoup):
    for selector in ('.se-main-container', '#postViewArea', '.se3_view', '.se_doc_viewer',
                     'article', '.post-view', '.post-content', 'main', 'body'):
        body = soup.select_one(selector)
        if body:
            return body
    return soup


def safe_img_file(root: Path, origin: Path, src: str, lookup: dict[str, list[Path]]) -> Path | None:
    if not src or src.startswith(('http:', 'https:', 'data:', '//', '#')):
        return None
    from urllib.parse import unquote, urlsplit
    src = unquote(urlsplit(src).path)
    if not src or src.startswith('/') or '\x00' in src:
        return None
    candidate = (origin.parent / src).resolve()
    if candidate.is_file() and candidate.is_relative_to(root.resolve()):
        return candidate
    # 백업 폴더 안에 같은 파일명으로 저장된 이미지 찾기. 중복이면 추측하지 않음.
    matches = lookup.get(Path(src).name.lower(), [])
    return matches[0] if len(matches) == 1 else None


def convert_one(root: Path, html_path: Path, lookup: dict[str, list[Path]]) -> dict:
    rel = html_path.relative_to(root)
    # html parser는 인코딩을 감지합니다.
    soup = BeautifulSoup(html_path.read_bytes(), 'html.parser')
    title = extract_title(soup, html_path)
    if html_path.name.lower() == 'index.html' and folder_title(html_path):
        # 공식 백업에서 메타 제목이 누락된 경우도 정확한 글 제목을 유지합니다.
        title = folder_title(html_path)
    date = extract_date(soup, rel)
    cat = classify(title)
    uid = sha1(str(rel).encode('utf-8')).hexdigest()[:12]
    body = extract_body(soup)
    # HTML 백업에 있는 스크립트/네비/푸터 등 제거.
    for bad in body.select('script, style, nav, form, button, noscript, footer'):
        bad.decompose()
    saved_images = 0
    external_images = 0
    for image in body.find_all('img'):
        src = image.get('data-lazy-src') or image.get('data-src') or image.get('src') or ''
        local = safe_img_file(root, html_path, src, lookup)
        if local and local.suffix.lower() in IMAGE_EXTS:
            staged = REVIEW_IMAGES / uid / f'img-{saved_images+1:03d}{local.suffix.lower()}'
            staged.parent.mkdir(parents=True, exist_ok=True)
            if not staged.exists(): shutil.copy2(local, staged)
            image['src'] = f'../images/{uid}/{staged.name}'
            saved_images += 1
        else:
            if src.startswith(('https://', 'http://')): external_images += 1
            image['src'] = src
        for key in ['data-src', 'data-lazy-src', 'srcset']:
            image.attrs.pop(key, None)
    markdown = html_to_md(str(body), heading_style='ATX', bullets='-', escape_underscores=False)
    markdown = re.sub(r'\n{4,}', '\n\n\n', markdown).strip()
    if len(re.sub(r'\W+', '', markdown)) < 10:
        return {'status':'SKIP_EMPTY', 'file':str(rel), 'title':title, 'date':date or '', 'category':cat,
                'local_images':saved_images, 'external_images':external_images, 'review_file':''}
    # 문서 외부 HTML 메타에 있던 원문 링크 표시
    original = source_url(soup)
    fm = [
        '---', 'layout: single', f'title: {yaml_quote(title)}',
    ]
    if date:
        fm.append(f'date: {yaml_quote(date + " 15:00:00 +0900")}')
    fm += [f'categories: [{cat}]', 'tags: ["네이버이관"]', 'toc: true', '---', '']
    intro = f'> 네이버 블로그에서 옮긴 글입니다. ' + (f'[원문 링크]({original})' if original else '원문 링크는 검수 후 추가하세요.')
    fm += [intro, '', markdown, '']
    md_name = f'{date}-naver-{uid}.md' if date else f'날짜확인필요-naver-{uid}.md'
    out = REVIEW_POSTS / md_name
    if out.exists():
        status = 'SKIP_EXISTS'
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text('\n'.join(fm), encoding='utf-8')
        status = 'READY' if date else 'CHECK_DATE'
    return {'status':status, 'file':str(rel), 'title':title, 'date':date or '', 'category':cat,
            'local_images':saved_images, 'external_images':external_images, 'review_file':str(out)}


def prepare(source: Path):
    if not (ROOT / '_config.yml').exists() or not PUBLIC_POSTS.is_dir():
        raise SystemExit('스크립트를 실제 GitHub 블로그 저장소의 tools 폴더에 넣었는지 확인하세요.')
    if not source.exists(): raise SystemExit(f'백업 파일/폴더를 찾지 못했습니다: {source}')
    with tempfile.TemporaryDirectory(prefix='naver_backup_') as temp:
        root = Path(temp)
        if source.is_dir():
            root = source.resolve()
        elif source.suffix.lower() == '.zip':
            with zipfile.ZipFile(source) as archive:
                entries = archive.infolist()
                if len(entries) > 50000 or sum(x.file_size for x in entries) > 5 * 1024**3:
                    raise SystemExit('매우 큰 백업입니다. ZIP을 먼저 별도 폴더에 압축해제하여 폴더 경로를 지정하세요.')
                for member in entries:
                    p = PurePosixPath(member.filename.replace('\\', '/'))
                    if member.is_dir() or p.is_absolute() or '..' in p.parts: continue
                    suffix = p.suffix.lower()
                    if suffix not in ('.html', '.htm', *IMAGE_EXTS): continue
                    dest = root.joinpath(*p.parts)
                    if not dest.resolve().is_relative_to(root.resolve()): continue
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        with archive.open(member) as s, dest.open('wb') as d:
                            shutil.copyfileobj(s, d)
                    except RuntimeError as e:
                        if 'encrypted' in str(e).lower() or 'password' in str(e).lower():
                            raise SystemExit(
                                '네이버 ZIP은 암호로 보호되어 있습니다. '
                                '먼저 7-Zip/반디집 등으로 백업 ZIP을 압축 해제한 뒤, '
                                '압축 해제된 폴더의 경로를 인수로 지정하세요. '
                                '개인 회원 압축 암호는 네이버에 등록된 생년월일 8자리입니다. '
                                '비밀번호를 코드나 GitHub에 입력하지 마세요.'
                            ) from e
                        raise
        else:
            raise SystemExit('ZIP 또는 백업 압축을 풀어놓은 폴더 경로를 지정하세요.')
        all_files = [x for x in root.rglob('*') if x.is_file()]
        def is_blog_html(path: Path) -> bool:
            rel = path.relative_to(root)
            if path.suffix.lower() not in ('.html', '.htm'):
                return False
            parts = rel.parts
            if any(re.search(r'댓글|comment|reply', part, re.I) for part in parts):
                return False
            # 공식 네이버 백업의 실제 게시글은 게시글별 폴더 속 index.html 입니다.
            # 따라서 모든 index.html을 제외하던 기존 필터를 수정했습니다.
            if path.name.lower() == 'index.html':
                return len(parts) >= 2 and any(normalize_date(part) for part in parts[:-1])
            return True

        html_files = [x for x in all_files if is_blog_html(x)]
        if not html_files: raise SystemExit('게시글 HTML을 찾지 못했습니다. 공식 콘텐츠 백업 ZIP인지 확인하세요.')
        lookup = {}
        for f in all_files:
            if f.suffix.lower() in IMAGE_EXTS:
                lookup.setdefault(f.name.lower(), []).append(f)
        results = []
        for i, f in enumerate(sorted(html_files), 1):
            try:
                result = convert_one(root, f, lookup)
                results.append(result)
                print(f'[{i}/{len(html_files)}] {result["status"]}: {result["title"][:48]}')
            except Exception as e:
                results.append({'status':f'ERROR: {str(e)[:100]}', 'file':str(f.relative_to(root)),
                                'title':'', 'date':'', 'category':'', 'local_images':0,
                                'external_images':0, 'review_file':''})
        REVIEW.mkdir(parents=True, exist_ok=True)
        report = REVIEW / '변환결과.csv'
        with report.open('w', encoding='utf-8-sig', newline='') as fp:
            w = csv.DictWriter(fp, fieldnames=['status','file','title','date','category','local_images','external_images','review_file'])
            w.writeheader(); w.writerows(results)
        print(f'\n변환 시도: {len(results)}편 / 날짜 확인 필요: {sum(not x["date"] for x in results)}편')
        print(f'검토 위치: {REVIEW_POSTS}\n리포트: {report}')
        print('아직 공개하지 않았습니다. 검수 후 다음 명령으로 발행: py tools/naver_backup_to_md.py --publish')


def publish():
    if not REVIEW_POSTS.is_dir():
        raise SystemExit('검토용 파일이 없습니다. 먼저 ZIP을 변환하세요.')
    count = 0
    for post in sorted(REVIEW_POSTS.glob('*.md')):
        if not re.match(r'^20\d{2}-\d{2}-\d{2}-naver-', post.name):
            print(f'[HOLD] 게시 날짜 미확인: {post.name}')
            continue
        dest = PUBLIC_POSTS / post.name
        if dest.exists():
            print(f'[SKIP] 원본 보호 (동일 파일 존재): {dest.name}')
            continue
        content = post.read_text(encoding='utf-8')
        image_refs = re.findall(r'\.\./images/([0-9a-f]{12})/(img-\d+\.[\w]+)', content)
        for uid, filename in set(image_refs):
            src = REVIEW_IMAGES / uid / filename
            if not src.is_file():
                print(f'[WARN] 이미지가 존재하지 않음: {src}'); continue
            target = PUBLIC_IMAGES / uid / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists(): shutil.copy2(src, target)
            content = content.replace(f'../images/{uid}/{filename}',
                                      "{{ '/assets/images/naver-import/" + uid + '/' + filename + "' | relative_url }}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding='utf-8')
        count += 1
        print(f'[PUBLISH PREPARED] {dest.relative_to(ROOT)}')
    print(f'\n게시용 파일 생성: {count}편. 실제 공개는 GitHub Desktop에서 Commit/Push한 이후입니다.')


def main():
    p = argparse.ArgumentParser(description='네이버 공식 콘텐츠 백업 HTML -> GitHub Jekyll Markdown')
    p.add_argument('backup', nargs='?', help='네이버 콘텐츠 백업 ZIP 또는 폴더')
    p.add_argument('--publish', action='store_true', help='검토한 Markdown만 _posts로 복사합니다. 기존 파일은 보호')
    args = p.parse_args()
    if args.publish: publish()
    elif args.backup: prepare(Path(args.backup).expanduser())
    else: p.print_help()

if __name__ == '__main__': main()
