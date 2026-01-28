from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from .schemas import ExplanationRecord
from .storage import SQLiteStore


class RAGSystem:
    def __init__(self, store: Optional[SQLiteStore] = None) -> None:
        self.store = store or SQLiteStore()

    def ingest_document(
        self,
        doc_id: str,
        text: str,
        *,
        source: Optional[str] = None,
        section: Optional[str] = None,
        risk_type: Optional[List[str]] = None,
        chunk_size: int = 700,
        overlap: int = 80,
    ) -> int:
        chunks = self._chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        payloads = []
        for chunk in chunks:
            payloads.append(
                {
                    "doc_id": doc_id,
                    "section": section,
                    "source": source,
                    "risk_type": risk_type or [],
                    "content": chunk,
                }
            )
        self.store.insert_rag_chunks(payloads)
        return len(payloads)

    def explain(self, anomaly_context: Dict[str, Any]) -> ExplanationRecord:
        risk_type = anomaly_context.get("risk_type") or self._infer_risk_type(
            anomaly_context.get("flags", {})
        )
        query = self._build_query(anomaly_context)
        matches = self._search(query, risk_type=risk_type, top_k=3)

        explanation = self._summarize(anomaly_context, matches)
        citations = [
            {
                "doc_id": match["doc_id"],
                "chunk_id": str(match["id"]),
                "score": round(match["score"], 3),
            }
            for match in matches
        ]

        return ExplanationRecord(
            interaction_id=anomaly_context.get("interaction_id", ""),
            risk_type=risk_type or "other",
            explanation=explanation,
            citations=citations,
        )

    def _search(self, query: str, risk_type: Optional[str], top_k: int) -> List[Dict[str, Any]]:
        chunks = self.store.load_rag_chunks(risk_type=risk_type)
        scored: List[Tuple[float, Dict[str, Any]]] = []
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        query_set = set(query_terms)

        for chunk in chunks:
            terms = self._tokenize(chunk["content"])
            if not terms:
                continue
            score = self._overlap_score(query_set, terms)
            if score > 0:
                chunk_copy = dict(chunk)
                chunk_copy["score"] = score
                scored.append((score, chunk_copy))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

    @staticmethod
    def _overlap_score(query_set: set, terms: List[str]) -> float:
        if not terms:
            return 0.0
        term_set = set(terms)
        overlap = len(query_set.intersection(term_set))
        return overlap / max(1, len(query_set))

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return re.findall(r"[a-z0-9]+", text.lower())

    @staticmethod
    def _chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
        words = text.split()
        if not words:
            return []
        chunks = []
        start = 0
        while start < len(words):
            end = min(len(words), start + chunk_size)
            chunk_words = words[start:end]
            chunks.append(" ".join(chunk_words))
            if end == len(words):
                break
            start = max(0, end - overlap)
        return chunks

    @staticmethod
    def _infer_risk_type(flags: Dict[str, Any]) -> str:
        if flags.get("weak_triage_for_emergency") or flags.get("emergency_case"):
            return "triage"
        if flags.get("gives_specific_dose") or flags.get("gives_medication_dosing"):
            return "dosing"
        if flags.get("missing_disclaimer"):
            return "disclaimer"
        return "other"

    @staticmethod
    def _build_query(anomaly_context: Dict[str, Any]) -> str:
        prompt = anomaly_context.get("prompt", "")
        response = anomaly_context.get("response", "")
        flags = anomaly_context.get("flags", {})
        flag_terms = " ".join([k for k, v in flags.items() if v])
        return f"{prompt} {response} {flag_terms}"

    @staticmethod
    def _summarize(anomaly_context: Dict[str, Any], matches: List[Dict[str, Any]]) -> str:
        if not matches:
            return (
                "The response triggered a safety flag, but no matching guideline text was found "
                "in the current corpus. Add guideline documents to improve explanations."
            )
        top = matches[0]
        return (
            "The response triggered a safety flag. Guidance indicates higher-risk symptoms "
            "require clear triage and cautious wording. "
            f"Relevant source: {top['doc_id']}."
        )
