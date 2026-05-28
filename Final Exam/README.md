# 🚨 AIOT Edge AI Smart Home Safety Monitoring System (Final Project)

라즈베리 파이 5(Raspberry Pi 5) 플랫폼 환경에서 컴퓨터 비전 파이프라인, 임베디드 멀티 센서 동시성 제어, 로컬 Flask 웹 서버 허브, 퍼블릭 클라우드 서비스 API(Google STT, Telegram Bot, OpenWeatherMap)를 유기적으로 결합한 **지능형 스마트 홈 통합 안전 모니터링 시스템**입니다.

본 프로젝트는 학부 과정에서 학습한 주요 융합 기술 도메인들을 단일 시스템으로 병합하여 실증한 기말 융합 산출물입니다.

---

## 🎓 Curriculum Mapping (수업 섹션 연동)
본 융합 프로젝트는 아래의 핵심 학급 실습 주제들을 전주기(Full-Cycle) 파이프라인으로 통합하여 구현되었습니다:
* **Section 3**: PIR 인체 감지 센서 하드웨어 커널 제어 및 인터페이스 구축 (`MotionSensor`)
* **Section 4 / 5**: Flask 웹 애플리케이션 서버 프레임워크 개발 및 실시간 공유 상태 동기화, GPIO LED 디지털 제어
* **Section 6 / 7 / 8**: 외부 오픈 클라우드 패킷 연동 (OpenWeatherMap API 기반 날씨 수집 및 Telegram Bot API 기반 멀티파트 사진 알림 송출)
* **Section 11**: ALSA 커널 마이크 제어 및 Linux `arecord` 연동, Google Speech Recognition 비동기 음성 인식 해제 프로토콜
* **Section 13 / 14**: OpenCV 비디오 가속 스트림 처리, 그레이스케일 이미지 프로세싱 및 Haar Cascade 기반 실시간 안면·양안 ROI(관심영역) 추출 졸음 추적 논리 제어

---

## 📂 System Architecture & Data Flow

본 시스템은 싱글 보드 컴퓨터(SBC) 단의 연산 병목 및 화면 렌더링 블로킹을 방지하기 위해 **뮤텍스(Mutex) 자원 락(`threading.Lock`)을 활용한 비동기 멀티스레딩 구조**로 설계되었습니다.

```text
[입력 계층 (Inputs)]                [중앙 제어 허브 (Flask Hub)]         [출력 계층 (Outputs)]
 ├── USB Webcam Stream     ────►   ├── app.py (Port 5000)      ────►   ├── Dashboard UI (HTML5/CSS3)
 ├── PIR Sensor (GPIO 12)  ────►   │    - Host Status Dict             ├── Green LED (GPIO 20) -> 정상 상태
 └── USB Mic (hw:3,0)      ────►   │    - REST API Endpoints           └── Red LED (GPIO 21)   -> 위험 발생
                                   └── Threading Engine (Async)                 │
                                        ├── OpenWeatherMap API ─────────────────┤
                                        └── Telegram Bot API ──────────────────► [모바일 텔레그램 알림 푸시]

🛠 Hardware Configuration (핀 결선도)
라즈베리 파이 5 보드와 주변 컴포넌트 간의 물리 제어를 위한 I/O 맵 맵핑 구조입니다.

부품명,핀 종류,라즈베리 파이 5 물리 핀 번호,BCM GPIO 번호,비고 / 역할 및 기능 정의
파란 LED (+),Digital Out,Pin 38,GPIO 20,시스템 정상 작동 상태(OK) 시그널 인디케이터
빨간 LED (+),Digital Out,Pin 40,GPIO 21,졸음 및 침입 이벤트 발생 시 위험 경고 인디케이터
LED 공통 (-),GND,Pin 39,GND,회로 전위 평형을 위한 공통 그라운드 (330Ω 저항 연결)
PIR 신호 (S),Digital In,Pin 32,GPIO 12,외부인 물리 침입 시그널 입력 인터페이스 (브레드보드 경유)
PIR 전원 (V),Power,Pin 1,3.3V,인체 감지 센서 구동을 위한 로컬 전원 공급 (브레드보드 경유)
PIR 접지 (G),GND,Pin 6,GND,센서 기준 전위 고정을 위한 그라운드 결선 (브레드보드 경유)
K66 USB Mic,USB 인터페이스,USB 3.0 Port,"hw:3,0",음성 명령(해제) 수집용 ALSA 오디오 커널 매핑 주소

📂 Project Directory Structure
📁 Aiot/
├── 📁 templates/
│   └── dashboard.html       # 실시간 상태 관제 원격 웹 대시보드 UI
├── app.py                  # Flask 웹 서버 중앙 제어 코어 및 GPIO LED 관리 브릿지
├── main.py                 # OpenCV 비전 파이프라인 + PIR 센서 감지 비동기 통합 스레드
├── telegram_alert.py       # OpenWeatherMap 기상 수집 및 텔레그램 봇 사진 푸시 모듈
└── voice_reset.py          # ALSA 기반 로컬 오디오 캡처 및 Google STT 음성 인식 해제 엔진

⚙️ Installation & Operation Guide
1. 필수 종속성 패키지 설치
라즈베리 파이 5 내부 가상 개발 환경(Opencv) 진입 후 아래의 패키지 환경을 조성합니다.
source Opencv/bin/activate
pip install flask opencv-python gpiozero requests speechrecognition

2. 실행 프로토콜 (Execution)
시스템의 유기적 연동을 위해 중앙 웹 제어 허브를 먼저 백그라운드로 서빙한 후, 센서/비전 엔진과 음성 리셋 루프를 차례로 가동합니다.
# Terminal 1: Flask 중앙 제어 웹 인프라 구동
python app.py

# Terminal 2: OpenCV 컴퓨터 비전 및 PIR 보안 탐지 스레드 동시 구동
python main.py

# Terminal 3: Google STT 보이스 클라우드 인터페이스 수집기 구동
python voice_reset.py

대시보드 원격 확인: 동일 호스트 단 유입 확인 포트 주소인 http://<라즈베리파이_IP>:5000 경로를 통해 실시간 웹 UI 관제 상태 창에 접속할 수 있습니다.

수동 완전 종료: 카메라 비전 오버레이 활성 창 상태에서 키보드 q 키를 누르면 cap.release() 가 작동하며 하드웨어 자원이 안전하게 릴리스되며 루프가 해제됩니다.