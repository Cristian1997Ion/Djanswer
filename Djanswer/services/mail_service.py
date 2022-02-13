from typing import List
from django.core.mail import send_mail
from django.conf import settings


class Mailer():
    
    def __init__(self, hostEmail: str):
        self.hostEmail = hostEmail

    def send(self, to: List[str], subject: str, message: str):
        send_mail(subject, message, self.hostEmail, to, False)