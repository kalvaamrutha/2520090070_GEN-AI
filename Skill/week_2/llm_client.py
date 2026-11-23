from abc import ABC, abstractmethod
import os
from google import genai
from google.genai import errors
import requests

# Common interface
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

# Gemini cloud provider
class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = None):
        if not api_key or not isinstance(api_key, str):
            raise ValueError("A valid Gemini API key must be provided.")
        
        cleaned_key = api_key.strip().strip("'\"")
        if not cleaned_key or "give your api key" in cleaned_key.lower():
            raise ValueError(
                "Gemini API key is not configured. Please set a valid GEMINI_API_KEY in .env"
            )
        
        try:
            cleaned_key.encode("ascii")
        except UnicodeEncodeError:
            raise ValueError(
                "Gemini API key contains invalid non-ASCII characters. Ensure your key was copied correctly."
            )
        
        self.api_key = cleaned_key
        # Default to GEMINI_MODEL env var or gemini-3.5-flash for maximum reliability
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
        self.client = genai.Client(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text
        except errors.APIError as e:
            raise RuntimeError(f"Gemini API error ({e.code}): {e.message}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to generate response from Gemini: {e}") from e

# Ollama local provider
class OllamaProvider(LLMProvider):
    def __init__(self, model="llama3.2"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()["response"]

# Common client
class LLMClient:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def generate(self, prompt: str) -> str:
        return self.provider.generate(prompt)
