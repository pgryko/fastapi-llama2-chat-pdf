from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    role: str
    content: str

class ChatInput(BaseModel):
    messages: List[Message]

class ChatOutput(BaseModel):
    message: Message
