from email.message import EmailMessage
import ssl, smtplib

from reader import funk

port = 465  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = input("Type your senders email and press enter:")
receiver_email = input("Type receivers email and press enter:")
password = input("Type your password and press enter:")
subjeck = 'Hi there'
message = funk('mail.txt')

em = EmailMessage()
em['From'] = sender_email
em['To'] = sender_email
em['Subject'] = subjeck
em.set_content(message)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as smtp:
    smtp.login(sender_email, password)
    smtp.sendmail(sender_email, receiver_email, em.as_string())
