from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, SparseVectorParams
from langchain_qdrant import QdrantVectorStore, RetrievalMode

from core.embeddings import dense_embeddings, sparse_embeddings
from core.config import QDRANT_DIR

DENSE_VECTOR_SIZE = dense_embeddings._client.get_sentence_embedding_dimension()

client = QdrantClient(path=str(QDRANT_DIR))


def ensure_collection_exists(collection_name: str):
    collections = client.get_collections().collections
    if any(c.name == collection_name for c in collections):
        return

    client.create_collection(
        collection_name=collection_name,
        vectors_config={
            "dense": VectorParams(
                size=DENSE_VECTOR_SIZE,
                distance=Distance.COSINE,
            )
        },
        sparse_vectors_config={
            "sparse": SparseVectorParams(
                index=models.SparseIndexParams(on_disk=False)
            )
        },
    )


def get_vectorstore(collection_name: str) -> QdrantVectorStore:
    ensure_collection_exists(collection_name)

    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=dense_embeddings,
        sparse_embedding=sparse_embeddings,
        retrieval_mode=RetrievalMode.HYBRID,
        vector_name="dense",
        sparse_vector_name="sparse",
    )


def get_retriever(collection_name: str):
    return get_vectorstore(collection_name).as_retriever(
        search_kwargs={
            "k": 5
        }
    )
