# SME Assistant UI

A Streamlit-based chat interface for the Wind Turbine Equipment Subject Matter Expert (SME) Assistant, powered by Amazon Bedrock and AWS Lambda.

## Overview

This application provides a conversational UI that allows users to interact with an AI assistant specialized in wind turbine manufacturing and maintenance. Users can paste equipment logs or ask questions, and the assistant returns expert-level summaries and insights powered by Amazon Nova Pro via Amazon Bedrock.

## Architecture

```
User (Browser)
    │
    ▼
Streamlit UI (sme_assistant_ui)
    │  HTTP POST /sme_assistant
    ▼
AWS API Gateway
    │
    ▼
AWS Lambda (lambda_function.py)
    │  invoke_model
    ▼
Amazon Bedrock (amazon.nova-pro-v1:0)
```

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Access to the deployed AWS API Gateway endpoint

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd Equipment_SME_Code/sme_assistant_ui

# Install dependencies with uv
uv sync
```

## Running the App

```bash
uv run streamlit run main.py
```

The app will open at `http://localhost:8501`.

## Usage

1. Type a question or paste equipment log data into the chat input.
2. Press **Enter** to submit.
3. The assistant responds with an AI-generated summary or analysis.

Chat history is preserved within the session — previous messages remain visible as you continue the conversation.

## Project Structure

```
sme_assistant_ui/
├── main.py              # Streamlit chat application
├── pyproject.toml       # Project metadata and dependencies
├── uv.lock              # Locked dependency versions
└── .python-version      # Python version pin (3.13)
```

## Backend (Lambda + Bedrock)

The backend is an AWS Lambda function exposed via API Gateway. It:

- Receives a `{ "prompt": "..." }` payload from API Gateway.
- Sends the prompt to `amazon.nova-pro-v1:0` via `bedrock-runtime`.
- Uses a system prompt instructing the model to act as a wind turbine manufacturing assistant and summarize logs in 5 lines.
- Returns the model response wrapped in `{ "statusCode": 200, "body": "<json string>" }`.

Key inference parameters:

| Parameter   | Value |
|-------------|-------|
| maxTokens   | 2500  |
| temperature | 0.7   |
| topP        | 0.9   |
| topK        | 20    |

## Dependencies

| Package      | Version  |
|--------------|----------|
| streamlit    | >=1.56.0 |
| requests     | (stdlib) |

## Related Files

| File                        | Purpose                                          |
|-----------------------------|--------------------------------------------------|
| `streamlit_app.py`          | Alternative enterprise-styled UI (no chat history) |
