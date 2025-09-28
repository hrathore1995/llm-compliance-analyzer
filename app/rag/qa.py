# app/rag/qa.py
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.chains import RetrievalQA

class ComplianceQA:
    def __init__(self):
        # ✅ New API usage, no proxies
        self.embeddings = OpenAIEmbeddings()
        self.client = QdrantClient(url="http://qdrant:6333")
        self.collection_name = "compliance_docs"

        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def ask(self, query: str, top_k: int = 5):
        vs = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings,
        )

        retriever = vs.as_retriever(search_kwargs={"k": top_k})

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever,
            chain_type="stuff",
        )

        result = qa_chain.run(query)
        return result
