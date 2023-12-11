import uuid
from grongier.pex import BusinessOperation
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.embeddings import FastEmbedEmbeddings
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain.vectorstores.utils import filter_complex_metadata
from langchain.chains import RetrievalQA

from rag.msg import ChatRequest, ChatClearRequest, FileIngestionRequest, ChatResponse

class ChatOperation(BusinessOperation):

    def __init__(self):
        self.model = None
        self.text_splitter = None
        self.vector_store = None
        self.retriever = None
        self.chain = None

    def on_init(self):
        self.model = Ollama(base_url="http://ollama:11434",model="orca-mini")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.vector_store = Chroma(persist_directory="vector",embedding_function=FastEmbedEmbeddings())

    def ingest(self, request: FileIngestionRequest):
        file_path = request.file_path
        file_type = self._get_file_type(file_path)
        if file_type == "pdf":
            self._ingest_pdf(file_path)
        elif file_type == "markdown":
            self._ingest_markdown(file_path)
        elif file_type == "text":
            self._ingest_text(file_path)
        else:
            raise Exception(f"Unknown file type: {file_type}")
        
    def _get_file_type(self, file_path: str):
        if file_path.lower().endswith(".pdf"):
            return "pdf"
        elif file_path.lower().endswith(".md"):
            return "markdown"
        elif file_path.lower().endswith(".txt"):
            return "text"
        else:
            return "unknown"

    def _store_chunks(self, chunks):
        ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in chunks]
        unique_ids = list(set(ids))
        self.vector_store.add_documents(chunks, ids = unique_ids)
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.5,
            },
        )

        self.chain = RetrievalQA.from_chain_type(
            self.model,
            retriever=self.retriever
        )
        
    def _ingest_text(self, file_path: str):
        docs = TextLoader(file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)

        self._store_chunks(chunks)
        
    def _ingest_pdf(self, file_path: str):
        docs = PyPDFLoader(file_path=file_path).load()
        chunks = self.text_splitter.split_documents(docs)
        chunks = filter_complex_metadata(chunks)

        self._store_chunks(chunks)
        
    def _ingest_markdown(self, file_path: str):
        # Document loader
        docs = TextLoader(file_path).load()

        # MD splits
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
        ]

        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        md_header_splits = markdown_splitter.split_text(docs[0].page_content)

        # Split
        chunks = self.text_splitter.split_documents(md_header_splits)
        chunks = filter_complex_metadata(chunks)

        self._store_chunks(chunks)

    def ask(self, request: ChatRequest):
        query = request.query
        rag = request.rag
        rsp = ChatResponse(response="")
        if not rag or self.chain is None:
            # send to ChatOllama
            rsp.response = self.model(query)
        else:
            # for logging purposes
            # check if the query is in the vector store
            docs = self.vector_store.similarity_search(query)
            for doc in docs:
                self.log_info(f"doc: {doc}")
            # send to ChatRag
            rsp.response = self.chain({"query": query})

        return rsp

    def clear(self, request: ChatClearRequest):
        self.on_tear_down()

    def on_tear_down(self):
        docs = self.vector_store.get()
        for id in docs['ids']:
            self.vector_store.delete(id)