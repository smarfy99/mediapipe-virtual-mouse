# firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
# firebase 인증 정보 초기화
# firebase 서비스 계정 키(json파일)의 경로를 지정
cred = credentials.Certificate("firebase-service-account.json")
# firebase storage 버킷 이름으로 대체
firebase_admin.initialize_app(cred, {
    'storageBucket': 'mwm-mozi.appspot.com'
})
bucket = storage.bucket()