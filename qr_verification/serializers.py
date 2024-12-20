# serializers.py
from rest_framework import serializers

class QRVerificationSerializer(serializers.Serializer):
    url = serializers.URLField()
    created_at = serializers.DateTimeField(required=False, allow_null=True)
    expires_at = serializers.DateTimeField(required=False, allow_null=True)
    transaction_at = serializers.DateTimeField(required=False, allow_null=True)

    def validate(self, data):
        # Basic timestamp validation
        if data.get('expires_at') and data.get('transaction_at'):
            if data['transaction_at'] > data['expires_at']:
                raise serializers.ValidationError("Transaction time cannot be after expiration time")
        
        if data.get('created_at') and data.get('expires_at'):
            if data['created_at'] > data['expires_at']:
                raise serializers.ValidationError("Creation time cannot be after expiration time")
        
        return data
