# app.py — Flask 중앙 허브
# Section 4/5: Flask 웹서버 + LED 제어

from flask import Flask, request, jsonify, render_template
from gpiozero import LED
import time, threading

app = Flask(__name__)

# ── GPIO 설정 ──────────────────────────────────────────
red_led   = LED(21)   # 경고 (졸음/침입)
green_led = LED(20)   # 정상

# ── 시스템 상태 (공유 변수) ────────────────────────────
status = {
    "alert":   False,   # 현재 경고 상태
    "reason":  "",      # 경고 원인 ("drowsy" | "intrusion")
    "timestamp": ""     # 마지막 이벤트 시각
}

def set_alert(reason: str):
    """경고 ON: 빨간 LED 켜고 상태 기록"""
    status["alert"]     = True
    status["reason"]    = reason
    status["timestamp"] = time.strftime("%H:%M:%S")
    green_led.off()
    red_led.on()
    print(f"[ALERT] {reason} @ {status['timestamp']}")

def clear_alert():
    """경고 OFF: 초록 LED 복귀"""
    status["alert"]  = False
    status["reason"] = ""
    red_led.off()
    green_led.on()
    print("[OK] Alert cleared")

# 시작 시 초록 LED ON
clear_alert()

# ── API 엔드포인트 ─────────────────────────────────────

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/status")
def get_status():
    """대시보드가 주기적으로 폴링하는 상태 API"""
    return jsonify(status)

@app.route("/alert", methods=["POST"])
def trigger_alert():
    """drowsiness.py / pir_monitor.py 가 호출 → 경고 발생"""
    data   = request.get_json(silent=True) or {}
    reason = data.get("reason", "unknown")
    set_alert(reason)

    # 텔레그램 알림은 별도 스레드로 (블로킹 방지)
    threading.Thread(target=send_telegram, args=(reason,), daemon=True).start()

    return jsonify({"ok": True, "reason": reason})

@app.route("/reset", methods=["POST"])
def reset_alert():
    """voice_reset.py 가 '해제' 감지 후 호출"""
    clear_alert()
    return jsonify({"ok": True})

# ── 텔레그램 알림 (내부 함수) ─────────────────────────
def send_telegram(reason: str):
    """telegram_alert.py 의 함수를 임포트해서 사용"""
    try:
        import telegram_alert
        msg = {
            "drowsy":     "⚠️ 졸음 감지! 눈이 3초 이상 감겼습니다.",
            "intrusion":  "🚨 침입 감지! PIR 센서가 움직임을 포착했습니다.",
        }.get(reason, f"⚠️ 알림: {reason}")
        telegram_alert.send_message(msg)
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")

# ── 실행 ──────────────────────────────────────────────
if __name__ == "__main__":
    # host="0.0.0.0" → 같은 Wi-Fi의 PC/폰에서도 접속 가능
    app.run(host="0.0.0.0", port=5000, debug=False)
