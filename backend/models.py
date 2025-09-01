from pydantic import BaseModel
from typing import List, Dict


class UploadResponse(BaseModel):
    file_name: str
    chunks_indexed: int

class ChatRequest(BaseModel):
    question: str
    top_k: int = 5
    history: List[List[str]] = []

class ChatResponse(BaseModel):
    answer: str
    sources: List[Dict]