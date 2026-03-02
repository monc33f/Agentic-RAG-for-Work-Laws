# ⚖️ Expert Légal Maroc - Advanced RAG Agent

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![LLM](https://img.shields.io/badge/LLM-Qwen_2.5_72B-green)
![Status](https://img.shields.io/badge/Status-Active-success)

Un assistant juridique intelligent spécialisé dans le **Droit du Travail Marocain** (Code du Travail, CNSS, CNOPS, litiges prud'homaux). Ce projet implémente une architecture **Advanced RAG (Retrieval-Augmented Generation)** de niveau production, incluant des boucles d'auto-correction, un routage de requêtes hybride et un système d'évaluation MLOps automatisé.

---

## 📚 Base de Connaissances (Corpus Juridique)

Le système RAG s'appuie sur une base vectorielle (ChromaDB) alimentée par **11 documents officiels** couvrant la législation marocaine. Ce corpus est structuré en trois grands piliers pour permettre un raisonnement croisé (Cross-Document Reasoning) de haute précision.

### 🏛️ Pilier 1 : Le Noyau Dur (Droit du Travail)
Ce pilier définit les règles fondamentales régissant les relations entre l'employeur et le salarié.
* 📄 **`Code-du-Travail-Maroc.pdf`** : Le document maître (Loi 65-99) couvrant les contrats, les salaires, les licenciements, les syndicats et les conditions de travail.
* 📄 **`Maroc-Decrets-code-travail.pdf`** : Les textes d'application pratiques (ex: mentions obligatoires sur la carte de travail, interdiction des travaux dangereux pour les femmes et les mineurs).
* 📄 **`heures-supplementaires.pdf`** : Le décret spécifique (2-04-570) fixant les conditions, les quotas annuels et la rémunération des heures supplémentaires.

### 🏥 Pilier 2 : Protection Sociale & Santé
Ce pilier gère la couverture sociale, les accidents et les cotisations obligatoires.
* 📄 **`dahir_1-72-184.pdf`** : Le Dahir fondateur régissant le régime de la Sécurité Sociale (CNSS) au Maroc.
* 📄 **`maroc-code-couverture-medicale.pdf`** : Le Code de la Couverture Médicale de Base (Loi 65-00), instaurant notamment l'Assurance Maladie Obligatoire (AMO).
* 📄 **`code-accident-travail-maroc.pdf`** : La législation sur la réparation des accidents du travail (rentes, indemnités pour les victimes et les ayants droit).

### 📘 Pilier 3 : Application Pratique & Guides Officiels
Ce pilier permet à l'agent de vulgariser les démarches administratives et de répondre aux cas pratiques complexes.
* 📄 **`nc-cnss.pdf`** : Note circulaire détaillée sur la détermination et le calcul de l'assiette de cotisations CNSS.
* 📄 **`Réussire sa retraite.pdf`** : Guide complet sur le cycle de fin de carrière, les pensions de vieillesse, les pensions de survivants et les règles de cumul emploi-retraite.
* 📄 **`Charte de l'affilié inspecté ou contrôlé.pdf`** : Document détaillant les droits, devoirs et pénalités d'une entreprise lors d'un contrôle de l'inspection CNSS.
* 📄 **`guide Fr.pdf`** : Guide officiel de l'employeur pour les travailleurs de maison (Loi 19-12), expliquant les procédures d'affiliation et de déclaration.
* 📄 **`Guide Ramedistes_fr_01_12def(2).pdf`** : Guide expliquant les procédures de basculement des bénéficiaires du RAMED vers l'AMO.

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

* **Similarité Sémantique Globale : 86.33 %**
* **Résistance aux attaques (Red Teaming) :** Taux de faux positifs réduit grâce au Guardrail Hybride sur d'autres domaines.

---

## 🚀 Installation & Démarrage

### 1. Prérequis
Assurez-vous d'avoir Python 3.9+ installé.

### 2. Cloner le dépôt
```bash
git clone [https://github.com/votre-nom-utilisateur/expert-legal-maroc.git](https://github.com/votre-nom-utilisateur/expert-legal-maroc.git)
cd expert-legal-maroc
