from pydantic import BaseModel
from quart import Blueprint, request, make_response

from src.flow import Generator, GenerateRequest
from src.logging import get_logger

streaming = Blueprint("streaming", __name__, url_prefix="/streaming")
log = get_logger(__name__)


class StreamDelta(BaseModel):
    role: str
    content: str


class StreamResponse(BaseModel):
    message: StreamDelta
    done: bool | None = None
    done_reason: str | None = None


@streaming.post("/generate")
async def response_stream():
    data = await request.get_json()
    log.debug(f"data = {data}")
    prompt = GenerateRequest(**data)
    log.debug(f"GenerateRequest = {prompt}")
    generator = Generator()

    async def json_stream():
        async for chunk in generator.generate(prompt):
            to_send = StreamResponse(
                message=StreamDelta(
                    role=chunk.message.role,
                    content=chunk.message.content,
                ),
            )

            if chunk.done:
                to_send.done = True

            if chunk.done_reason:
                to_send.done_reason = chunk.done_reason

            log.debug(f"sending >> {to_send}")
            yield to_send.model_dump_json() + "\n"

    response = await make_response(
        json_stream(), 200, {"Content-Type": "application/json-lines"}
    )
    response.timeout = None  # No timeout for this route

    return response
