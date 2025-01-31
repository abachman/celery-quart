import json
from quart import Blueprint, request

from src.flow import Generator, GenerateRequest
from src.logging import log

streaming = Blueprint("streaming", __name__)


@streaming.post("/generate")
async def response_stream():
    data = await request.get_json()
    log.debug(f"data = {data}")
    prompt = GenerateRequest(**data)
    log.debug(f"GenerateRequest = {prompt}")
    generator = Generator()

    async def json_stream():
        async for chunk in generator.generate(prompt):
            to_send = {
                "message": {
                    "role": chunk.message.role,
                    "content": chunk.message.content,
                },
                "done": chunk.done,
                "done_reason": chunk.done_reason,
            }
            log.debug(f"sending >> {to_send}")
            yield json.dumps(to_send) + "\n"

    return json_stream(), 200, {"Content-Type": "application/stream+json"}
