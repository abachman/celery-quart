from src.create_app import create_app

app = create_app()
worker = app.extensions["celery"]
