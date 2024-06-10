# llama-cpp-python-server

a simple inference server for llama cpp python, based on prompt configurations and more. used for JSON structured output by default.

## installation

```bash
# install llama-cpp-python
# CUDA?
CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip install 'llama-cpp-python[server]'
# Apple M?
CMAKE_ARGS="-DLLAMA_METAL=on" pip install -U "llama-cpp-python[server]" --no-cache-dir

# regular dependencies
# + downloads the necessary models/tokenizers and llm (.gguf) to the models directory
make install 
make download

# runs the server on port 8000
make
```

to use any LLM of your choice, download the model and place it as `llm.gguf` in the `/models` directory.

- make sure to place the huggingface model id as the `LLM_TOKENIZER` environment variable in the `.env` file.

any issues? run the equivalent command:

```bash
python3 -m llama_cpp.server --model models/llm.gguf --n_gpu_layers=-1 --chat_format chatml
```

## usage

after running the server (see above), you can use the api from `llm.py`.

everything is contained in this file, so this can easily be copied and modified to your other projects.

```python
from llm import LLM
from transformers import AutoTokenizer
import os

tokenizer = AutoTokenizer.from_pretrained(os.getenv("LLM_TOKENIZER_OUTPUT"))

llm = LLM(tokenizer)

# text = ...  # e.g., wikipedia on CNNs
query = "how are CNNs used for BCIs?"
# do not use f-strings. config is formatted pre-instruction
config = {
    "prompt": "You are given a document:\n{text}\nBased on its content, create three questions related to the following query: '{query}'. Answer in JSON according to the schema, where each question should receive a concise answer",
    "schema": {
        "questions": {
            "type": "array",
            "properties": {
                "question": {"type": "string"},
                "answer": {"type": "string"},
            },
        },
    }
}

NEW_TOKENS = 1000
res = llm.generate(
    query=query,
    text=text,
    temp=0.3,
    tokens=NEW_TOKENS,
    config=config,
    schema_type="object",  # array/object/number etc
)
res["questions"]
```

Output:

```json
[{'question': 'What is the role of convolutional neural networks (CNNs) in brain-computer interfaces (BCIs)?',
  'answer': 'CNNs are used for feature extraction and pattern recognition in BCIs, allowing them to detect and classify various brain signals and improve the accuracy of signal processing.'},
 {'question': 'How do CNNs help prevent overfitting in BCIs?',
  'answer': 'CNNs use regularization techniques such as weight decay and trimmed connectivity (e.g., dropout) to prevent overfitting in BCIs, ensuring that the network learns generalized principles rather than dataset-specific biases.'},
 {'question': 'What are some advantages of using CNNs for BCIs compared to traditional algorithms?',
  'answer': 'CNNs offer independence from prior knowledge and human intervention in feature extraction, as well as reduced pre-processing requirements, making them a more efficient and effective approach for BCIs.'}]
```

## environment variables

any program using huggingface models (if added) should run `load_dotenv()` for the correct environment variables.
this is to support offline hosting, controlling the storage location of all models manually.

```python
from util_env import init_dotenv
init_dotenv(custom_environments=".your-env-file")
# your program
```

## nifty things

numerical to human-readable:

```python
from num2words import num2words
num_words = num2words(2384)
suffix = f"Attempt to generate less than {num_words} words" 
```
