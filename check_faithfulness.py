from call_llm import call_llm

def check_faithfulness(context, answer):
    prompt = f"CONTEXTE:\n{context}\n\nRÉPONSE:\n{answer}\n\nLa réponse contient-elle des faits non présents dans le contexte ? Réponds OUI ou NON."
    res = call_llm(prompt, "Superviseur", max_tokens=5)
    return "NON" in res.upper()