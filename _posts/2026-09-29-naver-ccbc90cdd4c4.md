---
layout: single
title: "csv Lib 라이브러리"
date: "2026-09-29 15:00:00 +0900"
categories: [class-notes]
tags: ["네이버이관"]
toc: true
---

> 네이버 블로그에서 옮긴 글입니다. 원문 링크는 검수 후 추가하세요.

import csv

​

csv파일을 읽기 위해 설치하는 라이브러리

python 내장 라이브러리. 파이썬 기본 제공

​

.csv (Comma Seperated Values)

쉼표로 정보가 구분된 파일

---

csv 파일 읽기

import csv
with open(file_path, mode = 'r', encoding = 'utf-8-sig') as f :
reader = csv.reader(f)
next(reader) # 첫 번째 헤더 스킵
for row in reader :
print(row)
if len(row) >= 5 :
할 일 작성

​
