from ollama import Client, ChatResponse
from typing import Literal, AsyncGenerator

from src.logging import get_logger
from .types import Completion, GenerateRequest

log = get_logger(__name__)

# ChatResponse(
#     model="llama3.2",
#     created_at="2025-01-26T07:26:39.158508Z",
#     done=False,
#     done_reason=None,
#     total_duration=None,
#     load_duration=None,
#     prompt_eval_count=None,
#     prompt_eval_duration=None,
#     eval_count=None,
#     eval_duration=None,
#     message=Message(role="assistant", content="The", images=None, tool_calls=None),
# )


# given a prompt, generate a stream of completion chunks and store the complete response
# in a variable
class Generator:
    client: Client
    state: Literal["idle", "generating", "complete"]
    completion: Completion
    model: str

    def __init__(self):
        self.state = "idle"
        self.model = "llama3.2"  # "deepseek-r1:7b"
        self.client = Client(host="http://host.docker.internal:11434")

    def generate(self, prompt: GenerateRequest) -> AsyncGenerator[ChatResponse, None]:
        system_prompt = {
            "role": "system",
            "content": "You are a helpful assistant. Be careful to answer concisely and stick to the point.",
        }

        async def generate_stream():
            messages = [
                system_prompt,
                *[
                    dict(role=message.role, content=message.content)
                    for message in prompt.conversation.messages
                ],
                {"role": "user", "content": prompt.prompt},
            ]
            log.debug(messages)

            stream: ChatResponse = self.client.chat(
                model="llama3.2",
                messages=messages,
                stream=True,
            )

            for chunk in stream:
                # chunk is a ChatResponse
                yield chunk

        return generate_stream()
