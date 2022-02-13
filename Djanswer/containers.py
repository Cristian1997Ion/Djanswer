from distutils.command.config import config
from dependency_injector import containers, providers
from django.conf import settings

from .services import Mailer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    mailer = providers.Singleton(Mailer, hostEmail = settings.EMAIL_HOST)