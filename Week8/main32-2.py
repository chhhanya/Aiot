import speech_recognition as sr
import requests
import os
import time
from dotenv import load_dotenv

# .env 파일로부터 환경 변수 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
API_KEY = os.getenv("OPENWEATHER_API_KEY")
# 서울 지역 날씨 정보를 위한 URL 설정 (Metric 단위)
url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"

def speak(option, msg):
    """라즈베리 파이의 espeak 엔진을 사용하여 음성을 출력하는 함수"""
    os.system("espeak {} '{}'".format(option, msg))

try:
    # 음성 인식 객체 생성
    r = sr.Recognizer()
    
    while True:
        with sr.Microphone() as source:
            print("Say something!")
            # 마이크로부터 음성 수집
            audio = r.listen(source)
            
        try:
            # Google Speech API를 이용해 한국어로 변환
            text = r.recognize_google(audio, language='ko-KR')
            print("You said: " + text)
            
            # '날씨' 키워드가 포함되어 있는지 확인
            if "날씨" in text:
                print("날씨 음성을 인식하였습니다.")
                # 날씨 API 호출
                response = requests.get(url)
                data = response.json()
                
                # 기온 및 습도 데이터 파싱
                temp = data["main"]["temp"]
                humi = data["main"]["humidity"]
                
                # 음성 안내 메시지 구성
                msg = '    기온은 ' + str(int(temp)) + '도 습도는 ' + str(humi) + '퍼센트 입니다'
                
                # espeak 옵션 설정 (속도 180, 피치 50, 볼륨 200, 한글 음성)
                option = '-s 180 -p 50 -a 200 -v ko+f5'
                speak(option, msg)
            
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
    pass