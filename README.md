# Llama-3.2-1B Deployment on Baseten with Truss
This project implements a scalable inference pipeline for the Llama-3.2-1B-Instruct model using Truss on Baseten Cloud. It leverages a T4 GPU instance for cost-effective inference and utilizes the high-performance, Rust-based baseten-performance-client for querying the endpoint.

Project management and dependency resolution are handled via uv.

## 📂 Project Structure
- `model.py`: The interface between the Hugging Face model and the Truss server. Handles model loading (cold start) and inference logic (system prompts + conversation history).

- `config.yaml`: Defines the hardware (T4 GPU, 4 vCPUs) and software environment (Python 3.12, Torch, Transformers).

- `client.py`: A high-concurrency client script using baseten-performance-client (Python bindings for Rust) to benchmark and query the deployed endpoint.

- `exp.py`: A local development script using native Hugging Face pipelines to verify model logic and tokenization before deployment.

## 🚀 Prerequisites
- **Python 3.12+**

- **uv** (Fast Python package installer and resolver)

- **Baseten API Key**

- **Hugging Face Access** Token (Must have access to gated `meta-llama/Llama-3.2-1B-Instruct`).

## 🛠️ Setup & Installation
1. **Initialize Environment** Using `uv` for lightning-fast environment setup:

```bash
# Create virtual environment
uv venv

# Activate environment
source .venv/bin/activate
```

2. Install Dependencies Install the required packages for deployment, local testing, and the performance client:

```bash
uv pip install truss baseten-performance-client transformers torch python-dotenv huggingface_hub
```

3. Environment Variables Create a .env file in the root directory. Do not commit this file.
```bash
# .env
BASETEN_API_KEY=your_baseten_api_key
HF_ACCESS_TOKEN=your_hf_access_token

# Endpoints (Populate these after deployment)
MODEL_API_ENDPOINT=https://model-xxxx.api.baseten.co/production/predict
ASYNC_MODEL_API_ENDPOINT=https://model-xxxx.api.baseten.co/production/async_predict
```

## 🧪 Local Development (exp.py)
Before deploying to the cloud, verify that the model loads and tokenizes correctly on your local machine.

```bash
uv run exp.py
```

- What this does: It bypasses Truss and Baseten, directly loading the model via transformers.pipeline to ensure your system prompt and conversation history logic are valid.

## ☁️ Deployment
This project uses Truss to package and push the model to Baseten.

1. **Configure Secrets** Ensure your `config.yaml` allows for secrets (specifically the HF token for the gated model).

2. **Push to Baseten** Run the following command from the project root:

```Bash
truss push
```

3. **Set Remote Secrets** Once the model is created on Baseten, you must set the `hf_access_token` in the Baseten Console settings for this model, or the deployment will fail during the `load()` stage.

## ⚡ Inference & Benchmarking (`client.py`)
Once deployed, retrieve the Model Id or Endpoint URL from Baseten and update your .env file.

Run the high-performance client:

```Bash
uv run client.py
```

### About the Client
The `client.py` uses `baseten-performance-client`. This library relies on Rust bindings to handle high-concurrency asynchronous requests more efficiently than standard Python `requests` or `openai`.

- **Batching**: The client sends batched requests (`conversation_history`).

- **Metrics**: It outputs total time, individual request latency, and headers.

## ⚙️ Configuration Details (`config.yaml`)
The deployment is configured for cost-efficiency on standard tiers:

- Instance: Nvidia T4 GPU
- Resources: 4 vCPU, 16Gi RAM
- Runtime: Python 3.12
- Batch Size: Configured to `3` in `model.py` (adjustable based on latency requirements).
