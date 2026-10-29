---
layout: single
title: 'Python 자료형 정리: list·tuple·set·dict·range'
date: 2026-09-28 15:00:00 +0900
categories:
- python
tags:
- Python
- 자료형
- 반복문
series: 주제별 복습
excerpt: 'Python 자료형 정리: list·tuple·set·dict·range 핵심 개념을 예제로 정리한 학습 노트입니다.'
published: false
---

> **원문 이관 상태:** 기존 네이버 블로그 글을 복사한 것이 아니라, 교수님 카페의 **자료 제목을 참고해 새로 작성한 복습용 설명**입니다. 네이버 원문과 본인 실습 코드를 확인한 뒤 보완하세요.

9월 28일 주제를 바탕으로 새롭게 정리한 복습 노트입니다.

## 자료형 비교

| 자료형 | 특징 | 사용 예시 |
|---|---|---|
| `list` | 순서가 있으며 요소를 수정할 수 있음 | 목록 누적 |
| `tuple` | 순서가 있으며 요소를 변경할 수 없음 | 좌표, 고정된 묶음 |
| `set` | 중복을 허용하지 않음 | 중복 제거, 집합 연산 |
| `dict` | 키와 값의 대응 | 이름별 점수 조회 |
| `range` | 정수 범위를 나타내는 객체 | 반복문의 횟수 |

## 직접 실행해 보기

```python
numbers = [1, 2, 2, 3]
print(numbers)               # [1, 2, 2, 3]
print(set(numbers))          # {1, 2, 3} (출력 순서는 집합에 따라 달라질 수 있음)

person = {"name": "Mina", "age": 24}
print(person["name"])

for i in range(3):          # 0, 1, 2
    print(i)
```

## 리스트 컴프리헨션

```python
squares = [x * x for x in range(1, 6) if x % 2 == 1]
print(squares)  # [1, 9, 25]
```

읽기 어려울 만큼 복잡해진다면 일반적인 `for`문이 더 낫습니다.

## 삼항 표현식

```python
score = 75
result = "pass" if score >= 60 else "fail"
```

조건식과 참/거짓일 때의 결과가 한 줄에 들어갑니다.
