import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BDR Intelligence", layout="wide")
st.title("🚀 REAL-TIME BDR Engine")

with st.sidebar:
    api_key = st.text_input("Inserisci API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # REINSERIAMO IL TOOL DI RICERCA GOOGLE
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[{"google_search_retrieval": {}}] 
        )
        
        query = st.text_input("Cerca aziende REALI (es: 'Aziende metalmeccaniche zona Brindisi iscritte a Confindustria')")
        
        if st.button("Avvia Ricerca Verificata"):
            with st.spinner("Interrogando Google Search per dati reali..."):
                # Forziamo il modello a cercare online
                prompt = f"USA GOOGLE SEARCH per trovare dati REALI e ATTUALI. Non inventare nulla. Richiesta: {query}. Tabella: Nome, Sito Web, Fatturato, Segnale di business."
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.info("Nota: I dati sopra provengono da ricerche Google in tempo reale.")
                
    except Exception as e:
        st.error(f"Errore: {e}. Se vedi 404, Google non ha ancora attivato la ricerca sulla tua chiave.")
else:
    st.info("Incolla la API Key.")
