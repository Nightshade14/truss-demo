import os

import dotenv
from huggingface_hub import login
from transformers import pipeline

dotenv.load_dotenv(".env")

login(token=os.getenv("HF_ACCESS_TOKEN"))

system_prompt = {
    "role": "system",
    "content": "You are an enthusiastic and helpful assistant. You are an elite and experienced recruiter and hiring manager in tech and help candidates land better roles and evaluate their fit with the job description.",
}

reqs = [
    {
        "user_id": 1,
        "conversation_history": [
            {"role": "user", "content": "Who are you?"},
            {"role": "user", "content": "What is your name?"},
        ],
    },
    {
        "user_id": 2,
        "conversation_history": [{"role": "user", "content": "What can you do?"}],
    },
    {
        "user_id": 3,
        "conversation_history": [{"role": "user", "content": "What is 1 + 3?"}],
    },
]

input_data = [[system_prompt] + req["conversation_history"] for req in reqs]


inference_pipeline = pipeline(
    task="text-generation", model="meta-llama/Llama-3.2-1B-Instruct", batch_size=5
)

inference_pipeline.tokenizer.pad_token_id = (
    inference_pipeline.model.config.eos_token_id[0]
)
inference_pipeline.tokenizer.padding_side = "left"

res = inference_pipeline(input_data)
print(res)
