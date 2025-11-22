# Services

This directory contains API service integrations for the Shisui Learning Assistant.

## OpenRouter Service

The OpenRouter service provides a clean interface to interact with various LLM models through the OpenRouter API.

### Setup

1. **Get an API Key**: Sign up at [OpenRouter](https://openrouter.ai/) and get your API key

2. **Add to Environment**: Add your API key to `.env`:
   ```bash
   OPENROUTER_API_KEY=your_actual_api_key_here
   SITE_URL=http://localhost:8000  # Optional
   SITE_NAME=Shisui Learning Assistant  # Optional
   ```

3. **Install Dependencies**: Make sure `requests` and `python-dotenv` are installed:
   ```bash
   pip install requests python-dotenv
   ```

### Usage

#### Using the Service Class

```python
from services.openrouter_service import OpenRouterService

# Initialize the service
service = OpenRouterService()

# Send a chat completion request
messages = [
    {"role": "user", "content": "What is the meaning of life?"}
]

response = service.chat_completion(
    messages=messages,
    model="openai/gpt-4o",  # or any other model
    temperature=0.7
)

print(response["choices"][0]["message"]["content"])
```

#### Using the Convenience Function

```python
from services.openrouter_service import ask_openrouter

# Quick question
answer = ask_openrouter(
    question="Explain quantum computing in one sentence.",
    model="openai/gpt-4o",
    system_prompt="You are a helpful assistant."
)

print(answer)
```

### Available Models

Some popular models available through OpenRouter:

- `openai/gpt-4o` - GPT-4 Optimized
- `openai/gpt-4-turbo` - GPT-4 Turbo
- `anthropic/claude-3-opus` - Claude 3 Opus
- `anthropic/claude-3-sonnet` - Claude 3 Sonnet
- `google/gemini-flash-1.5` - Gemini Flash 1.5
- `google/gemini-pro-1.5` - Gemini Pro 1.5
- `meta-llama/llama-3.1-70b-instruct` - Llama 3.1 70B

To get a full list of available models:

```python
service = OpenRouterService()
models = service.get_available_models()
print(models)
```

### Testing

Run the test suite:

```bash
cd Shisui-backend
python tests/openrouter.py
```

### API Reference

#### `OpenRouterService`

**Methods:**

- `chat_completion(messages, model, temperature, max_tokens, stream)`: Send a chat completion request
  - `messages`: List of message dicts with 'role' and 'content'
  - `model`: Model identifier (default: "openai/gpt-4o")
  - `temperature`: Sampling temperature 0-2 (default: 0.7)
  - `max_tokens`: Maximum tokens to generate (optional)
  - `stream`: Enable streaming (default: False)

- `get_available_models()`: Fetch list of available models

#### `ask_openrouter(question, model, system_prompt)`

Convenience function for quick queries.

- `question`: The user's question
- `model`: Model to use (default: "openai/gpt-4o")
- `system_prompt`: Optional system prompt

Returns the assistant's response as a string.

### Error Handling

The service includes proper error handling:

```python
try:
    response = service.chat_completion(messages=messages)
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

### Notes

- The service automatically loads environment variables from `.env`
- API key is required and will raise `ValueError` if not found
- All requests include proper headers for OpenRouter rankings
- Timeout is set to 60 seconds for completion requests
