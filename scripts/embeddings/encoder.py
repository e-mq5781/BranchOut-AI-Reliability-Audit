import numpy as np
import numpy.typing as npt
import sentence_transformers

class TextEncoder:
    def __init__(self):
        self.transformer = sentence_transformers.SentenceTransformer(
                "BAAI/bge-large-en-v1.5",
                device="cuda"
        )

    def encode(self, text: str):
        return self.transformer.encode(text)

    def encode_all(self, texts: list[str]):
        return [ self.encode(text) for text in texts ]
