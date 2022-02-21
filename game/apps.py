from django.apps import AppConfig

from Djanswer import container as general_container
from game import container as game_container


class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'

    def ready(self) -> None:
        general_container.wire(modules=['.views'])
        game_container.wire(modules=['.engine'])
        return super().ready()
