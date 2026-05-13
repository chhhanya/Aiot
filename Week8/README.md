# 🌦️ AI Voice Weather Guidance System

라즈베리 파이 5 환경에서 Python 3.12.10을 사용하여 구현한 실시간 음성 인식 날씨 안내 시스템입니다.

## 📌 Project Overview
사용자의 음성을 인식(STT)하여 실시간 기상 데이터를 수집하고, 이를 다시 음성으로 합성(TTS)하여 출력하는 프로세스를 실증합니다.

## 🚀 Key Features
* **Speech-to-Text**: `SpeechRecognition` 라이브러리를 활용한 한국어 음성 명령 인식.
* **Weather Data Retrieval**: `OpenWeatherMap API` 연동을 통한 실시간 서울 지역 기온 및 습도 데이터 수집.
* **Text-to-Speech**: `espeak` 엔진을 활용한 보이스 인터페이스 구현.

## 🛠 Tech Stack
* **Hardware**: Raspberry Pi 5, USB Microphone, Speaker
* **Environment**: **Python 3.12.10**
* **Key Libraries**: `speech_recognition`, `requests`, `python-dotenv`

## 🔧 Installation & Setup
1. **필수 패키지 설치**:
   ```bash
   sudo apt-get install espeak -y
   sudo apt install -y fonts-unfonts-core
   pip install speech_recognition requests python-dotenv