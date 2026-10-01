import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lliga de Tenis", page_icon="🎾", layout="wide")

st.title("🎾 Lliga de Tenis - Resultats i Classificació")

SHEET_ID = "1Pw6HpqMFJl_tO3XUfS_egKvF9rD_HBgD"
url = f"https://docs.google.s/spreadsheets/d/{SHEET_ID}/export?format=csv"
# Nota: si dóna error l'enllaç anterior, fem servir el format directe de publicació web:
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=60)
def carregar_dades():
    try:
        df_complet = pd.read_csv(url, header=None)
        return df_complet
    except Exception as e:
        return None

df_complet = carregar_dades()

if df_complet is not None and not df_complet.empty:
    st.success("✅ Dades carregades correctament des del Google Drive!")
    
    # 1. Taula de Partits (files superiors)
    # Seleccionem des de la fila de capçalera fins abans de les penalitzacions
    st.subheader("📊 Partits i Resultats")
    # Suposant que les primeres 5 files tenen els partits
    df_partits = df_complet.iloc[1:5].dropna(how='all', axis=1)
    # Netegem la capçalera amb la primera fila de partits
    df_partits.columns = df_complet.iloc[2]
    df_partits = df_partits.iloc[1:].reset_index(drop=True)
    st.dataframe(df_partits, use_container_width=True)
    
    # 2. Taula de Penalitzacions / Sopar (files inferiors)
    st.subheader("🍽️ Penalitzacions i Sopar")
    # Busquem on comença la taula de penalitzacions
    df_penalitzacions = df_complet.iloc[6:].dropna(how='all', axis=1)
    df_penalitzacions.columns = df_complet.iloc[7]
    df_penalitzacions = df_penalitzacions.iloc[1:].reset_index(drop=True)
    st.dataframe(df_penalitzacions, use_container_width=True)
    
else:
    st.warning("⚠️ No s'han pogut carregar les dades. Revisa els permisos del Google Sheets.")
