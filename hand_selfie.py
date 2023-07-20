import cv2
import mediapipe as mp
import pyautogui

# firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# firebase 인증 정보 초기화
# firebase 서비스 계정 키(json파일)의 경로를 지정
cred = credentials.Certificate("mediapipe-virtual-mouse/firebase-service-account.json")
# firebase storage 버킷 이름으로 대체
firebase_admin.initialize_app(cred, {
    'storageBucket': 'mwm-mozi.appspot.com'
})
bucket = storage.bucket()

# my own video and webcam setting
cap = cv2.VideoCapture(0) # Replace with your own video and webcam
hand_detector = mp.solutions.hands.Hands()

# hand의 landmark를 연결해서 시각화
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

def coordinate(id, h, w):
    cx, cy = lm.x*w, lm.y*h
    cv2.circle(frame, (int(cx), int(cy)), 1, (255,255,255), cv2.FILLED)  
    return cx, cy

Take_photo=0

while True:
    success, frame = cap.read()
    
    # 0는 x축, 1은 y축으로 flip
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    
    if not success: 
        break
    
    # opencv는 BGR 형식(Blue Green Red)에서 작동하지만 mediapipe는 RGB(Red Green Blue) 형식에서 작동하기 때문에 이미지를 처리하기 전에 이미지 형식을 변경
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hand_detector.process(frameRGB)
    # hand landmark의 좌표 추출
    hands = results.multi_hand_landmarks

    h, w, c = frame.shape
    handsup=0
    thumbs_correct=0
    fingers_correct=0
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                # hand landmark
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                
                # 검지
                if id == 8:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255))
                    # 전체 화면 크기 비례한 마우스 위치 이동
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    pyautogui.moveTo(index_x, index_y)
                # 엄지 
                if id == 4:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    print('outside', abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 40:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                cv2.circle(img=frame, center=(x,y), radius=10, color=(0,255,255))
                if id == 0: 
                    __, cy_0 = coordinate(0, h, w)
                if id == 10: 
                    __, cy_10 = coordinate(10, h, w)
            
                if id == 2:
                    __, cy_2 = coordinate(2, h, w)
                if id == 3:
                    __, cy_3 = coordinate(3, h, w)
            
                if id == 5: 
                    __, cy_5 = coordinate(5, h, w)
                if id == 9: 
                    __, cy_9 = coordinate(9, h, w)
                if id == 13: 
                    __, cy_13 = coordinate(13, h, w)
                if id == 17: 
                    __, cy_17 = coordinate(17, h, w)
                    
                if id == 8: 
                    __, cy_8 = coordinate(8, h, w)  
                if id == 12: 
                    __, cy_12 = coordinate(12, h, w)
                if id == 16: 
                    __, cy_16 = coordinate(16, h, w)
                if id == 20: 
                    __, cy_20 = coordinate(20, h, w)
            
            if cy_10 < cy_0:
                handsup=1
            else:
                handsup=0
                    
            if (cy_2 > cy_10 and cy_2 < cy_0) and (cy_3 > cy_10 and cy_3 < cy_0):
                thumbs_correct=1
            else:
                thumbs_correct=0
            
            if (cy_5 < cy_8) and (cy_9 < cy_12) and (cy_13 < cy_16) and (cy_17 < cy_20):
                fingers_correct=1
            else:
                figners_correct=0
            
            if handsup==1 and thumbs_correct==1 and fingers_correct==1 and Take_photo==0:
                Take_photo=120

    if Take_photo>1:
        if Take_photo>=90:
            cv2.putText(frame, '3', (int(w/2),int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)        
        elif Take_photo>=60:
            cv2.putText(frame, '2', (int(w/2),int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
        elif Take_photo>=30:
            cv2.putText(frame, '1', (int(w/2),int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
        Take_photo-=1
        
    elif Take_photo==1:
        cv2.imwrite("photo.jpg", frame)
        
        # firebase storage에 이미지 업로드
        # 저장할 파일 경로와 이름을 지정
        blob = bucket.blob("images/photo.jpg")
        # 로컬파일을 firebase storage에 업로드
        blob.upload_from_filename("photo.jpg")
        
        Take_photo=0
    
    # cv2.imshow('Virtual Mouse', frame)
    # cv2.waitKey(1)
    cv2.imshow("Image", frame)
    
    if cv2.waitKey(5) & 0xFF==ord('q'):
        break  
        
cap.release()
cv2.destroyAllWindows()

# Show the selfie
# img = cv2.imread('photo.jpg')
# cv2.imshow('Selfie', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()