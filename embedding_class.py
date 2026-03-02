from langchain_community.embeddings import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL_NAME

class BGEEmbeddingFunction:
    def __init__(self):
        self.model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        
    def __call__(self, input):
        if isinstance(input, str): 
            input = [input]
        return self.model.embed_documents(input)
        
    def embed_query(self, input):
        if isinstance(input, list): 
            return self.model.embed_documents(input)
        return self.model.embed_query(input)
        
    def name(self): 
        return "bge_m3_semantic"