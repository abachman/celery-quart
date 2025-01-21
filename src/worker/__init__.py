import asyncio

from celery import Celery, Task
from quart import Quart

from src.worker.tasks import (
    get_task as get_task,
    get_task_from_app as get_task_from_app,
    register_tasks,
)


def celery_init_app(app: Quart) -> Celery:
    class QuartTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            async def run_in_async_context():
                async with app.app_context():
                    return await self.run(*args, **kwargs)

            return asyncio.run(run_in_async_context())

    celery_app = Celery(app.name, task_cls=QuartTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()

    register_tasks(celery_app)

    app.extensions["celery"] = celery_app
    return celery_app
