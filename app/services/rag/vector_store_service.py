
import hashlib
from pathlib import Path

import chromadb
from langchain_core.documents import Document


class VectorStoreService:

    def __init__(self):
        db_path = Path("data/chroma")
        db_path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient( path=str(db_path) )

        self.collection = self.client.get_or_create_collection(
            name="support_documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents( self, chunks: list[Document], embeddings: list[list[float]] ) -> None:

        if not chunks:
            return

        if len(chunks) != len(embeddings):
            raise ValueError( "Number of chunks and embeddings must match" )

        ids = []
        texts = []
        metadatas = []

        for chunk in chunks:
            source = chunk.metadata.get("source", "")
            start_index = chunk.metadata.get( "start_index", -1 )

            # Stable ID for the same chunk and source
            content_key = ( f"{source}:{start_index}:{chunk.page_content}" )

            chunk_id = hashlib.sha256( content_key.encode("utf-8") ).hexdigest()

            ids.append(chunk_id)
            texts.append(chunk.page_content)
            metadatas.append({ "source": str(source), "start_index": int(start_index) })

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def search( self, query_embedding: list[float], top_k: int = 3 ) -> list[Document]:

        if top_k < 1:
            raise ValueError("top_k must be at least 1")

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,    # up to three matching chunks
            include=["documents", "metadatas", "distances"]
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        retrieved_chunks = []

        for text, metadata, distance in zip( documents, metadatas, distances ):
            retrieved_chunks.append( Document( page_content=text, metadata={ **metadata, "distance": distance } ) )

        return retrieved_chunks
