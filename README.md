A Quart + Celery + Redis + LLM + Postgres + SQLAlchemy demo.

## uses

- [Quart](https://github.com/pgjones/quart)
- [Celery](https://github.com/celery/celery)
- [Redis](https://github.com/redis/redis)
- [pgvector](https://github.com/pgvector/pgvector)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
- [Ollama](https://github.com/ollama/ollama)
- [uv](https://docs.astral.sh/uv/)
- [docker compose](https://github.com/docker/compose)

## Run

```sh
docker compose up
```

## How Things Work

There are two apps we care about:

- `web`
- `worker`

Both use the same Dockerfile and ENV.

### web

`app.py` is the Quart app, when run it starts a Quart web server.

There are some API endpoints in `src/api/routes.py`:

```
Endpoint           Methods  Rule
-----------------  -------  ----------------------------
api.chat           POST     /api/chat
api.response       GET      /api/response/<task_id>
api.response_poll  GET      /api/response/<task_id>/poll
home               GET      /
static             GET      /static/<path:filename>
```

### worker

`src/worker` is the Celery supporting code.

`celery_init_app` is a [Celery app factory function](https://flask.palletsprojects.com/en/stable/patterns/appfactories/) which receives a Quart app instance and returns a Celery app instance.

Tasks are defined in `src/worker/tasks.py`, which includes another app factory function, `register_tasks`, which accepts the Celery app instance created in `celery_init_app`.

`src/make_celery.py` is run it starts a Celery worker.

It uses `src/create_app.py` to create the Quart app.
