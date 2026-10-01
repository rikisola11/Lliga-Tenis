import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lliga de Tenis", page_icon="🎾", layout="wide")

st.title("🎾 Lliga de Tenis - Resultats i Classificació")

SHEET_ID = "1Pw6HpqMFJl_tO3XUfS_egKvF9rD_HBgD"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=60)
def carregar_dades():
    try:
        df = pd.read_csv(url, header=None)
        return df
    except Exception as e:
        return None

df_complet = carregar_dades()

if df_complet is not None and not df_complet.empty:
    st.success("✅ Dades carregades correctament des del Google Drive!")
    
    # Busquem automàticament on comença la fila de "Penalitzacions"
    idx_penalitzacions = df_complet[df_complet.isin(['Penalitzacions per jugador']).any(axis=1)].index
    
    if len(idx_penalitzacions) > 0:
        corte = idx_penalitzacions[0]
        # Tot el que està abans de penalitzacions són els partits
        df_partits = df_complet.iloc[:corte].dropna(how='all')
        
        # Tot el que està a partir de penalitzacions és l'altra taula
        df_penal = df_complet.iloc[corte:].dropna(how='all')
    else:
        df_partits = df_complet
        df_penal = pd.DataFrame()

    # Mostrem la taula de Partits neta
    st.subheader("📊 Partits i Resultats")
    if not df_partits.empty:
        # Netegem la primera fila com a capçalera si escau
        df_partits = df_partits.dropna(how='all', axis=1)
        st.dataframe(df_partits, use_container_width=True, hide_index=True)
    
    # Mostrem la taula de Penalitzacions / Sopar
    if not df_penal.empty:
        st.subheader("🍽️ Penalitzacions i Sopar")
        df_penal = df_penal.dropna(how='all', axis=1)
        st.dataframe(df_penal, use_container_width=True, hide_index=True)
        
else:
    st.warning("⚠️ No s'han pogut carregar les dades. Revisa els permisos del Google Sheets.")
