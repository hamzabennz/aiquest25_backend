# fraud_detection.py
from abc import ABC, abstractmethod
from django.utils import timezone
from urllib.parse import urlparse
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class QRCodeData:
    url: str
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    transaction_at: Optional[datetime] = None

class FraudDetector(ABC):
    def is_suspicious(self, qr_data: QRCodeData) -> tuple[bool, str]:
        """
        Check if the QR code data is suspicious
        Returns: (is_suspicious: bool, reason: str)
        """

        # HERE IS THE BUSINESS LOGIC OF MODELS
        return (True, "Unknown")


