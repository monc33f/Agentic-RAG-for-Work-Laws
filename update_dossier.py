from call_llm import call_llm

def update_dossier(current_dossier, new_user_msg):
    sys_prompt = "Tu es un assistant juridique chargé de tenir à jour la fiche de renseignements d'un client."
    prompt = f"Dossier actuel :\n{current_dossier}\n\nNouvelle info/question :\n{new_user_msg}\n\nMets à jour le dossier client sous forme de liste à puces."
    return call_llm(prompt, sys_prompt)