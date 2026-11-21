from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

import logging
logger = logging.getLogger(__name__)

class DocumentService:

    def load_document(self, file_path:str) -> list[Document]:

        path = Path(file_path)
        if not path.is_file():
            logger.error("Document not found")
            raise FileNotFoundError("Document not found")

        text = path.read_text(encoding="utf-8") # read the content of the text file
        document = Document(
            page_content=text,    # actual text
            metadata={"source": str(path)} # Additional information, such as where the text came from
        )

        return [document]
    

    def split_document(self, documents:list[Document]) -> list[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,   # Maximum chunk length: 300 characters
            chunk_overlap=50,  # up to 50 shared characters between adjacent chunks
            length_function=len, # Measure text length using Python's character count
            add_start_index=True 
        )
        return splitter.split_documents(documents)