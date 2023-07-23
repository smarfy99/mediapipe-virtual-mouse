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

# 이미지 2개씩 2행으로 배열
row1 = np.hstack((images[0], images[1]))
row2 = np.hstack((images[2], images[3]))
merged_image = np.vstack((row1, row2))

# 합성이미지에 photo_frame 얹기
# photo_frame의 크기를 합성 이미지와 맞춤
frame_height, frame_width, _ = photo_frame.shape
merged_image_height, merged_image_width, _ = merged_image.shape

# 합성 이미지의 중앙에 photo_frame 얹음
y_offset = (merged_image_height - frame_height) // 2
x_offset = (merged_image_width - frame_width) // 2
merged_image[y_offset:y_offset + frame_height, x_offset:x_offset + frame_width] = photo_frame

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