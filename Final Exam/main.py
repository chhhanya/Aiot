# main.py — OpenCV 비디오 스트림 처리 + PIR 센서 하드웨어 동시성 제어
import cv2
import time
import threading
import requests
from gpiozero import MotionSensor

# ── 글로벌 환경 변수 설정 ──────────────────────────────
FLASK_URL = "http://localhost:5000/alert"
PIR_PIN = 12                 # PIR 센서 신호선 결선 (GPIO 12)
SNAPSHOT_PATH = "/tmp/intruder.jpg"
EYE_CLOSE_SEC = 2.5          # 눈 감김 누적 판정 스레시홀드 (초)

# Haar-like 계층 분류기 파일 디렉토리 바인딩 (Section 13/14)
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
EYE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# ── 스레드 안전 자원 공유용 전역 변수 및 뮤텍스 락 ──────
eye_closed_since = None
alert_sent = False
latest_frame = None
frame_lock = threading.Lock()

def notify_server(reason: str):
    """Flask 중앙 허브 API 서버로 비동기 POST 알림 전송"""
    try:
        requests.post(FLASK_URL, json={"reason": reason}, timeout=2)
        print(f"[main] 상태 변경 이벤트 송출 완료: {reason}")
    except Exception as e:
        print(f"[HTTP ERROR] Flask 통신 실패: {e}")

def take_snapshot():
    """자원 경합 방지를 위해 동기화 락 확보 후 공유 프레임 메모리 이진 파일 스냅샷 복사"""
    with frame_lock:
        frame = latest_frame.copy() if latest_frame is not None else None
    if frame is not None:
        cv2.imwrite(SNAPSHOT_PATH, frame)
        print(f"[main] 무손실 보안 스냅샷 캐싱 완료: {SNAPSHOT_PATH}")

def pir_thread():
    """PIR 하드웨어 인터럽트 이벤트를 상시 대기하는 비동기 워커 스레드 (Section 3)"""
    pir = MotionSensor(PIR_PIN)
    print("[PIR ENGINE] 백그라운드 인체 감지 센서 기동 완료.")
    while True:
        pir.wait_for_motion()
        print("[PIR ENGINE] 침입자 움직임 감지!")
        take_snapshot()
        
        # 네트워크 전송 지연에 따른 프레임 드랍을 막기 위한 비동기 처리
        threading.Thread(target=notify_server, args=("intrusion",), daemon=True).start()
        threading.Thread(target=send_telegram_intrusion, daemon=True).start()
        time.sleep(5)  # 연속 감지 방지용 안심 딜레이

def send_telegram_intrusion():
    try:
        import telegram_alert
        telegram_alert.send_intrusion_alert(SNAPSHOT_PATH)
    except Exception as e:
        print(f"[TELEGRAM INCIDENT ERROR] {e}")

def run():
    global eye_closed_since, alert_sent, latest_frame

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[CRITICAL] 웹캠 디바이스 하드웨어를 활성화할 수 없습니다.")
        return

    print("[비전 엔진] OpenCV 실시간 이미지 프로세싱 루프 기동 완료. (종료: 'q')")
    
    # 비동기 PIR 모니터링 엔진 독립 실행 (자원 격리)
    threading.Thread(target=pir_thread, daemon=True).start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # PIR 스레드와의 동기화를 위해 메모리 주소 버퍼 원자적 복사
        with frame_lock:
            latest_frame = frame.copy()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)

        eyes_open = False

        for (fx, fy, fw, fh) in faces:
            # 안구 연산 부하 최소화를 위해 안면 윈도우 상단 55% 영역만 관심 영역(ROI) 슬라이싱
            roi = gray[fy: fy + int(fh * 0.55), fx: fx + fw]
            eyes = EYE_CASCADE.detectMultiScale(roi, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))

            if len(eyes) >= 2:
                eyes_open = True

            cv2.rectangle(frame, (fx, fy), (fx+fw, fy+fh), (0, 255, 0), 2)

        # ── 양안 개폐 탐색 상태 계측 논리 알고리즘 ─────────
        now = time.time()
        if len(faces) > 0 and not eyes_open:
            if eye_closed_since is None:
                eye_closed_since = now
                alert_sent = False
            elif (now - eye_closed_since) >= EYE_CLOSE_SEC and not alert_sent:
                threading.Thread(target=notify_server, args=("drowsy",), daemon=True).start()
                alert_sent = True
        else:
            eye_closed_since = None

        # 화면 시각 가시성 오버레이 렌더링
        if eye_closed_since:
            elapsed = now - eye_closed_since
            cv2.putText(frame, f"Eyes Closed: {elapsed:.1f}s", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "STATUS: OK", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("AI Safety Monitor", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()