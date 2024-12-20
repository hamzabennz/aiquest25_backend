# fraud_detection.py
from abc import ABC, abstractmethod
from django.utils import timezone
from urllib.parse import urlparse
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import joblib
import pandas as pd

@dataclass
class QRCodeData:
    url: str
    created_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    transaction_at: Optional[datetime] = None

class FraudDetector(ABC):
    def is_suspicious(self, qr_data: QRCodeData) -> tuple[bool, str]:
        """
        Check if the QR code data is suspicious using the qr_code_pipeline.
        Returns: (is_suspicious: bool, reason: str)
        """
        def extract_features(df, url_column):
            df['url_length'] = df[url_column].apply(len)
            df['num_special_chars'] = df[url_column].apply(lambda x: sum(1 for char in x if char in ['/', '?', '&', '=', '-', '_', '%', '.']))
            df['has_ip'] = df[url_column].apply(lambda x: any(part.isdigit() for part in x.split('.')))
            df['num_subdomains'] = df[url_column].apply(lambda x: len(x.split('.')) - 2 if 'http' not in x else len(x.split('/')[2].split('.')) - 2)
            df['top_level_domain'] = df[url_column].apply(lambda x: x.split('.')[-1].split('/')[0])
            return df

        def extract_lexical_features(df, url_column):
            import re
            
            # Check for uncommon characters
            uncommon_chars = re.compile(r'[^a-zA-Z0-9/:.\-_]')
            df['num_uncommon_chars'] = df[url_column].apply(lambda x: len(uncommon_chars.findall(x)))

            # Check if URL contains "@" symbol
            df['has_at_symbol'] = df[url_column].apply(lambda x: '@' in x)

            # Check if URL contains "http" or "https"
            df['uses_https'] = df[url_column].apply(lambda x: 'https' in x.lower())

            # Check for suspicious patterns like '-' in the domain
            df['has_suspicious_hyphens'] = df[url_column].apply(lambda x: '-' in x.split('/')[2])

            # Check the length of the domain
            df['domain_length'] = df[url_column].apply(lambda x: len(x.split('/')[2]) if 'http' in x else len(x.split('.')[0]))

            return df

        def preprocess_url(url):
            """
            Preprocess a single URL to extract features.
            """
            # Define a helper DataFrame for the URL
            df = pd.DataFrame([{'URL': url}])
            
            # Extract features
            df = extract_features(df, 'URL')
            df = extract_lexical_features(df, 'URL')
            
            return df

        def preprocess_timestamps(created_at, expires_at, transaction_at):
            """
            Preprocess timestamps and add related features.
            """
            # Create a helper DataFrame for timestamps
            df = pd.DataFrame([{
                'created_at': pd.to_datetime(created_at) if created_at else None,
                'expires_at': pd.to_datetime(expires_at) if expires_at else None,
                'transaction_at': pd.to_datetime(transaction_at) if transaction_at else None,
            }])
            
            # Add new timestamp-based features
            if created_at and expires_at and transaction_at:
                df['transaction_within_valid_period'] = (
                    (df['created_at'] <= df['transaction_at']) & (df['transaction_at'] <= df['expires_at'])
                ).astype(int)
            else:
                df['transaction_within_valid_period'] = 0  # Default to invalid if timestamps are missing
            
            return df

        def qr_code_pipeline(url, created_at=None, expires_at=None, transaction_at=None):
            """
            Pipeline to classify a URL using pretrained models for static and dynamic QR codes.
            """
            # Preprocess the URL
            url_features = preprocess_url(url)
            
            # Check if timestamps exist (Dynamic Model)
            if created_at and expires_at and transaction_at:
                # Preprocess timestamps
                timestamp_features = preprocess_timestamps(created_at, expires_at, transaction_at)
                
                # Combine URL and timestamp features
                combined_features = pd.concat([url_features, timestamp_features], axis=1)
                
                # Load the dynamic model and encoders
                dynamic_model = joblib.load('model/rfmodel_dynamic.joblib')
                type_encoder = joblib.load('model/type_encoder_dynamic.joblib')
                top_level_domain_encoder = joblib.load('model/top_level_domain_encoder_dynamic.joblib')
                
                # Encode categorical features
                combined_features['top_level_domain_encoded'] = top_level_domain_encoder.transform(
                    combined_features['top_level_domain']
                )
                
                # Select features for prediction
                dynamic_features = [
                    'url_length', 'num_special_chars', 'has_ip', 'num_subdomains',
                    'top_level_domain_encoded', 'transaction_within_valid_period'
                ]
                prediction = dynamic_model.predict(combined_features[dynamic_features])
            
            else:
                # Use Static Model
                # Load the static model and encoders
                static_model = joblib.load('model/rfmodel_static.joblib')
                type_encoder = joblib.load('model/type_encoder_static.joblib')
                top_level_domain_encoder = joblib.load('model/top_level_domain_encoder_static.joblib')
                
                # Encode categorical features
                url_features['top_level_domain_encoded'] = top_level_domain_encoder.transform(
                    url_features['top_level_domain']
                )
                
                # Select features for prediction
                static_features = [
                    'url_length', 'num_special_chars', 'has_ip', 'num_subdomains',
                    'top_level_domain_encoded', 'num_uncommon_chars', 'has_at_symbol',
                    'uses_https', 'has_suspicious_hyphens', 'domain_length'
                ]
                prediction = static_model.predict(url_features[static_features])
            
            # Decode the prediction
            prediction_label = type_encoder.inverse_transform(prediction)[0]
            
            # Return the result
            return {
                'URL': url,
                'Prediction': prediction_label,
                'Created_At': created_at,
                'Expires_At': expires_at,
                'Transaction_At': transaction_at
            }

        # Process the QR code data
        try:
            result = qr_code_pipeline(
                qr_data.url,
                qr_data.created_at,
                qr_data.expires_at,
                qr_data.transaction_at
            )

            # Determine if suspicious
            is_suspicious = result['Prediction'] == 'suspicious'
            reason = 'Classified as suspicious' if is_suspicious else 'Classified as safe'
            return is_suspicious, reason
        except Exception as e:
            return True, f"Error during detection: {str(e)}"

