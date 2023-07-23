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
# photoFrame과 사진 합성하기
# cv2.imshow('Show image', photo_frame)
cv2.waitKey(0)
merged_image = photo_frame

merged_image_name = "mergedImage.jpg"
cv2.imwrite(merged_image_name, merged_image)
blob = bucket.blob(f"images/{merged_image_name}")
# 로컬파일을 firebase storage에 업로드
blob.upload_from_filename(merged_image_name)

# 메모리에서 이미지 삭제
for image in images:
    image.release()
    
cv2.destroyAllWindows()