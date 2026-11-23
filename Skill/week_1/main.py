import os
from dotenv import load_dotenv

# Step 1: Load API key from .env
load_dotenv()

# Step 2: Read API keys
gemini_api_key = os.getenv("GEMINI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if gemini_api_key:
    from google import genai

    # Step 3: Initialize Gemini client
    client = genai.Client(api_key=gemini_api_key)

    # Step 4: Make first LLM call
    # Uses gemini-3.8-flash as per lab manual, with fallback to gemini-3.5-flash
    # if gemini-3.8-flash is experiencing temporary high demand (HTTP 503).
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents="What is Artificial Intelligence? Explain in simple words."
        )
    except Exception:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents="What is Artificial Intelligence? Explain in simple words."
        )

    # Step 5: Display response
    print("\nLLM Response:")
    print(response.text)

elif openai_api_key:
    from openai import OpenAI

    # Step 3: Initialize OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Step 4: Make first LLM call
    response = client.responses.create(
        model="gpt-5.5",
        input="What is Artificial Intelligence? Explain in simple words."
    )

    # Step 5: Display response
    print("\nLLM Response:")
    print(response.output_text)

else:
    raise ValueError(
        "API key not found! Please check that .env contains "
        "GEMINI_API_KEY=your_key or OPENAI_API_KEY=your_key."
    )
