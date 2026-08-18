import os
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from groq import Groq
from prompts import prompt_builder

load_dotenv()


class RAGPipeline:
    def __init__(
        self,
        data_path: str = "data.csv",
        collection_name: str = "faqs",
        persist_path: str = "./chat_vectorDB",
        model_name: str = None,
    ):
        self.model_name = model_name or os.getenv("GROQ_MODEL")
        self.groq = Groq()
        self.client = chromadb.PersistentClient(path=persist_path)

        self.embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedder,
            metadata={"hnsw:space": "cosine"},
        )
        self._ingest_csv(data_path)

    def _ingest_csv(self, data_path: str) -> None:
        df = pd.read_csv(data_path)
        questions = df["question"].astype(str).tolist()
        answers = [{"answer": a} for a in df["answer"].astype(str).tolist()]
        ids = [f"id_{i}" for i in range(len(questions))]
        self.collection.upsert(documents=questions, metadatas=answers, ids=ids)

    @staticmethod
    def _normalize_query(q: str) -> str:
        return q.strip().rstrip(" ?!.")
    
    def _embed_one(self, text: str):
        # SentenceTransformerEmbeddingFunction is callable: returns List[List[float]]
        return self.embedder([text])[0]

    def retrieve(self, query: str, k: int = 5) -> str:
        q = self._normalize_query(query)
        # Query Embeddings
        q_emb = self._embed_one(q)
        res = self.collection.query(query_embeddings=[q_emb], n_results=k)
        #res = self.collection.query(query_texts=[q], n_results=k)
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]

        pairs = []
        for d, m in zip(docs, metas):
            a = (m.get("answer", "") if isinstance(m, dict) else "")
            if d or a:
                pairs.append(f"Q: {d}\nA: {a}")

        return "\n\n".join(pairs).strip()

    def answer(self, question: str) -> str:
        context = self.retrieve(question, k=5)
        final_prompt = prompt_builder(question, context )
        chat = self.groq.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": final_prompt}],
        )
        return chat.choices[0].message.content
