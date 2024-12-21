def validate_2fa_qr_content(content):
    # Expected otpauth format
    otp_auth_pattern = r"^otpauth:\/\/[a-z]+\/[A-Za-z0-9\-_]+(\?.+)?$"
    if re.match(otp_auth_pattern, content):
        return True, "Valid 2FA QR code."
    return False, "Invalid or suspicious 2FA QR code content."

# Example fake 2FA content
fake_2fa_content = "http://phishing-site.com"

# Validate 2FA QR code content
is_valid, message = validate_2fa_qr_content(fake_2fa_content)
print(message)