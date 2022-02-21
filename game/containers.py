import os
from dependency_injector import containers, providers
from game.loggers import RoomLoggerBuilder

class Container(containers.DeclarativeContainer):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djanswer.settings')

    config = providers.Configuration()
    room_logger_builder = providers.Singleton(RoomLoggerBuilder)