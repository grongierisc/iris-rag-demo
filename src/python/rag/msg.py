from grongier.pex import Message
from dataclasses import dataclass

@dataclass
class FileIngestionRequest(Message):
    file_path: str

@dataclass
class ChatRequest(Message):
    query: str = ""
    rag: bool = False
    history: list = None

@dataclass
class ChatResponse(Message):
    response: str = ""

@dataclass
class ChatClearRequest(Message):
    pass