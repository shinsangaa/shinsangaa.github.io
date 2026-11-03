---
layout: single
title: "2026-11-03 | 데이터베이스(DB) 수업 정리"
date: 2026-11-03 09:00:00 +0900
course_date: '2026-11-03'
categories: [class-notes]
tags: [데이터베이스, DB]
series: "수업일지"
toc: true
toc_sticky: true
published: true
excerpt: "2026년 11월 3일 데이터베이스 수업에서 배운 개념과 실습을 기록합니다."
---

> **기록일:** 2026-11-03  
> **학습 분야:** 데이터베이스(DB)  
> **기록 원칙:** 실제 수업에서 다룬 내용과 직접 실행한 코드만 추가합니다.

## 1. 오늘 배운 내용

- **수업 주제:** 관계형 데이터베이스 기초와 MySQL 고급 쿼리, DB 프로그래밍
- **핵심 개념:** (핵심 내용 2~3개 작성)
- **사용한 DBMS/도구:** MySQL, .sql 예제파일
- **교재:** https://wikidocs.net/book/21972  
[DMDG] 실전 MySQL & 관계형 데이터베이스(RDBMS) 아키텍처부터 NoSQL 빅데이터까지 마스터 바이블

## 2. 핵심 개념 정리

### 2-1. 관계형 데이터 모델의 핵심 용어
- 테이블명 = 릴레이션
- 필드명, 컬럼명 = 속성(Attribute)
- 필드 개수, 컬럼 개수 = 차수(Degree)
- 행 = 카디널리티, 레코드, 튜플


### 2-2. 데이터 무결성 제약조건 3대 원칙
- 개체 무결성 (Entity Integrity):  
기본키를 구성하는 어떤 속성도 NULL 값을 가질 수 없으며, 중복값을 가질 수 없습니다.  
이유: 튜플을 식별할 수 없는 개체는 DB에 존재할 가치가 없기 때문입니다.
- 참조 무결성 (Referential Integrity):  
외래키 값은 참조하는 부모 릴레이션의 기본키 값과 반드시 일치하거나, 아니면 NULL이어야 합니다.  
이유: 존재하지 않는 부모 레코드를 가리키는 유령 데이터(Dangling Pointer)를 방지하기 위함입니다.
- 도메인 무결성 (Domain Integrity):  
튜플의 모든 속성값은 해당 속성에 정의된 도메인의 데이터 타입, 길이, 허용 범위, 기본값(DEFAULT), 널 허용 여부(NOT NULL) 규칙을 엄격히 준수해야 합니다.

### 2-3. RDBMS 사용 시 순서
#### MySQL
- (1) database create
- (2) use database : 사용할 DB 선택
- (3) create Table (컬럼명, data type) : 최소 1개 이상의 컬럼 있어야 테이블 생성 가능
#### Oracle
- 사용자 계정 생성 후 바로 Table 생성
- 사용자에게 권한을 줌 (GRANT)

### 2-4. 관계대수의 본질과 폐포 성질
- 폐포 성질 (Closure Property):  
관계대수 연산의 입력 대상은 반드시 릴레이션이고, 연산 결과 또한 반드시 새로운 릴레이션

### 2-5. 일반 집합 연산자와 합병 가능(Union-Compatible) 조건
- 두 릴레이션의 차수(속성 개수)가 일치해야 함
- 대응하는 속성의 도메인(데이터 타입)이 상호 호환되어야 함

### 2-6. (금융권 필수) Deadlock
- 두 트랜잭션이 서로 상대방이 쥐고 있는 자원의 락(Lock)이 풀리기만을 무한정 기다리는 교착 상태  
ex. 한 계좌에서 동시에 입금과 출금이 이뤄질 때, 입금이 먼저 처리된 후 출금이 되도록 Deadlock
- (최종 프로젝트에서 Deadlock 필수로 사용해야 한다.)

### 2-7. VARCHAR(4) vs CHAR(4)
- VARCHAR(4) : 가변성. 줄일 수 있음
- CHAR(4) : 고정
- (한글 한글자는 2바이트)

### 2-8. Subquery
- 서브쿼리는 내부 쿼리부터 먼저 실행
- WHERE절에 집계함수 불가. 사용하고 싶다면 서브쿼리 활용
```sql
WHERE price = (SELECT MAX(price) FROM Book);
```
- 그룹화는 시간이 오래 걸리기 때문에, GROUP BY보다 중첩쿼리가 더 나은 선택일 수 있다.
- 같은 Book 테이블을 b1, b2로 나눠 쓸 수 있다.

### 2-9. 가상 테이블 뷰(View)
- 뷰 테이블은 SELECT문으로 조회 가능하다.

## 3. SQL 및 데이터베이스 실습
실행할 코드만 선택 후 Ctrl + Shift + Enter

```sql
SELECT DISTINCT 이름, 이메일 FROM 학생;
DISTINCT -- 중복값 허용X
```

```sql
-- 실습용 데이터베이스 및 Book 테이블 생성
CREATE DATABASE IF NOT EXISTS madang DEFAULT CHARACTER SET utf8mb4; -- madang이라는 DB가 있으면 생성
USE madang;

-- 1. Book(도서) 테이블 생성
DROP TABLE IF EXISTS Book; -- 기존에 Book테이블이 있다면 삭제
CREATE TABLE Book (
    bookid      INT PRIMARY KEY,
    bookname    VARCHAR(60) NOT NULL,
    publisher   VARCHAR(40) NOT NULL,
    price       INT NOT NULL
);

-- 2. 실습용 도서 데이터 10건 삽입
INSERT INTO Book VALUES(1, '축구의 역사', '굿스포츠', 7000);
INSERT INTO Book VALUES(2, '축구아는 여자', '나무수', 13000);
INSERT INTO Book VALUES(3, '축구의 이해', '대한미디어', 22000);
INSERT INTO Book VALUES(4, '골프 바이블', '대한미디어', 35000);
INSERT INTO Book VALUES(5, '피겨 교본', '굿스포츠', 8000);
INSERT INTO Book VALUES(6, '역도 단계별기술', '굿스포츠', 6000);
INSERT INTO Book VALUES(7, '야구의 추억', '이상미디어', 20000);
INSERT INTO Book VALUES(8, '야구를 부탁해', '이상미디어', 13000);
INSERT INTO Book VALUES(9, '올림픽 이야기', '삼성당', 7500);
INSERT INTO Book VALUES(10, 'Olympic Champions', 'Pearson', 13000);
```

**컬럼 선택과 별칭(Alias)**
```sql
-- 도서 테이블에서 책이름과 출판사를 조회하고 한글 별칭 부여
SELECT bookname AS 도서명, publisher AS 출판사, price AS "정가(원)"
FROM Book;

-- 중복 제거 (DISTINCT)
SELECT DISTINCT publisher
FROM Book;
```

**조건절(WHERE)의 다양한 필터링 연산자**
```sql
-- 1. 비교 연산자 및 범위 검색 (BETWEEN a AND b)
-- 가격이 10,000원 이상 20,000원 이하인 도서 검색
SELECT * FROM Book
WHERE price BETWEEN 10000 AND 20000;

-- 2. 목록 포함 검색 (IN)
-- 출판사가 '굿스포츠' 또는 '대한미디어'인 도서 검색
SELECT * FROM Book
WHERE publisher IN ('굿스포츠', '대한미디어');

-- 3. 패턴 매칭 검색 (LIKE %와 _)
-- %: 임의의 0개 이상 문자 / _: 정확히 1개 문자
SELECT * FROM Book
WHERE bookname LIKE '%축구%';     -- '축구'가 포함된 모든 도서

SELECT * FROM Book
WHERE bookname LIKE '_구%';       -- 두 번째 글자가 '구'인 도서
```

**test.sql (1)**
```sql
CREATE DATABASE IF NOT EXISTS madang DEFAULT CHARACTER SET utf8mb4;
SHOW DATABASES;
```
**실행 결과**
|  | Database |
|---|---|
|  | information_schema |
|  | madang |
|  | mysql |
|  | performance_schema |
|  | sakila |
|  | sys |
|  | world |

- mysql, performance_schema : 절대 건들면 안됨
- sakila, world : 학습용 데이터

**test.sql (2)**
```sql
USE madang;
CREATE TABLE Book (
    bookid      INT PRIMARY KEY,
    bookname    VARCHAR(60) NOT NULL,
    publisher   VARCHAR(40) NOT NULL,
    price       INT NOT NULL
);
SHOW tables;
```
**실행 결과**
|  | Tables_in_madang |
|---|---|
|  | book |
|  | customer |
|  | imported_book |
|  | orders |

**test.sql (3)**
```sql
INSERT INTO Book VALUES(1, '축구의 역사', '굿스포츠', 7000);
INSERT INTO Book VALUES(2, '축구아는 여자', '나무수', 13000);
INSERT INTO Book VALUES(3, '축구의 이해', '대한미디어', 22000);
INSERT INTO Book VALUES(4, '골프 바이블', '대한미디어', 35000);
INSERT INTO Book VALUES(5, '피겨 교본', '굿스포츠', 8000);
INSERT INTO Book VALUES(6, '역도 단계별기술', '굿스포츠', 6000);
INSERT INTO Book VALUES(7, '야구의 추억', '이상미디어', 20000);
INSERT INTO Book VALUES(8, '야구를 부탁해', '이상미디어', 13000);
INSERT INTO Book VALUES(9, '올림픽 이야기', '삼성당', 7500);
INSERT INTO Book VALUES(10, 'Olympic Champions', 'Pearson', 13000);

SELECT bookname AS 도서명, publisher AS 출판사, price AS "정가(원)"
FROM Book;
```
**실행 결과**
|  | 도서명 | 출판사 | 정가(원) |
|---|---|---|---|
|  | 축구의 역사 | 굿스포츠 | 7000 |
|  | 축구아는 여자 | 나무수 | 13000 |
|  | 축구의 이해 | 대한미디어 | 22000
|  | 골프 바이블 | 대한미디어 | 35000
|  | 피겨 교본 | 굿스포츠 | 8000 |
|  | 역도 단계별기술 | 굿스포츠 | 6000 |
|  | 야구의 추억 | 이상미디어 | 20000 |
|  | 야구를 부탁해 | 이상미디어 | 13000 |
|  | 올림픽 이야기 | 삼성당 | 7500 |
|  | Olympic Champions | Pearson | 13000 |

**test.sql (4)**
```sql
SELECT DISTINCT publisher
FROM Book;
```
**실행 결과**
|  | publisher |
|---|---|
|  | 굿스포츠 |
|  | 나무수 |
|  | 대한미디어 |
|  | 삼성당 |
|  | Pearson |

**test.sql (5)**
```sql
SELECT *
FROM Book;
```
**실행 결과**
| bookid | bookname | publisher | price |
|---:|---|---|---:|
| 1 | 축구의 역사 | 굿스포츠 | 7000 |
| 2 | 축구하는 여자 | 나무숲 | 13000 |
| 3 | 축구의 이해 | 대한미디어 | 22000 |
| 4 | 골프 바이블 | 대한미디어 | 35000 |
| 5 | 피겨 교본 | 굿스포츠 | 8000 |
| 6 | 역도 단계별기술 | 굿스포츠 | 6000 |
| 7 | 야구의 추억 | 이상미디어 | 20000 |
| 8 | 야구를 부탁해 | 이상미디어 | 13000 |
| 9 | 올림픽 이야기 | 삼성당 | 7500 |
| 10 | Olympic Champions | Pearson | 13000 |


## 4. 오류 및 해결 기록

| 발생한 문제 | 원인 | 해결 방법 |
|---|---|---|
| (없으면 '특이사항 없음') |  |  |

## 5. 프로젝트에 적용할 수 있는 부분

(프로젝트에 실제로 활용할 부분이 있을 때 작성)

## 6. 오늘 배운 점

- **새롭게 이해한 내용:** MySQL로 SQL 코드 작성법 익힘
- **추가로 복습할 내용:** JOIN, 서브쿼리 코드 공부

## 7. 찾아 볼 키워드
- 카카오톡, 다음 처음 시작한 이유
- 정부 spring 관련, 기업 spring 관련
- AWS : VM(Virtual Machine), EC2, S3
