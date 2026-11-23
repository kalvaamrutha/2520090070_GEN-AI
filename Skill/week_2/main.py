import os
from dotenv import load_dotenv
from llm_client import (
    GeminiProvider,
    OllamaProvider,
    LLMClient
)

# Robust .env path resolution relative to script location
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=env_path, override=True)

provider_name = input(
    "Choose provider (gemini/ollama): "
).strip().lower()

if provider_name == "gemini":
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Gemini API key not found in .env")
    
    cleaned_key = api_key.strip().strip("'\"")
    if not cleaned_key or "give your api key" in cleaned_key.lower():
        raise ValueError(
            "Gemini API key is not configured. Please set your actual GEMINI_API_KEY in .env before selecting Gemini."
        )
    
    provider = GeminiProvider(cleaned_key)
elif provider_name == "ollama":
    provider = OllamaProvider("llama3.2")
else:
    raise ValueError("Invalid provider selected")

client = LLMClient(provider)
prompt = input("Enter your question: ")
answer = client.generate(prompt)
print("\nLLM Response:")
print(answer)
