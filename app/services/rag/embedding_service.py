
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)

    def embed_documents( self, texts: list[str] ) -> list[list[float]]:

        if not texts:
            return []

        embeddings = self.model.encode( texts, normalize_embeddings=True )
        return embeddings.tolist()

    def embed_query( self, question: str ) -> list[float]:

        embedding = self.model.encode( question, normalize_embeddings=True )
        return embedding.tolist()
