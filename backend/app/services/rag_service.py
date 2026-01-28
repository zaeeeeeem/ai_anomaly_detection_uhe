from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer
from app.config import settings


class RAGService:
    def __init__(self) -> None:
        self._client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self._collection = self._client.get_or_create_collection(
            name="medical_guidelines"
        )
        self._embedder = SentenceTransformer(settings.EMBEDDING_MODEL)

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        if not documents:
            return
        texts = [doc["text"] for doc in documents]
        embeddings = self._embedder.encode(texts).tolist()
        ids = [f"{doc['doc_id']}:{doc['chunk_id']}" for doc in documents]
        metadatas = [
            {
                "doc_id": doc["doc_id"],
                "chunk_id": doc["chunk_id"],
                **(doc.get("metadata") or {}),
            }
            for doc in documents
        ]
        self._collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not query_text:
            return []
        embedding = self._embedder.encode([query_text]).tolist()
        results = self._collection.query(
            query_embeddings=embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        hits: List[Dict[str, Any]] = []
        for idx in range(len(results.get("ids", [[]])[0])):
            metadata = results["metadatas"][0][idx] or {}
            doc_id = metadata.get("doc_id")
            chunk_id = metadata.get("chunk_id")
            distance = results["distances"][0][idx]
            text = results["documents"][0][idx]
            hits.append(
                {
                    "doc_id": doc_id,
                    "chunk_id": chunk_id,
                    "score": float(1.0 - distance) if distance is not None else 0.0,
                    "text": text,
                }
            )
        return hits


rag_service = RAGService()
