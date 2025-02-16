import re
from vobject import readOne

# Function to validate vCard fields
def validate_vcard(vcard_content):
    try:
        # Parse the vCard content
        vcard = readOne(vcard_content)

        # Validate the full name (FN field)
        full_name = vcard.fn.value
        if not re.match(r"^[A-Za-z\s\-]+$", full_name):
            raise ValueError("Invalid full name format.")

        # Validate the telephone number (TEL field)
        if hasattr(vcard, 'tel'):
            phone_number = vcard.tel.value
            if not re.match(r"^\+?[0-9\s\-]+$", phone_number):
                raise ValueError("Invalid phone number format.")

        # Validate the email (EMAIL field)
        if hasattr(vcard, 'email'):
            email = vcard.email.value
            if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email):
                raise ValueError("Invalid email address format.")

        return True, "vCard is valid."
    except Exception as e:
        return False, str(e)

# Example vCard content (potentially malicious or valid)
vcard_data = """
BEGIN:VCARD
VERSION:3.0
FN:John Doe
TEL:+1234567890
EMAIL:john.doe@example.com
NOTE:<script>alert('This is malicious!');</script>
END:VCARD
"""

# Validate the vCard
is_valid, message = validate_vcard(vcard_data)

# Output the validation result
if is_valid:
    print("vCard is safe to use.")
else:
    print(f"vCard validation failed: {message}")