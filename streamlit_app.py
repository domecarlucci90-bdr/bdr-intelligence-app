import streamlit as st
import google.generativeai as genai

# Configurazione Pagina
st.set_page_config(page_title="BDR Intelligence Engine", layout="wide")

st.title("🚀 BDR Intelligence Engine | Mashfrog Edition")
st.markdown("Strumento di ricerca lead avanzato per BDR.")

# Sidebar per la API Key
with st.sidebar:
    st.header("Configurazione")
    api_key = st.text_input("Inserisci la tua Gemini API Key", type="password")
    st.info("Prendi la chiave su [AI Studio](https://aistudio.google.com/)")

# Prompt di sistema integrato
SYSTEM_PROMPT = """
Sei un esperto BDR per Mashfrog Group. Il tuo obiettivo è trovare lead per l'ERP Infor.
Usa strategie di Google Dorking (Recruiting Inverso, Webinar Spy, Compliance, End-of-Life).
Restituisci una tabella Markdown con: Lead, Azienda, Email (o pattern), Telefono, Trigger.
Usa 'ND' per i dati mancanti.
"""

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Usiamo il nome del modello più aggiornato e stabile
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[{"google_search_retrieval": {}}]
        )

        query = st.text_input("Cosa cerchiamo oggi? (es: Aziende Food Puglia fatturato > 10M)")

        if st.button("Avvia Ricerca Intelligence"):
            if query:
                with st.spinner("Analizzando i dati... attendi circa 20 secondi."):
                    # Chiamata al modello con gestione errori specifica
                    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nRichiesta: {query}")
                    
                    if response.text:
                        st.markdown(response.text)
                        st.success("Ricerca completata!")
            else:
                st.warning("Inserisci una richiesta.")
                
    except Exception as e:
        # Se il Grounding (Google Search) dà ancora errore 404, proviamo senza tool
        st.warning("Tentativo di ricerca senza Grounding in corso...")
        try:
            model_simple = genai.GenerativeModel('gemini-1.5-flash')
            response = model_simple.generate_content(f"{SYSTEM_PROMPT}\n\nRichiesta: {query}")
            st.markdown(response.text)
        except Exception as e2:
            st.error(f"Errore persistente: {e2}")
else:
    st.error("⚠️ Inserisci la chiave API a sinistra.")
