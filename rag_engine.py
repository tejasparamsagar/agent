"""
RAG Engine
Handles embeddings, vector store, and querying
"""
import os
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

# Try to import LangChain components
try:
    from langchain_community.vectorstores import Chroma
    from langchain.chains import RetrievalQA
    from langchain_core.prompts import PromptTemplate
    from langchain_core.documents import Document
    LANGCHAIN_AVAILABLE = True
except ImportError:
    logger.warning("LangChain not available")
    LANGCHAIN_AVAILABLE = False

# Try to import Groq
try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# Try to import HuggingFace embeddings
try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False


class RAGEngine:
    """RAG engine with configurable backends."""
    
    def __init__(self, persist_directory: str = "./chroma_db", top_k: int = 3):
        """
        Initialize RAG engine.
        
        Args:
            persist_directory: Directory for ChromaDB persistence
            top_k: Number of documents to retrieve
        """
        if not LANGCHAIN_AVAILABLE:
            raise RuntimeError("LangChain is required")
        
        self.persist_directory = Path(persist_directory)
        self.top_k = top_k
        self.vectorstore = None
        self.qa_chain = None
        self.embeddings = None
        self.llm = None
        self.initialized = False
    
    def _get_embeddings(self):
        """Initialize embeddings."""
        if HF_AVAILABLE:
            logger.info("Using HuggingFace embeddings")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            return self.embeddings
        
        raise RuntimeError("No embeddings backend available. Install HuggingFace embeddings: pip install transformers sentence-transformers")
    
    def _get_llm(self):
        """Initialize LLM."""
        groq_key = os.getenv("GROQ_API_KEY")
        
        if groq_key and GROQ_AVAILABLE:
            logger.info("Using Groq ChatGroq")
            self.llm = ChatGroq(
                model="llama-3.1-8b-instant",  # Fast and currently supported model
                groq_api_key=groq_key,
                temperature=0
            )
            return self.llm
        
        raise RuntimeError("No LLM backend available. Set GROQ_API_KEY and install langchain-groq: pip install langchain-groq")
    
    def initialize(self, documents: List[Document], force_reload: bool = False):
        """
        Initialize the RAG system.
        
        Args:
            documents: List of Document objects to index
            force_reload: Force re-indexing even if ChromaDB exists
        """
        if not documents:
            logger.warning("No documents provided")
            return False
        
        # Initialize embeddings and LLM
        self._get_embeddings()
        self._get_llm()
        
        # Check if ChromaDB exists
        if self.persist_directory.exists() and not force_reload:
            try:
                logger.info(f"Loading existing ChromaDB from {self.persist_directory}")
                self.vectorstore = Chroma(
                    persist_directory=str(self.persist_directory),
                    embedding_function=self.embeddings
                )
                logger.info("Successfully loaded existing ChromaDB")
            except Exception as e:
                logger.warning(f"Error loading ChromaDB: {e}. Re-indexing...")
                force_reload = True
        
        # Create new index if needed
        if force_reload or self.vectorstore is None:
            logger.info(f"Creating new ChromaDB index with {len(documents)} documents")
            self.persist_directory.mkdir(parents=True, exist_ok=True)
            
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=str(self.persist_directory)
            )
            logger.info(f"Successfully indexed {len(documents)} documents")
        
        # Create prompt template
        prompt_template = """Answer the question based only on the following context:

{context}

Question: {question}

Answer:"""
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": self.top_k}),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=False
        )
        
        self.initialized = True
        logger.info("RAG engine initialized successfully")
        return True
    
    def query(self, query: str) -> str:
        """
        Query the RAG system.
        
        Args:
            query: User query string
            
        Returns:
            Answer string
        """
        if not self.qa_chain:
            raise RuntimeError("RAG engine not initialized")
        
        logger.info(f"Processing query: {query}")
        result = self.qa_chain.invoke({"query": query})
        answer = result.get("result", "I don't know.")
        
        return answer
    
    def is_initialized(self) -> bool:
        """Check if RAG engine is initialized."""
        return self.initialized

