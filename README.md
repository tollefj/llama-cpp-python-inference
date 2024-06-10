# llama-cpp-python-server

a simple inference server for llama cpp python, based on prompt configurations and more. used for JSON structured output by default.

## installation

first, download a suitable torch version for your system. Any >2 version should suffice.

CPU:
`pip install torch --index-url https://download.pytorch.org/whl/cpu`

CUDA:
`pip install torch`

```bash
# downloads the necessary models/tokenizers and llm (.gguf) to the models directory
make download
# installs llama-cpp-python
make install  # /install-cuda/install-m1
# runs the server on port 8000
make
```

any issues? run the equivalent command:

```bash
python3 -m llama_cpp.server --model models/llm.gguf --n_gpu_layers=-1 --chat_format chatml
```

## usage

```python
from llm_config import prompt_configs
from llm import generate

# see `llm_config.py` for configurations
config = prompt_configs["question_and_reason"]

query = "this is a question about something related to the documents the LLM will receive"
data = [
    "doc 1: this is the first document",
    "doc 2: this is the second document",
    "doc 3: this is the third document",
    "doc 4: this is the fourth document",
]
data = "\n".join(data)

generate(
    query=query,
    text=data,
    prompt=config["prompt"],
    schema=config["schema"],
    schema_type="object",  # array/object, ...
)
```

## environment variables

any program using huggingface models (if added) should run `load_dotenv()` for the correct environment variables.
this is to support offline hosting, controlling the storage location of all models manually.

```python
from util_env import init_dotenv
init_dotenv(custom_environments=".your-env-file")
# your program
```
