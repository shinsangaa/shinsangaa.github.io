---
layout: single
title: "산업용 설비 예지보전 프로젝트 — 데이터 전처리 및 신호처리"
date: 2026-11-02 09:00:00 +0900
categories: [projects]
tags: [예지보전, 제조AI, 베어링, 데이터·신호처리]
series: "산업용 설비 예지보전"
project_id: industrial-predictive-maintenance
toc: true
toc_sticky: true
published: true
excerpt: "2026-11-02 프로젝트 개발일지: 데이터 전처리 및 신호처리"
---

> **프로젝트:** 산업용 설비 예지보전 · **기록일:** 2026-11-02  
> **주제:** 데이터 전처리 및 신호처리  
> **관련 기술:** NASA IMS, CWRU, FFT, STFT, RMS, Kurtosis, RUL

[프로젝트 전체 개발일지 보기]({{ '/projects/' | relative_url }})

## 1. 오늘의 목표

베어링 진동 데이터를 읽고 신호처리 및 열화 지표를 계산하여, 다음 단계의 모델 학습에 사용할 데이터와 시각화 결과를 준비한다.

## 2. 실제 진행한 작업

- [✓] VS Code · Python 가상환경 · 프로젝트 폴더 준비
- [✓] AI Hub 기계시설물 고장 예지 센서 및 kaggle NASA IMS 베어링 진동 데이터 확보
- [✓] CSV/MAT 파일 구조, 샘플링 주파수와 결측·이상값 확인
- [✓] 진동 파형의 FFT·STFT 분석 코드 실행
- [✓] RMS · Kurtosis · Crest Factor 특징 계산
- [✓] NASA Bearing Dataset 관측 종료 시점을 기준으로 RUL 라벨 CSV 생성
- [✓] 정상/고장 신호, FFT 스펙트럼, 베어링 열화 추세 그래프 확인

## 3. 핵심 개념 — 내가 이해한 내용

### RMS(Root Mean Square)
- 진동의 평균적인 크기
- 신호를 제곱하고 평균한 다음 제곱근을 구한 값
- 사인파의 RMS 구하는 공식 = 진폭 / √2
```python
import numpy as np
signal = np.array([1, -2, 3, -4])
rms = np.sqrt(np.mean(signal ** 2))
print(rms) # 2.739
```

### FFT (Fast Fourier Transform)
- 시간에 따라 변하는 진동 신호를 주파수 성분으로 나누어 특정 진동 주파수의 강도를 확인하는 방법이다.
- FFT 이용 시 진동에 어떤 주파수 성분이 강하게 포함되어 있는지 확인이 가능하다.
- 베어링 결함 분석에서는 회전주파수, 결함 관련 주파수, 고조파 등을 함께 분석한다.
```python
import numpy as np

fs = 2000 # 초당 샘플 수
t = np.arange(fs) / fs # 1초 동안의 샘플 시각
signal = 3 * np.sin(2 * np.pi * 50 * t) # 진폭 3, 주파수 50Hz

# FFT (Hann 윈도우 + 진폭 정규화)
window = np.hanning(len(signal))
fft = np.abs(np.fft.rfft(signal * window)) * 2 / window.sum()
freq = np.fft.rfftfreq(len(signal), d=1/fs)

idx = np.argmax(fft[1:]) + 1

print("FFT 피크 주파수:", freq[idx], "Hz") # 50.0 Hz
print("FFT 피크 진폭:", round(fft[idx], 4)) # 3.0
```

### Hann 윈도우
- FFT 분석 전 신호의 양 끝부분을 부드럽게 0으로 줄이는 함수
- FFT는 분석하면 신호가 주기적으로 반복된다고 가정한다.
- 그런데 잘라낸 신호의 시작점과 끝점이 서로 다르면, 신호가 반복되는 경계에서 불연속이 발생 가능하다.
- 이로 인해 원래 신호에 없는 주파수 성분이 퍼져 보이는 현상 발생 (스펙트럼 누설, Spectral Leakage)
- 수식 w[n] = 0.5 (1 - cos((2*pi*n) / (N-1)))  
N : 데이터 샘플 개수, n : 샘플 위치
```python
# 신호의 평균값을 제거하여 DC 성분을 줄입니다.
centered = x - np.mean(x)

# Hann 윈도우를 생성합니다.
window = np.hanning(len(x)) if len(x) > 2 else np.ones(len(x))

# 윈도우를 적용하고 FFT를 수행합니다.
# 윈도우에 따른 진폭 감소를 보정합니다.
spectrum = np.abs(np.fft.rfft(centered * window)) * 2 / window.sum()

# FFT 결과에 대응하는 주파수 배열을 생성합니다.
freq = np.fft.rfftfreq(len(x), 1 / fs)
```
- centered * window => 진동 데이터에 Hann 윈도우를 곱한 후 FFT 수행  
(RMS 계산은 윈도우 적용 전에 수행함 -> RMS는 원본 신호의 크기를 기준으로 계산함)

### STFT (Short-Time Fourier Transform)
신호를 짧은 시간 구간으로 나누어 각 구간의 주파수 성분을 확인한다. 시간에 따른 주파수 변화 관찰에 사용한다.

### FFT와 STFT는 무엇이 다른가?
| 구분 | FFT | STFT |
|---|---|---|
| 목적 | 신호 전체의 주파수 성분 분석 | 시간에 따른 주파수 변화 분석 |
| 분석 방법 | 전체 신호를 한 번에 분석 | 짧은 구간으로 나누어 반복 분석 |
| 그래프 | 주파수-진폭 | 시간-주파수-강도 |
| nperseg 영향 | 일반적으로 없음 | 있음 |

### nperseg를 512로 변경하면?
현재 AI-Hub 진동 데이터의 샘플링 주파수는 4,000Hz이다.
nperseg는 STFT가 한 번에 분석할 샘플 개수를 의미한다.
| 구분 | nperseg=1024 | nperseg=512 |
|---|---|---|
| 분석 구간 길이 | 0.256초 | 0.128초 |
| 주파수 bin 간격 | 3.90625Hz | 7.8125Hz |
| 시간 변화 추적 | 상대적으로 거침 | 상대적으로 세밀함 |
| 주파수 구분 능력 | 상대적으로 좋음 | 상대적으로 낮음 |

주파수 간격 계산 : Δf = fs / N = 4000 / 512 = 7.8125 Hz  
(STFT에서 nfft를 별도로 크게 지정하지 않았을 때의 bin 간격이며, 실제 시간 간격은 noverlap 설정에도 영향 받음)

STFT는 시간 해상도와 주파수 해상도 사이에 Trade-off(상충관계) 있음
- 윈도우가 짧으면 → 시간 변화를 분석하기 유리하지만 주파수 구분이 어려워짐
- 윈도우가 길면 → 주파수를 세밀하게 구분하기 유리하지만 짧은 순간의 변화를 포착하기 어려워짐
### RMS · Kurtosis · Crest Factor

| 특징 | 의미 | 분석 시 유의점 |
|---|---|---|
| RMS | 신호 크기의 전반적인 수준 | 측정 조건·단위가 달라지면 비교에 주의 |
| Kurtosis | 극단적 피크의 상대적 발생 특성 | 이상치와 잡음의 영향을 받을 수 있음 |
| Crest Factor | 피크 절대값 / RMS | RMS가 0이거나 매우 작을 때 처리 필요 |

### RUL (Remaining Useful Life)
RUL은 설비나 부품이 고장 또는 수명 종료 기준에 도달하기까지
남은 시간을 의미한다.

이번 프로젝트에서는 NASA IMS 베어링 진동 데이터를 활용해
열화 추세를 분석하고 RUL을 추정한다.

관측 종료 시점을 RUL=0으로 설정하는 경우,
그 시점이 실제 고장 시점과 동일한지 확인해야 한다.


## 4. 오늘 생성한 결과물

| 결과물 | 실제 파일명 | 확인할 내용 |
|---|---|---|
| 정상/고장 진동 파형 | `vibration_time_comparison.png` | 신호 구간, 샘플링 주파수, 단위 |
| FFT 스펙트럼 | `vibration_fft_comparison.png` | 주파수 피크와 축 단위 |
| STFT 결과 | `vibration_stft_comparison.png` | 시간·주파수 축 |
| 베어링 3 열화 추세 | `nasa_bearing3_degradation.png` | 베어링 3의 특징 변화 |
| 베어링 4 열화 추세 | `nasa_bearing4_degradation.png` | 베어링 4의 특징 변화 |
| RUL 추세 그래프 | `nasa_rul_timeline.png` | NASA IMS 관측 종료 시점 기준 RUL 추세 |
| 특징 데이터 CSV | `nasa_ims_features.csv` | 베어링 진동 특징 데이터 |
| AI-Hub 특징 추출 CSV | `aihub_features_sample.csv` | 진동·전류 신호의 통계 및 FFT 특징 검증 |

### 4-1. 정상/고장 진동 파형

![진동 파형 비교]({{ '/assets/images/predictive-maintenance/2026-11-02/vibration_time_comparison.png' | relative_url }})

### 4-2. FFT 스펙트럼

![FFT 분석 결과]({{ '/assets/images/predictive-maintenance/2026-11-02/vibration_fft_comparison.png' | relative_url }})

### 4-3. STFT 분석 결과

![STFT 분석 결과]({{ '/assets/images/predictive-maintenance/2026-11-02/vibration_stft_comparison.png' | relative_url }})

### 4-4. 베어링 열화 추세

**베어링 3**

![베어링 3 열화 추세]({{ '/assets/images/predictive-maintenance/2026-11-02/nasa_bearing3_degradation.png' | relative_url }})

**베어링 4**

![베어링 4 열화 추세]({{ '/assets/images/predictive-maintenance/2026-11-02/nasa_bearing4_degradation.png' | relative_url }})

### 4-5. RUL 추세 그래프

![RUL 추세 그래프]({{ '/assets/images/predictive-maintenance/2026-11-02/nasa_rul_timeline.png' | relative_url }})


## 5. 코드 및 실행 환경

### 5-1. 개발 환경

| 항목 | 사용 환경 |
|---|---|
| 운영체제 | Windows |
| 개발 도구 | VS Code |
| Python | 3.12 |
| 가상환경 | `.venv` |
| 프로젝트 경로 | `C:\bearing-pdm` |
| 주요 라이브러리 | NumPy, Pandas, SciPy, Matplotlib |
| 추가 설치 라이브러리 | scikit-learn, Streamlit |

### 5-2. 주요 Python 파일

| 파일 | 역할 |
|---|---|
| `src/preprocessing.py` | 진동 데이터 전처리 및 특징 추출 |
| `src/signal_processing.py` | FFT 및 STFT 분석과 시각화 |
| `src/preprocess_ims.py` | NASA IMS 전체 데이터 전처리, 특징 및 RUL 관련 데이터 생성 |
| `src/verify_ims.py` | NASA IMS 전처리 결과 검증 |
| `src/test_preprocess_ims.py` | 전처리 기능 테스트 |

### 5-3. NASA IMS 데이터 처리

NASA IMS 베어링 데이터셋을 이용해 진동 신호를 분석하였다.

- NASA IMS의 2,156개 파일을 대상으로 전처리 실행
- RMS, Kurtosis, Crest Factor 등 특징 추출
- 시간 영역 진동 파형 및 FFT·STFT 분석
- 베어링 3·4의 열화 추세 시각화
- 관측 종료 시점을 기준으로 RUL 추세 분석

전체 데이터 전처리:

```powershell
.\.venv\Scripts\python.exe src\preprocess_ims.py --limit 0
```

전처리 결과 검증:

```powershell
.\.venv\Scripts\python.exe src\verify_ims.py
```

전처리 테스트:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s src -p test_preprocess_ims.py -v
```

주요 출력 파일:

- `data/processed/nasa_ims_features.csv`
- `reports/figures/nasa_bearing3_degradation.png`
- `reports/figures/nasa_bearing4_degradation.png`
- `reports/figures/nasa_rul_timeline.png`

### 5-4. 신호처리 핵심 코드

아래는 실제 구현한 특징 추출 및 FFT 처리 방식의 핵심 연산을 설명하기 위해 재구성한 코드이다.

```python
import numpy as np

def extract_features(x, fs):
    x = np.asarray(x, dtype=float)

    # 시간 영역 특징
    rms = np.sqrt(np.mean(x ** 2))
    peak = np.max(np.abs(x))
    centered = x - np.mean(x)
    std = np.std(x)

    kurtosis = (
        np.mean((centered / std) ** 4)
        if std > 0 else None
    )

    crest_factor = (
        peak / rms if rms > 0 else None
    )

    # FFT 분석
    window = np.hanning(len(x))
    spectrum = np.fft.rfft(centered * window)
    frequencies = np.fft.rfftfreq(len(x), d=1 / fs)

    return {
        "rms": rms,
        "kurtosis": kurtosis,
        "crest_factor": crest_factor,
        "frequencies": frequencies,
        "spectrum": np.abs(spectrum)
    }
```

실제 구현은 `src/preprocessing.py` 및 `src/signal_processing.py`를 참고한다.

### 5-5. 데이터 출처

- 데이터셋: NASA IMS Bearing Dataset
- 원 데이터 제공: University of Cincinnati, Center for Intelligent Maintenance Systems
- 배포: NASA Prognostics Center of Excellence
- 공식 출처: https://data.nasa.gov/dataset/ims-bearings
- 데이터 저장소: https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/

NASA 데이터 저장소의 출처 표기 권고에 따라 원 데이터 제공 기관과 배포 기관을 명시하였다. 데이터 이용 시 원 출처의 조건을 확인한다.


### 5-6. AI-Hub 데이터 전처리 및 특징 추출

NASA IMS 데이터 외에도 AI-Hub에서 제공하는 설비 관련
진동·전류 데이터를 활용하여 전처리와 특징 추출을 검증하였다.

#### 사용 목적

- 진동 및 전류 신호의 데이터 구조 확인
- CSV 파일의 결측값과 비정상 수치 확인
- RMS, Kurtosis, Crest Factor 특징 추출
- FFT 기반 주파수 특징 추출
- 전처리 결과를 CSV 파일로 저장

#### 실제 수행 작업

`src/preprocessing.py`를 이용해 AI-Hub 원본 ZIP에서
샘플 CSV 파일 5개를 처리하였다.

ZIP을 별도로 압축 해제하지 않고 내부 데이터를 읽어
특징 추출을 수행하였다.

주요 특징은 다음과 같다.

| 특징 | 의미 |
|---|---|
| RMS | 신호의 전반적인 진동 크기 |
| Standard Deviation | 신호값의 변동 정도 |
| Kurtosis | 충격성 피크 발생 특성 |
| Crest Factor | 최대 진폭과 RMS의 비율 |
| FFT Peak Frequency | 주파수 스펙트럼의 주요 피크 위치 |
| FFT Spectral Centroid | 스펙트럼 에너지 분포의 중심 |

#### 주요 실행 파일

- `src/preprocessing.py`

#### 전처리 결과물

- `data/processed/aihub_features_sample.csv`

원본 CSV 파일에서 추출한 특징과 데이터 품질 점검 결과를
하나의 CSV 파일에 정리하였다.

결과 CSV는 신호 채널별 특징 행을 저장하므로,
원본 파일 5개와 결과 행 수가 반드시 동일하지는 않다.

#### NASA IMS 데이터와의 차이

AI-Hub 데이터는 신호처리 및 특징 추출 기능을 검증하는
용도로 활용하였다.

반면 NASA IMS 데이터는 베어링의 시간에 따른 열화 추세를
분석하고 잔여수명(RUL)을 추정하기 위해 사용한다.

따라서 AI-Hub 샘플 데이터를 RUL 정답 데이터로 사용한 것은 아니다.

## 6. 문제와 해결 기록

- 발생한 문제: `실제 오류가 없었다면 '특이사항 없음'으로 수정`
- 원인: `실제 확인 내용`
- 해결 방법: `실제 확인 내용`

## 7. 오늘 배운 점과 다음 단계

- 오늘 이해한 점: `본인의 말로 2~3문장 작성`
- 남은 확인 사항: `예: RUL 라벨 생성 기준의 타당성`
- 다음 작업: 머신러닝·딥러닝 모델 기준선과 평가 방식 정하기
