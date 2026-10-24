# Data & AI Study

GitHub Pages 주소: https://shinsangaa.github.io/

## 이 프로젝트에 있는 파일

- `_config.yml` : 블로그 이름, 주소, 작성자, 테마 설정
- `_data/navigation.yml` : 상단 메뉴
- `index.html` : 첫 화면
- `_pages/timeline.md` : 날짜별 학습 기록
- `_pages/topics.md` : 주제별 학습 목록
- `_posts/` : 글 본문 (`YYYY-MM-DD-제목.md` 형식)
- `_drafts/` : 아직 공개하지 않은 프로젝트 회고 초안
- `수업자료_목록_75건.csv` : 첨부 캡처에 나온 자료의 제목/글번호/작성일/수업기준일
- `네이버_이관_양식.csv` : 네이버 원문 수동 이관 예제
- `tools/import_naver_csv.py` : 본인 원문 CSV를 Markdown 글로 바꾸는 선택 도구
- `사용설명서.md` : 아주 자세한 적용/수정 방법

## 중요

이 폴더는 **사용자 GitHub 저장소에 아직 반영되지 않은 배포 준비본**입니다. 현재 블로그의 `index.html`을 교체합니다. 변경 전 GitHub 저장소 백업을 권장합니다.

교수님 카페 5개 캡처에서 확인한 **75개 제목**과 작성일을 기반으로 날짜별 글을 생성했습니다. 강의 원문과 네이버 블로그 원문은 읽거나 복제하지 않았습니다. 복습용 설명 13편은 새로 작성한 콘텐츠이며, 본인 학습 내용과 대조해 수정해야 합니다.

## 배포 방법 (GitHub Desktop 권장)

1. https://github.com/shinsangaa/shinsangaa.github.io 저장소를 자신의 PC에 Clone합니다.
2. 이 ZIP 압축을 푼 뒤, 안의 **모든 파일과 폴더**를 복제한 로컬 저장소 **루트**에 복사합니다 (`index.html` 덮어쓰기).
3. GitHub Desktop에서 변경된 파일 목록을 확인합니다.
4. 하단 Summary에 `Create study blog` 입력 → **Commit to main**.
5. 상단 **Push origin** 클릭.
6. GitHub 웹사이트 저장소의 Settings → Pages → Build and deployment → Source를 **Deploy from a branch**, Branch `main`, Folder `/(root)`로 설정한 뒤 저장.
7. GitHub 저장소 Actions와 Pages 배포 상태를 확인하고 https://shinsangaa.github.io/로 접속합니다. 배포 지연이 있을 수 있습니다.

## 새 글 쓰기

`_posts` 폴더에 `2026-10-24-my-new-post.md` 형태로 파일을 만들고 아래처럼 씁니다.

```markdown
---
title: "Pandas 그룹별 집계 실습"
date: 2026-10-24 15:00:00 +0900
categories: [data-analysis]
tags: [Pandas, groupby]
---

## 오늘 배운 것

이곳에 본문을 작성합니다.
```

**압축파일(zip)을 그대로 GitHub에 업로드하면 자동으로 풀리지 않습니다.** 반드시 압축을 풀고 내용물을 반영해야 합니다.
