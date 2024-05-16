import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailSender:

    def __init__(self, **kwargs):
        self._username = kwargs["username"]
        self._password = kwargs["password"]
        self._sender_email = kwargs["sender_email"]
        self._smtp_server = kwargs["smtp_server"]
        self._smtp_port = kwargs["smtp_port"]
        self._server = None
        self._logged_in = False

    def _get_server(self):
        if not self._logged_in:
            return self._login_server()
        return self._server

    def _login_server(self):
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(self._smtp_server, self._smtp_port, context=context)
        server.login(self._username, self._password)
        self._logged_in = True
        self._server = server
        return self._server

    def send_mail(self, subject, body, email_to):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self._sender_email
        message["To"] = email_to
        part = MIMEText(body, "html")
        message.attach(part)
        server = self._get_server()
        server.sendmail(self._sender_email, email_to, message.as_string())
        return "Da gui mail"
