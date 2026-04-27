# 🌦️ Lab 6: Real-time Weather Monitoring GUI

본 프로젝트는 **OpenWeatherMap API**를 활용하여 실시간 기상 데이터를 수집하고, 파이썬의 **Tkinter** 라이브러리를 통해 데스크톱 GUI 환경에 온습도를 시각화하는 시스템을 구현합니다.

## 🚀 개요
- **기술 스택:** Python 3.13.5, Tkinter, JSON, HTTP/REST API
- **핵심 기능:** - OpenWeatherMap API를 통한 실시간 기상 데이터(서울 지역) 수집
  - JSON 데이터 파싱 및 섭씨(Metric) 단위 변환
  - `window.after`를 활용한 1분 주기 자동 데이터 갱신 로직
  - 가독성 높은 대형 폰트 기반의 GUI 대시보드

## 🔌 시스템 구조
- **Backend:** `urllib.request`를 사용한 HTTP GET 요청 처리 및 JSON 데이터 파싱
- **Frontend:** `Tkinter` 기반의 고정형(400x100) GUI 윈도우

## 📁 프로젝트 파일
- `main24-3.py`: 실시간 데이터 수집 및 GUI 구동 메인 스크립트
- `README.md`: 프로젝트 설명 문서

## 🛠️ 실행 방법

### 1. API 키 준비
[OpenWeatherMap](https://openweathermap.org/)에서 회원가입 후 발급받은 API 키가 필요합니다.
> **참고:** 발급 직후에는 서버 활성화까지 약 10분~2시간 정도 소요될 수 있습니다.

### 2. 코드 실행
라즈베리 파이 또는 PC 환경에서 아래 명령어를 실행합니다.
```bash
python3 main24-3.py