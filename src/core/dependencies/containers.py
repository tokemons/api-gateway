from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from src.config import Config


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["src.core.api", "src.modules"])
    config = providers.Configuration()
    config.from_pydantic(settings=Config())
