# rag_lc.py
import os
import pandas as pd
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_groq import ChatGroq

from prompts import prompt_builder

load_dotenv()


class RAGPipeline:
    def __init__(
        self,
        data_path: str = "data.csv",
        collection_name: str = "faqs",
        persist_path: str = "./chat_vectorDB",
        model_name: str | None = None,
        embed_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        # LLM
        self.model_name = model_name or os.getenv("GROQ_MODEL")
        self.llm = ChatGroq(model=self.model_name)  # needs GROQ_API_KEY in env

        # Embeddings
        self.embedder = HuggingFaceEmbeddings(model_name=embed_model)

        # Vector store (persistent Chroma)
        self.vs = Chroma(
            collection_name=collection_name,
            embedding_function=self.embedder,
            persist_directory=persist_path,
        )

        # Ingest CSV (questions as docs; answers in metadata)
        self._ingest_csv(data_path)

    # ---------- data ingest ----------
    def _ingest_csv(self, data_path: str) -> None:
        df = pd.read_csv(data_path)
        docs: list[Document] = []
        ids: list[str] = []

        for i, row in df.iterrows():
            q = str(row["question"])
            a = str(row["answer"])
            docs.append(Document(page_content=q, metadata={"answer": a}))
            ids.append(f"id_{i}")

        # add with deterministic IDs (safe to re-run; duplicates will be skipped by Chroma by id)
        # note: Chroma skips existing ids silently; if you prefer a clean reload, delete the persist dir first.
        self.vs.add_documents(docs, ids=ids)
        self.vs.persist()

    # ---------- helpers ----------
    @staticmethod
    def _normalize_query(q: str) -> str:
        return (q or "").strip().rstrip(" ?!.")

    def _embed_one(self, text: str) -> list[float]:
        # HuggingFaceEmbeddings expects a list and returns List[List[float]]
        return self.embedder.embed_documents([text])[0]

    # ---------- retrieval ----------
    def retrieve(self, query: str, k: int = 5) -> str:
        q = self._normalize_query(query)
        q_emb = self._embed_one(q)

        # Explicit vector query (parity with your current code)
        # If you prefer text-based, use: self.vs.similarity_search(q, k=k)
        hits = self.vs.similarity_search_by_vector(q_emb, k=k)

        pairs = []
        for d in hits:
            a = d.metadata.get("answer", "")
            if d.page_content or a:
                pairs.append(f"Q: {d.page_content}\nA: {a}")

        return "\n\n".join(pairs).strip()

    # ---------- generation ----------
    def answer(self, question: str, k: int = 5) -> str:
        context = self.retrieve(question, k=k)
        final_prompt = prompt_builder(question, context)
        resp = self.llm.invoke(final_prompt)
        # ChatGroq returns an AIMessage; .content has the text
        return getattr(resp, "content", str(resp))