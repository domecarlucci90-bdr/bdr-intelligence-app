import streamlit as st
import google.generativeai as genai

st.title("🚀 BDR Engine")
api_key = st.sidebar.text_input("Inserisci API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usiamo il nome più universale in assoluto
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        query = st.text_input("Cosa cerchiamo?")
        if st.button("Cerca"):
            # Rimuoviamo i tool per ora, testiamo solo l'intelligenza base
            response = model.generate_content(f"Sei un assistente BDR. Trova: {query}")
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Errore: {e}")
