from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class Conversation(BaseModel):
    messages: list[Message]


class GenerateRequest(BaseModel):
    system: str | None = None
    model: str = "llama3.2"
    conversation: Conversation = Conversation(messages=[])
    prompt: str


class CompletionChunk(BaseModel):
    id: str
    role: str
    content: str
    finish: bool = False
    finish_reason: str | None = None


class Completion(BaseModel):
    id: str
    object: str
    created: int
    model: str
    chunks: list[CompletionChunk]
