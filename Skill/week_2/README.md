# Week 2 Lab: Provider-Agnostic LLM Client

Build a provider-agnostic LLM client in Python: one unified interface (`LLMClient`) over a hosted API (Google Gemini) and a local model (Ollama).

## Learning Objectives
- Design an abstract base class (`LLMProvider`) to define a common interface for different LLM backends.
- Implement a cloud-hosted provider (`GeminiProvider`) using the Google GenAI SDK.
- Implement a local provider (`OllamaProvider`) connecting to a locally running Ollama instance (`llama3.2`).
- Build a client class (`LLMClient`) that delegates generation to any provider adhering to the interface.
- Write unit tests using mock providers to test the client in isolation.

## Project Structure
```text
week_2/
├── .env                # Local secrets (ignored by git)
├── .env.example        # Template for environment variables
├── .gitignore          # Prevents committing secrets and virtual environments
├── llm_client.py       # Core classes: LLMProvider (ABC), GeminiProvider, OllamaProvider, LLMClient
├── main.py             # CLI application for prompting Gemini or Ollama
├── test_client.py      # Unit tests for LLMClient and providers
├── requirements.txt    # Project dependencies
└── README.md           # Documentation and instructions
```

## Setup Instructions

### 1. Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Create a `.env` file in the project directory:
```bash
cp .env.example .env
```
Open `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Set Up Local Ollama (Optional for local testing)
1. Download and install Ollama from [ollama.com](https://ollama.com/download).
2. Start the Ollama server:
   ```bash
   ollama serve
   ```
3. Pull the `llama3.2` model:
   ```bash
   ollama pull llama3.2
   ```

### 5. Run Unit Tests
```bash
pytest -v
```
or:
```bash
python test_client.py
```

### 6. Run the Program
```bash
python main.py
```
- Select `gemini` for Google GenAI cloud inference.
- Select `ollama` for local inference using your local `llama3.2` model.
