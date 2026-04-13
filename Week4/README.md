# 💡 Lab 4: Flask Web Server LED Control System

본 프로젝트는 **파이썬 플라스크(Flask)** 웹 프레임워크와 **라즈베리 파이 5**의 GPIO를 연동하여, 웹 브라우저상에서 원격으로 LED 하드웨어를 제어하는 IoT 시스템의 기초를 실습.

## 🚀 개요
- **기술 스택:** Python 3.x, Flask, Gpiozero, HTML/CSS
- **핵심 기능:** - Flask의 `render_template`을 활용한 UI 구성
  - HTTP POST 메소드를 이용한 클라이언트-서버 데이터 전송
  - GPIO 제어 로직을 통한 물리적 하드웨어(LED) 점멸

## 🔌 하드웨어 구성 (Pin Mapping)
| 부품명 | 연결 핀 | 비고 |
| :--- | :--- | :--- |
| **Red LED (Anode)** | **GPIO 21** | 330Ω 저항 연결 필수 |
| **Red LED (Cathode)** | **GND (Pin 6)** | |

## 📁 프로젝트 구조
```text
project_20/
├── main20-1.py          # Flask 백엔드 서버 코드
└── templates/
    └── index.html       # 웹 제어 인터페이스 (UI)