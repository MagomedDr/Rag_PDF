import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from langchain.schema import HumanMessage, AIMessage
from .settings import settings
from .ingest import ingest_file
from .chat import build_chain, format_sources
from .models import UploadResponse, ChatRequest, ChatResponse
from .vectorstore import get_vectorstore

app = FastAPI(
    title="RAG PDF",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "collection": settings.CHROMA_COLLECTION,
        "embedding_model": settings.EMBEDDING_MODEL,
        "llm_model": settings.LLM_MODEL,
    }

@app.post("/api/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    data = await file.read()
    os.makedirs("./uploads", exist_ok=True)
    path = os.path.join("./uploads", file.filename)
    with open(path, "wb") as f:
        f.write(data)

    try:
        chunks = ingest_file(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return UploadResponse(file_name=file.filename, chunks_indexed=chunks)

@app.post('/api/chat', response_model=ChatResponse)
async def chat(req: ChatRequest):
    message_history = []
    for user, bot in req.history:
        message_history.append(HumanMessage(content=user))
        message_history.append(AIMessage(content=bot))

    print(req.history)
    print(message_history)

    chain = build_chain(k=req.top_k)
    result = chain.invoke({'question': req.question,
                           "chat_history": message_history})
    answer = result.get('answer') or result.get("result") or ""
    docs = result.get("source_documents", [])

    return ChatResponse(answer=answer, sources=format_sources(docs, best_chunk=True))


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")