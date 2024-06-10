run:
	chmod +x serve.sh
	./serve.sh

install:
	pip install -r requirements.txt
	python3 install_local_models.py
	wget -nc -O models/llm.gguf https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF/resolve/main/Hermes-2-Pro-Llama-3-8B-Q6_K.gguf?download=true