import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from multiprocessing import Process, Queue
import time
from server.config import *
from server.protocol.interface import ServerLauncher, Server

class SMTPServer (Server):
    def __init__(self, txt_queue: Queue, file_queue: Queue):
        self.txt_queue = txt_queue
        self.file_queue = file_queue

    def connect(self):
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(RECIPIENT_EMAIL, RECIPIENT_PASSWORD)

        # Select the mailbox you want to check (e.g., 'inbox')
        mail.select('inbox')
        return mail

    def fetch_new_emails(self, mail : imaplib.IMAP4_SSL):
        # Search for all unread emails from a specific sender in the mailbox
        status, messages = mail.search(None, f'(UNSEEN FROM "{SENDER_EMAIL}")')
        email_ids = messages[0].split()

        # Fetch and process each unread email
        emails = []
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            emails.append((email_id, msg, msg_data))

        # Sort emails by sent time
        emails.sort(key=lambda x: parsedate_to_datetime(x[1]['Date']))
        # Close the connection and logout
        return emails

    def handle_emails(self, emails):
        for email_id, msg, msg_data in emails:
            # Decode the email subject
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else 'utf-8')

            # Check if the email is read or not
            flags = msg_data[0][0].decode()
            if '\\Seen' not in flags:

                # Extract the email body and attachments
                body = ""
                attachments = []
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if "attachment" in content_disposition:
                            filename = part.get_filename()
                            file_data = part.get_payload(decode=True)
                            attachments.append((filename, file_data))
                        elif content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode()
                else:
                    body = msg.get_payload(decode=True).decode()

                # Put the email body in the txt_queue
                self.txt_queue.put(body)

                # Put the attachments in the file_queue
                for filename, file_data in attachments:
                    self.file_queue.put((filename, file_data))

    def run(self):
        while True:
            try:
                mail = self.connect()
                emails = self.fetch_new_emails(mail)

                self.handle_emails(emails)

                time.sleep(SMTP_REFRESH_INTERVAL)
                mail.logout()
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(SMTP_REFRESH_INTERVAL)

class SMTPServerLauncher(ServerLauncher):
    def __init__(self, txt_queue: Queue, file_queue: Queue):
        self.txt_queue = txt_queue
        self.file_queue = file_queue
        self.process = None

    def launch(self):
        smtp_server = SMTPServer(self.txt_queue, self.file_queue)
        self.process = Process(target=smtp_server.run)
        self.process.start()
