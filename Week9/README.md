# 👁️ OpenCV & GPIO Drowsiness Prevention System (Section 14-1)

라즈베리 파이 5(Raspberry Pi 5) 환경에서 Python 3.12.10과 OpenCV, 물리 부저 센서를 연동하여 구현한 실시간 졸음방지 디바이스 프로토타입입니다.

## 📌 Project Overview
웹캠 비디오 스트림으로부터 하르 카스케이드(Haar Cascade) 알고리즘을 활용해 얼굴과 안구를 계층적으로 탐색(ROI 추출)하고, 안구의 실시간 검출 수에 따라 GPIO 핀에 연결된 전자 부저(Buzzer)를 직접 제어하는 실시간 임베디드 시각 컴퓨팅 시스템입니다.

## 🚀 Key Features
* **Real-time Image Processing**: 입력 비디오 스트림을 640×480 해상도로 프레임 캡처 후 고속 연산을 위해 1채널 Grayscale 이미지로 변환.
* **Hierarchical Cascade Classifier**: `cv2.data.haarcascades` 내부 가중치 모델을 링크하여 선제적으로 얼굴을 서칭한 뒤, 해당 바운딩 박스를 관심 영역(ROI)으로 지정해 안구를 한정 추적함으로써 연산 효율 극대화.
* **Hardware Interlocking Alert**: 실시간 안구 검출 수가 1개 이하(`len(eyes) <= 1`)로 떨어질 경우 졸음 상태로 판정, `gpiozero` 라이브러리를 통해 GPIO 16번 핀에 연결된 부저 센서를 즉각 트리거(`buzzerPin.on()`).

## 🛠 Tech Stack
* **Hardware**: Raspberry Pi 5, USB WebCam, Active Buzzer (Connected to GPIO 16)
* **Environment**: **Python 3.12.10** (`voice3.12` 가상 환경)
* **Core Libraries**: `opencv-python` (OpenCV), `gpiozero`

## 🔧 Installation & Setup
1. **필수 라이브러리 및 의존성 설치**:
   ```bash
   pip install opencv-python gpiozero