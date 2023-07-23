from firebase_config import bucket
from hand_selfie import cv2, np

# 이미지를 병합해서 firebase에 저장하기
image_names = ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg"]
images = []

for image_name in image_names:
    blob = bucket.blob(f"images/{image_name}")
    image_bytes = blob.download_as_bytes()
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    images.append(image)

# photoFrame 읽어오기
photo_frame = cv2.imread('mediapipe-virtual-mouse/photoframe.png')

merged_image = photo_frame.copy()
# photoFrame과 이미지 합성하기
photo_width, photo_height = images[0].shpae[1], images[0].shape[0]

# 콜라주 만들기 위해 사진 배치 - 4개 사진 가로 2개씩 2행
row_1 = np.hstack((images[0], images[1]))
row_2 = np.hstack((images[2], images[3]))
merged_image[100:100+photo_height, 50:50+photo_width*2] = row_1
merged_image[200:200+photo_height, 50:50+photo_width*2] = row_2

cv2.imshow('Show image', photo_frame)
cv2.waitKey(0)
# 합성한 콜라주를 로컬에 저장
merged_image_name = "mergedImage.jpg"
cv2.imwrite(merged_image_name, merged_image)
blob = bucket.blob(f"images/{merged_image_name}")
# 로컬파일을 firebase storage에 업로드
blob.upload_from_filename(merged_image_name)

# 메모리에서 이미지 삭제
for image in images:
    image.release()
    
cv2.destroyAllWindows()