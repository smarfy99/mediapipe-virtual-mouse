import cv2
import mediapipe as mp

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

cap = cv2.VideoCapture(0) # Replace with your own video and webcam

mpHands = mp.solutions.hands
hands = mpHands.Hands() 

def coordinate(id, h, w):
    cx, cy = lm.x*w, lm.y*h
    cv2.circle(img, (int(cx), int(cy)), 1, (255,255,255), cv2.FILLED)  
    return cx, cy

Take_photo=0

while True:
    success, img = cap.read()
    
    if not success: 
        break
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    h, w, c = img.shape
    handsup=0
    thumbs_correct=0
    fingers_correct=0
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
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
            cv2.putText(img, '3', (int(w/2),int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)        
        elif Take_photo>=60:
            cv2.putText(img, '2', (int(w/2),int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
        elif Take_photo>=30:
            cv2.putText(img, '1', (int(w/2),int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
        Take_photo-=1
        
    elif Take_photo==1:
        cv2.imwrite("photo.jpg", img)
        
        # firebase storage에 이미지 업로드
        # 저장할 파일 경로와 이름을 지정
        blob = bucket.blob("images/photo.jpg")
        # 로컬파일을 firebase storage에 업로드
        blob.upload_from_filename("photo.jpg")
        
        Take_photo=0
    
    cv2.imshow("Image", img)
    
    if cv2.waitKey(10) & 0xFF==ord('q'):
        break  
        
cap.release()
cv2.destroyAllWindows()

# Show the selfie
# img = cv2.imread('photo.jpg')
# cv2.imshow('Selfie', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()