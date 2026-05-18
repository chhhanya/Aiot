import cv2
from gpiozero import Buzzer
import time

# 하드웨어 인터페이스 설정 (GPIO 16번 핀)
buzzerPin = Buzzer(16)

def main():
    camera = cv2.VideoCapture(-1)
    camera.set(3, 640)
    camera.set(4, 480)
    
    # OpenCV 내장 사전 학습 모델(Haar Cascade) XML 가중치 경로 지정
    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml'
    
    face_cascade = cv2.CascadeClassifier(face_xml)
    eye_cascade = cv2.CascadeClassifier(eye_xml)
    
    while camera.isOpened():
        _, image = camera.read()
        # 고속 연산을 위한 1채널 Grayscale 변환 (Pre-processing)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Haar Cascade 기반 다중 스케일 얼굴 객체 검출
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,               # 이미지 피라미드 축소 비율
            minNeighbors=5,                # 후보 사각형 인접 신뢰도 임계값
            minSize=(100, 100),            # 원거리 배경 노이즈 제거를 위한 최소 객체 스케일
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        print("faces detected Number: " + str(len(faces)))
        
        if len(faces):
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                # 탐색 연산량 최적화를 위한 얼굴 영역 내부 관심 영역(ROI) 추출
                face_gray = gray[y:y+h, x:x+w]
                face_color = image[y:y+h, x:x+w]
                
                # 얼굴 ROI 내 한정 알고리즘을 통한 안구 객체 탐지
                eyes = eye_cascade.detectMultiScale(face_gray, scaleFactor=1.1, minNeighbors=5)
                
                # [실시간 졸음 판단 로직] 개폐 유무 및 가림 현상으로 안구가 1개 이하 검출 시 부저 트리거
                if len(eyes) <= 1:
                    buzzerPin.on()
                else:
                    buzzerPin.off()
                    
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                    
        cv2.imshow('result', image)
        
        if cv2.waitKey(1) == ord('q'):
            break
            
    camera.release()
    cv2.destroyAllWindows()
    buzzerPin.off()  # 프로세스 종료 시 하드웨어 자원 점유 예외 처리 해제

if __name__ == '__main__':
    main()