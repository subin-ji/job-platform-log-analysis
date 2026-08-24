# 채용 플랫폼 사용자 로그 분석

2022~2023년 채용 플랫폼의 사용자 행동 로그를 기반으로  
**가입 → 이력서 작성 → 지원 완료 퍼널과 리텐션을 분석하고, 전환 저해 구간과 주요 행동 패턴을 파악한 프로젝트**입니다.

## 분석 목표

- 가입 과정에서 이탈이 집중되는 구간 확인
- 가입 이후 이력서 작성 및 지원 완료까지의 전환 퍼널 분석
- Classic / Range / Rolling Retention 비교
- 미전환 유저의 마지막 행동 파악
- 원클릭 지원 기능과 지원 완료 간의 관계 확인

## 주요 결과

- 가입 퍼널에서 `step2 → step3` 구간의 전환율은 **79.1%**로 마지막 가입 단계에서 이탈이 상대적으로 크게 나타났습니다.
- 가입 완료 유저 중 **62.5%**가 이력서 작성을 시작했으며, 작성 시작 이후 다음 단계 전환은 상대적으로 높았습니다.
- 지원 퍼널은 후반 단계에서 이탈이 커졌고, 최종 지원 완료율은 분석 기준 **34.1%**였습니다.
- Classic Retention은 **Day 1 38.5% → Day 30 15.1% → Day 365 1.7%**로 감소했습니다.
- 원클릭 지원 기능을 사용한 유저는 지원 완료와 높은 연관성을 보였습니다.

> 위 수치는 본 프로젝트의 정의와 로그 이벤트 기준으로 계산한 결과입니다.

## Project One-Pager

### 1. Analysis Overview

![Analysis Overview](one_pager/01_analysis_overview.png)

### 2. Tableau Dashboard

![Tableau Dashboard](one_pager/02_tableau_dashboard.png)

## Documents

- [Project One-Pager](docs/01_project_one_pager.pdf)
- [Web Log Analysis Report](docs/02_web_log_analysis_report.pdf)

## Repository Structure

```text
job-platform-log-analysis/
├── README.md
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   └── 03_analysis.ipynb
├── sql/
│   └── 01_log_preprocessing.sql
├── src/
│   └── pipeline.py
├── images/
│   └── README.md
├── data/
│   └── README.md
├── .env.example
├── .gitignore
└── requirements.txt
```

## Notebook Guide

### 01. EDA
데이터베이스 구조, 로그 기간, 사용자 수, URL 패턴을 탐색합니다.

### 02. Preprocessing
가입 완료, 이력서 작성, 지원 단계 이벤트를 정의하고 유저 단위 퍼널 데이터를 구성합니다.

### 03. Analysis
Acquisition / Activation 퍼널, 전환 소요시간, 코호트 및 리텐션, 원클릭 지원, 미전환 유저 행동을 분석합니다.

## SQL Preprocessing

`sql/01_log_preprocessing.sql`

- 밀린 컬럼 형태 보정
- UTC → KST 변환
- timestamp 타입 변환
- 빈 URL 제거
- 분석용 2022 / 2023 로그 테이블 생성

## Tech Stack

- Python
- Pandas
- Matplotlib / Seaborn
- MySQL
- SQLAlchemy
- Tableau

## Tableau Dashboard

Tableau 대시보드를 함께 공개할 경우 아래 두 가지를 같이 제공하는 것을 권장합니다.

1. `images/tableau_dashboard.png`에 전체 대시보드 캡처 1장
2. 아래에 Tableau Public 링크

<!-- Tableau 자료를 추가한 뒤 주석을 해제하세요.

![Tableau Dashboard](images/tableau_dashboard.png)

[Tableau Public에서 인터랙티브 대시보드 보기](TABLEAU_PUBLIC_URL)

-->

## 실행 방법

```bash
pip install -r requirements.txt
```

`.env.example`을 복사하여 `.env`를 만든 뒤 DB 정보를 설정합니다.

```text
DB_URL=mysql+pymysql://USERNAME:PASSWORD@localhost:3306/job_subs?charset=utf8mb4
```

이후 `notebooks/01_eda.ipynb`부터 순서대로 실행할 수 있습니다.

## Data

원본 사용자 로그는 개인정보 및 데이터 공개 범위를 고려하여 저장소에 포함하지 않았습니다.
