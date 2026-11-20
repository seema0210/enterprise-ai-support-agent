
from langchain_core.documents import Document

from app.services.index_service.embedding_service import EmbeddingService
from app.services.index_service.vector_store_service import VectorStoreService


class RetrieverService:

    def __init__( self, embedding_service: EmbeddingService, vector_store: VectorStoreService ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve( self, question: str, top_k: int = 3 ) -> list[Document]:

        if not question.strip():
            raise ValueError("Question cannot be empty")

        if top_k < 1:
            raise ValueError("top_k must be at least 1")

        # Step 1: Convert the question into an embedding
        query_embedding = self.embedding_service.embed_query( question )

        # Step 2: Search the vector database
        documents = self.vector_store.search( query_embedding=query_embedding, top_k=top_k )

        # Step 3: Return relevant document chunks
        return documents
