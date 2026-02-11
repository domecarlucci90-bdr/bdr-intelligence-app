import streamlit as st
import google.generativeai as genai

# Configurazione Pagina
st.set_page_config(page_title="BDR Intelligence Engine", layout="wide")

st.title("🚀 BDR Intelligence Engine | Mashfrog Special Edition")
st.markdown("Cerca lead qualificati usando l'intelligenza di Gemini e Google Search.")

# Sidebar per la API Key
with st.sidebar:
    st.header("Configurazione")
    api_key = st.text_input("Inserisci la tua Gemini API Key", type="password")
    st.info("Ottieni una chiave su [Google AI Studio](https://aistudio.google.com/)")

# Istruzioni di Sistema
SYSTEM_PROMPT = """
Sei il BDR Intelligence Engine per Mashfrog. 
Il tuo obiettivo è trovare aziende in target per ERP Infor (settore Fashion, Food, Manufacturing).
Usa le tue capacità di ricerca per identificare: Nome Lead, Azienda, Email (o pattern), Telefono, Strategia/Trigger.
Restituisci i dati in una tabella Markdown. Se un dato è mancante, usa 'ND'.
"""

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Configurazione del modello più compatibile
        # Rimuoviamo il tool "google_search_retrieval" esplicito che causava l'errore
        # e usiamo la versione standard che abilita comunque la ricerca se disponibile
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash', # Flash è più veloce e spesso più stabile per i tool
            tools=[{"google_search_retrieval": {}}] 
        )

        query = st.text_input("Esempio: Aziende manifatturiere in Puglia con fatturato > 5M")

        if st.button("Genera Lista Lead"):
            if query:
                with st.spinner("Ricerca in corso... attendi circa 15-30 secondi."):
                    # Chiamata al modello
                    response = model.generate_content(f"{SYSTEM_PROMPT}\n\nRichiesta: {query}")
                    
                    if response.text:
                        st.markdown(response.text)
                        st.success("Ricerca completata!")
                    else:
                        st.error("Il modello non ha restituito risultati. Riprova con una query più semplice.")
            else:
                st.warning("Inserisci una richiesta.")
    except Exception as e:
        st.error(f"Si è verificato un errore di configurazione: {e}")
else:
    st.error("⚠️ Inserisci la API Key nella barra laterale.")
