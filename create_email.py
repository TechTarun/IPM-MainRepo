import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import web_speech2text as s2t
import web_text2speech as t2s

def send_mail(content):
    sender_email = "testitonpython@gmail.com"
    t2s.say("Enter receiver email")
    text = s2t.listen().split()
    if('dot' in text):
        text[text.index('dot')] = '.'
    if('underscore' in text):
        text[text.index('underscore')] = '_'
    receiver_email = ''.join(text)
    subject = "Query result data"
    password = "test_password"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = str(content)
    # html = """\
    # <html>
    #   <body>
    #     <p>Hi,<br>
    #        How are you?<br>
    #        <a href="http://www.realpython.com">Real Python</a> 
    #        has many great tutorials.
    #     </p>
    #   </body>
    # </html>
    # """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    # part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    # message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

