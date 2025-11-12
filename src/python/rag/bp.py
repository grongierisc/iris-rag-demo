from iop import BusinessProcess

from rag.msg import ChatRequest, ChatResponse, VectorSearchRequest, ChatClearRequest, FileIngestionRequest

class ChatProcess(BusinessProcess):
    """
    the aim of this process is to generate a prompt from a query
    if the vector similarity search returns a document, then we use the document's content as the prompt
    if the vector similarity search returns nothing, then we use the query as the prompt
    """
    def on_init(self):
        if not hasattr(self, "target_vector"):
            self.target_vector = "IrisVectorOperation"
        if not hasattr(self, "target_chat"):
            self.target_chat = "ChatOperation"

        # prompt template
        self.prompt_template = "Given the context: \n {context} \n Answer the question: {question}"


    def ask(self, request: ChatRequest):
        query = request.query
        prompt = ""
        # build message
        msg = VectorSearchRequest(query=query)
        # send message
        response = self.send_request_sync(self.target_vector, msg)
        # if we have a response, then use the first document's content as the prompt
        if response.docs:
            # add each document's content to the context
            context = "\n".join([doc['page_content'] for doc in response.docs])
            # build the prompt
            prompt = self.prompt_template.format(context=context, question=query)
        else:
            # use the query as the prompt
            prompt = query
        # build message
        msg = ChatRequest(query=prompt)
        # send message
        response = self.send_request_sync(self.target_chat, msg)
        # return response
        return response

    def clear(self, request: ChatClearRequest):
        # send message
        self.send_request_sync(self.target_vector, request)

    def ingest(self, request: FileIngestionRequest):
        # send message
        self.send_request_sync(self.target_vector, request)