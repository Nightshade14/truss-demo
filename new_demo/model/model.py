"""
The `Model` class is an interface between the ML model that you're packaging and the model
server that you're running it on.

The main methods to implement here are:
* `load`: runs exactly once when the model server is spun up or patched and loads the
   model onto the model server. Include any logic for initializing your model, such
   as downloading model weights and loading the model into memory.
* `predict`: runs every time the model server is called. Include any logic for model
  inference and return the model output.

See https://truss.baseten.co/quickstart for more.
"""

from huggingface_hub import login
from transformers import pipeline

class Model:
    def __init__(self, **kwargs):
        # Uncomment the following to get access
        # to various parts of the Truss config.

        # self._data_dir = kwargs["data_dir"]
        # self._config = kwargs["config"]
        self._secrets = kwargs["secrets"]
        login(token=self._secrets["hf_access_token"])
        self.system_prompt = {
                "role": "system",
                "content": "You are an enthusiastic and helpful assistant. You are an elite and experienced recruiter and hiring manager in tech and help candidates land better roles and evaluate their fit with the job description.",
            }
        self._model = None

    def load(self):
        # Load model here and assign to self._model.
        self._model = pipeline(
            "text-generation",
            model="meta-llama/Llama-3.2-1B-Instruct",
            batch_size = 3
        )
        self._model.tokenizer.pad_token_id = self._model.model.config.eos_token_id[0]

    def predict(self, requests):
        # Run model inference here
        # for request in requests:
        #     self._messages.append(request)
        x = [[self.system_prompt] + [req] for req in requests]
        return self._model(x)
