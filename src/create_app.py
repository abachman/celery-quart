import os

from quart import Quart

from src.api import background, streaming
from src.commands import attach_commands
from src.worker import celery_init_app


def create_app() -> Quart:
    app = Quart(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=os.environ.get("REDIS_URL"),
            result_backend=os.environ.get("REDIS_URL"),
            broker_connection_retry_on_startup=True,
            # task_ignore_result=True,
        ),
    )

    app.register_blueprint(background, url_prefix="/api")
    app.register_blueprint(streaming, url_prefix="/streaming")

    celery_init_app(app)
    attach_commands(app)

    return app
