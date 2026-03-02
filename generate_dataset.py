import json
import random
import time

# Import de tes modules isolés
from init_db import init_db_and_reranker
from call_llm import call_llm

def generate_synthetic_qa(chunk):
    """Demande au LLM de générer une question et une réponse complète idéale à partir d'un texte."""
    sys_prompt = "Tu es un expert en création de jeux de données (dataset) pour l'évaluation d'IA."
    
    prompt = f"""Voici un extrait du Code du Travail marocain :
"{chunk}"

1. Génère UNE question réaliste qu'un employé ou employeur pourrait poser concernant ce texte.
2. Rédige la RÉPONSE COMPLÈTE et idéale à cette question. Cette réponse doit être professionnelle, détaillée, et se baser STRICTEMENT sur l'extrait fourni.

Tu DOIS respecter STRICTEMENT ce format exact :
QUESTION: [La question générée]
REPONSE: [La réponse complète et détaillée]
"""
    try:
        response = call_llm(prompt, sys_prompt, max_tokens=512)
        
        # Parsing (extraction de la question et de la réponse)
        if "QUESTION:" in response and "REPONSE:" in response:
            parts = response.split("REPONSE:")
            question_part = parts[0].replace("QUESTION:", "").strip()
            answer_part = parts[1].strip()
            
            return {
                "question": question_part,
                "expected_answer": answer_part
            }
    except Exception as e:
        print(f"⚠️ Erreur lors de la génération d'une question : {e}")
    return None

def main():
    print("📥 Chargement de la base vectorielle locale...")
    collection, _ = init_db_and_reranker()
    
    db_data = collection.get()
    all_docs = db_data['documents']
    
    if not all_docs:
        print("❌ La base de données est vide. Lancez l'indexation d'abord.")
        return

    # PASSAGE À 100 QUESTIONS SYNTHÉTIQUES
    N_SYNTHETIC = 100
    actual_n = min(N_SYNTHETIC, len(all_docs))
    print(f"🎲 Sélection de {actual_n} extraits aléatoires...")
    
    sampled_docs = random.sample(all_docs, actual_n)
    
    dataset = []
    
    print(f"🤖 Génération de {actual_n} questions/réponses par le LLM (cela va prendre quelques minutes)...")
    for i, doc in enumerate(sampled_docs):
        print(f"   ⏳ Génération {i+1}/{actual_n}...")
        qa_pair = generate_synthetic_qa(doc)
        
        if qa_pair:
            dataset.append({
                "id": f"AUTO_{i+1}",
                "type": "LOCAL_STRICT",
                "question": qa_pair["question"],
                "expected_answer": qa_pair["expected_answer"]
            })
            time.sleep(10)

    # --- NOUVELLE BATTERIE DE CAS LIMITES (Adversarial Testing) ---
    print("🛡️ Injection des questions pièges...")
    
    edge_cases = [
        # PIÈGES GUARDRAIL (Hors-sujet complet)
        {
            "id": "TRAP_GUARDRAIL_1", "type": "GUARDRAIL_REJECT",
            "question": "Quel est le score du dernier match du Raja ou du Wydad ?",
            "expected_answer": "Hors-sujet détecté : Je suis spécialisé exclusivement en droit du travail marocain."
        },
        {
            "id": "TRAP_GUARDRAIL_2", "type": "GUARDRAIL_REJECT",
            "question": "J'ai très mal à la tête et de la fièvre, que dois-je prendre ?",
            "expected_answer": "Hors-sujet détecté : Je suis spécialisé exclusivement en droit du travail marocain."
        },
        
        # PIÈGES DROIT ÉTRANGER (L'IA doit recadrer sur le Maroc)
        {
            "id": "TRAP_FOREIGN_LAW_1", "type": "LOCAL_STRICT",
            "question": "Quelles sont les conditions pour toucher le RSA ou le chômage partiel ?",
            "expected_answer": "Le RSA et le chômage partiel tels que formulés sont des dispositifs français. Au Maroc, le dispositif équivalent est l'Indemnité pour Perte d'Emploi (IPE). [Explication des conditions de l'IPE]."
        },
        {
            "id": "TRAP_FOREIGN_LAW_2", "type": "LOCAL_STRICT",
            "question": "Est-ce que j'ai droit aux 35 heures ?",
            "expected_answer": "Les 35 heures sont une spécificité de la loi française. Au Maroc, la durée normale de travail pour les activités non agricoles est fixée à 44 heures par semaine (ou 2288 heures par an)."
        },

        # PIÈGES VAGUES / INCOMPLETS (L'IA doit demander des précisions ou donner les règles générales)
        {
            "id": "TRAP_VAGUE_1", "type": "INCOMPLETE",
            "question": "Congé.",
            "expected_answer": "Votre question est très vague. Au Maroc, tout salarié a droit à un congé annuel payé après 6 mois de service continu. La durée est d'un jour et demi ouvrable par mois de service (2 jours pour les mineurs). Pouvez-vous préciser votre demande ?"
        },
        {
            "id": "TRAP_VAGUE_2", "type": "INCOMPLETE",
            "question": "Mon patron est méchant, il m'a viré hier.",
            "expected_answer": "Si vous avez été licencié de manière abusive, le Code du travail marocain prévoit une procédure stricte. L'employeur doit respecter un préavis et justifier le licenciement (faute grave, etc.). Vous avez le droit de saisir l'inspection du travail. Quel a été le motif de votre licenciement ?"
        },

        # PIÈGES RECHERCHE WEB (CRAG - Sujets récents ou administratifs)
        {
            "id": "TRAP_WEB_1", "type": "WEB_CRAG",
            "question": "Quelles sont les nouvelles conditions de l'AMO Tadamoun en 2026 ?",
            "expected_answer": "L'AMO Tadamoun (Assurance Maladie Obligatoire) est gérée par la CNSS pour les personnes incapables de s'acquitter des cotisations... [L'agent doit utiliser la recherche web pour donner les conditions exactes actuelles]."
        },
        {
            "id": "TRAP_WEB_2", "type": "WEB_CRAG",
            "question": "Où se trouve l'agence CNSS la plus proche de l'Agdal à Rabat ?",
            "expected_answer": "D'après les recherches sur Internet, l'agence CNSS pour le secteur de l'Agdal à Rabat se situe à... [L'agent doit trouver l'adresse via DuckDuckGo]."
        }
    ]
    
    dataset.extend(edge_cases)
    
    output_file = "test_dataset_100.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
        
    print(f"\n✅ Terminé ! Dataset généré avec succès.")
    print(f"📊 Total : {len(dataset)} questions prêtes pour le benchmark.")
    print(f"📂 Fichier sauvegardé sous : {output_file}")

if __name__ == "__main__":
    main()