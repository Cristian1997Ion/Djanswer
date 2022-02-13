from .containers import Container
from .settings import __dict__


container = Container()
container.config.from_dict(__dict__)