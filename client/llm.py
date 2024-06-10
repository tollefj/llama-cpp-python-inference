import os
import re

from llm_api import pred
from transformers import AutoTokenizer


def parse_llm_output(response: str):
    response = response.replace("false", "False")
    response = response.replace("true", "True")
    response = response.replace("null", "None")
    response = response.replace("\n", "")
    response = re.sub(r"\s+", " ", response)

    obj = eval(response)
    # unify keys in case of capitalization.
    obj = {k.lower(): v for k, v in obj.items()}

    return obj


class LLM:
    def __init__(self, root_dir="./") -> None:
        tokenizer_path = os.getenv("LLM_TOKENIZER_OUTPUT")
        tokenizer_path = os.path.join(root_dir, tokenizer_path)
        print(f"Loading tokenizer from {tokenizer_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

    def generate(
        self,
        query: str,
        text: str,
        config: dict,  # config in "llm_config"
        suffix: str = "",
        temp: float = 0.0,
        tokens: int = 150,
        schema_type: str = "object",
        verbose: bool = False,
        verbose_prompt: bool = False,
    ) -> dict:
        prompt = config["prompt"]
        schema = None
        if "schema" in config:
            schema = config["schema"]

        instruction = prompt.format(query=query, text=text, suffix=suffix).strip()
        template = self.tokenizer.apply_chat_template(
            [{"content": instruction, "role": "user"}], tokenize=False
        )
        if verbose_prompt:
            print("Prompt", template, "\n")
        output = pred(
            template,
            temp=temp,
            max_tokens=tokens,
            schema=schema,
            schema_type=schema_type,
        )
        try:
            output = parse_llm_output(output)
        except SyntaxError as e:
            print(e)
            print("SyntaxError. Returning raw output")
        if verbose:
            print("Output", output, "\n")
        return output
