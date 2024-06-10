import json
import re

import requests
from transformers import PreTrainedTokenizer

url = "http://localhost:8000/v1/chat/completions"
headers = {"accept": "application/json", "Content-Type": "application/json"}

system_prompts = {
    "default": "You are a helpful assistant, fluent in any language. You give answers in English. You will output structured JSON objects when asked.",
}

prompt_configs = {
    "question_and_reason": {
        "prompt": "From the following documents:\n{text}\nBased the content, generate three relevant questions rooted in the query: '{query}'. For each question, create a JSON object that contains: 1. the question, 2. the answer: detailed answer with key takeaways (including important citations and your reasoning), 3. score: relevance of this answer in context of the asked query (from 1 to 100). Finally, list relevant entities for the entire document (formatted as objects with entity_type and value). {suffix}",
        "schema": {
            "query": {"type": "string"},
            "questions": {
                "type": "array",
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                    "score": {"type": "number"},
                },
            },
            "entities": {"type": "array"},
        },
    }
    # ADD MORE HERE :-)
    # ALWAYS use the "prompt" and "schema" keys,
    # along with "text" and "query" in the prompt string,
    # that will be filled in later.
}


def api(
    instruction,
    sys=None,
    max_tokens=300,
    temp=0.0,  # temperature. 0: deterministic, 1+: random
    # min_p=0.1,  # minimum probability
    # max_p=0.9,  # maximum probability
    # top_p=0.9,  # nucleus sampling
    # top_k=40,  # consider top k tokens at each generation step
    suffix=None,
    seed=None,
    autostop="###",  # enforce gen.stop. should be modified based on the model
    schema: dict = {},
    schema_type: str = "object",
):
    if len(instruction) == 0:
        raise ValueError("Instruction cannot be empty")
    if not sys:
        sys = system_prompts["default"]

    response_format = {"type": "json_object"}
    if schema != {} and len(schema_type) > 0:
        response_format["schema"] = {
            "type": schema_type,  # e.g. "object" or "array"
            "properties": schema,
        }
        response_format["required"] = list(schema.keys())

    data = {
        "messages": [
            {"role": "system", "content": sys},
            {"role": "user", "content": instruction},
        ],
        "response_format": response_format,
        "max_tokens": max_tokens,
        "temperature": temp,
        # "min_p": min_p,
        # "max_p": max_p,
        # "top_p": top_p,
        # "top_k": top_k,
        "stop": [autostop],
        "echo": True,
        "stream": False,
        "suffix": suffix,
        "seed": seed,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()
    if "choices" not in response:
        print(f"Error: {response}")
        return "Error: Invalid response format."
    try:
        response = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        print(e)
        print(f"Invalid response format: {response}")
        print("Returning raw response.")
    return response


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
    def __init__(self, tokenizer: PreTrainedTokenizer) -> None:
        self.tokenizer = tokenizer

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
        output = api(
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
