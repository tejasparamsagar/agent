"""
Flask RAG API - Production Ready
Document ingestion and query API with authentication
"""
import os
import logging
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

# Lazy imports to avoid PyTorch DLL issues on Windows
# These will be imported when needed, not at module level
TextLoader = None
PyPDFLoader = None
Document = None
RecursiveCharacterTextSplitter = None

def _import_document_loaders():
    """Lazy import of document loaders."""
    global TextLoader, PyPDFLoader, Document, RecursiveCharacterTextSplitter
    
    if TextLoader is not None:
        return True
    
    # Get logger here since it's defined later
    _logger = logging.getLogger(__name__)
    
    try:
        from langchain_community.document_loaders import TextLoader as _TextLoader, PyPDFLoader as _PyPDFLoader
        from langchain_core.documents import Document as _Document
        from langchain_text_splitters import RecursiveCharacterTextSplitter as _Splitter
        
        TextLoader = _TextLoader
        PyPDFLoader = _PyPDFLoader
        Document = _Document
        RecursiveCharacterTextSplitter = _Splitter
        return True
    except (ImportError, OSError, RuntimeError) as e:
        _logger.error(f"Failed to import document loaders: {e}")
        # Try fallback
        try:
            from langchain.document_loaders import TextLoader as _TextLoader, PyPDFLoader as _PyPDFLoader
            from langchain.schema import Document as _Document
            from langchain.text_splitter import RecursiveCharacterTextSplitter as _Splitter
            
            TextLoader = _TextLoader
            PyPDFLoader = _PyPDFLoader
            Document = _Document
            RecursiveCharacterTextSplitter = _Splitter
            return True
        except Exception as fallback_error:
            _logger.error(f"Fallback import also failed: {fallback_error}")
            raise RuntimeError("Failed to import document loaders. Check PyTorch installation.")

# Local imports
from config import Config
from rag.vectorstore import VectorStore
from rag.retriever import Retriever

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_FILE_SIZE

# Enable CORS - Allow Laravel site
ALLOWED_ORIGINS = [
    "https://learning.heuristictechpark.com",
    "https://www.learning.heuristictechpark.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*"  # Allow all for now, restrict in production
]
CORS(app, origins=ALLOWED_ORIGINS, supports_credentials=True)

# Initialize components
try:
    Config.validate()
    vectorstore = VectorStore()
    retriever = Retriever()
    logger.info("RAG system initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG system: {e}")
    vectorstore = None
    retriever = None

# Ensure upload directory exists
upload_dir = Path(Config.UPLOAD_FOLDER)
upload_dir.mkdir(parents=True, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def authenticate_request():
    """
    Authenticate API request.
    
    Returns:
        Tuple of (is_authenticated, error_response)
    """
    api_key = request.headers.get('X-API-Key') or request.form.get('api_key') or \
              (request.get_json() or {}).get('api_key')
    
    if not api_key:
        return False, {"error": "Missing API key"}, 401
    
    if api_key != Config.AUTH_TOKEN:
        return False, {"error": "Invalid API key"}, 401
    
    return True, None, None


def load_document(file_path: Path):
    """
    Load document based on file type.
    
    Args:
        file_path: Path to document file
        
    Returns:
        List of Document objects
    """
    # Lazy import document loaders
    if not _import_document_loaders():
        raise RuntimeError("Document loaders not available")
    
    file_ext = file_path.suffix.lower()
    
    try:
        if file_ext == '.txt':
            loader = TextLoader(str(file_path), encoding='utf-8')
        elif file_ext == '.pdf':
            loader = PyPDFLoader(str(file_path))
        elif file_ext == '.docx':
            # Use python-docx for .docx files
            from docx import Document as DocxDocument
            doc = DocxDocument(str(file_path))
            text_content = []
            for paragraph in doc.paragraphs:
                text_content.append(paragraph.text)
            text = '\n'.join(text_content)
            return [Document(page_content=text, metadata={"source": str(file_path.name)})]
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        documents = loader.load()
        return documents
        
    except Exception as e:
        logger.error(f"Error loading document {file_path}: {e}")
        raise


def chunk_documents(documents):
    """
    Split documents into chunks.
    
    Args:
        documents: List of Document objects
        
    Returns:
        List of chunked Document objects
    """
    # Lazy import text splitter
    if not _import_document_loaders():
        raise RuntimeError("Document loaders not available")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    """Handle file size limit error."""
    return jsonify({
        "error": f"File too large. Maximum size is {Config.MAX_FILE_SIZE / (1024*1024)}MB"
    }), 413


@app.errorhandler(Exception)
def handle_exception(e):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    import traceback
    error_trace = traceback.format_exc()
    logger.error(f"Full traceback: {error_trace}")
    
    # Return more detailed error in debug mode
    if Config.DEBUG:
        return jsonify({
            "error": "Internal server error",
            "message": str(e),
            "type": type(e).__name__
        }), 500
    else:
        return jsonify({
            "error": "Internal server error",
            "message": "An error occurred. Check server logs for details."
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    rag_initialized = vectorstore is not None and retriever is not None
    
    response = {
        "status": "running",
        "rag_initialized": rag_initialized
    }
    
    if not rag_initialized:
        response["error"] = "RAG system failed to initialize. Check logs for errors or ensure GROQ_API_KEY is set correctly."
    
    return jsonify(response), 200


@app.route('/ingest', methods=['POST'])
def ingest():
    """
    Document ingestion endpoint.
    
    Accepts:
    - file(s): PDF, TXT, or DOCX files
    - dataset_name: Name of the dataset
    - api_key: Authentication token
    """
    # Authenticate
    auth, error, status = authenticate_request()
    if not auth:
        return jsonify(error), status
    
    # Validate dataset name
    dataset_name = request.form.get('dataset_name')
    if not dataset_name:
        return jsonify({"error": "Missing 'dataset_name' parameter"}), 400
    
    # Check for files
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        all_chunks = []
        
        # Process each file
        for file in files:
            if not file or not allowed_file(file.filename):
                continue
            
            # Save file temporarily
            filename = secure_filename(file.filename)
            file_path = upload_dir / filename
            file.save(str(file_path))
            
            try:
                # Load document
                documents = load_document(file_path)
                
                # Add source metadata
                for doc in documents:
                    doc.metadata['source'] = filename
                    doc.metadata['dataset'] = dataset_name
                
                # Chunk documents
                chunks = chunk_documents(documents)
                all_chunks.extend(chunks)
                
            finally:
                # Clean up uploaded file
                if file_path.exists():
                    file_path.unlink()
        
        if not all_chunks:
            return jsonify({"error": "No valid documents processed"}), 400
        
        # Add to vector store
        chunks_added = vectorstore.add_documents(dataset_name, all_chunks)
        
        logger.info(f"Ingested {chunks_added} chunks into dataset: {dataset_name}")
        
        return jsonify({
            "status": "success",
            "chunks_added": chunks_added,
            "dataset": dataset_name
        }), 200
        
    except Exception as e:
        logger.error(f"Error in ingestion: {e}", exc_info=True)
        # Always show error details for debugging
        error_details = str(e)
        logger.error(f"Full error: {error_details}")
        return jsonify({
            "error": "Failed to process documents",
            "message": error_details,  # Show actual error for debugging
            "type": type(e).__name__
        }), 500


@app.route('/query', methods=['POST'])
def query():
    """
    Query endpoint for RAG.
    
    Body:
    {
        "question": "...",
        "dataset_name": "...",
        "api_key": "..."
    }
    """
    # Authenticate
    auth, error, status = authenticate_request()
    if not auth:
        return jsonify(error), status
    
    # Get request data
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    question = data.get('question', '').strip()
    dataset_name = data.get('dataset_name', '')
    
    if not question:
        return jsonify({"error": "Missing 'question' field"}), 400
    
    if not dataset_name:
        return jsonify({"error": "Missing 'dataset_name' field"}), 400
    
    try:
        # Perform RAG query
        result = retriever.query(dataset_name, question)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in query: {e}", exc_info=True)
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Full traceback: {error_trace}")
        return jsonify({
            "error": "Failed to process query",
            "message": str(e) if Config.DEBUG else "Query processing error",
            "type": type(e).__name__ if Config.DEBUG else None
        }), 500


@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def api_chat():
    """
    Chat endpoint compatible with Laravel chat widget.
    
    Body:
    {
        "query": "..."
    }
    
    Returns:
    {
        "answer": "..."
    }
    """
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    # Get request data
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({"error": "Missing 'query' field"}), 400
    
    # Use default dataset name or get from env
    dataset_name = data.get('dataset_name', os.getenv('DEFAULT_DATASET_NAME', 'htcodehub'))
    
    try:
        # Check if RAG is initialized
        if not retriever or not vectorstore:
            logger.warning("RAG system not initialized when /api/chat called")
            return jsonify({
                "answer": "I'm currently initializing. Please try again in a moment."
            }), 200  # Return 200 so Laravel doesn't show error
        
        # Perform RAG query (no auth required for public chat endpoint)
        result = retriever.query(dataset_name, query)
        
        # Extract answer from result
        answer = result.get('answer', 'I am not sure. Please check our website.')
        
        # If answer indicates no data, provide helpful message
        if 'don\'t have information' in answer.lower() or 'not sure' in answer.lower():
            answer = "I don't have specific information about that in my knowledge base. Please contact us at info@heuristictechpark.com or +91 9309079965 for more details."
        
        return jsonify({
            "answer": answer
        }), 200
        
    except Exception as e:
        logger.error(f"Error in chat query: {e}", exc_info=True)
        # Log full traceback for debugging
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        # Return helpful error message instead of technical error
        return jsonify({
            "answer": "I'm sorry, I encountered an error processing your question. Please try again later or contact us directly at info@heuristictechpark.com or +91 9309079965."
        }), 200  # Return 200 so Laravel doesn't show error to user


@app.route('/', methods=['GET'])
def index():
    """API information endpoint."""
    return jsonify({
        "name": "Learning RAG API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "ingest": "POST /ingest",
            "query": "POST /query"
        },
        "status": "running"
    }), 200


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
