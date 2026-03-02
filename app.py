import streamlit as st
import time

# Imports de nos fonctions uniques
from init_db import init_db_and_reranker
from retrieve_and_rerank import retrieve_and_rerank
from call_llm import call_llm
from update_dossier import update_dossier
from check_domain_relevance import check_domain_relevance
from get_search_query import get_search_query
from check_faithfulness import check_faithfulness
from check_relevance import check_relevance
from perform_web_search import perform_web_search

st.set_page_config(page_title="Expert Légal Maroc", page_icon="⚖️", layout="wide")

@st.cache_resource(show_spinner="Chargement du moteur vectoriel...")
def load_db():
    try:
        return init_db_and_reranker()
    except Exception as e:
        st.error(str(e))
        st.stop()

db_collection, reranker_model = load_db()

def run_advanced_agent(user_query):
    try:
        with st.spinner("🛡️ Analyse de la pertinence..."):
            if not check_domain_relevance(user_query):
                return "🛡️ **Hors-sujet détecté** : Je suis spécialisé exclusivement en droit du travail marocain."
                
        with st.spinner("📝 Mise à jour du dossier client..."):
            st.session_state.dossier = update_dossier(st.session_state.dossier, user_query)
            
        with st.spinner("🔄 Formulation de la recherche..."):
            current_search_query = get_search_query(st.session_state.dossier, user_query, strategy="strict")
        
        for attempt in range(2):
            with st.status(f"🛠️ Cycle d'analyse {attempt+1}...") as status:
                context_list = retrieve_and_rerank(current_search_query, db_collection, reranker_model)
                
                if not context_list:
                    current_search_query = get_search_query(st.session_state.dossier, user_query, strategy="broaden")
                    continue
                
                context_str = "\n\n".join(context_list)
                sys_prompt = "Tu es un expert en droit du travail marocain. Réponds strictement selon le contexte. Cite la source et la page."
                final_prompt = f"Dossier Client:\n{st.session_state.dossier}\n\nContexte:\n{context_str}\n\nQuestion: {user_query}"
                
                answer = call_llm(final_prompt, sys_prompt)
                
                if check_faithfulness(context_str, answer) and check_relevance(user_query, answer):
                    status.update(label="✅ Réponse validée", state="complete")
                    return answer
                else:
                    current_search_query = get_search_query(st.session_state.dossier, user_query, strategy="broaden")
                    continue
                    
        with st.status("🌐 Lancement de la recherche Web...") as status:
            web_context = perform_web_search(user_query)
            with st.expander("👀 Voir les sources brutes (Liens & Extraits)"):
                st.text(web_context) 
                
            sys_prompt_web = "Tu es un expert. Réponds via le contexte web. Précise toujours que l'information provient d'Internet."
            final_prompt_web = f"Dossier:\n{st.session_state.dossier}\n\nContexte Web:\n{web_context}\n\nQuestion: {user_query}"
            
            answer_web = call_llm(final_prompt_web, sys_prompt_web)
            status.update(label="✅ Réponse générée via Web", state="complete")
            return answer_web

    except Exception as e:
        return f"❌ Une erreur est survenue : {e}"

st.title("⚖️ Assistant Juridique Certifié")

if "messages" not in st.session_state: st.session_state.messages = []
if "dossier" not in st.session_state: st.session_state.dossier = "- Nouveau client."

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

with st.sidebar:
    st.header("🧠 Mémoire Active")
    st.info(st.session_state.dossier)
    st.divider()
    st.success(f"Segments indexés : {db_collection.count()}")
    if st.button("🗑️ Nouvelle session"):
        st.session_state.messages = []
        st.session_state.dossier = "- Nouveau client."
        st.rerun()

if prompt := st.chat_input("Posez votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        response = run_advanced_agent(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        time.sleep(0.5)
        st.rerun()