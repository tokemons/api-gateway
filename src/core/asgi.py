from fastapi import FastAPI
from sentry_sdk import init as sentry_init
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.asyncpg import AsyncPGIntegration
from sentry_sdk.integrations.loguru import LoguruIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from starlette.middleware.cors import CORSMiddleware

from src.config import settings
from src.core.api import core_router
from src.core.dependencies.containers import Container


class FastAPIWrapper(FastAPI):
    container: Container


def get_app() -> FastAPIWrapper:
    container = Container()

    if sentry_dsn := settings.sentry.api_dsn.get_secret_value():
        sentry_init(
            dsn=sentry_dsn,
            enable_tracing=settings.sentry.enable_tracing,
            traces_sample_rate=settings.sentry.traces_sample_rate,
            profiles_sample_rate=settings.sentry.profiles_sample_rate,
            integrations=[
                AsyncioIntegration(),
                AsyncPGIntegration(),
                LoguruIntegration(),
                SqlalchemyIntegration(),
            ],
        )
    app = FastAPIWrapper(
        title=settings.project_title,
        description=settings.project_description,
        version="0.0.1",
        swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
    )
    app.container = container
    allowed_origins = settings.allowed_hosts
    if allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_origin_regex="^https?://.*$",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    app.include_router(core_router)
    return app
