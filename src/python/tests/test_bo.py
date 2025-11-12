import unittest
from unittest.mock import MagicMock

from rag.bo import ChatOperation
from rag.msg import FileIngestionRequest, ChatRequest, ChatClearRequest

class TestChatOperation(unittest.TestCase):
    def setUp(self):
        self.operation = ChatOperation()

    def test_on_init(self):
        self.operation.on_init()
        self.assertIsNotNone(self.operation.model)
        self.assertIsNotNone(self.operation.text_splitter)

    def test_ask_without_rag(self):
        request = ChatRequest(query="What is the answer?")
        self.operation.model = MagicMock()
        self.operation.model.return_value = "response"

        response = self.operation.ask(request)

        self.operation.model.assert_called_once_with({"question": "What is the answer?"})
        self.assertEqual(response, "response")

    def test_ask_with_rag(self):
        request = ChatRequest(query="What is the answer?", rag=True)
        self.operation.chain = MagicMock()
        self.operation.chain.invoke.return_value = "response"

        response = self.operation.ask(request)

        self.operation.chain.invoke.assert_called_once_with("What is the answer?")
        self.assertEqual(response, "response")

    def test_clear(self):
        request = ChatClearRequest()
        self.operation.on_tear_down = MagicMock()

        self.operation.clear(request)

        self.operation.on_tear_down.assert_called_once()

    def test_on_tear_down(self):
        self.operation.vector_store = MagicMock()
        self.operation.retriever = MagicMock()
        self.operation.chain = MagicMock()

        self.operation.on_tear_down()

        self.assertIsNone(self.operation.vector_store)
        self.assertIsNone(self.operation.retriever)
        self.assertIsNone(self.operation.chain)

    def test_on_tear_down_no_mock(self):
        self.operation.on_init()
        self.operation.on_tear_down()

    def test_ask_whithout_rag_no_mock(self):
        request = ChatRequest(query="what is the iop module ?", rag=False)
        self.operation.on_init()

        response = self.operation.ask(request)

        self.assertIsNotNone(response)

    def test_ask_with_rag_no_mock(self):
        request = ChatRequest(query="what is the iop module ?", rag=True)
        self.operation.on_init()

        markdown_file = "misc/context.md"
        ingestion_request = FileIngestionRequest(file_path=markdown_file)
        self.operation.ingest(ingestion_request)

        response = self.operation.ask(request)

        self.assertIsNotNone(response)

    def test_ingest_text(self):
        text_file = "requirements.txt"
        ingestion_request = FileIngestionRequest(file_path=text_file)
        self.operation.on_init()

        self.operation.ingest(ingestion_request)

if __name__ == "__main__":
    unittest.main()