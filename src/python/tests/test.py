from langchain.llms import Ollama
ollama = Ollama(base_url='http://localhost:11434',
model="orca-mini")
print(ollama("what is the grongier.pex module ?"))

# with langchain parse the README.md file
from langchain.document_loaders import TextLoader

# Document loader
data = TextLoader("demo/README.md")

# Markdown 
from langchain.text_splitter import MarkdownHeaderTextSplitter

headers_to_split_on = ["# ", "## ", "### ", "#### ", "##### ", "###### "]


headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]

# MD splits
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits = markdown_splitter.split_text(data.load()[0].page_content)

# Char-level splits
from langchain.text_splitter import RecursiveCharacterTextSplitter

chunk_size = 250
chunk_overlap = 30
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)

# Split
splits = text_splitter.split_documents(md_header_splits)

from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="orca-mini")
vectorstore = Chroma.from_documents(documents=splits, embedding=oembed)

question="what is the grongier.pex module ?"
docs = vectorstore.similarity_search(question)
print(len(docs))

from langchain.chains import RetrievalQA
qachain=RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
print(qachain({"query": question}))