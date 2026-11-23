# Week 1 Lab: First LLM API Call

Connect a Python program to a Large Language Model (LLM) using the Google Gemini or OpenAI API.

## Learning Objectives
- Understand the role of an API key when connecting a Python application to an LLM.
- Securely store API keys in a `.env` file instead of hard-coding them.
- Send a prompt to an LLM model and display the generated response.
- Troubleshoot common authentication, quota, and model availability issues.

## Project Structure
```text
week_1/
├── .env                # Local secrets (ignored by git)
├── .env.example        # Template for environment variables
├── .gitignore          # Prevents committing secrets and virtual environments
├── main.py             # Main Python script for making LLM API calls
└── requirements.txt    # Project dependencies
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
Create a `.env` file in the project root:
```bash
cp .env.example .env
```
Open `.env` and add your API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
```
*(or `OPENAI_API_KEY=your_actual_openai_api_key` if using OpenAI)*

### 4. Run the Program
```bash
python main.py
```
