from gpiozero import LED # 하드웨어 핀 제어용 'LED' 클래스
from time import sleep # 시간 지연용 'sleep' 함수 임포트

# 가독성을 위해 각 GPIO 핀 번호를 직관적인 변수명에 매핑
carRed    = 2
carYellow = 3
carGreen  = 4
humanRed  = 20
humanGreen = 21

# 각 변수에 LED 클래스안에 인스턴스를 생성하여 하드웨어 제어 준비
carRed    = LED(2)
carYellow = LED(3)
carGreen  = LED(4)
humanRed  = LED(20)
humanGreen = LED(21)

try:
    while 1:
        # [Phase 1] 차량 통행 및 보행자 정지 로직.
        carRed.value = 0
        carYellow.value = 0
        carGreen.value = 1  
        humanRed.value = 1  
        humanGreen.value = 0
        sleep(3.0)

        # [Phase 2] 신호 전환 예고
        carRed.value = 0
        carYellow.value = 1 
        carGreen.value = 0
        humanRed.value = 1 
        humanGreen.value = 0
        sleep(1.0)

        # [Phase 3] 차량 정지 및 보행자 통행 로직
        carRed.value = 1    
        carYellow.value = 0
        carGreen.value = 0
        humanRed.value = 0
        humanGreen.value = 1 
        sleep(3.0)

except KeyboardInterrupt:
    # 시스템 인터럽트 발생 시 무한 루프를 중단하고 예외 처리 블록으로 이동
    pass

# 종료 할 때 잔류 전압 차단 및 모든 LED 소등 ==> 안전성 확보
carRed.value = 0
carYellow.value = 0
carGreen.value = 0
humanRed.value = 0
humanGreen.value = 0