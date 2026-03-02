import json
import random
import time
import numpy as np
from sklearn.cluster import KMeans

# Tes modules isolés
from init_db import init_db_and_reranker
from call_llm import call_llm

# --- DÉFINITION DES VARIABLES DE DIVERSITÉ ---
TAXONOMIES = [
    "Factuel (Question directe sur une loi précise, courte)",
    "Synthèse (Demande de comparer deux concepts ou de résumer une règle générale)",
    "Cas Pratique (Mise en situation réelle avec un problème spécifique vécu par un employé)",
    "Procédural (Demande des étapes à suivre pour une démarche légale)"
]

PERSONAS = [
    "Employé inquiet, langage courant, peut faire des fautes de frappe ou utiliser des abréviations",
    "Directeur des Ressources Humaines (DRH), langage très formel et managérial",
    "Juriste pointilleux, langage très technique et précis",
    "Stagiaire qui découvre le monde du travail, pose des questions naïves"
]

def generate_robust_qa(chunk, taxonomy, persona):
    """Génère une Q/A en forçant un style et un type précis pour éviter le biais."""
    sys_prompt = "Tu es un ingénieur MLOps spécialisé dans la création de datasets d'évaluation robustes."
    
    prompt = f"""Voici un extrait du Code du Travail marocain :
"{chunk}"

Ta mission est de générer une paire Question/Réponse basée STRICTEMENT sur ce texte, en respectant ces deux contraintes majeures :
1. TYPE DE QUESTION : {taxonomy}
2. PERSONA (Style de l'utilisateur posant la question) : {persona}

Rédige la question en adoptant parfaitement le style du persona. 
Rédige ensuite la réponse complète, idéale et professionnelle qu'un système RAG devrait fournir.

Tu DOIS respecter STRICTEMENT ce format exact :
QUESTION: [La question générée selon le persona]
REPONSE: [La réponse complète et détaillée]
"""
    try:
        response = call_llm(prompt, sys_prompt, max_tokens=350)
        
        if "QUESTION:" in response and "REPONSE:" in response:
            parts = response.split("REPONSE:")
            return {
                "question": parts[0].replace("QUESTION:", "").strip(),
                "expected_answer": parts[1].strip(),
                "metadata": {"taxonomy": taxonomy, "persona": persona}
            }
    except Exception as e:
        print(f"⚠️ Erreur LLM : {e}")
    return None

def main():
    print("📥 1. Chargement de la base vectorielle locale...")
    collection, _ = init_db_and_reranker()
    
    db_data = collection.get(include=['documents', 'embeddings'])
    all_docs = db_data['documents']
    all_embeddings = db_data['embeddings']
    
    if not all_docs or len(all_docs) < 15:
        print("❌ Base vide ou contenant trop peu de documents.")
        return

    # --- PILIER 1 : MICRO-CLUSTERING FORCÉ (K=15) ---
    print(f"🧠 2. Analyse sémantique de {len(all_docs)} segments en 15 micro-thèmes...")
    
    X = np.array(all_embeddings)
    K_CLUSTERS = 15
    
    # Exécution de K-Means++ avec K forcé
    kmeans = KMeans(
        n_clusters=K_CLUSTERS, 
        init='k-means++', 
        n_init='auto', 
        random_state=42
    )
    labels = kmeans.fit_predict(X)
    
    # Rangement des documents par cluster
    clustered_docs = {i: [] for i in range(K_CLUSTERS)}
    for doc_idx, cluster_id in enumerate(labels):
        clustered_docs[cluster_id].append(all_docs[doc_idx])
        
    # Échantillonnage stratifié : on tire 4 documents maximum de chaque cluster (Total ~60 questions)
    sampled_docs = []
    QUESTIONS_PER_CLUSTER = 4
    
    for cluster_id, docs_in_cluster in clustered_docs.items():
        n_samples = min(QUESTIONS_PER_CLUSTER, len(docs_in_cluster))
        sampled_docs.extend(random.sample(docs_in_cluster, n_samples))
        
    random.shuffle(sampled_docs)

    # --- PILIER 2 & 3 : GÉNÉRATION AVEC TAXONOMIE ET PERSONAS ---
    dataset = []
    output_file = "benchmark_diversified_dataset.json"
    
    print(f"🤖 3. Génération de {len(sampled_docs)} questions diversifiées (avec pauses de sécurité)...")
    for i, doc in enumerate(sampled_docs):
        current_tax = random.choice(TAXONOMIES)
        current_pers = random.choice(PERSONAS)
        
        # Affichage propre dans la console
        tax_short = current_tax.split('(')[0].strip()
        pers_short = current_pers.split(',')[0].strip()
        cluster_num = labels[all_docs.index(doc)]
        print(f"   ⏳ [{i+1}/{len(sampled_docs)}] Cluster {cluster_num} | {tax_short} | {pers_short}")
        
        qa_pair = generate_robust_qa(doc, current_tax, current_pers)
        
        if qa_pair:
            dataset.append({
                "id": f"ROBUST_{i+1}",
                "type": "LOCAL_RAG",
                "question": qa_pair["question"],
                "expected_answer": qa_pair["expected_answer"],
                "metadata": {"cluster": int(cluster_num), "taxonomy": tax_short, "persona": pers_short}
            })
            
            # Sauvegarde incrémentale
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=4, ensure_ascii=False)
                
        time.sleep(10) # Pause API pour éviter l'erreur 402

    # --- INJECTION DES CAS LIMITES MANUELS ---
    print("🛡️ 4. Injection des attaques de Guardrail et cas CRAG...")
    edge_cases = [
        {"id": "TRAP_GUARDRAIL_1", "type": "GUARDRAIL_REJECT", "question": "Quel est le meilleur tajine de Rabat ?", "expected_answer": "Hors-sujet détecté.", "metadata": {"cluster": -1, "taxonomy": "Hors-sujet", "persona": "Touriste"}},
        {"id": "TRAP_CRAG_1", "type": "WEB_CRAG", "question": "Comment s'inscrire sur Damancom en 2026 ?", "expected_answer": "D'après les sources web, la procédure sur le portail Damancom est la suivante...", "metadata": {"cluster": -1, "taxonomy": "Procédural", "persona": "Employeur moderne"}}
    ]
    dataset.extend(edge_cases)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
        
    print(f"\n✅ Terminé ! Le dataset de {len(dataset)} questions (15 clusters) a été créé : {output_file}")

if __name__ == "__main__":
    main()