# 🤖 Lab 7: Automated Telegram Weather Alerter

본 프로젝트는 **OpenWeatherMap 5일/3시간 예보 API**와 **Telegram Bot API**를 연동하여, 사용자가 설정한 주기 및 특정 시간에 기상 정보를 자동으로 전송하는 **IoT 알림 시스템**을 구현합니다.

## 🚀 개요
- **기술 스택:** Python 3.13.5, `python-telegram-bot`, `asyncio`, JSON, REST API
- **핵심 기능:**
  - 3시간 간격의 기상 예보 데이터 수집 및 KST(한국 표준시) 시간 보정
  - `asyncio` 이벤트 루프 기반의 실시간 스케줄링 (비동기 방식)
  - 텔레그램 봇을 통한 능동적 푸시(Push) 알림 기능
  - 리스트 컴프리헨션 및 반복문을 활용한 데이터 전처리

## 📂 프로젝트 구조
- `main28-2.py`: 자동 알림 시스템 메인 스크립트
- `config.py`: API 키 및 토큰 보관 파일 (**GitHub 업로드 제외 필수**)
- `.gitignore`: 보안 파일 업로드 방지 설정

## 🛠️ 실행 방법

### 1. 보안 설정 (config.py)
프로젝트 폴더에 `config.py` 파일을 생성하고 아래의 정보를 입력합니다.
```python
API_KEY = "발급받은_OpenWeatherMap_API키"
MY_TOKEN = "발급받은_텔레그램_봇_토큰"
TELEGRAM_ID = "본인의_텔레그램_채팅ID"