---
layout: single
title: 과적합·드롭아웃·배치 정규화·Early Stopping·Adam
date: 2026-10-08 15:00:00 +0900
categories:
- deep-learning
tags:
- 과적합
- 드롭아웃
- 배치정규화
- Early Stopping
- Adam
series: 주제별 복습
excerpt: 과적합·드롭아웃·배치 정규화·Early Stopping·Adam 핵심 개념을 예제로 정리한 학습 노트입니다.
published: false
---

> **원문 이관 상태:** 기존 네이버 블로그 글을 복사한 것이 아니라, 교수님 카페의 **자료 제목을 참고해 새로 작성한 복습용 설명**입니다. 네이버 원문과 본인 실습 코드를 확인한 뒤 보완하세요.

10월 8~12일에 나온 학습 최적화 관련 용어를 묶어 새로 설명한 글입니다.

## 과소적합과 과적합

훈련 데이터에도 성능이 낮으면 **과소적합**, 훈련 성능은 높지만 검증 성능이 낮으면 **과적합**을 의심할 수 있습니다. 진단에는 훈련·검증 지표를 함께 보아야 합니다.

## 대표적인 대응

| 기법 | 목적 또는 역할 |
|---|---|
| Dropout | 학습 중 일부 유닛을 확률적으로 비활성화하여 정규화 효과를 줌 |
| Batch Normalization | 배치 단위 통계를 활용해 활성값을 정규화하여 학습을 돕는 층 |
| Early Stopping | 검증 지표가 더 개선되지 않을 때 학습을 중단 |
| Adam | 적응적 학습률 추정을 사용하는 경사 기반 옵티마이저 |

## Keras 예시

```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Input(shape=(10,)),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(1, activation="sigmoid"),
])
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

callback = keras.callbacks.EarlyStopping(
    monitor="val_loss", patience=5, restore_best_weights=True
)
# model.fit(X_train, y_train, validation_data=(X_val, y_val), callbacks=[callback])
```

검증셋을 분리해 `val_loss`가 실제로 기록되도록 해야 합니다. 예시는 학습 흐름을 설명하며 입력 데이터 준비는 생략했습니다.
