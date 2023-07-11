import cv2
print(cv2.__version__)
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
    
    