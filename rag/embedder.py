"""
HuggingFace Embeddings Handler
"""
import logging
from typing import List

logger = logging.getLogger(__name__)

# Lazy import to avoid PyTorch DLL issues
HuggingFaceEmbeddings = None

def _import_huggingface_embeddings():
    """Lazy import HuggingFace embeddings."""
    global HuggingFaceEmbeddings
    if HuggingFaceEmbeddings is not None:
        return HuggingFaceEmbeddings
    
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings as _Embeddings
        HuggingFaceEmbeddings = _Embeddings
        return HuggingFaceEmbeddings
    except (ImportError, OSError, RuntimeError) as e:
        logger.error(f"Failed to import HuggingFaceEmbeddings: {e}")
        raise RuntimeError("Failed to import HuggingFaceEmbeddings. Install with: pip install transformers sentence-transformers")


class Embedder:
    """Handles HuggingFace embeddings."""
    
    def __init__(self):
        """Initialize HuggingFace embeddings."""
        # Lazy import
        EmbeddingsClass = _import_huggingface_embeddings()
        
        self.embeddings = EmbeddingsClass(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        logger.info("HuggingFace embeddings initialized")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.embeddings.embed_documents(texts)
            logger.info(f"Generated embeddings for {len(texts)} documents")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query.
        
        Args:
            text: Query text
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.embeddings.embed_query(text)
            return embedding
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            raise

