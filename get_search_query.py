from call_llm import call_llm

def get_search_query(dossier, query, strategy="strict"):
    if strategy == "broaden":
        consigne = "Recherche précédente échouée. Élargis les concepts juridiques (synonymes, catégorie générale)."
    else:
        consigne = "Reformule la question pour un moteur de recherche vectoriel juridique (mots-clés précis)."
        
    prompt = f"Dossier : {dossier}\nQuestion : {query}\nInstruction : {consigne}\nRenvoie UNIQUEMENT la question reformulée."
    return call_llm(prompt, "Expert en recherche documentaire")