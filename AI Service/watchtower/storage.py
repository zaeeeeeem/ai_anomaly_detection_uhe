from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .config import DEFAULT_DB_PATH, DEFAULT_JSONL_DIR
from .schemas import (
    AnalysisRecord,
    ExplanationRecord,
    FeedbackRecord,
    InteractionLog,
    ScoringRecord,
)


class SQLiteStore:
    def __init__(
        self,
        db_path: Path | str = DEFAULT_DB_PATH,
        jsonl_dir: Optional[Path | str] = DEFAULT_JSONL_DIR,
    ) -> None:
        self.db_path = Path(db_path)
        self.jsonl_dir = Path(jsonl_dir) if jsonl_dir is not None else None

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if self.jsonl_dir is not None:
            self.jsonl_dir.mkdir(parents=True, exist_ok=True)

        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._init_db()

    def close(self) -> None:
        self._conn.close()

    def _init_db(self) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS interaction_logs (
                id TEXT PRIMARY KEY,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                model_name TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                user_id TEXT NOT NULL,
                conversation_id TEXT NOT NULL,
                metadata TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_records (
                interaction_id TEXT PRIMARY KEY,
                topics TEXT NOT NULL,
                risk_context_flags TEXT NOT NULL,
                hallucination_hints TEXT NOT NULL,
                FOREIGN KEY(interaction_id) REFERENCES interaction_logs(id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scoring_records (
                interaction_id TEXT PRIMARY KEY,
                scores TEXT NOT NULL,
                flags TEXT NOT NULL,
                FOREIGN KEY(interaction_id) REFERENCES interaction_logs(id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS explanations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interaction_id TEXT NOT NULL,
                risk_type TEXT NOT NULL,
                explanation TEXT NOT NULL,
                citations TEXT NOT NULL,
                FOREIGN KEY(interaction_id) REFERENCES interaction_logs(id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                interaction_id TEXT PRIMARY KEY,
                human_label TEXT NOT NULL,
                corrected_response TEXT,
                comments TEXT,
                timestamp TEXT,
                reviewer_id TEXT,
                FOREIGN KEY(interaction_id) REFERENCES interaction_logs(id)
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rag_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id TEXT NOT NULL,
                section TEXT,
                source TEXT,
                risk_type TEXT,
                content TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def insert_interaction(self, record: InteractionLog) -> None:
        payload = asdict(record)
        self._conn.execute(
            """
            INSERT INTO interaction_logs
            (id, prompt, response, model_name, timestamp, user_id, conversation_id, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["id"],
                payload["prompt"],
                payload["response"],
                payload["model_name"],
                payload["timestamp"],
                payload["user_id"],
                payload["conversation_id"],
                json.dumps(payload.get("metadata", {}), ensure_ascii=True),
            ),
        )
        self._conn.commit()
        self._append_jsonl("logs", payload, payload["timestamp"])

    def insert_analysis(self, record: AnalysisRecord, timestamp: Optional[str] = None) -> None:
        payload = asdict(record)
        self._conn.execute(
            """
            INSERT OR REPLACE INTO analysis_records
            (interaction_id, topics, risk_context_flags, hallucination_hints)
            VALUES (?, ?, ?, ?)
            """,
            (
                payload["interaction_id"],
                json.dumps(payload.get("topics", []), ensure_ascii=True),
                json.dumps(payload.get("risk_context_flags", {}), ensure_ascii=True),
                json.dumps(payload.get("hallucination_hints", {}), ensure_ascii=True),
            ),
        )
        self._conn.commit()
        self._append_jsonl("analysis", payload, timestamp)

    def insert_scoring(self, record: ScoringRecord, timestamp: Optional[str] = None) -> None:
        payload = asdict(record)
        self._conn.execute(
            """
            INSERT OR REPLACE INTO scoring_records
            (interaction_id, scores, flags)
            VALUES (?, ?, ?)
            """,
            (
                payload["interaction_id"],
                json.dumps(payload.get("scores", {}), ensure_ascii=True),
                json.dumps(payload.get("flags", {}), ensure_ascii=True),
            ),
        )
        self._conn.commit()
        self._append_jsonl("scoring", payload, timestamp)

    def insert_explanation(self, record: ExplanationRecord, timestamp: Optional[str] = None) -> None:
        payload = asdict(record)
        self._conn.execute(
            """
            INSERT INTO explanations
            (interaction_id, risk_type, explanation, citations)
            VALUES (?, ?, ?, ?)
            """,
            (
                payload["interaction_id"],
                payload["risk_type"],
                payload["explanation"],
                json.dumps(payload.get("citations", []), ensure_ascii=True),
            ),
        )
        self._conn.commit()
        self._append_jsonl("explanations", payload, timestamp)

    def insert_feedback(self, record: FeedbackRecord, timestamp: Optional[str] = None) -> None:
        payload = asdict(record)
        self._conn.execute(
            """
            INSERT OR REPLACE INTO feedback
            (interaction_id, human_label, corrected_response, comments, timestamp, reviewer_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                payload["interaction_id"],
                payload["human_label"],
                payload.get("corrected_response"),
                payload.get("comments"),
                payload.get("timestamp"),
                payload.get("reviewer_id"),
            ),
        )
        self._conn.commit()
        self._append_jsonl("feedback", payload, timestamp or payload.get("timestamp"))

    def get_interaction(self, interaction_id: str) -> Optional[InteractionLog]:
        cursor = self._conn.execute(
            """
            SELECT id, prompt, response, model_name, timestamp, user_id, conversation_id, metadata
            FROM interaction_logs
            WHERE id = ?
            """,
            (interaction_id,),
        )
        row = cursor.fetchone()
        return self._row_to_interaction(row) if row else None

    def get_analysis_record(self, interaction_id: str) -> Optional[AnalysisRecord]:
        cursor = self._conn.execute(
            """
            SELECT interaction_id, topics, risk_context_flags, hallucination_hints
            FROM analysis_records
            WHERE interaction_id = ?
            """,
            (interaction_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return AnalysisRecord(
            interaction_id=row["interaction_id"],
            topics=json.loads(row["topics"] or "[]"),
            risk_context_flags=json.loads(row["risk_context_flags"] or "{}"),
            hallucination_hints=json.loads(row["hallucination_hints"] or "{}"),
        )

    def get_scoring_record(self, interaction_id: str) -> Optional[ScoringRecord]:
        cursor = self._conn.execute(
            """
            SELECT interaction_id, scores, flags
            FROM scoring_records
            WHERE interaction_id = ?
            """,
            (interaction_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return ScoringRecord(
            interaction_id=row["interaction_id"],
            scores=json.loads(row["scores"] or "{}"),
            flags=json.loads(row["flags"] or "{}"),
        )

    def list_scoring_records(self) -> List[ScoringRecord]:
        cursor = self._conn.execute(
            """
            SELECT interaction_id, scores, flags
            FROM scoring_records
            """
        )
        rows = cursor.fetchall()
        records = []
        for row in rows:
            records.append(
                ScoringRecord(
                    interaction_id=row["interaction_id"],
                    scores=json.loads(row["scores"] or "{}"),
                    flags=json.loads(row["flags"] or "{}"),
                )
            )
        return records

    def list_explanations(self, interaction_id: str) -> List[ExplanationRecord]:
        cursor = self._conn.execute(
            """
            SELECT interaction_id, risk_type, explanation, citations
            FROM explanations
            WHERE interaction_id = ?
            """,
            (interaction_id,),
        )
        rows = cursor.fetchall()
        records = []
        for row in rows:
            records.append(
                ExplanationRecord(
                    interaction_id=row["interaction_id"],
                    risk_type=row["risk_type"],
                    explanation=row["explanation"],
                    citations=json.loads(row["citations"] or "[]"),
                )
            )
        return records

    def insert_rag_chunks(self, chunks: List[Dict[str, Any]]) -> None:
        if not chunks:
            return
        rows = [
            (
                chunk["doc_id"],
                chunk.get("section"),
                chunk.get("source"),
                json.dumps(chunk.get("risk_type", []), ensure_ascii=True),
                chunk["content"],
            )
            for chunk in chunks
        ]
        self._conn.executemany(
            """
            INSERT INTO rag_chunks
            (doc_id, section, source, risk_type, content)
            VALUES (?, ?, ?, ?, ?)
            """,
            rows,
        )
        self._conn.commit()

    def load_rag_chunks(self, risk_type: Optional[str] = None) -> List[Dict[str, Any]]:
        if risk_type:
            cursor = self._conn.execute(
                """
                SELECT id, doc_id, section, source, risk_type, content
                FROM rag_chunks
                WHERE risk_type LIKE ?
                """,
                (f"%{risk_type}%",),
            )
        else:
            cursor = self._conn.execute(
                """
                SELECT id, doc_id, section, source, risk_type, content
                FROM rag_chunks
                """
            )
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append(
                {
                    "id": row["id"],
                    "doc_id": row["doc_id"],
                    "section": row["section"],
                    "source": row["source"],
                    "risk_type": json.loads(row["risk_type"] or "[]"),
                    "content": row["content"],
                }
            )
        return results

    def load_logs(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[InteractionLog]:
        query, params = self._build_log_query(filters, limit, offset)
        cursor = self._conn.execute(query, params)
        rows = cursor.fetchall()
        return [self._row_to_interaction(row) for row in rows]

    def stream_logs(
        self,
        filters: Optional[Dict[str, Any]] = None,
        batch_size: int = 100,
    ) -> Iterable[InteractionLog]:
        offset = 0
        while True:
            batch = self.load_logs(filters=filters, limit=batch_size, offset=offset)
            if not batch:
                break
            for record in batch:
                yield record
            offset += batch_size

    def _row_to_interaction(self, row: sqlite3.Row) -> InteractionLog:
        return InteractionLog(
            id=row["id"],
            prompt=row["prompt"],
            response=row["response"],
            model_name=row["model_name"],
            timestamp=row["timestamp"],
            user_id=row["user_id"],
            conversation_id=row["conversation_id"],
            metadata=json.loads(row["metadata"] or "{}"),
        )

    def _build_log_query(
        self,
        filters: Optional[Dict[str, Any]],
        limit: int,
        offset: int,
    ) -> Tuple[str, List[Any]]:
        filters = filters or {}
        clauses: List[str] = []
        params: List[Any] = []

        for key, value in filters.items():
            if key == "timestamp_from":
                clauses.append("timestamp >= ?")
                params.append(value)
                continue
            if key == "timestamp_to":
                clauses.append("timestamp <= ?")
                params.append(value)
                continue
            if key in {"id", "user_id", "conversation_id", "model_name"}:
                clauses.append(f"{key} = ?")
                params.append(value)
                continue

        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        query = (
            "SELECT id, prompt, response, model_name, timestamp, user_id, conversation_id, metadata "
            f"FROM interaction_logs {where} "
            "ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        )
        params.extend([limit, offset])
        return query, params

    def _append_jsonl(self, prefix: str, payload: Dict[str, Any], timestamp: Optional[str]) -> None:
        if self.jsonl_dir is None:
            return
        record_time = self._parse_timestamp(timestamp)
        filename = f"{prefix}_{record_time.strftime('%Y_%m')}.jsonl"
        path = self.jsonl_dir / filename
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=True) + "\n")

    @staticmethod
    def _parse_timestamp(timestamp: Optional[str]) -> datetime:
        if not timestamp:
            return datetime.utcnow()
        try:
            return datetime.fromisoformat(timestamp)
        except ValueError:
            return datetime.utcnow()
