# Data & AI Study

Python, 데이터 분석, 머신러닝, 딥러닝, LLM 실습을 날짜별·주제별로 정리한 학습 블로그입니다.

- 블로그: https://shinsangaa.github.io/
- 기반: Jekyll + Minimal Mistakes (GitHub Pages)

## 폴더 구성

- `_config.yml` : 블로그 이름, 주소, 작성자, 테마 설정
- `_data/navigation.yml` : 상단 메뉴
- `index.html` : 첫 화면
- `_pages/timeline.md` : 날짜별 학습 기록
- `_pages/topics.md` : 주제별 학습 목록
- `_pages/projects.md` : 프로젝트 목록
- `_pages/about.md` : 소개
- `_posts/` : 글 본문
- `_drafts/` : 아직 공개하지 않은 초안
- `assets/css/custom.css` : 화면 스타일
- `assets/images/` : 글에 넣는 이미지

## 카테고리

글마다 `categories`에 아래 이름 중 하나를 적습니다. 주제별 학습 목록은 이 값으로 글을 모읍니다.

| 값 | 주제 |
| --- | --- |
| `llm-agent` | LLM 기초 |
| `python` | Python 기초 |
| `data-analysis` | 데이터 분석 · 시각화 |
| `machine-learning` | 머신러닝 |
| `deep-learning` | 딥러닝 |
| `llm-service` | LLM 서비스 · 멀티 에이전트 |
| `data-engineering` | DB · 빅데이터 |
| `projects` | 프로젝트 |
| `study-notes` | 수업 메모 |
| `error-notes` | 오류 노트 |
| `reading` | 뉴스 · 읽을거리 |

## 새 글 쓰기

`_posts` 폴더에 `YYYY-MM-DD-class-log.md` 형태로 파일을 만듭니다. 같은 날 글이 더 있으면 `YYYY-MM-DD-class-log-주제.md`처럼 뒤에 주제를 붙입니다.

```markdown
---
layout: single
title: "4. 글 제목"
date: 2026-11-11 09:00:00 +0900
course_date: '2026-11-11'
categories: [data-engineering]
tags: ["태그1", "태그2"]
toc: true
toc_sticky: true
published: true
---

## 1. 오늘 배운 내용

이곳에 본문을 작성합니다.
```

- `course_date`가 있는 글만 날짜별 학습 기록에 나옵니다. 값은 따옴표로 감쌉니다.
- 아직 공개하지 않을 글은 `published: false`로 둡니다. 저장소가 공개라서, 화면에서만 숨겨지고 파일은 GitHub에서 보입니다.

## 블로그에 반영하기

```bash
git add -A
git commit -m "docs: 2026-11-11 포스트 추가"
git push origin main
```

Push 후 1~2분 뒤 저장소의 Actions 탭에서 배포가 끝났는지 확인합니다.