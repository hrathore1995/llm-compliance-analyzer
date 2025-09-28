from langchain_openai import OpenAIEmbeddings
import os


class EmbeddingsClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment")

        #  Do not pass unsupported params like `proxies`
        self.client = OpenAIEmbeddings(
            model="text-embedding-3-small",  # lightweight & cheap
            openai_api_key=api_key
        )

    def embed(self, texts):
        """Generate embeddings for list of texts"""
        return self.client.embed_documents(texts)

    def embed_query(self, query: str):
        """Generate embedding for a single query"""
        return self.client.embed_query(query)
