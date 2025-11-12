from iop import Message
from dataclasses import dataclass

@dataclass
class FileIngestionRequest(Message):
    file_path: str
@dataclass
class ChatRequest(Message):
    query: str = ""

@dataclass
class ChatResponse(Message):
    response: str = ""
@dataclass
class ChatClearRequest(Message):
    pass

@dataclass
class VectorSearchRequest(Message):
    query: str = ""

@dataclass
class VectorSearchResponse(Message):
    docs: list = None