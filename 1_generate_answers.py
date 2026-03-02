import json
import time
from init_db import init_db_and_reranker
from evaluate_rag import simulate_agent_pipeline # On réutilise la fonction de simulation qu'on a codée

def main():
    print("🚀 Démarrage de la génération des réponses (Mode Batch)...")
    collection, reranker = init_db_and_reranker()
    
    input_file = "test_dataset_100.json"
    output_file = "generated_test_answers.json"
    
    with open(input_file, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # Système de reprise : charger ce qui a déjà été généré
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            results = json.load(f)
            processed_ids = {item["id"] for item in results}
    except FileNotFoundError:
        results = []
        processed_ids = set()

    print(f"📊 Progression : {len(processed_ids)}/{len(dataset)} questions déjà traitées.")
    
    for i, item in enumerate(dataset):
        if item["id"] in processed_ids:
            continue # On saute ce qui est déjà fait !
            
        print(f"\n▶️ Génération [{i+1}/{len(dataset)}] : {item['question'][:60]}...")
        
        start_time = time.time()
        # Ton agent génère la réponse (utilise tes quotas API restants)
        generated_answer = simulate_agent_pipeline(item['question'], collection, reranker)
        latency = round(time.time() - start_time, 2)
        
        item['generated_answer'] = generated_answer
        item['latency'] = latency
        results.append(item)
        
        # Sauvegarde immédiate
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
        print(f"   ✅ Réponse sauvegardée ({latency}s).")
        time.sleep(30) # Pause API de courtoisie

if __name__ == "__main__":
    main()