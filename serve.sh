#!/bin/bash
source .env
echo "$LLM_TOKENIZER"
python3 -m llama_cpp.server --model "$LLM_PATH" --n_gpu_layers=-1 --chat_format chatml --n_ctx=4096
