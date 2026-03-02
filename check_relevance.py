from call_llm import call_llm

def check_relevance(query, answer):
    prompt = f"QUESTION: '{query}'\n\nRÉPONSE: '{answer}'\n\nHors-sujet ? Réponds OUI ou NON."
    res = call_llm(prompt, "Superviseur", max_tokens=5)
    return "OUI" in res.upper()