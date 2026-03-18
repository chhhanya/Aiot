# gpiozero 라이브러리에서 하드웨어 그룹 제어용 'LEDBoard' 클래스를 임포트
# 하드웨어 제어 로직을 객체 단위로 추상화해서 관리
from gpiozero import LEDBoard
from time import sleep

# GPIO 2, 3, 4, 20, 21번 핀을 하나의 'leds' 인스턴스로 생성
# 하나의 객체로 묶어 병렬 제어
leds = LEDBoard(2, 3, 4, 20, 21)

try:
    while 1:
        # 이진 상태 값을 대입하여 전체 핀 상태 제어
        # [차량G / 보행자R]
        leds.value = (0, 0, 1, 1, 0)
        sleep(3.0) 
        
        # [차량Y / 보행자R]
        leds.value = (0, 1, 0, 1, 0)
        sleep(1.0) 
        
        # [차량R / 보행자G]
        leds.value = (1, 0, 0, 0, 1)
        sleep(3.0)

except KeyboardInterrupt:
    # 프로그램 강제 종료(Ctrl+C) 시 탈출
    pass

# 하드웨어 리소스를 초기화, LED 소등.
leds.off()