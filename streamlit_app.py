import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="BDR Intelligence", layout="wide")
st.title("🚀 BDR Engine | Versione Universale")

with st.sidebar:
    api_key = st.text_input("Inserisci API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 1. Troviamo automaticamente il modello disponibile per il tuo account
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            st.error("Nessun modello trovato per questa API Key. Controlla AI Studio.")
        else:
            # Scegliamo il miglior modello disponibile (preferibilmente flash o pro)
            selected_model = available_models[0] 
            st.caption(f"Modello in uso: {selected_model}")
            
            model = genai.GenerativeModel(selected_model)
            
            query = st.text_input("Cosa cerchiamo? (es: Aziende Food Puglia)")
            
            if st.button("Cerca"):
                with st.spinner("Generando risultati..."):
                    # Prompt focalizzato sul BDR
                    full_prompt = f"Agisci come BDR Mashfrog. Trova lead per ERP Infor basandoti su: {query}. Tabella Markdown: Azienda, Settore, Potenziale Pain Point."
                    response = model.generate_content(full_prompt)
                    st.markdown(response.text)
                    
    except Exception as e:
        if "API_KEY_INVALID" in str(e):
            st.error("La tua API Key non è valida. Ricreala su AI Studio.")
        else:
            st.error(f"Errore tecnico: {e}")
else:
    st.info("Incolla la tua API Key nella barra laterale per attivare il motore.")
