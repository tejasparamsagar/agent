"""
Document Loader for RAG System
Handles loading and chunking of documents
"""
import os
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

# Try to import LangChain components
try:
    from langchain_community.document_loaders import TextLoader, PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document
    LANGCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("LangChain not available. Install with: pip install langchain langchain-community langchain-text-splitters")
    LANGCHAIN_AVAILABLE = False
    Document = None
    RecursiveCharacterTextSplitter = None


class DocumentLoader:
    """Handles document loading and chunking."""
    
    def __init__(self, data_dir: str = "./data", chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize document loader.
        
        Args:
            data_dir: Directory containing documents
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        if not LANGCHAIN_AVAILABLE:
            raise RuntimeError("LangChain is required. Install with: pip install langchain langchain-community langchain-text-splitters")
        
        self.data_dir = Path(data_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def load_document(self, file_path: Path) -> List[Document]:
        """
        Load a single document.
        
        Args:
            file_path: Path to document file
            
        Returns:
            List of Document objects
        """
        file_ext = file_path.suffix.lower()
        
        try:
            if file_ext == '.txt':
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif file_ext == '.pdf':
                loader = PyPDFLoader(str(file_path))
            else:
                logger.warning(f"Unsupported file type: {file_ext}")
                return []
            
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} document(s) from {file_path}")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {e}")
            return []
    
    def load_all_documents(self) -> List[Document]:
        """
        Load all supported documents from data directory.
        
        Returns:
            List of all Document objects
        """
        if not self.data_dir.exists():
            logger.warning(f"Data directory {self.data_dir} does not exist")
            self.data_dir.mkdir(parents=True, exist_ok=True)
            return []
        
        all_documents = []
        supported_extensions = {'.txt', '.pdf'}
        
        # Walk through data directory
        for file_path in self.data_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                docs = self.load_document(file_path)
                all_documents.extend(docs)
        
        logger.info(f"Total documents loaded: {len(all_documents)}")
        return all_documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of chunked Document objects
        """
        if not documents:
            return []
        
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
        return chunks

