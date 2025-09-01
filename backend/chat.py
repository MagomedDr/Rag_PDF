from typing import List, Dict, Any
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate
from .llm_client import get_llm
from .vectorstore import get_vectorstore


SYSTEM = (
    "Ты — ассистент по документации. Отвечай строго на основе контекста (извлечённых фрагментов). "
    "Если информации недостаточно — так и скажи. "
)

def build_chain(k: int = 5) -> ConversationalRetrievalChain:
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": k})
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM),
            (
                "human",
                "Контекст:\n{context}\n\nВопрос: {question}\nОтвет на русском:",
            )
        ]
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        condense_question_llm=llm,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt},
    )
    return chain

def format_sources(docs: List[Any], best_chunk=False) -> List[dict]:
    out = []

    for i, d in enumerate(docs, start=1):
        out.append(
            {
                "tag": f"{d.metadata['source']} chunk{i}",
                "text": d.page_content,
                "meatdata": d.metadata
            }
        )
        if best_chunk:
            break
        
    return out