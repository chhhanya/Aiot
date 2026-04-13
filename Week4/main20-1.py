from flask import Flask, render_template, request
from gpiozero import LED

app = Flask(__name__)

# [Hardware Setup] LED connected to GPIO 21
red_led = LED(21)

@app.route('/')
def home():
    """기본 경로 접속 시 templates/index.html 렌더링"""
    return render_template("index.html")

@app.route('/data', methods=['POST'])
def data():
    """HTML Form의 POST 요청을 받아 LED 상태 제어"""
    # 전송된 데이터에서 'led' 키의 값 추출
    data = request.form['led']

    if data == 'on':
        red_led.on()
        print("[Status] LED turned ON")
    elif data == 'off':
        red_led.off()
        print("[Status] LED turned OFF")

    # 제어 후 메인 페이지로 복귀
    return home()

if __name__ == "__main__":
    # 모든 호스트(0.0.0.0)에서 80번 포트로 서버 실행
    # (주의: 80번 포트 실행을 위해 관리자 권한 'sudo'가 필요함)
    app.run(host="0.0.0.0", port="80")