from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .fraud_detection import FraudDetector, QRCodeData
from .models import QRTransaction

class QRVerificationView(APIView):
    fraud_detector = None

    def __init__(self, fraud_detector: FraudDetector = None, **kwargs):
        super().__init__(**kwargs)
        self.fraud_detector = fraud_detector

    def post(self, request):
        data = request.data

        # Create QRCodeData instance
        qr_data = QRCodeData(
            url=data.get('url'),
            created_at=data.get('created_at'),
            expires_at=data.get('expires_at'),
            transaction_at=data.get('transaction_at')
        )

        # Check for suspicious patterns
        is_suspicious, reason = self.fraud_detector.is_suspicious(qr_data)

        # Record transaction
        transaction = QRTransaction.objects.create(
            url=qr_data.url,
            created_at=qr_data.created_at,
            expires_at=qr_data.expires_at,
            transaction_at=qr_data.transaction_at,
            is_suspicious=is_suspicious,
            suspicion_reason=reason
        )

        return Response({
            'is_suspicious': is_suspicious,
            'reason': reason,
            'verification_id': transaction.id
        }, status=status.HTTP_200_OK)