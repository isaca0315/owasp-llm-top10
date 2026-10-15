import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

VECTOR_DIR = "vectorstores"
os.makedirs(VECTOR_DIR, exist_ok=True)

# Lazy-load embedder to improve startup time
_embedder = None
_embedder_error = None

def get_embedder():
    """Lazy-load embeddings only when needed"""
    global _embedder, _embedder_error
    if _embedder is None and _embedder_error is None:
        try:
            _embedder = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        except Exception as e:
            _embedder_error = str(e)
            print(f"Error loading embeddings: {e}")
            raise
    
    if _embedder_error:
        raise RuntimeError(f"Embedder initialization failed: {_embedder_error}")
    
    return _embedder

def build_vectorstore(text, session_id):
    try:
        # Check if text is valid
        if not text or len(text.strip()) == 0:
            print(f"Warning: Empty text for session {session_id}, skipping vectorstore")
            return
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )
        chunks = splitter.split_text(text)
        
        # Check if chunks are valid
        if not chunks or len(chunks) == 0:
            print(f"Warning: No chunks generated for session {session_id}, skipping vectorstore")
            return
        
        vs = FAISS.from_texts(chunks, get_embedder())
        vs.save_local(f"{VECTOR_DIR}/{session_id}")
        print(f"Vectorstore built successfully for session {session_id} with {len(chunks)} chunks")
    except Exception as e:
        print(f"Error building vectorstore: {e}")
        raise

def load_vectorstore(session_id):
    try:
        return FAISS.load_local(
            f"{VECTOR_DIR}/{session_id}",
            get_embedder(),
            allow_dangerous_deserialization=True
        )
    except Exception as e:
        print(f"Error loading vectorstore: {e}")
        raise
