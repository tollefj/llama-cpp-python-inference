import nltk


def get_sentences(raw_text: str, min_tokens: int = 3, separator: str = "\n") -> str:
    sentences = nltk.sent_tokenize(raw_text)
    sentences = [
        sentence for sentence in sentences if len(sentence.split()) >= min_tokens
    ]
    sentences = f"{separator}".join(sentences)
    return sentences
