import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from markdown_it import MarkdownIt
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .vectorstore import get_vectorstore
from .settings import settings

def _split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        add_start_index=True,
    )
    return splitter.split_documents(docs)

def ingest_file(path: str) -> int:
    """
    Поддержка: .pdf, .txt, .docx, .md
    """
    lower = path.lower()
    if lower.endswith(".pdf"):
        loader = PyPDFLoader(path)
        docs = loader.load()
        print(len(docs))
        for d in docs:
            d.metadata['source'] = os.path.basename(path)
            d.metadata['file_path'] = path
    elif lower.endswith(".txt"):
        loader = TextLoader(path, encoding="utf-8")
        docs = loader.load()
        for d in docs:
            d.metadata['source'] = os.path.basename(path)
            d.metadata['file_path'] = path
    elif lower.endswith(".docx"):
        loader = Docx2txtLoader(path)
        docs = loader.load()
        for d in docs:
            d.metadata["source"] = os.path.basename(path)
            d.metadata["file_path"] = path
    elif lower.endswith(".md"):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            md_text = f.read()
        
        docs = [Document(page_content=md_text,
                        metadata={
                            "source": os.path.basename(path),
                            "file_path": path
                                    }
                         )]
    else:
        raise ValueError("Unsupported file type")

    splits = _split_docs(docs)
    vs = get_vectorstore()
    vs.add_documents(splits)
    return len(splits)