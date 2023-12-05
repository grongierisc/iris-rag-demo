from grongier.pex import BusinessService

from rag.msg import ChatRequest, ChatClearRequest, FileIngestionRequest, ChatResponse

class ChatService(BusinessService):

    def __init__(self):
        self.target = ""

    def on_init(self):
        if self.target:
            self.target = "ChatOperation"

    def ingest(self, file_path: str):
        # build message
        msg = FileIngestionRequest(file_path=file_path)
        # send message
        self.send_request_sync(target=self.target, request=msg)

    def ask(self, query: str, rag: bool = False):
        # build message
        msg = ChatRequest(query=query, rag=rag)
        # send message
        response = self.send_request_sync(target=self.target, request=msg)
        # return response
        if type(response) is type(ChatResponse):
            return response.response
        else:
            return None

    def clear(self):
        # build message
        msg = ChatClearRequest()
        # send message
        self.send_request_sync(target=self.target, request=msg)