import os
import chromadb
from FlagEmbedding import FlagReranker
from config import DB_PATH, RERANKER_MODEL_NAME
from embedding_class import BGEEmbeddingFunction

def init_db_and_reranker():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Base introuvable dans {DB_PATH}.")
        
    chroma_client = chromadb.PersistentClient(path=DB_PATH)
    collection = chroma_client.get_or_create_collection(
        name="labor_code_semantic",
        embedding_function=BGEEmbeddingFunction()
    )
    
    try:
        reranker = FlagReranker('models/reranker', use_fp16=True)
    except:
        reranker = FlagReranker(RERANKER_MODEL_NAME, use_fp16=True)
        
    return collection, reranker