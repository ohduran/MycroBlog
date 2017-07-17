"""Send email functionality."""
from flask_mail import Message
from flask import render_template
from config import ADMINS
from app import mail, app
from threading import Thread
from .decorators import async


@async
def send_async_email(application, msg):
    """Render the page and let the email handling happen in background."""
    with application.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """Send email functionality."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def follower_notification(followed, follower):
    """Send an email to the followed."""
    send_email("[MycroBlog] %s is now following you!" % follower.username,
                ADMINS[0],
                [followed.email, ADMINS[0]],
                render_template("follower_email.txt",
                                user=followed, follower=follower),
                render_template("follower_email.html",
                                user=followed, follower=follower))
