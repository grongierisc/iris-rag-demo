from grongier.pex import BusinessService

from rag.msg import ChatRequest, ChatClearRequest, FileIngestionRequest, ChatResponse

class ChatService(BusinessService):

    def on_init(self):
        if not hasattr(self, "target"):
            self.target = "ChatOperation"

    def ingest(self, file_path: str):
        # build message
        msg = FileIngestionRequest(file_path=file_path)
        # send message
        self.send_request_sync(self.target, msg)

    def ask(self, query: str, rag: bool = False):
        # build message
        msg = ChatRequest(query=query, rag=rag)
        # send message
        response = self.send_request_sync(self.target, msg)
        # return response
        if response:
            self.log_info(f"response: {response.response}")
            # check if dict response.response has key "result"
            if "result" in response.response:
                return response.response["result"]
            else:
                return response.response
        else:
            return None

    def clear(self):
        # build message
        msg = ChatClearRequest()
        # send message
        self.send_request_sync(self.target, msg)