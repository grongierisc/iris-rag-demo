import unittest
from unittest.mock import MagicMock, patch

from rag.bo import ChatOperation, ChromaVectorOperation, IrisVectorOperation
from rag.msg import FileIngestionRequest, ChatRequest, ChatClearRequest, VectorSearchRequest

class TestChatOperation(unittest.TestCase):
    def setUp(self):
        self.operation = ChatOperation()

    def test_on_init(self):
        with patch('rag.bo.OllamaLLM') as mock_llm:
            self.operation.on_init()
            self.assertIsNotNone(self.operation.model)
            mock_llm.assert_called_once_with(base_url="http://ollama:11434", model="orca-mini")

    def test_ask(self):
        request = ChatRequest(query="What is the answer?")
        self.operation.model = MagicMock()
        self.operation.model.invoke.return_value = "response"

        response = self.operation.ask(request)

        self.operation.model.invoke.assert_called_once_with("What is the answer?")
        self.assertEqual(response.response, "response")


class TestChromaVectorOperation(unittest.TestCase):
    def setUp(self):
        self.operation = ChromaVectorOperation()

    @patch('rag.bo.FastEmbedEmbeddings')
    @patch('rag.bo.Chroma')
    def test_on_init(self, mock_chroma, mock_embeddings):
        self.operation.on_init()
        self.assertIsNotNone(self.operation.text_splitter)
        self.assertIsNotNone(self.operation.vector_store)
        mock_chroma.assert_called_once()

    def test_clear(self):
        self.operation.vector_store = MagicMock()
        self.operation.vector_store.get.return_value = {'ids': ['id1', 'id2']}
        
        request = ChatClearRequest()
        self.operation.clear(request)

        self.assertEqual(self.operation.vector_store.delete.call_count, 2)

    def test_similar(self):
        request = VectorSearchRequest(query="test query")
        self.operation.vector_store = MagicMock()
        self.operation.vector_store.similarity_search.return_value = ["doc1", "doc2"]

        response = self.operation.similar(request)

        self.operation.vector_store.similarity_search.assert_called_once_with("test query")
        self.assertEqual(response.docs, ["doc1", "doc2"])

    @patch('rag.bo.TextLoader')
    def test_ingest_text(self, mock_loader):
        text_file = "requirements.txt"
        ingestion_request = FileIngestionRequest(file_path=text_file)
        
        mock_docs = [MagicMock(page_content="content")]
        mock_loader.return_value.load.return_value = mock_docs
        
        self.operation.text_splitter = MagicMock()
        self.operation.text_splitter.split_documents.return_value = mock_docs
        self.operation.vector_store = MagicMock()

        self.operation.ingest(ingestion_request)

        self.operation.vector_store.add_documents.assert_called_once()


class TestIrisVectorOperation(unittest.TestCase):
    def setUp(self):
        self.operation = IrisVectorOperation()
        self.operation.remote = False

    @patch('rag.bo.FastEmbedEmbeddings')
    @patch('rag.bo.IRISVector')
    def test_on_init_local(self, mock_iris, mock_embeddings):
        self.operation.on_init()
        self.assertIsNotNone(self.operation.text_splitter)
        self.assertIsNotNone(self.operation.vector_store)
        mock_iris.assert_called_once()

    @patch('rag.bo.FastEmbedEmbeddings')
    @patch('rag.bo.IRISVector')
    def test_on_init_remote(self, mock_iris, mock_embeddings):
        self.operation.remote = True
        self.operation.on_init()
        self.assertIsNotNone(self.operation.text_splitter)
        self.assertIsNotNone(self.operation.vector_store)
        mock_iris.assert_called_once_with(
            collection_name="vector",
            embedding_function=mock_embeddings.return_value,
            connection_string="iris://SuperUser:SYS@localhost:1972/IRISAPP"
        )

    def test_similarity_search_integration(self):
        """Integration test for similarity search without mocks"""
        # Initialize the operation
        self.operation.remote = True
        self.operation.on_init()
        
        # Clean up any existing data first
        clear_request = ChatClearRequest()
        try:
            self.operation.clear(clear_request)
        except Exception:
            pass  # Ignore if no data exists
        
        # Ingest a text file
        text_file = "requirements.txt"
        ingestion_request = FileIngestionRequest(file_path=text_file)
        self.operation.ingest(ingestion_request)
        
        # Perform similarity search
        search_request = VectorSearchRequest(query="langchain")
        response = self.operation.similar(search_request)
        
        # Verify results
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.docs)
        self.assertGreater(len(response.docs), 0)
        
        # Clean up
        self.operation.clear(clear_request)

if __name__ == "__main__":
    unittest.main()