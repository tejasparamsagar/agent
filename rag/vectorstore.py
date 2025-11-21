"""
ChromaDB Vector Store Handler
"""
import os
import logging
from pathlib import Path
from typing import List, Dict, Any
from rag.embedder import Embedder
from config import Config

logger = logging.getLogger(__name__)

# Lazy imports to avoid PyTorch DLL issues
Chroma = None
Document = None

def _import_chroma():
    """Lazy import ChromaDB components."""
    global Chroma, Document
    
    if Chroma is not None:
        return True
    
    try:
        from langchain_community.vectorstores import Chroma as _Chroma
        from langchain_core.documents import Document as _Document
        
        Chroma = _Chroma
        Document = _Document
        return True
    except (ImportError, OSError, RuntimeError) as e:
        logger.error(f"Failed to import ChromaDB components: {e}")
        raise RuntimeError("Failed to import ChromaDB components. Check PyTorch installation.")


class VectorStore:
    """Manages ChromaDB vector store operations."""
    
    def __init__(self):
        """Initialize vector store."""
        self.embedder = Embedder()
        self.persist_directory = Path(Config.PERSIST_DIRECTORY)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Vector store initialized with persist directory: {self.persist_directory}")
    
    def create_collection(self, dataset_name: str):
        """
        Create or get a ChromaDB collection for a dataset.
        
        Args:
            dataset_name: Name of the dataset
            
        Returns:
            Chroma vector store instance
        """
        # Lazy import
        _import_chroma()
        
        collection_path = self.persist_directory / dataset_name
        collection_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # Try to load existing collection
            vectorstore = Chroma(
                persist_directory=str(collection_path),
                embedding_function=self.embedder.embeddings
            )
            logger.info(f"Loaded existing collection: {dataset_name}")
        except Exception:
            # Create new collection
            vectorstore = Chroma(
                persist_directory=str(collection_path),
                embedding_function=self.embedder.embeddings
            )
            logger.info(f"Created new collection: {dataset_name}")
        
        return vectorstore
    
    def add_documents(
        self, 
        dataset_name: str, 
        documents,
        metadatas: List[Dict[str, Any]] = None
    ) -> int:
        """
        Add documents to the vector store.
        
        Args:
            dataset_name: Name of the dataset
            documents: List of Document objects
            metadatas: Optional list of metadata dictionaries
            
        Returns:
            Number of documents added
        """
        if not documents:
            return 0
        
        vectorstore = self.create_collection(dataset_name)
        
        # Add documents with metadata
        if metadatas:
            for doc, meta in zip(documents, metadatas):
                doc.metadata.update(meta)
        
        # Add to ChromaDB
        try:
            vectorstore.add_documents(documents)
            # ChromaDB persists automatically, but try persist() if available
            if hasattr(vectorstore, 'persist'):
                vectorstore.persist()
            logger.info(f"Added {len(documents)} documents to dataset: {dataset_name}")
            return len(documents)
        except Exception as e:
            logger.error(f"Error adding documents to vectorstore: {e}", exc_info=True)
            raise
    
    def similarity_search(
        self, 
        dataset_name: str, 
        query: str, 
        k: int = None
    ):
        """
        Search for similar documents.
        
        Args:
            dataset_name: Name of the dataset
            query: Search query
            k: Number of results to return
            
        Returns:
            List of similar documents
        """
        k = k or Config.TOP_K
        
        try:
            vectorstore = self.create_collection(dataset_name)
            results = vectorstore.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents for query")
            return results
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            raise
    
    def get_collection_info(self, dataset_name: str) -> Dict[str, Any]:
        """
        Get information about a collection.
        
        Args:
            dataset_name: Name of the dataset
            
        Returns:
            Dictionary with collection information
        """
        try:
            vectorstore = self.create_collection(dataset_name)
            collection = vectorstore._collection
            
            return {
                "dataset": dataset_name,
                "count": collection.count(),
                "exists": True
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {
                "dataset": dataset_name,
                "count": 0,
                "exists": False
            }

