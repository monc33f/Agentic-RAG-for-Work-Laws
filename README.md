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
- **Évaluation MLOps :** Scikit-learn (Similarité Cosinus)

## 📊 Évaluation et Performances (MLOps)

Le système intègre une suite d'évaluation automatisée robuste (inspirée des architectures *LLM-as-a-Judge*) pour mesurer la qualité des réponses. Les performances ont été mesurées hors-ligne en calculant la **Similarité Cosinus (Scikit-learn)** entre les réponses générées par le système et un *Ground Truth* (réponses idéales de référence générées à l'aide d'un LLM en se basant sur des extraits différents de notre base de connaissances).

### 🧬 Composition du Dataset de Test
Pour simuler un environnement de production réel, les requêtes ont été croisées selon deux axes :
* **4 Taxonomies de requêtes :** Factuel (Lois directes), Procédural (Démarches étape par étape), Synthèse (Croisement de plusieurs articles), et Cas Pratiques (Mises en situation complexes).
* **4 Personas simulés :** * *Le DRH* (Langage très formel et managérial)
    * *Le Juriste pointilleux* (Vocabulaire hautement technique)
    * *L'Employé inquiet* (Langage courant, fautes de frappe, abréviations)
    * *Le Stagiaire* (Questions naïves et découvertes)

### 🏆 Résultats Clés

* 🎯 **Similarité Sémantique Globale : 86.33 %**
    * Un score exceptionnellement élevé pour le domaine juridique, démontrant la capacité du pipeline *Retrieve & Rerank* à extraire les bons articles (Code du Travail, Décrets, CNSS) et du modèle Qwen 72B à générer une réponse fidèle au contexte sans halluciner.

* 🛡️ **Résistance aux attaques et Guardrail Hybride (Red Teaming) :**
    * **Peu de Faux Positif sur les "Edge Cases" :** Le système a appris à ne plus bloquer les questions juridiquement valides partageant un champ lexical avec d'autres domaines (ex: *Moudawana/Héritage* pour les rentes d'orphelins suite à un accident de travail, *Droit Immobilier* pour l'acquisition de locaux par les syndicats).
    * **Blocage absolu du Hors-Sujet :** Le routeur rejette avec une haute précision les requêtes n'ayant aucun lien avec le droit du travail marocain (ex: Test validé sur le rejet de la requête *"Quel est le meilleur tajine de Rabat ?"*).

* 🌐 **Validation du Fallback Web (CRAG) :**
    * Le système a prouvé sa capacité à identifier les "trous" dans sa propre base de connaissances locale. Face à des questions nécessitant des données futures ou non documentées dans les PDF (ex: *"Comment s'inscrire sur Damancom en 2026 ?"*), l'agent court-circuite avec succès la base vectorielle pour déclencher une recherche DuckDuckGo en temps réel.

---

## 🚀 Installation & Démarrage

### 1. Prérequis
Assurez-vous d'avoir Python 3.9+ installé.

### 2. Cloner le dépôt
```bash
git clone [https://github.com/votre-nom-utilisateur/expert-legal-maroc.git](https://github.com/votre-nom-utilisateur/expert-legal-maroc.git)
cd expert-legal-maroc
