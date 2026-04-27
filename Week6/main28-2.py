import urllib.request
import json
import datetime
import asyncio
from telegram import Bot
# [보안] 별도 파일에서 API 키, 토큰, 채팅 ID를 불러옵니다.
from config import API_KEY, MY_TOKEN, TELEGRAM_ID

# 알림 시간 설정 (정각 알림 및 사용자 지정 시간 알림)
ALERT_HOURS = [7, 10, 13, 16, 19, 22]
ALERT_TIMES = ["08:30", "15:21"]

def getWeather():
    """
    OpenWeatherMap 5일/3시간 예보 API로부터 데이터를 수집하여 
    가공된 문자열로 반환하는 함수입니다.
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={API_KEY}&units=metric&lang=en&cnt=8"
    
    try:
        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read())
        
        text = ""
        for i in range(8):
            item = data['list'][i]
            # UTC 시간을 한국 표준시(KST)로 보정 (+9시간)
            hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)
            temp = item['main']['temp']
            humi = item['main']['humidity']
            desc = item['weather'][0]['description']
            
            text += f"({hour}h {temp}C {humi}% {desc})\n"
        return text
    except Exception as e:
        return f"날씨 데이터를 가져오는 중 오류가 발생했습니다: {e}"

async def main():
    """
    무한 루프 내에서 현재 시간을 감시하며 설정된 시간에 메시지를 전송하는 비동기 함수입니다.
    """
    bot = Bot(token=MY_TOKEN)
    print("[System] Weather Alert Bot is now running...")

    while True:
        now = datetime.datetime.now()
        hm = now.strftime("%H:%M")
        
        # 정각 알림 조건 (분/초가 0인 경우)
        is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0
        # 지정 시간 알림 조건 (초가 0인 경우)
        is_alert_time = hm in ALERT_TIMES and now.second == 0
        
        if is_alert_hour or is_alert_time:
            print(f"[Event] Alert triggered at {now.strftime('%Y-%m-%d %H:%M:%S')}")
            msg = getWeather()
            await bot.send_message(chat_id=TELEGRAM_ID, text=msg)
            print("[Success] Message sent to Telegram.")
            
        # 1초 대기 후 다음 루프 실행
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[System] Bot has been stopped by user.")