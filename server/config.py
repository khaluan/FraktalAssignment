import os

def try_getenv(key):
    try:
        return os.getenv(key)
    except:
        raise Exception(f"Environment variable {key} not found")

SERVER_IP = os.getenv('SERVER_IP', '0.0.0.0')
HTTPS_PORT = int(os.getenv('SERVER_PORT', 4443))

DNS_SERVER_IP = os.getenv('DNS_SERVER_IP', '0.0.0.0')
DNS_PORT = int(os.getenv('DNS_PORT', 5353))
DOMAIN_NAME = os.getenv('DOMAIN_NAME', 'mydomain.com')

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
SMTP_REFRESH_INTERVAL = os.getenv('SMTP_REFRESH_INTERVAL', 300)
HEADER_FORMAT = os.getenv('HEADER_FORMAT', 'Arbitrary email header')
BODY_FORMAT = os.getenv('BODY_FORMAT', 'Arbitrary email body')

SENDER_EMAIL = try_getenv('SENDER_EMAIL')
SENDER_PASSWORD = try_getenv('SENDER_PASSWORD')

RECIPIENT_EMAIL = try_getenv('RECIPIENT_EMAIL')
RECIPIENT_PASSWORD = try_getenv('RECIPIENT_PASSWORD')

