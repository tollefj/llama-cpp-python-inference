import os
import shutil
import sys
from copy import deepcopy
from pathlib import Path
from typing import List

import nltk
from huggingface_hub import snapshot_download
from huggingface_hub.file_download import repo_folder_name

from utils.util_env import init_dotenv

llm_tokenizer = os.getenv("LLM_TOKENIZER")
# this will only download config files + tokenizer for the selected models
ignore_patterns = ["*.msgpack", "*.safetensors", "*.onnx", "onnx/*", "*.h5"]

# download nltk sentence tokenizer:
nltk.download("punkt")


# modified from
# https://github.com/huggingface/huggingface_hub/issues/1240
def download_model(
    repo_id,
    save_path,
    output_dir="./models",
    ignore_patterns=ignore_patterns,
):
    print(f"Attempting to download {repo_id}")
    destination = Path(output_dir) / save_path
    if destination.exists():
        print(f"Model already exists at {destination}")
        return
    print(f"Output destination: {destination}")

    # Download and copy without symlinks
    tmp_ignore = deepcopy(ignore_patterns)
    downloaded = snapshot_download(
        repo_id,
        ignore_patterns=tmp_ignore,
        cache_dir=output_dir,
    )
    shutil.copytree(downloaded, destination)
    # Remove all downloaded files
    cache_folder = Path(output_dir) / repo_folder_name(
        repo_id=repo_id, repo_type="model"
    )
    shutil.rmtree(cache_folder)
    return destination


def install(custom_environments: List[str] = []):
    # environments are paths to .env files with custom overridden variables
    init_dotenv(custom_environments)

    for env_path in ["LLM_TOKENIZER"]:
        download_model(
            repo_id=os.getenv(env_path),
            save_path=env_path,
            ignore_patterns=ignore_patterns,
        )


if __name__ == "__main__":
    install(sys.argv[1:])  # allow user to input any number of custom environment paths
