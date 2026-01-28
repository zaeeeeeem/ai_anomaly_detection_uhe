from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
from uuid import uuid4

from .schemas import InteractionLog
from .storage import SQLiteStore


class LogAgent:
    def __init__(self, store: Optional[SQLiteStore] = None) -> None:
        self.store = store or SQLiteStore()

    def log_interaction(
        self,
        prompt: str,
        response: str,
        metadata: Optional[Dict[str, Any]],
        model_name: str,
        user_id: str,
        conversation_id: str,
        timestamp: Optional[str] = None,
    ) -> str:
        interaction_id = str(uuid4())
        normalized_metadata = self._normalize_metadata(metadata)
        normalized_timestamp = timestamp or self._now_iso()

        record = InteractionLog(
            id=interaction_id,
            prompt=prompt,
            response=response,
            model_name=model_name,
            timestamp=normalized_timestamp,
            user_id=user_id,
            conversation_id=conversation_id,
            metadata=normalized_metadata,
        )
        self.store.insert_interaction(record)
        return interaction_id

    def load_logs(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[InteractionLog]:
        return self.store.load_logs(filters=filters, limit=limit, offset=offset)

    def stream_logs(
        self,
        filters: Optional[Dict[str, Any]] = None,
        batch_size: int = 100,
    ) -> Iterable[InteractionLog]:
        return self.store.stream_logs(filters=filters, batch_size=batch_size)

    @staticmethod
    def _normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        metadata = dict(metadata or {})
        metadata.setdefault("source", "local_ui")
        metadata.setdefault("language", "en")
        metadata.setdefault("tags", [])
        return metadata

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()
