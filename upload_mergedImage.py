from firebase_config import bucket
from hand_selfie import cv2, np
import os

# 이미지를 병합해서 firebase에 저장하기
image_names = ["photo1.jpg", "photo2.jpg", "photo3.jpg", "photo4.jpg"]
images = []

for image_name in image_names:
    blob = bucket.blob(f"images/{image_name}")
    image_bytes = blob.download_as_bytes()
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    images.append(image)

# photoFrame 읽어오기 - 투명한 배경을 가진 png
photo_frame = cv2.imread('mediapipe-virtual-mouse/photoframe.png', cv2.IMREAD_UNCHANGED)

# 이미지 2개씩 2행으로 배열
row1 = np.hstack((images[0], images[1]))
row2 = np.hstack((images[2], images[3]))
merged_image = np.vstack((row1, row2))

# 합성이미지에 photo_frame 얹기
resized_photo_frame = cv2.resize(photo_frame, (merged_image.shape[1], merged_image.shape[0]))

# 알파 채널 분리
foreground_alpha = resized_photo_frame[:, :, 3]
foreground_rgb = resized_photo_frame[:, :, :3]

# 알파 채널을 3채널로 확장
foreground_alpha_expanded = np.expand_dims(foreground_alpha, axis=2)
foreground_alpha_expanded = np.repeat(foreground_alpha_expanded, 3, axis=2)

# photo_frame과 합성이미지 합치기
result = cv2.multiply(merged_image.astype(float), (1-(foreground_alpha_expanded / 255)))
result += cv2.multiply(foreground_rgb.astype(float), (foreground_alpha_expanded / 255))
result = result.astype(np.uint8)

# 합성한 콜라주를 로컬에 저장
merged_image_name = "mergedImage.jpg"
cv2.imwrite(merged_image_name, result)

blob = bucket.blob(f"images/{merged_image_name}")
# 로컬파일을 firebase storage에 업로드
blob.upload_from_filename(merged_image_name)

# Firebase Storage에서 기존 이미지들 삭제
for image_name in image_names:
    bucket.blob(f"images/{image_name}").delete()

# 메모리에서 이미지 삭제
for image in images:
    image.release()

# 로컬에 저장된 합성 이미지 파일 삭제
os.remove(merged_image_name)
    
cv2.destroyAllWindows()