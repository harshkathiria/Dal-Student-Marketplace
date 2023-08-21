import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app


def email_send(name, email, secret):
    sender_email = current_app.config['MAIL_USERNAME']  # move this to config file
    receiver_email = email
    password = current_app.config['MAIL_PASSWORD']
    mailserver = current_app.config['MAIL_SERVER']
    mailport = current_app.config['MAIL_PORT']

    message = MIMEMultipart("alternative")
    message["Subject"] = "One time login password for Student MarketPlace"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the HTML version of your message

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

    # Turn these into plain/html MIMEText objects
    htmlmessage = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(htmlmessage)

    # Create secure connection with server and send email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(mailserver, mailport, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

# referenced from https://realpython.com/python-send-email/
