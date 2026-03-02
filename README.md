# ⚖️ Expert Légal Maroc - Advanced RAG Agent

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![LLM](https://img.shields.io/badge/LLM-Qwen_2.5_72B-green)
![Status](https://img.shields.io/badge/Status-Active-success)

Un assistant juridique intelligent spécialisé dans le **Droit du Travail Marocain** (Code du Travail, CNSS, CNOPS, litiges prud'homaux). Ce projet implémente une architecture **Advanced RAG (Retrieval-Augmented Generation)** de niveau production, incluant des boucles d'auto-correction, un routage de requêtes hybride et un système d'évaluation MLOps automatisé.

---

## ✨ Fonctionnalités Clés (Architecture RAG Avancée)

- **🛡️ Guardrail Hybride (Filtre Lexical + Sémantique) :** Un routeur de requêtes ultra-rapide qui bloque les questions hors-sujet tout en acceptant les cas limites complexes (accidents de travail, médecine du travail, taxes judiciaires) sans consommer de tokens inutiles.
- **🔄 Self-Refine Loop (Superviseurs d'Hallucination) :** Le système évalue ses propres réponses avant de les afficher. Si la réponse n'est pas fidèle au contexte juridique (`Faithfulness`) ou ne répond pas à la question (`Relevance`), l'agent reformule sa recherche et tente un second cycle.
- **🌐 CRAG (Corrective RAG) & Web Fallback :** Si les documents locaux ne contiennent pas la réponse (ex: lois récentes de 2026), l'agent bascule automatiquement sur une recherche Web via DuckDuckGo pour trouver un contexte à jour.
- **🧠 Mémoire Active (Dossier Client) :** Le chatbot maintient un contexte conversationnel continu, mettant à jour le "dossier" de l'utilisateur à chaque interaction pour des réponses personnalisées.

## 🛠️ Stack Technique

- **Interface Utilisateur :** Streamlit
- **Modèle LLM :** Qwen 2.5 72B Instruct (via API)
- **Modèle d'Embedding :** BAAI/bge-m3 (Local)
- **Base Vectorielle :** ChromaDB
- **Évaluation MLOps :** Scikit-learn (Similarité Cosinus), LLM-as-a-Judge

## 📊 Évaluation et Performances (MLOps)

Le système intègre une suite d'évaluation automatisée robuste pour mesurer la qualité des réponses sur un dataset de 60 questions couvrant diverses taxonomies (Factuel, Cas Pratique, Procédural) et personas.

* **Similarité Sémantique Globale : 87.33 %**
* **Résistance aux attaques (Red Teaming) :** Taux de faux positifs réduit grâce au Guardrail Hybride sur d'autres domaines.

---

## 🚀 Installation & Démarrage

### 1. Prérequis
Assurez-vous d'avoir Python 3.9+ installé.

### 2. Cloner le dépôt
```bash
git clone [https://github.com/votre-nom-utilisateur/expert-legal-maroc.git](https://github.com/votre-nom-utilisateur/expert-legal-maroc.git)
cd expert-legal-maroc
