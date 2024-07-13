import smtplib
from smtplib import SMTPNotSupportedError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.core.config import settings

class EmailService:
    def __init__(self) -> None:
        self.port = settings.MAIL_PORT
        self.host = settings.MAIL_HOST
        self.user = settings.MAIL_USERNAME
        self.password = settings.MAIL_PASSWORD
        self.sender_email = settings.MAIL_SENDER

    def send_email(self, to: str, message_str: str):
        try:
            message = MIMEMultipart('alternative')
            message['From'] = self.sender_email
            message['To'] = to
            message['Subject'] = 'BTG Pactual - FVP Subscription notification'

            html = f"""\
                <html>
                <body>
                    <p>
                        BTG Pactual - Notification
                        <br>
                        <b> {message_str} </b>
                    </p>
                </body>
                </html>
            """

            part = MIMEText(html, "html")
            message.attach(part)

            with smtplib.SMTP(host=self.host, port=self.port) as server:
                server.set_debuglevel(1)
                server.login(user=self.user, password=self.password)

                server.sendmail(
                    from_addr=self.sender_email,
                    to_addrs=to,
                    msg=message.as_string(),
                )
                server.quit()
            print(f"[INFO] Email sent to {to}")
        except SMTPNotSupportedError as e:
            print(f"[ERROR] EmailService.send_email: {str(e)}")
            raise e
