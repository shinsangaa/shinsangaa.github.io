---
layout: single
title: 'NumPy와 Pandas: 데이터 분석 첫 실습'
date: 2026-10-01 15:00:00 +0900
categories:
- data-analysis
tags:
- NumPy
- Pandas
- 데이터프레임
series: 주제별 복습
excerpt: 'NumPy와 Pandas: 데이터 분석 첫 실습 핵심 개념을 예제로 정리한 학습 노트입니다.'
---

> **원문 이관 상태:** 기존 네이버 블로그 글을 복사한 것이 아니라, 교수님 카페의 **자료 제목을 참고해 새로 작성한 복습용 설명**입니다. 네이버 원문과 본인 실습 코드를 확인한 뒤 보완하세요.

10월 1일 NumPy·Pandas 자료 제목에 맞춰 정리한 복습용 글입니다.

## NumPy와 Pandas의 역할

- **NumPy:** 다차원 배열과 수치 계산에 강점이 있습니다.
- **Pandas:** 열 이름과 인덱스가 있는 데이터프레임으로 표 형태 데이터를 쉽게 다룹니다.

## 기초 코드

```python
import numpy as np
import pandas as pd

arr = np.array([10, 20, 30])
print(arr.mean())

df = pd.DataFrame({
    "month": ["01", "01", "02", "02"],
    "type": ["택시", "배달", "택시", "배달"],
    "amount": [10000, 15000, 20000, 25000],
})
print(df.groupby("month")["amount"].mean())
print(df.groupby("type")["amount"].sum())
```

## 분석 순서

데이터 구조 확인(`head`, `info`) → 결측치·이상치 점검 → 그룹별 집계 → 시각화 → 결과 해석으로 진행하면 정리가 수월합니다. 누락된 값을 평균으로 채우는 것이 언제나 최선은 아니므로 데이터 의미를 먼저 확인합니다.

## 실습 연결

병원 노쇼 분석처럼 결과가 두 부류인 과제를 진행한다면, **예측 대상의 의미와 입력 정보가 실제 예측 시점에 이용 가능한지**부터 정의해야 합니다.
