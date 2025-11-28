import os

import dotenv
from baseten_performance_client import PerformanceClient

dotenv.load_dotenv(".env")

baseten_api_key = os.getenv("BASETEN_API_KEY")

async_model_api_endpoint = os.getenv("ASYNC_MODEL_API_ENDPOINT")
model_api_endpoint = os.getenv("MODEL_API_ENDPOINT")

async_client = PerformanceClient(
    base_url=async_model_api_endpoint, api_key=baseten_api_key
)
client = PerformanceClient(base_url=model_api_endpoint, api_key=baseten_api_key)


async def make_async_api_call(async_client, payload_batch):
    response_obj = await async_client.async_batch_post(
        payloads=payload_batch, max_concurrent_requests=4, timeout_s=360
    )
    print(f"Async total time for batch POST: {response_obj.total_time:.4f}s")
    for i, (resp_data, headers, time_taken) in enumerate(
        zip(
            response_obj.data,
            response_obj.response_headers,
            response_obj.individual_request_times,
        )
    ):
        print(f"Async Response {i + 1}:")
        print(f"  Data: {resp_data}")
        print(f"  Headers: {headers}")
        print(f"  Time taken: {time_taken:.4f}s")


def make_api_call(client, payload_batch):
    response_obj = client.batch_post(
        url_path="", payloads=payload_batch, max_concurrent_requests=4, timeout_s=360
    )
    print(f"Total time for batch POST: {response_obj.total_time:.4f}s")
    for i, (resp_data, headers, time_taken) in enumerate(
        zip(
            response_obj.data,
            response_obj.response_headers,
            response_obj.individual_request_times,
        )
    ):
        print(f"  Response {i + 1}:")
        print(f"  Data: {resp_data}")
        print(f"  Headers: {headers}")
        print(f"  Time taken: {time_taken:.4f}s")

        print(f"  Headers: {headers}")
        print(f"  Time taken: {time_taken:.4f}s")


messages = [
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

# payload = {"data": messages}


res = make_api_call(client, messages)
print(res)
