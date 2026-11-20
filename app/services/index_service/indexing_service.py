
from app.services.index_service.document_service import DocumentService
from app.services.index_service.embedding_service import EmbeddingService
from app.services.index_service.vector_store_service import VectorStoreService


class IndexingService:

    def __init__( self, document_service: DocumentService, embedding_service: EmbeddingService, vector_store: VectorStoreService ):
        self.document_service = document_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def index_document(self, file_path: str) -> int:

        # Step 1: Load document
        documents = self.document_service.load_document( file_path )

        # Step 2: Split documents into chunks
        chunks = self.document_service.split_document( documents )

        if not chunks:
            return 0

        # Step 3: Extract text from chunks
        texts = [ chunk.page_content for chunk in chunks ]

        # Step 4: Generate document embeddings
        embeddings = self.embedding_service.embed_documents( texts )

        # Step 5: Store chunks and embeddings
        self.vector_store.add_documents( chunks=chunks, embeddings=embeddings )

        return len(chunks)
