import smtplib
from email.message import EmailMessage

from celery import Celery
from src.config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker='redis://localhost:6379')


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = 'Натрейдил Отчет Дашборд'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {username}, а вот и ваш отчет. Зацените 😊</h1>'
        '<img width="600" src="https://www.google.com/url?sa=i&url=https%3A%2F%2Fsmartprogress.do%2Fgoal%2F'
        '417961%2F&psig=AOvVaw3FLhWthzuIz_uwLzNzo6_e&ust=1725796954431000&source=images&cd=vfe&opi=89978449&ved='
        '0CBQQjRxqFwoTCMDOyubksIgDFQAAAAAdAAAAABAE" alt="">'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
