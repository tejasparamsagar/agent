"""
Document Retriever and RAG Pipeline
"""
import os
import logging
from typing import List, Dict, Any
from rag.vectorstore import VectorStore
from config import Config

logger = logging.getLogger(__name__)

# Lazy imports to avoid PyTorch DLL issues
ChatGroq = None
ChatPromptTemplate = None
Document = None

def _import_langchain_components():
    """Lazy import LangChain components."""
    global ChatGroq, ChatPromptTemplate, Document
    
    if ChatGroq is not None:
        return True
    
    try:
        from langchain_groq import ChatGroq as _ChatGroq
        from langchain_core.prompts import ChatPromptTemplate as _ChatPromptTemplate
        from langchain_core.documents import Document as _Document
        
        ChatGroq = _ChatGroq
        ChatPromptTemplate = _ChatPromptTemplate
        Document = _Document
        return True
    except (ImportError, OSError, RuntimeError) as e:
        logger.error(f"Failed to import LangChain components: {e}")
        raise RuntimeError("Failed to import LangChain components. Install with: pip install langchain-groq")


class Retriever:
    """Handles document retrieval and RAG queries."""
    
    def __init__(self):
        """Initialize retriever."""
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required")
        
        # Lazy import
        _import_langchain_components()
        
        self.vectorstore = VectorStore()
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",  # Fast and currently supported model
            groq_api_key=Config.GROQ_API_KEY,
            temperature=0
        )
        logger.info("Retriever initialized with Groq LLM")
    
    def retrieve(self, dataset_name: str, query: str, k: int = None) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            dataset_name: Name of the dataset
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        k = k or Config.TOP_K
        documents = self.vectorstore.similarity_search(dataset_name, query, k=k)
        return documents
    
    def query(
        self, 
        dataset_name: str, 
        question: str,
        k: int = None
    ) -> Dict[str, Any]:
        """
        Perform RAG query: retrieve + generate answer.
        
        Args:
            dataset_name: Name of the dataset
            question: User question
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with answer and sources
        """
        # Retrieve relevant documents
        documents = self.retrieve(dataset_name, question, k)
        
        if not documents:
            return {
                "answer": "I don't have information about that.",
                "sources": []
            }
        
        # Prepare context from documents
        context = "\n\n".join([doc.page_content for doc in documents])
        
        # Ensure components are imported
        _import_langchain_components()
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant. Answer ONLY using the provided context.
If the answer is not present in the context, reply: 'I don't have information about that.'

Context: {context}"""),
            ("human", "Question: {question}\n\nAnswer:")
        ])
        
        # Generate answer
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                "context": context,
                "question": question
            })
            
            answer = response.content if hasattr(response, 'content') else str(response)
            
            # Extract sources
            sources = [
                {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in documents
            ]
            
            logger.info(f"Generated answer for question: {question[:50]}...")
            
            return {
                "answer": answer,
                "sources": sources
            }
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return {
                "answer": "I encountered an error while processing your question.",
                "sources": []
            }

