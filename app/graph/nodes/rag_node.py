
import asyncio
from functools import lru_cache

from app.graph.state import AgentState
from app.prompts.rag_prompt import RAG_SYSTEM_PROMPT

from app.services.rag.embedding_service import EmbeddingService
from app.services.rag.vector_store_service import VectorStoreService
from app.services.rag.retriever_service import RetrieverService
from app.services.llm_service import llm_service

import logging
logger = logging.getLogger(__name__)

@lru_cache
def get_retriever() -> RetrieverService:

    embedding_service = EmbeddingService()
    vector_store = VectorStoreService()

    return RetrieverService(
        embedding_service=embedding_service,
        vector_store=vector_store
    )



async def rag_node(state: AgentState) -> dict:

    question = state["rewritten_question"]

    logger.info("RAG node started")

    # Get the existing RetrieverService
    retriever = await asyncio.to_thread(get_retriever)

    # Search the vector database
    documents = await asyncio.to_thread(
        retriever.retrieve,
        question,
        3
    )

    logger.info("Retrieved %d chunks", len(documents))

    # Prepare context for the LLM node
    context = "\n\n".join(
        doc.page_content for doc in documents
    )

    return {
        "context": context
    }

# RetrieverService.retrieve() is synchronous This runs the blocking retrieval operation in a worker thread instead of blocking FastAPI's event loop (asyncio.to_thread()) used