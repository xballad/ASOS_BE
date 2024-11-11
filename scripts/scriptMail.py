import base64
import smtplib
from email.mime.image import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_email: str, new_password: str):
    sender_email = "plantit.noreply@gmail.com"
    sender_password = "xpny krpf hsst hksb"  # Use app-specific password if 2FA is enabled

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your New Password"
    message["From"] = sender_email
    message["To"] = to_email

    html_content = f"""
        <html>
          <body>
            <div style="text-align: center;">
              <h1>Forgot Password Request</h1>
              <p>Your new password is: <strong>{new_password}</strong></p>
              <p>Please log in with this new password and update it as soon as possible.</p>
            </div>
          </body>
        </html>
        """
    part_html = MIMEText(html_content, "html")
    message.attach(part_html)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {str(e)}")