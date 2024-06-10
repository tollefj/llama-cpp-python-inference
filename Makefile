run:
	chmod +x serve.sh
	./serve.sh

install-cuda:
    CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip install 'llama-cpp-python[server]'

install-m1:
	CMAKE_ARGS="-DLLAMA_METAL=on" pip install -U "llama-cpp-python[server]" --no-cache-dir

install:
	pip install -r requirements.txt

download:
	python3 install_local_models.py
	wget -nc -O models/llm.gguf https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF/resolve/main/Hermes-2-Pro-Llama-3-8B-Q6_K.gguf?download=true