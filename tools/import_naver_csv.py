"""네이버에서 사용자가 직접 복사해 온 본인 글(CSV)을 Jekyll Markdown으로 변환.
불특정 블로그를 자동 크롤링하지 않습니다.
실행: python tools/import_naver_csv.py 네이버_이관_양식.csv
"""
from pathlib import Path
from datetime import datetime
import csv, json, re, sys

ALLOWED = {'python','data-analysis','data-visualization','machine-learning','deep-learning','llm-agent','projects','class-notes'}

def quoted(v):
    return json.dumps(str(v), ensure_ascii=False)

def process(csv_path):
    out = Path('_posts')
    out.mkdir(exist_ok=True)
    with open(csv_path, encoding='utf-8-sig', newline='') as f:
        for i, row in enumerate(csv.DictReader(f), 1):
            if not row.get('date','').strip() or not row.get('title','').strip() or not row.get('content','').strip():
                print(f'[SKIP] {i}행: 날짜/제목/내용 중 비어 있음')
                continue
            try:
                day = datetime.strptime(row['date'].strip(), '%Y-%m-%d').date().isoformat()
            except ValueError:
                print(f'[SKIP] {i}행: 날짜 형식은 YYYY-MM-DD')
                continue
            cat = row.get('category','').strip()
            if cat not in ALLOWED:
                print(f'[SKIP] {i}행: category는 {sorted(ALLOWED)} 중 하나여야 함')
                continue
            title = row['title'].strip()
            tags = [x.strip() for x in row.get('tags','').split(';') if x.strip()]
            source = row.get('source_url','').strip()
            if source and not source.startswith(('http://','https://')):
                print(f'[SKIP] {i}행: source_url 형식 오류')
                continue
            name = f'{day}-naver-import-{i:03d}.md'
            path = out / name
            if path.exists():
                print(f'[SKIP] {path}: 기존 파일 보호')
                continue
            fm = [
                '---', f'title: {quoted(title)}', f'date: {quoted(day+" 15:00:00 +0900")}',
                f'categories: [{quoted(cat)}]',
                'tags: [' + ', '.join(quoted(t) for t in tags) + ']',
                'series: "네이버 이관 글"', 'toc: true',
                '---', ''
            ]
            note = (f'> 원문: {source}\n\n' if source else '')
            path.write_text('\n'.join(fm) + note + row['content'].strip()+'\n', encoding='utf-8')
            print(f'[OK] {path}')

if __name__=='__main__':
    if len(sys.argv)!=2:
        print('사용법: python tools/import_naver_csv.py 네이버_이관_양식.csv')
        sys.exit(2)
    process(sys.argv[1])
