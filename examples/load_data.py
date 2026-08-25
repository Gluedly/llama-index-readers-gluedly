"""Example: load Gluedly snapshot rows into LlamaIndex Documents."""

from __future__ import annotations

import os

from llama_index_readers_gluedly import GluedlyReader


def main() -> None:
    api_key = os.environ["GLUEDLY_API_KEY"]
    page_id = int(os.environ.get("GLUEDLY_PAGE_ID", "12"))
    base_url = os.environ.get("GLUEDLY_BASE_URL", "https://gluedly.com/api/v1")

    reader = GluedlyReader(api_key=api_key, base_url=base_url)
    documents = reader.load_data(page_id=page_id)

    print(f"Loaded {len(documents)} documents from page {page_id}")
    for doc in documents[:3]:
        print("---")
        print(doc.metadata)
        print(str(doc.text)[:400])


if __name__ == "__main__":
    main()
