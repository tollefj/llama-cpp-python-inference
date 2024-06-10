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
