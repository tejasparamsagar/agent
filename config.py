"""
Configuration settings for the RAG API
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # Groq LLM
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Authentication
    AUTH_TOKEN = os.getenv("AUTH_TOKEN", "default-token-change-in-production")
    
    # ChromaDB
    PERSIST_DIRECTORY = os.getenv("PERSIST_DIRECTORY", "./chroma")
    
    # File upload settings
    MAX_FILE_SIZE = 15 * 1024 * 1024  # 15MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "./uploads")
    
    # Chunking settings
    CHUNK_SIZE = 700  # Characters (between 500-800)
    CHUNK_OVERLAP = 100
    
    # Retrieval settings
    TOP_K = 5  # Number of chunks to retrieve
    
    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    @staticmethod
    def validate():
        """Validate required configuration."""
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required in environment variables")
        return True

