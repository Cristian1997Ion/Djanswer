import os
from dependency_injector import containers, providers
import Djanswer.settings as settings
from .services import Mailer

class Container(containers.DeclarativeContainer):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djanswer.settings')

    config = providers.Configuration()
    mailer = providers.Singleton(Mailer, hostEmail = settings.EMAIL_HOST)