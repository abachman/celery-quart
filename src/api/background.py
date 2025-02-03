import mistune
import structlog
from celery.result import AsyncResult
from pydantic import BaseModel
from quart import Blueprint, jsonify, request, render_template

from src.logging import get_logger
from src.worker import get_task

background = Blueprint("background", __name__, url_prefix="/background")
log = get_logger(__name__)


# 1. send a POST request to /chat to start a background generation task
@background.post("/chat")
async def chat():
    data = await request.form
    if not data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400

    task = get_task("generate_completion").delay(data["message"])

    structlog.contextvars.bind_contextvars(task_id=task.id)
    log.info("task enqueued")

    return await render_template("response_poll.html", task_id=task.id)


# 2. poll ths response endpoint to get the result when it becomes available
@background.get("/response/<task_id>")
async def response(task_id: str):
    structlog.contextvars.bind_contextvars(task_id=task_id)

    result = AsyncResult(task_id)
    payload = {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }

    log.info("task status check")
    return jsonify({"data": payload})


class PromptResponse(BaseModel):
    model: str
    role: str
    content: str
    created_at: str
    total_duration: int
    prompt_eval_count: int
    eval_count: int

    @property
    def formatted_content(self) -> str:
        return mistune.html(self.content)

    class Config:
        extra = "ignore"


# htmx compatible response polling
@background.get("/response/<task_id>/poll")
async def response_poll(task_id: str):
    structlog.contextvars.bind_contextvars(task_id=task_id)

    result = AsyncResult(task_id)

    if not result.ready():
        return await render_template("response_poll.html", task_id=task_id)

    message = result.result["message"]
    response = PromptResponse(**message, **result.result)
    return await render_template("response.html", response=response)
