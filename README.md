# 🛡️ Hybrid Phishing Detection System

> **이메일 본문과 URL을 함께 분석하여 피싱 위험도를 정량적으로 판단하는 하이브리드 AI 기반 피싱 탐지 시스템**

이 프로젝트는 이메일의 **텍스트 내용**, **URL 구조적 특징**, **외부 URL 평판 정보**를 결합하여 이메일의 피싱 위험도를 분석하는 시스템입니다.

단일 AI 모델의 판단에 의존하지 않고,

**Email Text Analysis → URL Analysis → Reputation Check → Risk Engine**

으로 이어지는 다단계 분석 파이프라인을 구성하여 보다 종합적인 위험도 판단을 목표로 합니다.

---

## 📌 Project Overview

기존의 피싱 탐지 방식은 이메일 본문이나 URL 중 하나의 특징에 집중하는 경우가 많습니다.

본 프로젝트에서는 이러한 접근을 확장하여 **서로 다른 데이터 특성을 처리하는 모델을 결합한 Hybrid Detection Architecture**를 설계했습니다.

| 분석 대상          | 사용 기술        | 역할                      |
| -------------- | ------------ | ----------------------- |
| Email Text     | XLM-RoBERTa  | 이메일 문맥 및 피싱 표현 분석       |
| URL Structure  | LightGBM     | URL의 구조적 특징 기반 위험도 분석   |
| URL Reputation | External API | 외부 평판 정보를 통한 위험도 보완     |
| Final Decision | Risk Engine  | 각 분석 결과를 종합하여 최종 위험도 산출 |

최종적으로 각 분석 결과를 하나의 **Risk Score**로 통합하여 이메일을 `NORMAL`, `SUSPICIOUS`, `PHISHING`으로 분류합니다.

---

## 🎯 Project Goals

### 1. Multi-modal Phishing Detection

이메일의 텍스트와 URL은 서로 다른 정보를 가지고 있습니다.

따라서 하나의 모델로 모든 정보를 처리하기보다 각각의 특성에 적합한 모델을 적용합니다.

```text
Email
 │
 ├── Subject / Body
 │        │
 │        ▼
 │   XLM-RoBERTa
 │        │
 │        ▼
 │   Email Risk
 │
 └── URLs
          │
          ├──────────────┐
          ▼              ▼
      LightGBM       Reputation API
          │              │
          ▼              ▼
       URL Risk     Reputation Risk
          │              │
          └───────┬──────┘
                  ▼
             Risk Engine
                  │
                  ▼
          Final Risk Score
                  │
          ┌───────┼────────┐
          ▼       ▼        ▼
       NORMAL  SUSPICIOUS PHISHING
```

### 2. Explainable Risk Pipeline

단순히 `Phishing / Safe`를 출력하는 것이 아니라 각각의 분석 결과를 분리하여 최종 판단에 반영합니다.

이를 통해 최종 Risk Score가 **어떤 요소의 영향을 받았는지 확인할 수 있는 구조**를 목표로 합니다.

### 3. Real-time Browser Detection

Chrome Extension을 통해 사용자가 웹메일을 확인하는 과정에서 이메일 내용을 분석 서버로 전달하고 결과를 화면에 표시할 수 있도록 구성했습니다.

---

# 🧠 AI Architecture

## Email Text Analysis

### XLM-RoBERTa

이메일의 Subject와 Body를 입력으로 받아 텍스트 기반 피싱 위험도를 분석합니다.

```text
Subject
   +
Body
   │
   ▼
XLM-RoBERTa
   │
   ▼
Email Risk Score
```

XLM-R은 다국어 텍스트를 처리할 수 있기 때문에 다양한 언어로 작성된 피싱 이메일을 고려할 수 있도록 선택했습니다.

---

## URL Analysis

### LightGBM

이메일에 포함된 URL에서 추출한 구조적 특징을 기반으로 URL 자체의 위험도를 분석합니다.

예를 들어 다음과 같은 특징을 활용하는 방향을 고려합니다.

* URL Length
* Domain Length
* Subdomain Count
* Special Character Count
* HTTPS 여부
* IP Address 사용 여부
* 의심스러운 URL 패턴

```text
URL
 │
 ▼
Feature Extraction
 │
 ▼
LightGBM
 │
 ▼
URL Risk Score
```

---

## 🌐 URL Reputation

머신러닝 모델만으로 판단하기 어려운 URL의 실제 평판 정보를 외부 Reputation Provider를 통해 보완합니다.

```text
URL
 │
 ▼
Reputation Provider
 │
 ▼
Reputation Risk
```

현재 구조는 특정 Provider에 강하게 종속되지 않도록 **Reputation Service를 별도의 계층으로 분리**했습니다.

이를 통해 향후 다른 URL Reputation API로 교체하거나 추가할 수 있도록 설계했습니다.

---

# ⚙️ Risk Engine

각 분석 모듈에서 생성된 Risk Score를 하나의 최종 위험도로 통합합니다.

예시:

```text
Final Risk
    =
Email Risk × 0.5
+
URL ML Risk × 0.2
+
Reputation Risk × 0.3
```

최종 Risk Score를 기반으로 다음과 같이 분류합니다.

|  Risk Score | Classification |
| ----------: | -------------- |
| 0.00 ~ 0.29 | 🟢 NORMAL      |
| 0.30 ~ 0.69 | 🟡 SUSPICIOUS  |
| 0.70 ~ 1.00 | 🔴 PHISHING    |

가중치와 threshold는 향후 실험 결과에 따라 조정할 수 있도록 구성합니다.

---

# 🧩 Browser Extension

Chrome Extension은 사용자가 웹메일을 사용하는 환경에서 탐지 시스템과 상호작용하는 **Client Layer**입니다.

현재 Extension은 다음 기능을 제공합니다.

* 이메일 분석 시작
* 이메일 분석 중지
* 자동 분석
* 수동 이메일 입력
* 분석 결과 표시
* 최종 위험도 표시
* 이메일에 포함된 URL 개수 표시

### Extension Flow

```text
Web Page
   │
   ▼
Content Script
   │
   │ Subject / Body
   ▼
Background Service Worker
   │
   │ HTTP POST
   ▼
FastAPI Backend
   │
   ▼
AI Analysis Pipeline
   │
   ▼
Analysis Result
   │
   ▼
Extension Widget
```

### Current Auto Extraction

현재 자동 분석에서는 웹페이지의 텍스트를 기반으로 분석 데이터를 구성하는 프로토타입 방식을 사용합니다.

```javascript
const subject = document.title;
const body = document.body.innerText.substring(0, 500);
```

이는 다양한 웹페이지에서 동작 여부를 확인하기 위한 초기 구현입니다.

향후 Gmail, Outlook 등의 실제 메일 DOM 구조에 맞춰 **서비스별 이메일 추출 모듈**로 확장할 예정입니다.

---

# 🖥️ Frontend

Frontend는 **Next.js + TypeScript + Tailwind CSS**를 기반으로 구성합니다.

주요 역할은 다음과 같습니다.

* 분석 결과 시각화
* Risk Score 표시
* Classification 표시
* 분석 이력 관리
* 사용자 인터페이스 제공

Extension과 Backend API를 통해 분석 결과를 전달받아 사용자에게 직관적으로 제공합니다.

---

# 🚀 Backend

Backend는 **FastAPI**를 기반으로 구성합니다.

### API

```http
POST /api/analyze
```

### Request

```json
{
  "subject": "Your account requires verification",
  "body": "Please click the following link..."
}
```

### Processing

```text
Request
  │
  ▼
FastAPI
  │
  ├── Email Analyzer
  │       └── XLM-R
  │
  ├── URL Analyzer
  │       └── LightGBM
  │
  ├── Reputation Service
  │
  └── Risk Engine
          │
          ▼
      Final Result
```

### Response Example

```json
{
  "classification": "PHISHING",
  "final_risk": 0.87,
  "urls": [
    {
      "url": "https://example.com",
      "risk": 0.91
    }
  ]
}
```

---

# 🗄️ Database

PostgreSQL을 사용하여 분석 결과와 관련 데이터를 저장할 수 있도록 구성합니다.

예상 저장 데이터:

* 분석 요청 정보
* Email Risk
* URL Risk
* Reputation Risk
* Final Risk
* Classification
* 분석 시간
* URL 정보

Database Layer는 AI 분석 로직과 분리하여 유지보수성을 확보합니다.

---

# 🐳 Docker Architecture

전체 시스템은 Docker 기반으로 실행할 수 있도록 구성합니다.

```text
┌─────────────────────────────────────────────┐
│                 Docker Compose              │
│                                             │
│   ┌──────────┐   ┌──────────┐              │
│   │ Frontend │   │ Backend  │              │
│   │ Next.js  │──▶│ FastAPI  │              │
│   └──────────┘   └────┬─────┘              │
│                        │                    │
│                        ▼                    │
│                  ┌──────────┐               │
│                  │PostgreSQL│               │
│                  └──────────┘               │
│                                             │
└─────────────────────────────────────────────┘

                 ▲
                 │ HTTP
                 │
        ┌─────────────────┐
        │ Chrome Extension│
        └─────────────────┘
```

---

# 📁 Project Structure

```text
Hybrid-Phishing-Detection/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── package.json
│   ├── next.config.ts
│   └── Dockerfile
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   └── analyze.py
│   │   │
│   │   ├── models/
│   │   │   ├── xlmr/
│   │   │   └── lightgbm/
│   │   │
│   │   ├── services/
│   │   │   ├── email_analyzer.py
│   │   │   ├── url_analyzer.py
│   │   │   ├── reputation.py
│   │   │   └── risk_engine.py
│   │   │
│   │   └── schemas/
│   │       └── analysis.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── database/
│   └── init.sql
│
├── extension/
│   ├── background.js
│   ├── content.js
│   ├── content.css
│   └── manifest.json
│
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

# 🔐 Security Considerations

피싱 탐지 시스템 자체가 보안 취약점을 발생시키지 않도록 다음 사항을 고려합니다.

### Environment Variables

API Key 및 민감한 설정값은 코드에 직접 작성하지 않고 `.env`를 통해 관리합니다.

```env
REPUTATION_API_KEY=your_api_key
DATABASE_URL=your_database_url
```

`.env` 파일은 Git에 포함하지 않습니다.

### SSRF Protection

Backend가 사용자가 제공한 URL을 직접 요청하는 구조는 SSRF 위험을 발생시킬 수 있으므로 URL 분석 과정에서 직접적인 외부 요청을 최소화하고 Reputation Provider를 통한 검증 구조를 사용합니다.

### Additional Security

* SQL Injection 방어
* XSS 방어
* API Timeout 설정
* 입력값 검증
* 민감 정보 로그 출력 방지
* API Key 노출 방지

---

# 🧪 Model Experiments

하이브리드 구조의 효과를 검증하기 위해 단계별 모델 구성을 비교합니다.

| Experiment | Configuration                 |
| ---------- | ----------------------------- |
| Baseline 1 | XLM-R only                    |
| Baseline 2 | LightGBM only                 |
| Hybrid 1   | XLM-R + LightGBM              |
| Hybrid 2   | XLM-R + LightGBM + Reputation |

평가 지표:

* Accuracy
* Precision
* Recall
* F1-Score
* ROC-AUC
* PR-AUC

특히 피싱 탐지에서는 정상 이메일을 피싱으로 잘못 판단하는 문제와 피싱 이메일을 놓치는 문제를 함께 고려하기 위해 Precision과 Recall을 중점적으로 비교합니다.

---

# 🛠️ Tech Stack

### AI / Machine Learning

* Python
* PyTorch
* Hugging Face Transformers
* XLM-RoBERTa
* LightGBM
* Scikit-learn

### Backend

* FastAPI
* Pydantic
* PostgreSQL

### Frontend

* Next.js
* TypeScript
* Tailwind CSS

### Browser Extension

* Chrome Extension Manifest V3
* JavaScript
* Content Script
* Background Service Worker

### Infrastructure

* Docker
* Docker Compose
* Git / GitHub

---

# 📈 Development Roadmap

### Phase 1 · System Prototype

* [x] 프로젝트 구조 설계
* [x] Chrome Extension 기본 UI
* [x] Extension → Backend 통신
* [x] `/api/analyze` API 설계
* [x] 수동 이메일 분석 기능

### Phase 2 · AI Pipeline

* [ ] XLM-R 모델 연결
* [ ] URL Feature Extraction
* [ ] LightGBM 모델 연결
* [ ] Reputation Service 연결
* [ ] Risk Engine 구현

### Phase 3 · Integration

* [ ] Extension 자동 이메일 추출
* [ ] Gmail / Outlook 지원
* [ ] Frontend Dashboard
* [ ] PostgreSQL 연동
* [ ] Docker 기반 통합 실행

### Phase 4 · Evaluation

* [ ] Dataset 구성
* [ ] Baseline 실험
* [ ] Hybrid 모델 실험
* [ ] Threshold 최적화
* [ ] 성능 비교 및 분석

### Phase 5 · Deployment

* [ ] Production 환경 구성
* [ ] API 보안 강화
* [ ] Model Serving 최적화
* [ ] Chrome Extension 배포 준비

---

# 💡 Why Hybrid?

피싱 이메일은 하나의 특징만으로 판단하기 어려운 경우가 많습니다.

예를 들어 정상적인 이메일처럼 작성된 메시지라도 내부에 악성 URL이 포함될 수 있고, 반대로 URL 자체는 정상적으로 보이더라도 이메일의 문맥이 계정 탈취를 유도할 수 있습니다.

따라서 본 프로젝트에서는

```text
Text
+
URL Structure
+
External Reputation
```

이라는 서로 다른 정보를 결합합니다.

이를 통해 **"이메일 내용이 얼마나 의심스러운가?"**, **"URL 구조가 얼마나 위험한가?"**, **"해당 URL이 외부적으로 위험하다고 알려져 있는가?"**를 각각 분석한 뒤 최종 위험도를 산출합니다.

이러한 구조는 단일 모델의 성능에만 의존하지 않고 여러 독립적인 신호를 결합할 수 있다는 장점이 있습니다.

---

# 🔭 Future Improvements

### Service-specific Email Parsing

현재의 단순 DOM 텍스트 추출 방식을 Gmail, Outlook 등 서비스별 DOM 구조에 맞는 parser로 확장합니다.

### Explainable Detection

최종 Risk Score뿐만 아니라

* 의심스러운 문장
* 의심스러운 URL
* URL 구조적 특징
* Reputation 결과

등을 함께 표시하여 사용자가 **왜 피싱으로 판단되었는지** 확인할 수 있도록 개선합니다.

### Model Optimization

XLM-R 모델의 inference latency와 메모리 사용량을 줄여 실시간 분석에 적합한 형태로 최적화합니다.

### Edge / Local Inference

향후 모델 경량화를 통해 일부 분석을 브라우저 또는 로컬 환경에서 수행하는 방향도 고려할 수 있습니다.

---

# 📊 Expected Result

최종적으로 다음과 같은 사용자 경험을 목표로 합니다.

```text
┌─────────────────────────────────┐
│ 🛡️ Phishing Detector            │
├─────────────────────────────────┤
│                                 │
│  ⚠️ PHISHING                    │
│                                 │
│  Risk Score                     │
│  ████████████████░░  87%        │
│                                 │
│  Email Risk       92%           │
│  URL Risk         81%           │
│  Reputation Risk  85%           │
│                                 │
│  Detected URLs    2             │
│                                 │
└─────────────────────────────────┘
```

사용자가 이메일을 열었을 때 별도의 분석 과정을 거치지 않고 **위험도를 직관적으로 확인할 수 있는 보안 보조 시스템**을 구축하는 것이 최종 목표입니다.

---

# 👨‍💻 Project

**Hybrid Phishing Detection System**

> AI 기반 이메일 및 URL 분석을 결합한 실시간 피싱 탐지 플랫폼

**Core Architecture**

`XLM-RoBERTa` · `LightGBM` · `URL Reputation` · `Risk Engine`

**Application**

`Chrome Extension` · `FastAPI` · `Next.js` · `PostgreSQL` · `Docker`
