from langchain_qdrant  import FastEmbedSparse 
from langchain_huggingface import HuggingFaceEmbeddings
 

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
cache_folder = "embedding_model"
dense_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    cache_folder=cache_folder
)

# Sparse embeddings (unchanged)
sparse_embeddings = FastEmbedSparse (
    model_name="Qdrant/bm25"
)
