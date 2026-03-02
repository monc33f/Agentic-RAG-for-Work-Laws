import os

def retrieve_and_rerank(query, collection, reranker_model, top_k=3):
    results = collection.query(query_texts=[query], n_results=10)
    
    if not results['documents'] or not results['documents'][0]: 
        return []
    
    docs, metas = results['documents'][0], results['metadatas'][0]
    pairs = [[query, doc] for doc in docs]
    scores = reranker_model.compute_score(pairs)
    ranked = sorted(zip(docs, metas, scores), key=lambda x: x[2], reverse=True)
    
    formatted_docs = []
    for d, m, s in ranked[:top_k]:
        if s > -2:
            filename = os.path.basename(m.get('source', 'Inconnu'))
            formatted_docs.append(f"[Source: {filename}, Page: {m.get('page', '?')}] {d}")
            
    return formatted_docs