from threading import Thread
from flask import render_template
from flask_mail import Message
from flask_babel import _
from app import app, mail
import time


def send_async_email(app, msg):
    """Send email with retry logic and exponential backoff."""
    max_retries = 3
    retry_delay = 1  # Start with 1 second delay
    
    with app.app_context():
        for attempt in range(max_retries):
            try:
                mail.send(msg)
                app.logger.info(f'Email sent successfully: {msg.subject}')
                return
            except Exception as e:
                app.logger.warning(
                    f'Failed to send email (attempt {attempt + 1}/{max_retries}): {str(e)}'
                )
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    app.logger.error(
                        f'Failed to send email after {max_retries} attempts: {msg.subject}'
                    )
                    raise


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[Microblog] Reset Your Password'),
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
