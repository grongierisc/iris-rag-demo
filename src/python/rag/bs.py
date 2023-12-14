from grongier.pex import BusinessService

from rag.msg import ChatRequest, ChatClearRequest, FileIngestionRequest

class ChatService(BusinessService):

    def on_init(self):
        if not hasattr(self, "target_chat"):
            self.target_chat = "ChatProcess"
        if not hasattr(self, "target_vector"):
            self.target_vector = "VectorOperation"

    def ingest(self, file_path: str):
        # build message
        msg = FileIngestionRequest(file_path=file_path)
        # send message
        self.send_request_sync(self.target_vector, msg)

    def ask(self, query: str, rag: bool = False):
        # build message
        msg = ChatRequest(query=query)
        # send message
        response = self.send_request_sync(self.target_chat, msg)
        # return response
        return response.response

    def clear(self):
        # build message
        msg = ChatClearRequest()
        # send message
        self.send_request_sync(self.target_vector, msg)