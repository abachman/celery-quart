import asyncio
import os

import click

# then, load the Alembic configuration and generate the
# version table, "stamping" it with the most recent rev:
from alembic.config import Config
from alembic import command

from src.logging import get_logger
from src.storage import Base, get_database_engine
from src.worker import get_task_from_app

log = get_logger(__name__)
alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "../alembic.ini"))


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

    async def drop_db():
        click.echo("resetting the database...")

        engine = get_database_engine()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        click.echo("done")

    async def create_db():
        click.echo("creating the database...")

        # engine = get_database_engine()

    async def upgrade_db():
        click.echo("upgrading database schema...")

        engine = get_database_engine()
        async with engine.begin() as conn:
            alembic_cfg.attributes["connection"] = conn
            command.upgrade(alembic_cfg, "head")

        click.echo("done")

    @db.command()
    def drop():
        asyncio.run(drop_db())

    @db.command()
    def reset():
        asyncio.run(drop_db())
        asyncio.run(create_db())
        asyncio.run(upgrade_db())

    @db.command()
    def upgrade():
        asyncio.run(upgrade_db())
