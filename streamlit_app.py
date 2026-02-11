import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BDR Intelligence", layout="wide")

st.title("🚀 BDR Intelligence Engine | Mashfrog")

with st.sidebar:
    st.header("Configurazione")
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Prendi la chiave su aistudio.google.com")

# Funzione per provare i diversi nomi dei modelli
def get_model_response(api_key, query):
    genai.configure(api_key=api_key)
    
    # Lista dei nomi modelli dal più recente al più stabile
    model_names = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
    
    system_prompt = "Sei un BDR Mashfrog. Trova lead per ERP Infor. Tabella Markdown: Lead, Azienda, Email, Tel, Trigger."
    
    for name in model_names:
        try:
            # Tentativo con ricerca Google (Grounding)
            model = genai.GenerativeModel(
                model_name=name,
                tools=[{"google_search_retrieval": {}}]
            )
            return model.generate_content(f"{system_prompt}\n\n{query}")
        except Exception:
            try:
                # Tentativo senza ricerca Google (conoscenza base)
                model = genai.GenerativeModel(model_name=name)
                return model.generate_content(f"{system_prompt}\n\n{query}")
            except Exception:
                continue # Prova il prossimo nome nella lista
    
    raise Exception("Nessun modello disponibile. Verifica la tua API Key su AI Studio.")

if api_key:
    query = st.text_input("Cosa cerchiamo? (es: Aziende Fashion in Puglia)")
    
    if st.button("Avvia Ricerca"):
        if query:
            with st.spinner("In corso..."):
                try:
                    response = get_model_response(api_key, query)
                    st.markdown(response.text)
                    st.success("Fatto!")
                except Exception as e:
                    st.error(f"Errore: {e}")
        else:
            st.warning("Inserisci una richiesta.")
else:
    st.info("Inserisci la API Key nella barra laterale.")
