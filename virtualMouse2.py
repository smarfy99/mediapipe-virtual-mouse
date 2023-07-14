import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
# hand의 landmark를 연결해서 시각화
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

# cv2 라이브러리를 활용해 웹캠 불러오기
while True:
    _, frame = cap.read()
    # 0는 x축, 1은 y축으로 flip
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    
    # opencv는 BGR 형식(Blue Green Red)에서 작동하지만 mediapipe는 RGB(Red Green Blue) 형식에서 작동하기 때문에 이미지를 처리하기 전에 이미지 형식을 변경
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    
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
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
    
    