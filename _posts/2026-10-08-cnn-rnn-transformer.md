---
layout: single
title: CNN·RNN·LSTM·Transformer를 한 번에 비교
date: 2026-10-08 15:00:00 +0900
categories:
- deep-learning
tags:
- CNN
- RNN
- LSTM
- Transformer
series: 주제별 복습
excerpt: CNN·RNN·LSTM·Transformer를 한 번에 비교 핵심 개념을 예제로 정리한 학습 노트입니다.
published: false
---

> **원문 이관 상태:** 기존 네이버 블로그 글을 복사한 것이 아니라, 교수님 카페의 **자료 제목을 참고해 새로 작성한 복습용 설명**입니다. 네이버 원문과 본인 실습 코드를 확인한 뒤 보완하세요.

10월 8일에 다룬 여러 신경망 구조의 역할을 비교하는 복습용 글입니다.

## CNN

합성곱 신경망(CNN)은 필터를 이동시켜 국소 패턴을 추출하는 구조로 이미지 작업에서 널리 쓰입니다. `Conv2D`는 특징을 추출하고 `MaxPooling2D`는 특징 맵의 공간 크기를 줄일 수 있습니다. `Flatten`은 다차원 특징을 1차원으로 펴는 역할을 합니다.

## RNN과 LSTM

RNN은 순서가 있는 입력을 단계적으로 처리하지만 긴 의존성을 학습하는 데 어려움이 생길 수 있습니다. LSTM은 게이트 구조를 사용해 정보를 유지하거나 잊을지 조절합니다.

## Transformer

Transformer는 attention 기법을 핵심으로 사용하며, 입력의 위치 정보도 함께 고려하도록 설계합니다. GPT 계열은 주로 다음 토큰을 예측하는 자기회귀 생성 작업에, BERT 계열은 양방향 문맥 표현을 학습하는 이해 작업에 강점을 갖도록 발전했습니다. 다만 모델의 실제 사용 방식은 세부 변형에 따라 다릅니다.

## 기억할 키워드

CNN: 공간적 패턴 / RNN: 순차 처리 / LSTM: 게이트 기반 기억 / Transformer: attention
