import cv2
import mediapipe as mp
print(cv2.__version__)
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
# hand의 landmark를 연결해서 시각화
drawing_utils = mp.solutions.drawing_utils

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
    print(hands)
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                # hand landmark
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                print(x,y)
                    
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
    
    