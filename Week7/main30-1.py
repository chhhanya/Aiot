import paho.mqtt.client as mqtt # MQTT 통신 모듈 불러오기
import time # 시간 관련 기능 모듈 불러오기
from gpiozero import LED # GPIO 제어 모듈에서 LED 클래스 불러오기
import threading # 두 작업을 동시에 처리하기 위한 스레드 모듈 불러오기

# 16, 20, 21번 핀에 연결된 초록, 파랑, 빨간 LED 설정
greenLed = LED(16)
blueLed = LED(20)
redLed = LED(21)

# 브로커로부터 메시지 수신 시 자동으로 실행되는 함수 정의
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload)) # 수신된 토픽과 데이터 출력
    message = msg.payload.decode() # 수신된 바이트 데이터를 문자열로 변환
    print(message) # 변환된 메시지 터미널에 출력
    
    # 수신된 메시지 내용에 따라 LED 켜기/끄기 제어
  if message == "green_on":
        green_led.on()
    elif message == "green_off":
        green_led.off()
    elif message == "blue_on":
        blue_led.on()
    elif message == "blue_off":
        blue_led.off()
    elif message == "red_on":
        red_led.on()
    elif message == "red_off":
        red_led.off()

client = mqtt.Client() # MQTT 클라이언트 객체 생성
client.on_message = on_message # 메시지 수신 시 실행될 함수 연결

# 라즈베리 파이 브로커 IP 주소 설정 및 연결
broker_address = "192.168.0.44" 
client.connect(broker_address)
client.subscribe("led", 1) # "led" 토픽 구독 등록 (QoS 1)

count = 0 # 발행할 숫자의 초기값 설정

# 1초마다 메시지를 발행하는 스레드용 함수 정의
def send_thread():
    global count
    while 1:
        count = count + 1 # count 값을 1씩 증가
        # "hello" 토픽으로 count 값을 문자열로 변환하여 발행
        client.publish("hello", str(count))
        time.sleep(1.0) # 1초 대기 후 다시 반복

# send_thread 함수를 별도의 스레드로 생성하여 실행 (양방향 통신 가능하게 함)
task = threading.Thread(target=send_thread)
task.start()

# 메시지 수신을 위한 무한 대기 루프 실행
client.loop_forever()