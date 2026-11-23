import unittest
from unittest.mock import MagicMock, patch
from llm_client import LLMClient, GeminiProvider, OllamaProvider

# Fake provider for testing LLMClient isolation
class FakeProvider:
    def generate(self, prompt):
        return "AI stands for Artificial Intelligence."

class TestLLMClient(unittest.TestCase):
    def test_generate(self):
        provider = FakeProvider()
        client = LLMClient(provider)
        result = client.generate("Explain AI")
        self.assertEqual(
            result,
            "AI stands for Artificial Intelligence."
        )

class TestGeminiProvider(unittest.TestCase):
    def test_empty_or_placeholder_key_raises_value_error(self):
        with self.assertRaises(ValueError):
            GeminiProvider("")
        with self.assertRaises(ValueError):
            GeminiProvider("Give your API Key here…")
        with self.assertRaises(ValueError):
            GeminiProvider("   ")

    def test_non_ascii_key_raises_value_error(self):
        with self.assertRaises(ValueError):
            GeminiProvider("AIzaSyTestKeyWithUnicode\u2026")

    @patch("llm_client.genai.Client")
    def test_gemini_generate_success(self, mock_genai_client_class):
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "This is a response from Gemini."
        mock_instance.models.generate_content.return_value = mock_response
        mock_genai_client_class.return_value = mock_instance

        provider = GeminiProvider("AIzaSyValidDummyTestKey123456789")
        client = LLMClient(provider)
        response = client.generate("Hello Gemini")

        self.assertEqual(response, "This is a response from Gemini.")
        mock_instance.models.generate_content.assert_called_once_with(
            model=provider.model,
            contents="Hello Gemini"
        )

class TestOllamaProvider(unittest.TestCase):
    @patch("llm_client.requests.post")
    def test_ollama_generate_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "This is a response from Ollama."}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        provider = OllamaProvider("llama3.2")
        client = LLMClient(provider)
        response = client.generate("Hello Ollama")

        self.assertEqual(response, "This is a response from Ollama.")
        mock_post.assert_called_once_with(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": "Hello Ollama",
                "stream": False
            },
            timeout=120
        )

if __name__ == "__main__":
    unittest.main()
