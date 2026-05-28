# voice_reset.py — 음성 명령 수집 및 Google STT 안전 해제 파이프라인
import subprocess
import os
import requests
import time
import speech_recognition as sr

FLASK_URL = "http://localhost:5000/reset"
RESET_WORDS = ["해제", "취소", "리셋", "reset", "cancel"]
RECORD_SEC = 3             # 윈도우 버퍼 단위 녹음 주기 (초)
WAV_PATH = "/tmp/voice_cmd.wav"
ALSA_DEVICE = "hw:3,0"     # K66 USB 마이크 하드웨어 디바이스 주소 (Section 11)

recognizer = sr.Recognizer()

print(f"[보이스 엔진] ALSA 마이크 버퍼 채널 [{ALSA_DEVICE}] 수집기 가동 완료.")
print("[보이스 엔진] 위험 감지 시 '해제' 키워드 인입을 대기합니다.")

def record_once():
    """Linux 커널 시스템 arecord 인프라 호출 프로세스 실행"""
    subprocess.run([
        "arecord",
        "-D", ALSA_DEVICE,
        "-d", str(RECORD_SEC),
        "-f", "cd",
        "-q",
        WAV_PATH
    ], check=True)

def recognize_wav() -> str:
    """녹음된 이진 임시 음성 파일을 구글 STT 동기식 API 엔진으로 전송"""
    with sr.AudioFile(WAV_PATH) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio, language="ko-KR")

def listen_and_reset():
    while True:
        try:
            record_once()
            text = recognize_wav()
            print(f"[보이스 엔진] 음성 인식 텍스트 결과 패킷: {text}")

            # 음성 명령 리스트 비교 분석 검증 문맥 필터링
            if any(word in text for word in RESET_WORDS):
                print("[보이스 ENGINE] 복구 시그널 패턴 포착. 해제 REST API 호출.")
                try:
                    res = requests.post(FLASK_URL, timeout=2)
                    if res.ok:
                        print("[보이스 ENGINE] 하드웨어 복구 플래그 수집 승인 완료.")
                except Exception as e:
                    print(f"[HTTP REST ERROR] 리셋 엔드포인트 도달 실패: {e}")

        except subprocess.CalledProcessError as e:
            print(f"[HARDWARE ALSA ERROR] 녹음 프로세스 제어 실패: {e}")
            time.sleep(1)
        except sr.UnknownValueError:
            pass    # 무음구간 또는 인식 에러 시 스킵 후 재수집 루프 회전
        except sr.RequestError as e:
            print(f"[CLOUD STT NETWORK ERROR] 구글 원격 가속 API 통신 차단: {e}")
            time.sleep(1)
        except Exception as e:
            time.sleep(1)

if __name__ == "__main__":
    listen_and_reset()