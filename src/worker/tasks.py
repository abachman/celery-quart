import asyncio
import random

import structlog
from celery import Task
from ollama import ChatResponse, Client
from quart import Quart, current_app

from src.logging import log


def register_tasks(celery_app):
    @celery_app.task
    async def example_background_job(message: str):
        log.info(f"simlating processing in {current_app.name}")
        await asyncio.sleep(random.randint(1, 5))
        log.info("completed processing")
        return {"result": f"[echo] {message}"}

    @celery_app.task
    async def generate_completion(prompt: str):
        model = "llama3.2"
        structlog.contextvars.bind_contextvars(model=model)

        client = Client(host="http://host.docker.internal:11434")
        response: ChatResponse = client.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        sleep_for = random.randint(4, 10)
        structlog.contextvars.bind_contextvars(sleep_for=sleep_for)

        await asyncio.sleep(sleep_for)

        log.info("GENERATION COMPLETE")
        return response.model_dump()


# if you have an instance of a Quart app, use this method
# for example, inside a Quart app.cli.command function
def get_task_from_app(app: Quart, name: str) -> Task:
    return app.extensions["celery"].tasks[f"src.worker.tasks.{name}"]


# if you are calling from inside the context of a running Quart app, use this method
# for example, inside a Quart route handler function
def get_task(name: str) -> Task:
    return get_task_from_app(current_app, name)
