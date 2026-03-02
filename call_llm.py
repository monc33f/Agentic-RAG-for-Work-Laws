from huggingface_hub import InferenceClient
from config import HF_API_KEY, LLM_REPO_ID

hf_client = InferenceClient(api_key=HF_API_KEY)

def call_llm(prompt, system_msg="Tu es un expert juridique.", max_tokens=1024):
    try:
        response = hf_client.chat_completion(
            model=LLM_REPO_ID,
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Erreur API Hugging Face : {e}")