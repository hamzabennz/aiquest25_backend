# views.py
from datetime import timezone
import re
from urllib.parse import urlparse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from qr_verification.fraud_detection import FraudDetector, QRCodeData
from qr_verification.models import QRTransaction
from qr_verification.serializers import QRVerificationSerializer

class QRVerificationView(APIView):
    fraud_detector = None
    def __init__(self, fraud_detector: FraudDetector = None, **kwargs):
        super().__init__(**kwargs)
        # Use configured detector or fallback to pass-through
        self.fraud_detector = fraud_detector

    def post(self, request):
        serializer = QRVerificationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = serializer.validated_data
        qr_data = QRCodeData(
            url=data['url'],
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
        })

