from django.db import models

class QRTransaction(models.Model):
    url = models.URLField()
    created_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    transaction_at = models.DateTimeField(null=True, blank=True)
    is_suspicious = models.BooleanField(default=False)
    suspicion_reason = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QR Transaction {self.url} - {'Suspicious' if self.is_suspicious else 'Safe'}"
