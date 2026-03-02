import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def scrape_webpage(url):
    """Visite une URL et extrait tout son texte principal."""
    try:
        # On simule un vrai navigateur pour ne pas être bloqué
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=5)
        
        # On parse le HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On supprime les scripts et le style (menus, pubs)
        for script in soup(["script", "style", "nav", "footer", "aside"]):
            script.extract()
            
        # On récupère le texte propre
        text = soup.get_text(separator=' ', strip=True)
        
        # On limite à 3000 caractères pour ne pas exploser la mémoire du LLM
        return text[:3000] + "..." 
    except Exception:
        return "" # En cas d'échec de lecture, on renvoie du vide

def perform_web_search(query):
    """Trouve la meilleure page web et lit son contenu complet."""
    optimized_query = f"droit du travail Maroc loi : {query}"
    
    try:
        with DDGS() as ddgs:
            # On cherche juste les 2 meilleurs résultats
            results = list(ddgs.text(optimized_query, max_results=2))
            
        if not results:
            return "Aucun résultat pertinent trouvé sur le web."
            
        formatted_results = []
        
        # Pour le premier résultat (le plus pertinent), on va lire la page ENTIÈRE
        top_result = results[0]
        full_page_text = scrape_webpage(top_result['href'])
        
        # Si on a réussi à lire la page, on met son contenu complet
        if full_page_text:
            formatted_results.append(
                f"Titre: {top_result['title']}\nLien: {top_result['href']}\nCONTENU COMPLET DE LA PAGE:\n{full_page_text}"
            )
        else:
            # Sinon (site bloqué), on se rabat sur le petit extrait
            formatted_results.append(
                f"Titre: {top_result['title']}\nLien: {top_result['href']}\nExtrait: {top_result['body']}"
            )
            
        return f"[Source: Recherche Web (DuckDuckGo + Web Scraper)]\n" + "\n\n---\n\n".join(formatted_results)
        
    except Exception as e:
        raise Exception(f"Erreur Web Search : {e}")