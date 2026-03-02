from call_llm import call_llm

def check_domain_relevance(query):
    mots_cles_absolus = [
        # --- Institutions & Concepts de base ---
        "damancom", "cnss", "cnops", "amo", "smig", "smag", "dahir",
        "code du travail", "article", "entreprise", "emploi",
        
        # --- Les acteurs de l'entreprise (Mis à jour) ---
        "salarié", "employeur", "employé", "travailleur", "ouvrier", 
        "stagiaire", "apprenti", "mineur", "drh", "rh", "ressources humaines",
        "syndicat", "délégué", "inspection", "inspecteur",
        
        # --- La vie du contrat ---
        "licenciement", "congé", "démission", "contrat", "cdd", "cdi", "chantier",
        
        # --- Justice, Santé & Réparation ---
        "cid", "peine", "amende", "sanction", "indemnité",
        "rente", "orphelin", "accident", "maladie professionnelle", "ayant droit", "pension",
        "retraite", "retraité", "étranger", "main-d'œuvre", "expatrié", "anapec",
        "taxe", "judiciaire", "tribunal", "juge", "justice", "litige", "prud'hommes", "assistance",
        "appel", "jugement", "recours", "délai", "décision", "dahir"
    ]

    query_lower = query.lower()
    
    # On vérifie si un mot-clé est présent dans la question
    for mot in mots_cles_absolus:
        if mot in query_lower:
            # Succès immédiat : on bypass le LLM
            return True 

   
    
    sys_prompt = "Tu es un routeur de requêtes intelligent et expert en classification. Tu réponds STRICTEMENT par OUI ou NON."
    
    prompt = f"""Le système est un expert du Droit du Travail Marocain.

            RÈGLES D'ACCEPTATION (Répondre OUI si la question concerne ou mentionne) :
            - Les relations employeurs/salariés/stagiaires au Maroc.
            - Le Code du Travail, la CNSS, l'AMO, Damancom.
            - Les salaires, congés, licenciements, contrats, indemnités.
            - La médecine du travail, les prestataires de soins dans le cadre professionnel, les accidents de travail.
            - Les procédures pénales, peines, sanctions, amendes ou litiges liés au travail ou au code du travail.
            - Les élections professionnelles, syndicats, et délégués du personnel (même si cela utilise le mot "élection").
            - Des questions sur la lecture du document juridique lui-même (erreurs de formatage, symboles étranges comme cid, pages, numéros d'articles).
            - Toute question contenant les mots "Code du travail", "salarié", "employeur" ou "article" (même si la question est très courte).
            - Le patrimoine, les finances, ou les biens immobiliers appartenant aux syndicats, à la CNSS ou aux entités du travail.
            - Les formalités administratives de l'employeur (déclaration d'ouverture d'entreprise ou de chantier, inspection du travail, registres).
            - Les accidents du travail, les maladies professionnelles, et les rentes/pensions versées aux familles et ayants droit (veuves, orphelins).
            - Les litiges devant les tribunaux, l'assistance judiciaire, les taxes judiciaires, et les procédures de recours entre un salarié et un employeur.
            - Le travail des mineurs, des apprentis, et l'implication de la puissance paternelle ou des tuteurs légaux dans le cadre professionnel.

            RÈGLES DE REJET (Répondre NON si la question concerne EXCLUSIVEMENT) :
            - La politique nationale ou internationale, le sport, la cuisine, le tourisme.
            - Le droit pénal général (vols, meurtres hors contexte professionnel).
            - La programmation informatique générale (Python, C++, etc.) ou des tâches hors-sujet.

            EXEMPLES :
            Question : "Quelle est la peine pour non-respect du code ?" -> OUI
            Question : "Comment se passe la procédure électorale Section III ?" -> OUI
            Question : "C'est quoi ces caractères étranges (cid:9) dans le texte ?" -> OUI
            Question : "Comment s'inscrire sur Damancom ?" -> OUI
            Question : "Quel est le score du match du Raja ?" -> NON
            Question : "Écris une fonction Python pour trier une liste." -> NON

            La question suivante appartient-elle au domaine d'expertise autorisé ou est-elle juridiquement pertinente ?
            Question : "{query}"

            Réponds STRICTEMENT par 'OUI' ou 'NON'."""

    try:
        # On demande un max_tokens bas car on veut juste OUI ou NON
        res = call_llm(prompt, sys_prompt, max_tokens=10).upper()
        # Si la réponse contient "OUI", on laisse passer la requête
        return "OUI" in res
    except Exception as e:
        print(f"⚠️ Erreur du Guardrail : {e}")
        # Sécurité MLOps : en cas de plantage de l'API, on laisse passer la question par défaut 
        # pour que l'utilisateur puisse au moins tenter d'avoir une réponse.
        return True