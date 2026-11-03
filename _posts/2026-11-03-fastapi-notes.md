---
layout: single
title: "2026-11-03 | FastAPI 학습 정리"
date: 2026-11-03 09:01:00 +0900
course_date: '2026-11-03'
categories: [class-notes]
tags: [FastAPI, 백엔드, API]
series: "수업일지"
toc: true
toc_sticky: true
published: false
excerpt: "2026년 11월 3일 FastAPI 학습 내용과 실행 결과를 기록합니다."
---

> **기록일:** 2026-11-03  
> **학습 분야:** Python 백엔드 · FastAPI  
> **기록 원칙:** 실제 학습·실습한 내용만 기입합니다.

특정 공정의 데이터를 수집 후 분산처리 - fastapi

(AI는 streamlit을 사용. FastAPI나 Django 안 쓰는 이유는 한 번 거쳐야 하기 때문에)

특정 공정에서 데이터 들어옴

raw데이터 일단 저장

분석에 필요한 데이터만 뽑아 분석용 DB로  -> radis, kafa, airflow 필요

[Data Pipeline] 공장 대규모 센서 데이터 분산 처리 아키텍처: FastAPI와 Kafka의 역할
## 수천 개의 공정 설비에서 0.1초 단위로 쏟아지는 방대한 Raw 데이터를 어떻게 처리해야 할까?
현장의 센서나 Edge 기기들이 보내는 엄청난 양의 데이터를 데이터베이스에 직접 꽂아 넣는(Direct Insert) 방식은 치명적인 병목 현상을 유발하고, 결국 시스템 전체의 다운타임으로 이어질 수 있다.
이러한 문제를 해결하기 위해 데이터 수집(Ingestion)과 처리(Processing)를 완전히 분리(Decoupling)하는 아키텍처가 필수적이다. 이 중심에서 완충 지대이자 라우터 역할을 하는 것이 바로 FastAPI와 Apache Kafka다.

## 1. FastAPI를 초고속 데이터 수집 관문으로 선택한 이유
압도적인 비동기(Async) 처리 성능: 동시다발적으로 발생하는 HTTP POST 요청을 지연 없이 초고속으로 처리한다.
Python 생태계와의 완벽한 호환: 수집된 데이터를 실시간 불량 탐지(Anomaly Detection)나 예지 보전 AI 모델(PyTorch, TensorFlow 등)로 즉시 연결하기에 가장 유리하다.
빠른 개발과 자동 문서화 (Swagger UI): 현장의 자동화 엔지니어(OT)와 백엔드 개발자(IT) 간의 API 통신 규격 소통을 극도로 단순화해 협업 효율을 높인다.

## 2. 전체 데이터 흐름 (Data Flow) 상세
1. 데이터 수신 및 1차 검증 (Edge → FastAPI)
공정 설비의 PLC나 Edge 기기가 측정한 온도, 압력, 진동 등의 Raw 데이터를 JSON 형태로 FastAPI 엔드포인트에 전송한다. 이때 FastAPI는 내장된 Pydantic 모델을 통해 데이터 타입과 필수 값 누락 여부를 매우 빠르게 1차 검증한다.

2. 메시지 발행 및 버퍼링 (FastAPI → Kafka Broker)
응답 속도 저하를 막기 위해 FastAPI는 데이터를 직접 DB에 쓰지 않고, 비동기 방식으로 Apache Kafka의 특정 Topic(예: wafer-sensor-raw)에 메시지를 발행(Publish)한다. 이 단계에서 FastAPI는 Kafka Producer 역할을 수행하며, Kafka는 트래픽 폭주 시 거대한 버퍼 역할을 한다.

3. 병렬 분산 처리 (Kafka → Spark/Celery 등)
Kafka 파티션(Partition)에 분산 저장되어 유실 방지 처리가 된 스트리밍 데이터를, 여러 대의 분산 처리 워커가 동시에 가져와(Consume) 처리한다. 노이즈 제거, 단위 변환, 데이터 정제 등을 병렬로 수행하여 속도를 극대화한다.

4. 목적에 따른 다중 분산 저장
가공된 데이터는 활용 목적에 따라 알맞은 스토리지로 라우팅된다.
    - 시계열 DB (InfluxDB): 0.1초 단위의 센서 시계열 데이터 저장 (실시간 대시보드 모니터링용)
    - 데이터 레이크 (S3, HDFS): 가공 전후의 대용량 Raw 데이터 전체 보관 (추후 AI 모델 및 머신러닝 학습용)
    - RDBMS (PostgreSQL): 설비 정보, 공정 메타데이터, 알람 이력 등 관계형 데이터 저장

5. 데이터 서빙 (저장소 → 대시보드/외부 시스템)
저장된 데이터를 현장 작업자의 모니터링 화면(Grafana 등)에 띄우거나, 외부 ERP/MES 시스템과 연동할 때도 FastAPI가 저장소의 데이터를 조회해 전달하는 RESTful API 역할을 마무리한다.

## 결론. 시스템 안정성과 확장성의 극대화
FastAPI와 Kafka를 연계한 아키텍처는 시스템 결합도를 낮추는 디커플링(Decoupling)의 정석을 보여준다. 앞단에서는 FastAPI가 가볍고 빠르게 데이터를 수용하고, 중간에서는 Kafka가 든든하게 트래픽을 방어해주며, 뒷단에서는 여러 워커가 목적에 맞게 데이터를 요리한다. 새로운 AI 모델이나 스토리지 노드를 추가하더라도 기존 수집 서버 코드를 건드릴 필요가 없어, 확장성과 안정성이 모두 보장되는 제조 AI의 표준 인프라라 할 수 있다.
