import os
import re

from transformers import AutoTokenizer

from llm_api import pred

tokenizer_path = os.getenv("LLM_TOKENIZER_OUTPUT")
print(f"Loading tokenizer from {tokenizer_path}")
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)


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


def chat_template(instruction, warm_start_assistant=None):
    chat = [{"content": instruction, "role": "user"}]
    template = tokenizer.apply_chat_template(chat, tokenize=False)
    if warm_start_assistant:
        template += (
            f"<|start_header_id|>assistant<|end_header_id|>{warm_start_assistant}"
        )
    return template


def generate(
    query: str,
    text: str,
    prompt: dict,  # prompt in "llm_config"
    temp: float = 0.0,
    tokens: int = 150,
    schema: dict = {},
    schema_type: str = "object",
    verbose: bool = False,
    verbose_prompt: bool = False,
) -> dict:
    instruction = prompt.format(query=query, text=text)
    template = tokenizer.apply_chat_template(
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
