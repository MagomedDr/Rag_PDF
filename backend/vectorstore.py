import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from .settings import settings

_client = None
_vs = None
_embeddings = None

def get_client() -> chromadb.HttpClient:
    global _client
    if _client is None:
        _client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT
        )
    return _client

def get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"}, # cuda
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings

def get_vectorstore() -> Chroma:
    global _vs
    if _vs is None:
        _vs = Chroma(
            client=get_client(),
            collection_name=settings.CHROMA_COLLECTION,
            embedding_function=get_embeddings()
        )
    return _vs