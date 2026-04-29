import urllib.request
import json
import datetime
import asyncio
from telegram import Bot
from config import telegram_id, my_token, api_key

bot = Bot(token=my_token)

# PPT와 동일한 알림 시간 설정
ALERT_HOURS = [7, 10, 13, 16, 19, 22]
ALERT_TIMES = ["08:30", "14:45"]

def getWeather():
    # 서울 24시간 예보 URL 호출
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8"

    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read())

    text = ""
    for i in range(8):
        item = data['list'][i]
        # 시간 추출 후 KST(UTC+9) 변환 및 2자리 유지
        hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)
        temp = item['main']['temp']
        humi = item['main']['humidity']
        desc = item['weather'][0]['description']
        # 문자열 가공
        text += f"({hour}h {temp}C {humi}% {desc})\n"

    return text

async def main():
    try:
        while True:
            now = datetime.datetime.now()
            hm = now.strftime("%H:%M")

            # 정각 및 지정 시간 알림 조건 확인
            is_alert_hour = now.hour in ALERT_HOURS and now.minute == 0 and now.second == 0
            is_alert_time = hm in ALERT_TIMES and now.second == 0

            if is_alert_hour or is_alert_time:
                msg = getWeather()
                print(msg) # 터미널 출력
                # 텔레그램 메시지 전송
                await bot.send_message(chat_id=telegram_id, text=msg)

            # 1초 대기 후 루프 반복
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        pass

# 비동기 메인 함수 실행
asyncio.run(main())
