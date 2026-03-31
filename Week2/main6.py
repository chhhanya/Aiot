from gpiozero import DigitalInputDevice, OutputDevice
from time import sleep

# MQ-2 센서 및 능동 부저 하드웨어 매핑
gas = DigitalInputDevice(17)
bz  = OutputDevice(18)

try:
    while 1:
        # MQ-2 센서 특성 제어 (가스 감지 시 Low 신호 발생)
        if gas.value == 0:
            print("Detected Gas")
            bz.value = 1  # 알람 활성화
        else:
            print("Normal")
            bz.value = 0  # 알람 비활성화
            
        sleep(0.2)

except KeyboardInterrupt:
    pass

# 프로그램 강제 종료 시 0으로 초기화
bz.value = 0