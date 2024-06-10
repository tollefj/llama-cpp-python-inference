import json

import requests

from llm_config import system_prompts

url = "http://localhost:8000/v1/chat/completions"
headers = {"accept": "application/json", "Content-Type": "application/json"}


def pred(
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
