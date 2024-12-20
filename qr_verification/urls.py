# urls.py
from django.urls import path
from .views import QRVerificationView
from .fraud_detection import FraudDetector

# Initialize with production fraud detector
fraud_detector = FraudDetector()

urlpatterns = [
    path('api/verify-qr/', QRVerificationView.as_view(fraud_detector=fraud_detector), name='verify-qr'),
]