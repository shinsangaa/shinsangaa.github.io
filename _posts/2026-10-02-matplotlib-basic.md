---
layout: single
title: Matplotlib으로 기본 그래프 그리기
date: 2026-10-02 15:00:00 +0900
categories:
- data-visualization
tags:
- Python
- Matplotlib
- 시각화
series: 주제별 복습
excerpt: Matplotlib으로 기본 그래프 그리기 핵심 개념을 예제로 정리한 학습 노트입니다.
---

> **원문 이관 상태:** 기존 네이버 블로그 글을 복사한 것이 아니라, 교수님 카페의 **자료 제목을 참고해 새로 작성한 복습용 설명**입니다. 네이버 원문과 본인 실습 코드를 확인한 뒤 보완하세요.

10월 1~2일 시각화 참고자료 주제를 바탕으로 작성한 실습 노트입니다.

## 그래프 종류 고르기

- 시간에 따른 변화: 선그래프
- 범주별 크기 비교: 막대그래프
- 수치형 변수의 분포: 히스토그램
- 두 수치형 변수 사이의 관계: 산점도

## 예제

```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr"]
values = [18, 21, 17, 26]

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(months, values, marker="o")
ax.set_title("Monthly Usage")
ax.set_xlabel("Month")
ax.set_ylabel("Count")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

한글이 깨지는 환경이라면 한글 폰트 설치 여부와 `matplotlib`의 폰트 설정을 확인합니다. 숫자 차이를 과장하지 않도록 축 범위도 확인하는 습관이 필요합니다.

## 그래프 읽기

수치 비교가 목적이라면 모양보다 **단위·축·기간·표본 수**가 더 중요합니다. 상관관계가 곧 인과관계는 아니라는 점도 잊지 않습니다.
