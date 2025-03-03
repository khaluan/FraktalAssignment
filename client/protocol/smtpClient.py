import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from client.config import *


class SMTPClient:
    def __init__(self, sender_email: str, sender_password: str, recipient_email: str):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email

    def send_file(self, attachment_path: str):
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = HEADER_FORMAT

        # Add the email body
        # msg.attach(MIMEText(BODY_FORMAT, 'plain'))

        # Add the attachment
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
            msg.attach(part)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)

    def send(self, payload: str):
        # Create the email message
        msg = EmailMessage()
        msg['Subject'] = HEADER_FORMAT
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg.set_content(payload)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
