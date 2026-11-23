# Week 3 Lab: LLM Monitoring with MongoDB

Extend the provider-agnostic LLM client developed in Week-2. Log token usage, response latency, and estimated cost for every LLM call in MongoDB Atlas. Add request timeouts and retry handling for temporary failures.

---

## Learning Objectives
- **Token Tracking**: Capture prompt (input) and candidate/eval (output) tokens from Gemini and Ollama.
- **Latency Monitoring**: Measure the roundtrip time taken by each LLM request in milliseconds (including any retries).
- **Cost Estimation**: Estimate hosted API cost using configurable per-million token rates.
- **MongoDB Logging**: Store detailed usage records for both successful calls and final failures in MongoDB Atlas with resilient exponential backoff writes.
- **Reliability & Resilience**: Implement request timeouts and retry logic for transient errors (408, 429, 500, 502, 503, 504, connection errors, timeouts).

---

## Project Structure
```text
week_3/
├── .env                  # Local secrets and configuration (ignored by git)
├── .env.example          # Template for environment variables
├── .gitignore            # Prevents committing secrets, venvs, and cache files
├── encode_password.py    # Helper utility to URL-encode MongoDB password special characters
├── llm_client.py         # Common client with retry logic, cost computation, and provider abstractions
├── main.py               # Interactive CLI interface to query Gemini or Ollama
├── requirements.txt      # Project dependencies
├── test_client.py        # Unit tests verifying client behavior with mock providers and loggers
├── test_mongodb.py       # Diagnostic script to test connectivity to MongoDB Atlas
├── usage_logger.py       # MongoDB logger with timeouts and exponential retry backoff
└── README.md             # Lab documentation and instructions
```

---

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

### 3. Configure Environment Variables (`.env`)
Create a `.env` file in the `week_3` folder:
```bash
cp .env.example .env
```

Fill in your actual credentials:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.5-flash
MONGODB_URI=mongodb+srv://<username>:<encoded_password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
GEMINI_INPUT_PRICE_PER_MILLION=0
GEMINI_OUTPUT_PRICE_PER_MILLION=0
```
> **Tip**: If your MongoDB database password contains special characters like `@`, `#`, `%`, or `!`, run `python encode_password.py` to obtain the URL-safe encoded password before pasting it into `MONGODB_URI`.

### 4. Test MongoDB Connectivity
Run the test script to ensure your IP is whitelisted and credentials are correct:
```bash
python test_mongodb.py
```

### 5. Run Unit Tests
Run the mock tests without calling external APIs:
```bash
python -m unittest test_client.py
```
or with pytest:
```bash
pytest test_client.py -v
```

### 6. Run the Application
```bash
python main.py
```
1. Type `gemini` or `ollama` when prompted.
2. Enter your question/prompt.
3. Observe real-time metrics:
   - Latency (ms)
   - Input & Output token counts
   - Estimated cost (USD)
   - Status message confirming persistence to MongoDB Atlas

---

## Database & Collection Schema

The application automatically stores records in:
- **Database**: `llm_monitoring`
- **Collection**: `api_usage`

### Example MongoDB Document (Success)
```json
{
  "_id": { "$oid": "6b03f92f7bddca33647fc081" },
  "provider": "Gemini",
  "model": "gemini-3.5-flash",
  "input_tokens": 8,
  "output_tokens": 8,
  "total_tokens": 16,
  "latency_ms": 2333.83,
  "estimated_cost_usd": 0.0,
  "cost_type": "estimated_hosted_api_cost",
  "status": "success",
  "attempts": 1,
  "timestamp": { "$date": "2026-11-23T08:28:31.864Z" }
}
```

### Example MongoDB Document (Failure)
```json
{
  "_id": { "$oid": "6b03f93a7bddca33647fc082" },
  "provider": "Gemini",
  "model": "gemini-3.5-flash",
  "input_tokens": null,
  "output_tokens": null,
  "total_tokens": null,
  "latency_ms": 7120.45,
  "estimated_cost_usd": null,
  "status": "failed",
  "attempts": 3,
  "error": "Temporary error: Connection timed out",
  "timestamp": { "$date": "2026-11-23T08:29:10.120Z" }
}
```
