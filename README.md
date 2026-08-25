# llama-index-readers-gluedly

LlamaIndex `BaseReader` that loads Gluedly scrape snapshots as `Document` objects.

## Install

```bash
pip install llama-index-readers-gluedly
```

## Usage

```python
from llama_index_readers_gluedly import GluedlyReader

reader = GluedlyReader(api_key="YOUR_GLUEDLY_API_KEY")
documents = reader.load_data(page_id=12)
# documents = reader.load_data(page_id=12, snapshot_id=100)
```

Each row becomes one document. Text prefers `markdown`, otherwise `str(row)`. Metadata includes `page_id`, `snapshot_id`, `source_url`, and `row_index`.

## Example

```bash
export GLUEDLY_API_KEY=…
export GLUEDLY_PAGE_ID=12
python examples/load_data.py
```

## Development

Install with test dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```
