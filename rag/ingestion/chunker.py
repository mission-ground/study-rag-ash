from transformers import AutoTokenizer

class Chunker:

    def __init__(
        self,
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        chunk_size=256,
        overlap=50
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text):

        tokens = self.tokenizer.encode(text)

        chunks = []

        start = 0

        while start < len(tokens):

            end = start + self.chunk_size

            chunk_tokens = tokens[start:end]

            chunk_text = self.tokenizer.decode(chunk_tokens)

            chunks.append(chunk_text)

            start += self.chunk_size - self.overlap

        return chunks