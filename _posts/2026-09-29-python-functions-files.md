---
layout: single
title: 함수·모듈·클래스와 with open 파일 읽기
date: 2026-09-29 15:00:00 +0900
categories:
- python
tags:
- Python
- 함수
- 클래스
- 파일 입출력
series: 주제별 복습
excerpt: 함수·모듈·클래스와 with open 파일 읽기 핵심 개념을 예제로 정리한 학습 노트입니다.
published: false
---

> **원문 이관 상태:** 기존 네이버 블로그 글을 복사한 것이 아니라, 교수님 카페의 **자료 제목을 참고해 새로 작성한 복습용 설명**입니다. 네이버 원문과 본인 실습 코드를 확인한 뒤 보완하세요.

9월 29~30일 수업 제목을 연결한 복습용 새 글입니다.

## 함수는 반복 작업을 묶는다

```python
def total_amount(amounts):
    return sum(amounts)

print(total_amount([1200, 3000, 800]))
```

인자를 입력받고 결과를 `return`하는 구조를 이해하면, 같은 코드를 복사하는 대신 재사용할 수 있습니다.

## 모듈과 클래스

모듈은 관련 코드가 담긴 파이썬 파일이고, 클래스는 데이터와 그 데이터에 적용할 동작을 하나의 구조로 묶는 방법입니다. **문제를 함수만으로 명확히 해결할 수 있다면 반드시 클래스를 만들 필요는 없습니다.**

```python
class Counter:
    def __init__(self):
        self.count = 0

    def add(self):
        self.count += 1

counter = Counter()
counter.add()
print(counter.count)
```

## `with open()`의 의미

```python
from pathlib import Path

path = Path("memo.txt")
path.write_text("첫 번째 메모\n", encoding="utf-8")

with path.open("r", encoding="utf-8") as f:
    content = f.read()
print(content)
```

`with` 블록이 끝나면 파일을 정리하므로, 직접 `close()`를 빼먹을 위험이 줄어듭니다. 파일이 없거나 인코딩이 맞지 않을 때는 예외가 발생할 수 있습니다.
