import streamlit as st
import requests
import uuid

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="Document Chatbot",
    page_icon="📄",
    layout="wide",
)

# ──────────────────────────────
# Session State
# ──────────────────────────────

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "collection_name" not in st.session_state:
    st.session_state.collection_name = None

# ──────────────────────────────
# Sidebar: Upload Documents
# ──────────────────────────────

st.sidebar.title("📄 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF / DOCX",
    type=["pdf", "docx"],
    accept_multiple_files=True,
)

if st.sidebar.button("Ingest Documents"):
    if not uploaded_files:
        st.sidebar.warning("Upload at least one document.")
    else:
        files = [
            ("files", (file.name, file, file.type))
            for file in uploaded_files
        ]

        try:
            with st.spinner("Uploading & indexing..."):
                response = requests.post(
                    f"{API_BASE}/upload",
                    files=files,
                    timeout=60,
                )

            if response.status_code == 200:
                data = response.json()
                st.session_state.collection_name = data["collection_name"]
                st.sidebar.success(
                    f"Documents ingested into `{st.session_state.collection_name}`"
                )
            else:
                st.sidebar.error(
                    f"Upload failed ({response.status_code})."
                )

        except requests.exceptions.RequestException as e:
            st.sidebar.error(f"Backend error: {e}")

# ──────────────────────────────
# Main Chat UI
# ──────────────────────────────

st.title("📚 Document Chatbot")

if not st.session_state.collection_name:
    st.info("👈 Upload and ingest documents to start chatting.")
    st.stop()

for role, content in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(content)

user_input = st.chat_input("Ask a question about your documents...")

if user_input:
    # User message
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        try:
            with requests.post(
                f"{API_BASE}/chat",
                params={
                    "message": user_input,
                    "thread_id": st.session_state.thread_id,
                    "collection_name": st.session_state.collection_name,
                },
                stream=True,
                timeout=60,
            ) as r:
                print(r)
                if r.status_code != 200:
                    st.error(f"Chat failed ({r.status_code})")
                else:
                    for chunk in r.iter_content(chunk_size=None):
                        if not chunk:
                            continue
                        token = chunk.decode("utf-8", errors="ignore")
                        full_response += token
                        response_container.markdown(full_response + "▌")

            response_container.markdown(full_response)

        except requests.exceptions.RequestException as e:
            st.error(f"Chat backend error: {e}")
            full_response = "⚠️ Error contacting backend."

    st.session_state.chat_history.append(
        ("assistant", full_response)
    )
