# Assignment App

Lightweight local embeddings + Qdrant demo app with simple API endpoints for uploading documents and chatting.

## Quick Start

1. Create and activate a virtual environment (Windows):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Provide environment variables in `creds.env` (already present in repo). Ensure any required API keys or DB settings are set.

3. Run the app (development):

   ```powershell
   uvicorn main:app --reload
   ```

## Usage

- POST files to `/upload` to add documents.
- POST chat queries to `/chat` to query the vector DB and generate responses.

See `api/upload.py` and `api/chat.py` for endpoint details.

## Ingestion

To ingest documents into the vector store (Qdrant), run the ingestion script:

```powershell
python ingestion/ingest.py
```

## Embedding Model

This project includes a local embedding model snapshot under `embedding_model/models--sentence-transformers--all-mpnet-base-v2/`. The code loads embeddings from `core/embeddings.py` — adjust paths if you move the model files.

## Persistence / Vector DB

Local Qdrant collections are stored under `qdrant_db/collection/` and metadata in `qdrant_db/meta.json`. The integration code is in `memory/qdrant.py`.

## Project Structure (high level)

- `main.py` — application entrypoint
- `api/` — FastAPI route handlers (`chat.py`, `upload.py`)
- `core/` — config and embedding helpers
- `ingestion/` — document loaders and ingestion scripts
- `graph/` — graph-related utilities
- `memory/` — Qdrant integration
- `embedding_model/` — local model snapshots
- `qdrant_db/` — persisted collection files

## Notes

- This README is a concise overview. Inspect the individual modules for implementation details and configuration options.
- Ask me to expand any section (detailed API examples, env vars list, or deployment steps).
