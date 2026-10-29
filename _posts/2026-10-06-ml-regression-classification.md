---
layout: single
title: '회귀와 분류의 차이: 자전거 대여량·생존 여부 예측'
date: 2026-10-06 15:00:00 +0900
categories:
- machine-learning
tags:
- 회귀
- 분류
- 모델 평가
series: 주제별 복습
excerpt: '회귀와 분류의 차이: 자전거 대여량·생존 여부 예측 핵심 개념을 예제로 정리한 학습 노트입니다.'
published: false
---

> **원문 이관 상태:** 기존 네이버 블로그 글을 복사한 것이 아니라, 교수님 카페의 **자료 제목을 참고해 새로 작성한 복습용 설명**입니다. 네이버 원문과 본인 실습 코드를 확인한 뒤 보완하세요.

10월 6일 과제 제목(자전거 대여 횟수, 합격·생존 예측)을 구분해 보는 복습용 설명입니다.

## 회귀와 분류

**회귀(Regression)**는 연속적인 수치(예: 자전거 대여 횟수)를 예측할 때 사용합니다. **분류(Classification)**는 범주(예: 생존/비생존)를 예측합니다. 다만 '합격 여부'는 보통 두 범주의 **분류 문제**이므로, 수업 제목의 회귀 표기를 그대로 따라가기보다 실제 정답값의 의미부터 확인해야 합니다.

## 평가 지표

| 문제 유형 | 대표 지표 | 해석할 때 주의점 |
|---|---|---|
| 회귀 | MAE, RMSE, R² | 오차의 단위와 큰 오차의 영향 |
| 분류 | Precision, Recall, F1 | 불균형 데이터의 정확도 착시 |
| 확률 예측 | ROC-AUC, PR-AUC | 클래스 비율과 사용 목적 고려 |

## scikit-learn 기본 흐름

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# X: 특성 데이터프레임, y: 0/1 정답 시리즈가 준비되었다고 가정
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, stratify=y, random_state=42
# )
# model = RandomForestClassifier(random_state=42)
# model.fit(X_train, y_train)
# print(classification_report(y_test, model.predict(X_test)))
```

위 코드는 **학습 절차를 보여주는 틀**이며 실제 데이터를 먼저 준비해야 실행됩니다. 전처리기는 가능한 한 훈련 데이터에만 `fit`해 데이터 누수를 막습니다.
