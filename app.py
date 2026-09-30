import streamlit as pandas_or_st # Només per referència, fem servir streamlit i pandas
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lliga de Tenis", page_icon="🎾", layout="wide")

st.title("🎾 Lliga de Tenis - Resultats i Classificació")

# Enllaç del teu Google Sheets adaptat per descarregar en format CSV automàticament
SHEET_ID = "1Pw6HpqMFJl_tO3XUfS_egKvF9rD_HBgD"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60) # S'actualitza automàticament cada minut
def carregar_dades():
    try:
        # Llegeix directament del Google Sheets
        df = pd.read_csv(url)
        return df
    except Exception as e:
        return None

df = carregar_dades()

if df is not None and not df.empty:
    st.success("✅ Dades carregades correctament des del Google Drive!")
    
    # Mostrem les dades a l'aplicació (pots adaptar aquesta part segons com tinguis organitzades les columnes)
    st.subheader("📊 Partits i Resultats")
    st.dataframe(df, use_container_width=True)
    
    # Aquí pots afegir la teva lògica de classificació o taules que tenies prèviament
else:
    st.warning("⚠️ No s'han pogut carregar les dades. Assegura't que el Google Sheets és públic ('Qualsevol persona amb l'enllaç pot ser lector').")
