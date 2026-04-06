from gpiozero import MotionSensor
from picamera2 import Picamera2
import datetime
import time

# PIR 센서 및 웹캠 하드웨어 매핑
pirPin = MotionSensor(16)
picam2 = Picamera2()

# 카메라 초기 설정 및 스트리밍 시작
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

try:
    while True:
        try:
            # PIR 센서 특성 제어 (움직임 감지 시 High 신호 발생)
            if pirPin.value == 1:
                now = datetime.datetime.now()
                fileName = now.strftime('%Y-%m-%d %H:%M:%S')
                
                print(now)
                picam2.capture_file(fileName + '.jpg') # 사진 촬영 및 저장
                time.sleep(0.5) # 연속 촬영 간격 조절
                
        except:
            pass

except KeyboardInterrupt:
    pass

# 종료 시 카메라 자원 해제
picam2.stop()