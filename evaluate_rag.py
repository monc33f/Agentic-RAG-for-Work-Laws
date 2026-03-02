import json
import time
import re

# Imports de tous tes modules (comme dans app.py)
from init_db import init_db_and_reranker
from retrieve_and_rerank import retrieve_and_rerank
from call_llm import call_llm
from check_domain_relevance import check_domain_relevance
from perform_web_search import perform_web_search
from update_dossier import update_dossier
from get_search_query import get_search_query
from check_faithfulness import check_faithfulness
from check_relevance import check_relevance

def llm_as_a_judge(question, expected_answer, generated_answer):
    """Utilise le LLM pour noter la réponse générée de 0 à 5."""
    sys_prompt = "Tu es un juge expert et impartial spécialisé en droit du travail marocain."
    
    prompt = f"""Évalue la qualité et l'exactitude de la réponse générée par rapport à la réponse de référence.

QUESTION POSÉE :
"{question}"

RÉPONSE DE RÉFÉRENCE (La vérité terrain absolue) :
"{expected_answer}"

RÉPONSE GÉNÉRÉE PAR LE SYSTÈME À ÉVALUER :
"{generated_answer}"

Évalue la réponse générée sur une échelle de 0 à 5 selon ces critères :
5 = Parfaite : Exactement les mêmes faits juridiques, complète et claire.
4 = Très bonne : Faits corrects, mais manque un détail mineur ou formulation légèrement imprécise.
3 = Moyenne : L'idée générale est là, mais il manque des éléments importants de la référence.
2 = Médiocre : Partiellement fausse ou trop incomplète.
1 = Mauvaise : Majoritairement fausse ou hors-sujet.
0 = Dangereuse : Contredit totalement la référence ou donne un conseil juridique illégal.

Renvoie UNIQUEMENT ton évaluation sous ce format strict :
SCORE: [chiffre de 0 à 5]
JUSTIFICATION: [Une phrase expliquant brièvement la note]
"""
    try:
        response = call_llm(prompt, sys_prompt, max_tokens=100)
        
        match = re.search(r"SCORE:\s*([0-5])", response)
        score = int(match.group(1)) if match else 0
        
        justification = response.split("JUSTIFICATION:")[-1].strip() if "JUSTIFICATION:" in response else "Pas de justification."
        return score, justification
    except Exception as e:
        print(f"⚠️ Erreur du Juge : {e}")
        return 0, "Erreur API lors de l'évaluation."

def simulate_agent_pipeline(query, collection, reranker):
    """Clone exact de run_advanced_agent de app.py, sans Streamlit."""
    try:
        # 1. Guardrail
        if not check_domain_relevance(query):
            return "🛡️ **Hors-sujet détecté** : Je suis spécialisé exclusivement en droit du travail marocain."
            
        # 2. Simulation de la mémoire (On crée un dossier neuf pour chaque question du benchmark)
        dossier = "- Nouveau client."
        dossier = update_dossier(dossier, query)
        
        # 3. Formulation de la recherche
        current_search_query = get_search_query(dossier, query, strategy="strict")
        
        # 4. Boucle d'analyse (Exactement comme dans app.py)
        for attempt in range(2):
            context_list = retrieve_and_rerank(current_search_query, collection, reranker)
            
            if not context_list:
                current_search_query = get_search_query(dossier, query, strategy="broaden")
                continue
            
            context_str = "\n\n".join(context_list)
            sys_prompt = "Tu es un expert en droit du travail marocain. Réponds strictement selon le contexte. Cite la source et la page."
            final_prompt = f"Dossier Client:\n{dossier}\n\nContexte:\n{context_str}\n\nQuestion: {query}"
            
            answer = call_llm(final_prompt, sys_prompt)
            
            # Évaluation interne par tes Superviseurs
            if check_faithfulness(context_str, answer) and check_relevance(query, answer):
                return answer
            else:
                current_search_query = get_search_query(dossier, query, strategy="broaden")
                continue
                
        # 5. Recherche Web (Si la boucle a échoué 2 fois)
        web_context = perform_web_search(query)
        sys_prompt_web = "Tu es un expert. Réponds via le contexte web. Précise toujours que l'information provient d'Internet."
        final_prompt_web = f"Dossier:\n{dossier}\n\nContexte Web:\n{web_context}\n\nQuestion: {query}"
        
        return call_llm(final_prompt_web, sys_prompt_web)

    except Exception as e:
        return f"❌ Une erreur est survenue : {e}"

def main():
    print("🚀 Initialisation de la suite d'évaluation MLOps...")
    collection, reranker = init_db_and_reranker()
    
    input_file = "benchmark_dataset_robust.json"
    output_file = "robust_evaluation_results.json"
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            dataset = json.load(f)
    except FileNotFoundError:
        print(f"❌ Fichier {input_file} introuvable.")
        return

    results = []
    total_score = 0
    total_latency = 0
    
    print(f"\n⚖️ Démarrage de l'évaluation de {len(dataset)} questions...")
    print("-" * 50)
    
    for i, item in enumerate(dataset):
        print(f"\n▶️ Test [{i+1}/{len(dataset)}] : {item['metadata'].get('taxonomy', 'Cas Limite')}")
        print(f"   Question : {item['question']}")
        
        # Chronomètre du pipeline complet (incluant reformulations et superviseurs)
        start_time = time.time()
        generated_answer = simulate_agent_pipeline(item['question'], collection, reranker)
        latency = round(time.time() - start_time, 2)
        total_latency += latency
        
        print(f"   ⏱️ Temps de réponse : {latency}s")
        
        # Notation par le Juge
        score, justification = llm_as_a_judge(
            question=item['question'], 
            expected_answer=item['expected_answer'], 
            generated_answer=generated_answer
        )
        
        total_score += score
        
        # Affichage
        stars = "⭐" * score + "❌" * (5 - score)
        print(f"   Note du Juge : {stars} ({score}/5)")
        print(f"   Justification : {justification}")
        
        item['evaluation'] = {
            "generated_answer": generated_answer,
            "score_out_of_5": score,
            "justification": justification,
            "latency_seconds": latency
        }
        results.append(item)
        
        # On sauvegarde à chaque étape pour ne rien perdre
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
        time.sleep(30) # Pause pour l'API du juge

    max_possible_score = len(dataset) * 5
    accuracy_percentage = (total_score / max_possible_score) * 100
    avg_latency = round(total_latency / len(dataset), 2)
    
    print("\n" + "=" * 50)
    print("📊 RAPPORT FINAL D'ÉVALUATION")
    print("=" * 50)
    print(f"✅ Précision globale : {accuracy_percentage:.1f}% ({total_score}/{max_possible_score} points)")
    print(f"⚡ Latence moyenne   : {avg_latency} secondes / requête")
    print("=" * 50)
    
if __name__ == "__main__":
    main()