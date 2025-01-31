from ollama import Client, ChatResponse
from typing import Iterator

client = Client(host="http://host.docker.internal:11434")
stream: Iterator[ChatResponse] = client.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
    stream=True,
)

for chunk in stream:
    breakpoint()
    print(chunk["message"]["content"], end="", flush=True)
