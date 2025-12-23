import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ingestion.loaders import load_document
from memory.qdrant import get_vectorstore

def ingest_files(paths: list[str]) -> str:
    collection_name = f"doc_{uuid.uuid4().hex}"

    docs = []
    for p in paths:
        docs.extend(load_document(p))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_documents(docs)

    vectorstore = get_vectorstore(collection_name)
    vectorstore.add_documents(chunks)

    return collection_name
