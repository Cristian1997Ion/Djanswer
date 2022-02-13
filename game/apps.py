from django.apps import AppConfig

from Djanswer import container


class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'

    def ready(self) -> None:
        container.wire(modules=['.views'])
        return super().ready()
