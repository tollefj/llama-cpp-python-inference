# your local llm server

## Installation

Before anything, download a suitable torch version for your system. Any >2 version should suffice.

CPU only:
`pip install torch --index-url https://download.pytorch.org/whl/cpu`

With CUDA:
`pip install torch`

```bash
# downloads the huggingface models and llm (.gguf) to the models directory
make download  # download-nor or any other added language in the makefile with custom environments.
# installs llama-cpp-python
make install  # /install-cuda/install-m1
# runs the server on port 8000
make
```

If there are any issues running the makefile, do the equivalent python llama-cpp-python command:

```bash
python3 -m llama_cpp.server --model models/llm.gguf --n_gpu_layers=-1 --chat_format chatml
```

## Overview/architecture

There's two main components:

1. the server (model located in `models/llm.gguf`)
   - runnable with `make` or `./serve.sh`
   - uses llama-cpp python bindings
2. the client (or example notebook)
   - a rag system that talks to the server

## RAG workflow

See `rag-pipeline.ipynb`.

1. load + preprocess data (json, csv, ...)
2. initializes chromadb for local persistent storage
   - stores to the `/chroma` dir
   - the embedding model is listed in the environment file (`.env`)
3. compute embeddings for the loaded data
4. retrieve and rerank
   - separate steps:
     - retrieve:
       - `docs = collection.query(query, n_results=N)`
     - with reranking:
       - `ranked = rank_collection(collection, reranker, query=query, top_n=N)`
   - reranker defined in `.env`
5. combine it with LLMs
   1. Fetch documents with `get_ranked_and_contextualized`
      - Rank documents with `llm_rerank`
        1. rank with reranker (`rank_collection`)
        2. reason about each result, and only use the ones that are deemed _relevant_
   2. For each ID (original sentence), extract a sliding window context (e.g., -2, sent_id, +2)
6. reason about the query in the larger context (sliding window)

## Offline usage

1. `make download`
2. copy the project to the target offline computer.

## Environment variables

Any program utilizing huggingface models should use `load_dotenv()` for the correct environment variables.
See the `utils.generic` module for info, allowing overriding variables from custom env files.

```python
from utils.generic import init_dotenv
init_dotenv(custom_environments=".env-nor")
# your program
```