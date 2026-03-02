import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embedding_class import BGEEmbeddingFunction

def main():
    print("⚖️ Démarrage de l'évaluation sémantique hors-ligne...")
    
    # On charge ton modèle d'embedding local (Zéro API Hugging Face nécessaire ici)
    print("📥 Chargement du modèle BGE-M3 local...")
    embedder = BGEEmbeddingFunction()
    
    input_file = "generated_test_answers.json"
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            dataset = json.load(f)
    except FileNotFoundError:
        print("❌ Fichier introuvable. Lancez '1_generate_answers.py' d'abord.")
        return

    scores = []
    
    print("\n🔍 Calcul des similarités cosinus...")
    for item in dataset:
        # Si le Guardrail a bloqué à juste titre, c'est un succès (score 1.0)
        if item["type"] == "GUARDRAIL_REJECT" and "Hors-sujet" in item["generated_answer"]:
            score = 1.0
        # S'il y a eu une erreur API
        elif "Erreur" in item["generated_answer"]:
            score = 0.0
        # Sinon, on compare mathématiquement le sens des deux réponses
        else:
            # On vectorise les deux textes
            vec_expected = embedder([item["expected_answer"]])[0]
            vec_generated = embedder([item["generated_answer"]])[0]
            
            # Calcul de la similarité cosinus (formatage numpy)
            vec_expected = np.array(vec_expected).reshape(1, -1)
            vec_generated = np.array(vec_generated).reshape(1, -1)
            
            # Score de 0 à 1
            score = cosine_similarity(vec_expected, vec_generated)[0][0]
        
        # On convertit le score en pourcentage pour la lisibilité
        score_pct = round(score * 100, 2)
        scores.append(score_pct)
        item["semantic_score_pct"] = score_pct
        
        print(f"[{item['id']}] Score: {score_pct}%")

    # Rapport Final
    avg_score = sum(scores) / len(scores) if scores else 0
    
    print("\n" + "=" * 50)
    print("📊 RAPPORT FINAL D'ÉVALUATION SÉMANTIQUE")
    print("=" * 50)
    print(f"Questions évaluées : {len(dataset)}")
    print(f"Score de similarité global : {avg_score:.2f} %")
    print("=" * 50)
    
    # Sauvegarde
    with open("testset_final_report.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()