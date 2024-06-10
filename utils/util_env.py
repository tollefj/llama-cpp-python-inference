import os
import subprocess
import sys
from typing import List

from dotenv import dotenv_values, load_dotenv


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def init_dotenv(custom_environments: List[str] = []):
    if isinstance(custom_environments, str):
        custom_environments = [custom_environments]
    load_dotenv(".env")
    for env in custom_environments:
        print(f"Overriding env with path {env}")
        load_dotenv(env, override=True)
        dotenv_keys = list(dotenv_values(dotenv_path=env).keys())
        for dk in dotenv_keys:
            print(f"Override {dk} --> {os.getenv(dk)}")
