import streamlit as st
import google.generativeai as genai

# Configurazione Pagina
st.set_page_config(page_title="BDR Intelligence Engine", layout="wide")

st.title("🚀 BDR Intelligence Engine | Mashfrog Special Edition")
st.markdown("Cerca lead qualificati usando il Google Dorking strategico.")

# Sidebar per la API Key
with st.sidebar:
    st.header("Configurazione")
    api_key = st.text_input("Inserisci la tua Gemini API Key", type="password")
    st.info("Ottieni una chiave su [Google AI Studio](https://aistudio.google.com/)")

# Definizione del Sistema (Le tue istruzioni)
SYSTEM_PROMPT = """
Sei il BDR Intelligence Engine per Mashfrog. 
Il tuo compito è trovare lead per ERP Infor usando il Google Search Grounding.
Usa strategie di: Recruiting Inverso, Webinar Spy, Compliance Pain, End-of-Life.
Restituisci i dati in una tabella Markdown con: Nome Lead, Azienda, Email (o pattern), Telefono, Strategia/Trigger, Pain Point.
Se un dato è mancante, usa 'ND'.
"""

if api_key:
    genai.configure(api_key=api_key)
    # Importante: abilitiamo il grounding (Google Search)
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        tools=[{"google_search_retrieval": {}}]
    )

    query = st.text_input("Esempio: Aziende manifatturiere in Puglia con fatturato > 5M€ che usano AS400")

    if st.button("Genera Lista Lead"):
        if query:
            with st.spinner("Interrogando Google e analizzando i lead..."):
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\nRichiesta utente: {query}")
                st.markdown(response.text)
                st.success("Ricerca completata! Copia i dati nel tuo CRM.")
        else:
            st.warning("Inserisci una richiesta per iniziare.")
else:
    st.error("⚠️ Inserisci la API Key nella barra laterale per attivare l'app.")
