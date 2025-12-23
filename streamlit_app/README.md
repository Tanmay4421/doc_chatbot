# Document Chatbot (Streamlit)

A simple Streamlit front-end for a document-question-answering chatbot. Upload PDF/DOCX files, ingest them to a backend indexer, and ask questions about the uploaded documents.

**Files**
- See [app.py](app.py) for the Streamlit app.
- See [requirements.txt](requirements.txt) for Python dependencies.

**Requirements**
- Python 3.8+
- The backend API must be running and reachable (default: `http://localhost:8000`).

**Setup (Windows)**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

**Run**
```powershell
.\.venv\Scripts\activate
streamlit run app.py
```

**Usage**
- Open the Streamlit app in your browser (Streamlit opens automatically).
- In the sidebar, upload one or more PDF/DOCX files.
- Click **Ingest Documents** to upload and index files (this calls the backend `/upload` endpoint).
- Once ingestion succeeds, ask questions in the chat input — the app sends queries to the backend `/chat` endpoint.

**Configuration**
- The app uses `API_BASE = "http://localhost:8000"` in `app.py`. Change this value if your backend runs at a different host or port.

**Troubleshooting**
- If uploads or chat fail, ensure the backend is running and accessible at the configured `API_BASE` URL.
- Increase the `timeout` values in `app.py` if large files or long backend processing cause timeouts.

**Notes**
- This frontend does not perform document parsing or indexing itself — those functions are provided by the backend API.

