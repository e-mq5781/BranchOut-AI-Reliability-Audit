from sentence_transformers import SentenceTransformer
import numpy as np
import torch

MODEL = "BAAI/bge-large-en-v1.5"

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer(
                MODEL,
                device="cuda" if torch.cuda.is_available() else "cpu"
                )

    def encode(self, texts): # encode a list
        return self.model.encode(
                texts,
                batch_size=32,
                normalize_embeddings=True,
                show_progress_bar=True
                )

def generate_prompt_embeddings(prompts):
    texts = [p.prompt_text for p in prompts] # get text of prompt
    
    embeddings = Embedder().encode(texts) # encode prompts
    np.save("embeddings/prompts.npy", embeddings) # save to embeddings directory

def generate_response_embeddings(prompts):
    texts = [
            f"""
            Prompt: 
            {p.prompt_text}
            
            Response:
            {p.raw_output}
            """
            for p in prompts
            ] # get text of prompt and response out of prompts (i'm sure that having multi-line strings will have no impact whatsoever

    embeddings = Embedder().encode(texts) # encode responses

    np.save("embeddings/responses.npy", embeddings)

if __name__ == "__main__":
    from database import get_prompts

    prompts = get_prompts()

    generate_prompt_embeddings(prompts)
    generate_response_embeddings(prompts)
