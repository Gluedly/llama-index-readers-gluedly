"""Gluedly reader for LlamaIndex vector store ingestion."""

from __future__ import annotations

from typing import Any, List, Optional

import requests
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document

DEFAULT_BASE_URL = "https://gluedly.com/api/v1"


class GluedlyReader(BaseReader):
    """Gluedly reader for LlamaIndex vector store ingestion."""

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        session: Optional[requests.Session] = None,
        timeout: float = 30,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.session = session or requests.Session()
        self.timeout = timeout

    def load_data(
        self,
        page_id: int,
        snapshot_id: Optional[int] = None,
    ) -> List[Document]:
        target_snapshot_id = snapshot_id
        if not target_snapshot_id:
            res = self.session.get(
                f"{self.base_url}/pages/{page_id}/data",
                headers=self.headers,
                timeout=self.timeout,
            )
            res.raise_for_status()
            snapshots = res.json().get("data", [])
            if not snapshots:
                return []
            target_snapshot_id = int(snapshots[0]["id"])

        res = self.session.get(
            f"{self.base_url}/pages/{page_id}/data/{target_snapshot_id}",
            headers=self.headers,
            timeout=self.timeout,
        )
        res.raise_for_status()
        payload: dict[str, Any] = res.json()

        documents: List[Document] = []
        for idx, row in enumerate(payload.get("data", {}).get("rows", [])):
            if isinstance(row, dict):
                text = row.get("markdown") or str(row)
                source_url = row.get("url")
            else:
                text = str(row)
                source_url = None

            extra_info = {
                "page_id": page_id,
                "snapshot_id": target_snapshot_id,
                "source_url": source_url,
                "row_index": idx,
            }
            documents.append(Document(text=str(text), metadata=extra_info))

        return documents
