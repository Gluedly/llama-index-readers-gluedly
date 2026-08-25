from __future__ import annotations

import responses

from llama_index_readers_gluedly import GluedlyReader

BASE = "https://gluedly.com/api/v1"


@responses.activate
def test_load_data_resolves_latest_snapshot() -> None:
    responses.add(
        responses.GET,
        f"{BASE}/pages/12/data",
        json={"data": [{"id": 100}]},
        status=200,
    )
    responses.add(
        responses.GET,
        f"{BASE}/pages/12/data/100",
        json={
            "id": 100,
            "page_id": 12,
            "data": {
                "ok": True,
                "rows": [
                    {
                        "url": "https://example.com/a",
                        "markdown": "# Product A",
                    },
                    {"title": "No markdown"},
                ],
                "match_counts": {},
                "warnings": [],
            },
        },
        status=200,
    )

    docs = GluedlyReader(api_key="test-key").load_data(page_id=12)

    assert len(docs) == 2
    assert docs[0].text == "# Product A"
    assert docs[0].metadata == {
        "page_id": 12,
        "snapshot_id": 100,
        "source_url": "https://example.com/a",
        "row_index": 0,
    }
    assert "No markdown" in str(docs[1].text)
    assert docs[1].metadata["row_index"] == 1


@responses.activate
def test_load_data_returns_empty_when_no_snapshots() -> None:
    responses.add(
        responses.GET,
        f"{BASE}/pages/12/data",
        json={"data": []},
        status=200,
    )

    docs = GluedlyReader(api_key="test-key").load_data(page_id=12)
    assert docs == []


@responses.activate
def test_load_data_uses_explicit_snapshot_id() -> None:
    responses.add(
        responses.GET,
        f"{BASE}/pages/12/data/55",
        json={
            "id": 55,
            "page_id": 12,
            "data": {
                "ok": True,
                "rows": [{"markdown": "# Explicit"}],
                "match_counts": {},
                "warnings": [],
            },
        },
        status=200,
    )

    docs = GluedlyReader(api_key="test-key").load_data(page_id=12, snapshot_id=55)

    assert len(docs) == 1
    assert docs[0].text == "# Explicit"
    assert docs[0].metadata["snapshot_id"] == 55
    assert len(responses.calls) == 1
