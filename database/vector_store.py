
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import pandas as pd
import os

from config import settings
from core import constants


class VectorStoreManager:
    """Manages vector database operations."""
    
    def __init__(self):
        """Initialize embeddings and vector store."""
        self.embeddings = OllamaEmbeddings(model=settings.EMBEDDING_MODEL)
        self.vector_store = None
        self.retriever = None
        
    def initialize_vector_store(self):
        """Initialize or load the vector store."""
        add_documents = not os.path.exists(settings.DB_DIR)
        
        self.vector_store = Chroma(
            collection_name=settings.COLLECTION_NAME,
            persist_directory=settings.DB_DIR,
            embedding_function=self.embeddings
        )
        
        if add_documents:
            self._add_documents_to_store()
        
        self.retriever = self.vector_store.as_retriever(
            search_kwargs=settings.SEARCH_KWARGS
        )
        
        return self.retriever
    
    def _add_documents_to_store(self):
        """Add documents from CSV to vector store."""
        df = pd.read_csv(settings.CSV_FILE_PATH)
        documents = []
        ids = []
        
        for i, row in df.iterrows():
            document = Document(
                page_content=row[constants.CSV_COLUMNS["TITLE"]] + " " + 
                           row[constants.CSV_COLUMNS["REVIEW"]],
                metadata={
                    constants.CSV_COLUMNS["RATING"].lower(): 
                        row[constants.CSV_COLUMNS["RATING"]],
                    constants.CSV_COLUMNS["DATE"].lower(): 
                        row[constants.CSV_COLUMNS["DATE"]]
                },
                id=str(i)
            )
            ids.append(str(i))
            documents.append(document)
        
        self.vector_store.add_documents(documents=documents, ids=ids)


# Global retriever instance
_vector_manager = VectorStoreManager()
retriever = _vector_manager.initialize_vector_store()