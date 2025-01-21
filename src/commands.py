import asyncio

import click

from src.logging import log
from src.store import Base, get_database_engine
from src.worker import get_task_from_app


def attach_commands(app):
    @app.cli.command()
    @click.argument("message")
    def enqueue(message):
        task = get_task_from_app(app, "example_background_job").delay(message)
        log.info("example task enqueued: %s", task.id)

    @app.cli.command()
    @click.argument("message")
    def chat(message):
        task = get_task_from_app(app, "generate_completion").delay(message)
        log.info("generate_completion enqueued: %s", task.id)

    @app.cli.group()
    def db():
        pass

    @db.command()
    def reset():
        async def reset_db():
            click.echo("resetting the database...")

            engine = get_database_engine()
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

            click.echo("done")

        asyncio.run(reset_db())
