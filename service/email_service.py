import smtplib, ssl

from system.load_data import *
from system.logger import logger

config = load_data('config/config.yml')

def send_notification(message):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sent_from = config['EMAIL_ADDRESS']
    to = [config['EMAIL_ADDRESS']]
    subject = f'Notification from your DCA bot'
    body = message
    message = 'Subject: {}\n\n{}'.format(subject, body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sent_from, config['EMAIL_PASSWORD'])
            server.sendmail(sent_from, to, message)

    except Exception as e:
        logger.error(e)
