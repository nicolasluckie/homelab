import smtplib
from email.mime.text import MIMEText

"""
Replace the SMTPserver and SMTPport variables with your own.
"""

def sendEmail(_subject, _msg):
    SMTPserver = '<smtp_server_url>'
    SMTPport = 587
    sender = 'Your Name <your_email>'
    destination = ['Receipient <receipient_email>']

    USERNAME = "<your_email>"
    PASSWORD = r'<your_password>'

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'html'

    message = f'''\
    <html>
    <head></head>
    <body>
    {_msg}
    </body>
    </html>
    '''

    try:
        msg = MIMEText(_msg, text_subtype)
        msg['Subject'] = _subject
        msg['From'] = sender
        msg['To'] = ','.join(destination)

        print("[+] Starting SMTP connection...")
        server = smtplib.SMTP(SMTPserver, SMTPport)
        server.ehlo()
        server.set_debuglevel(False)

        print("[+] Starting TLS...")
        server.starttls()
        server.ehlo()

        print("[+] Authenticating...")
        server.login(USERNAME, PASSWORD)
        try:
            print("[+] Sending...")
            server.sendmail(sender, destination, msg.as_string())
            print("[+] Sent!")
        finally:
            server.quit()
            print("[+] Closed SMTP connection.\n")

    except:
        print("[x] Failed.\n")

if __name__ == "__main__":
    sendEmail("Subject", "<p>Test email</p></>Written in HTML</p>")
