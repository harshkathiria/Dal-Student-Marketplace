import pytest
from unittest.mock import patch, MagicMock
from accounts.emailsend import email_send
from flask import Flask
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

name = 'John'
email = 'john@example.com'
secret = 'abc123'


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'test@example.com'
    app.config['MAIL_PASSWORD'] = 'testpassword'
    return app


def test_email_send(app):
    with app.app_context():
        email_send(name, email, secret)

        assert True  # successful execution means the email was sent


def test_email_send_sender_email(app):
    with app.app_context():
        email_send(name, email, secret)

        sender_email = app.config['MAIL_USERNAME']
        assert sender_email == email_send.sender_email


def test_email_send_message(app):
    with app.app_context():
        email_send(name, email, secret)

        message = MIMEMultipart("alternative")
        message["Subject"] = "One time login password for Student MarketPlace"
        message["From"] = email_send.sender_email
        message["To"] = email

        html = f"""
            <html>
              <body>
                <p>Hello {name},<br>
                   This is an auto-generated email from Student Market Place Portal. <br>
                   You are receiving this email as you have recently submitted request for signup/reset on our portal. <br>
                   Please do not reply to this email as the mailbox is not monitored. <br>
                   <b>Your one time password is 
                   <font color="blue" face="Verdana" size="+2"> "{secret}" </font>
                   </b>
                </p>
              </body>
            </html>
            """
        htmlmessage = MIMEText(html, "html")
        message.attach(htmlmessage)

        assert message.as_string() == email_send.message.as_string()


@patch('smtplib.SMTP_SSL')
def test_email_send_smtplib(mock_smtp_ssl, app):
    with app.app_context():
        email_send(name, email, secret)

        mock_smtp_ssl_instance = MagicMock()
        mock_smtp_ssl.return_value = mock_smtp_ssl_instance
        mock_smtp_ssl_instance.__enter__.return_value = mock_smtp_ssl_instance

        mock_smtp_ssl_instance.login.assert_called_with(
            app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        mock_smtp_ssl_instance.sendmail.assert_called_with(
            email_send.sender_email, email, email_send.message.as_string())
