import uuid
from grongier.pex import BusinessOperation
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.embeddings import FastEmbedEmbeddings
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain.vectorstores.utils import filter_complex_metadata

from rag.msg import ChatRequest, ChatClearRequest, FileIngestionRequest, ChatResponse, VectorSearchRequest, VectorSearchResponse

class VectorOperation(BusinessOperation):

    def __init__(self):
        self.text_splitter = None
        self.vector_store = None

    def on_init(self):
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

    def clear(self, request: ChatClearRequest):
        self.on_tear_down()

    def similar(self, request: VectorSearchRequest):
        # do a similarity search
        docs = self.vector_store.similarity_search(request.query)
        # return the response
        return VectorSearchResponse(docs=docs)

    def on_tear_down(self):
        docs = self.vector_store.get()
        for id in docs['ids']:
            self.vector_store.delete(id)
        
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

class ChatOperation(BusinessOperation):

    def __init__(self):
        self.model = None

    def on_init(self):
        self.model = Ollama(base_url="http://ollama:11434",model="orca-mini")

    def ask(self, request: ChatRequest):
        return ChatResponse(response=self.model(request.query))

