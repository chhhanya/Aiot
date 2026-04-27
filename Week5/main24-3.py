import urllib.request
import json
import tkinter
import tkinter.font
# [보안] 별도 파일에서 API 키를 불러옵니다.
from config import API_KEY 

def tick1Min():
    """1분 주기로 기상 데이터를 수집하고 GUI를 갱신합니다."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"
        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read())
            
        temp = data["main"]["temp"]
        humi = data["main"]["humidity"]
        
        # GUI 라벨 텍스트 업데이트
        label.config(text=f"{temp:.1f}C   {humi}%")
        print(f"[Success] Data updated at 1-minute interval.")
        
    except Exception as e:
        label.config(text="API Error")
        print(f"[Error] 확인이 필요합니다: {e}")
    
    # 1분 후 재실행
    window.after(60000, tick1Min)

# GUI 설정
window = tkinter.Tk()
window.title("TEMP HUMI DISPLAY")
window.geometry("400x100")
window.resizable(False, False)

font = tkinter.font.Font(size=30, weight="bold")
label = tkinter.Label(window, text="Loading...", font=font)
label.pack(expand=True)

# 초기 실행 및 루프 시작
tick1Min()
window.mainloop()