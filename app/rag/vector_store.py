import os
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient


class VectorStore:
    def __init__(self):
        # ✅ Initialize OpenAI embeddings (no proxies issue)
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",  # or text-embedding-3-large
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # ✅ Connect to Qdrant inside Docker
        self.client = QdrantClient(
            host="qdrant",  # service name from docker-compose.yml
            port=6333
        )

        self.collection_name = "compliance_docs"

        # ✅ Ensure collection exists
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config={"size": 1536, "distance": "Cosine"}  # matches text-embedding-3-small
        )

    def add(self, texts, metadatas):
        """Add new documents into Qdrant"""
        Qdrant.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            client=self.client,
            collection_name=self.collection_name,
        )

    def search(self, query, top_k=3):
        """Search for similar documents"""
        qdrant_store = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings,
        )
        return qdrant_store.similarity_search(query, k=top_k)
