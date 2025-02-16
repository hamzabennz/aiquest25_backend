import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def validate_phone_number(phone_number):
    """
    Validates the phone number format.
    """
    return re.match(r"^\+?[1-9]\d{1,14}$", phone_number)

def validate_email(email):
    """
    Validates the email format.
    """
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", email)

def send_sms(phone_number, message):
    """
    Sends an SMS after validation and confirmation.
    """
    if not validate_phone_number(phone_number):
        return "Invalid phone number format."

    # Simulate user confirmation
    confirmation = input(f"Send SMS to {phone_number}? (yes/no): ").strip().lower()
    if confirmation != "yes":
        return "SMS sending canceled by user."

    # Simulate SMS sending (use an actual SMS API like Twilio in production)
    print(f"SMS sent to {phone_number}: {message}")
    return "SMS sent successfully."

def send_email(email, subject, body):
    """
    Sends an email after validation and confirmation.
    """
    if not validate_email(email):
        return "Invalid email format."

    # Simulate user confirmation
    confirmation = input(f"Send email to {email}? (yes/no): ").strip().lower()
    if confirmation != "yes":
        return "Email sending canceled by user."

    # Example email sending (replace with actual credentials)
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    try:
        # Create email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send email via SMTP
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email: {e}"

# Example Usage
action = input("Enter action (sms/email): ").strip().lower()

if action == "sms":
    phone = input("Enter phone number: ")
    message = input("Enter SMS message: ")
    print(send_sms(phone, message))
elif action == "email":
    email = input("Enter recipient email: ")
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")
    print(send_email(email, subject, body))
else:
    print("Invalid action.")