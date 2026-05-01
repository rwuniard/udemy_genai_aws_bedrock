# Chatbot App (LangChain Agent + AWS Bedrock)

Interactive console chatbot using:
- `ChatBedrockConverse` (Bedrock model connector)
- `create_agent` (LangChain agent runtime)
- `InMemorySaver` (LangGraph checkpointer for thread state)

Current model configuration lives in `chatbot_backend.py` and uses:
- model: `us.deepseek.r1-v1:0`
- AWS profile: `default`

## 1) Prerequisites

- An AWS account
- AWS CLI installed (`aws --version`)
- Bedrock model access enabled in your AWS account/region
- Python environment manager (`uv`, `pip`, or `venv`)

## 2) Create IAM user/policy for Bedrock

You can use an IAM User (local development) or IAM Role (recommended for AWS-hosted workloads).
For local `aws configure`, IAM User + access keys is the usual setup.

### Minimum policy example

Create a customer-managed IAM policy (for example: `BedrockInvokePolicy`) and attach it to your IAM user:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockInvoke",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:Converse",
        "bedrock:ConverseStream"
      ],
      "Resource": "*"
    }
  ]
}
```

> You can scope `Resource` down to specific model ARNs later. Start with `*` for initial setup/debugging.

### IAM steps (console)

1. Go to **IAM -> Users -> Create user**
2. Enable **Programmatic access** (create access key)
3. Attach the Bedrock policy above (or an equivalent least-privilege policy)
4. Save:
   - `AWS Access Key ID`
   - `AWS Secret Access Key`

## 3) Configure AWS CLI (`aws configure`)

Run:

```bash
aws configure
```

Enter:

- `AWS Access Key ID`: from IAM user
- `AWS Secret Access Key`: from IAM user
- `Default region name`: Bedrock-supported region you will use (example: `us-east-1`)
- `Default output format`: `json`

Verify:

```bash
aws sts get-caller-identity
```

If this command works, credentials are set correctly for profile `default`.

## 4) Enable Bedrock model access

In AWS Console:

1. Open **Amazon Bedrock**
2. Go to **Model access**
3. Request/enable access for the model you use (`us.deepseek.r1-v1:0` in this project)
4. Confirm your selected AWS region supports that model

## 5) Install dependencies

From this folder (`chatbotapp`):

```bash
pip install -e .
```

Alternative (if you use uv):

```bash
uv sync
```

## 6) Run the chatbot backend

```bash
uv run python chatbot_backend.py
```

Expected behavior:
- prints a startup message
- starts an input loop in terminal
- sends each user message through LangChain agent to Bedrock
- prints AI response
- type `exit` to stop

## 7) Run the Streamlit frontend (uv + streamlit)

From the `chatbotapp` directory:

```bash
uv sync
uv run streamlit run chatbot_frontend.py
```

Streamlit will print a local URL (typically `http://localhost:8501`).
Open that URL in your browser and chat in the UI.

### Optional: run on custom port

```bash
uv run streamlit run chatbot_frontend.py --server.port 8502
```

### Notes for frontend state

- `chatbot_frontend.py` stores `ChatbotBackend()` in `st.session_state` so it survives Streamlit reruns.
- Chat messages are also stored in `st.session_state.messages` and re-rendered each run.
- This allows `InMemorySaver` in the backend agent to remain effective during one browser session.

## 8) How the app is wired

- `ChatbotBackend.get_llm()` creates `ChatBedrockConverse`
- `ChatbotBackend.get_agent()` wraps that model with `create_agent(...)`
- checkpointer is `InMemorySaver()` and uses `thread_id="1"` in invoke config
- `send_message(...)` returns the final assistant text from the agent result object

## 9) Common issues

- **AccessDeniedException**
  - IAM policy missing Bedrock actions, or wrong AWS account/region

- **ValidationException / model not found**
  - Model ID incorrect for region, or model access not enabled in Bedrock

- **Credential errors**
  - Re-run `aws configure`
  - Confirm `aws sts get-caller-identity` works

- **Parameter not permitted (for example `temperature`)**
  - Not all Bedrock models accept the same inference params; remove unsupported params and retry

- **`unexpected keyword argument 'llm'` with `create_agent`**
  - Use `model=` instead of `llm=` in `create_agent(...)`

- **Response extraction errors**
  - Bedrock/LangChain response content can be string or block list; ensure your extraction logic matches runtime structure

## Project files

- `chatbot_backend.py` - interactive chatbot backend (LLM + agent + loop)
- `chatbot_frontend.py` - Streamlit chat UI
- `pyproject.toml` - project/dependency config
