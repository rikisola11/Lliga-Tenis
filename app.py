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
    
    # 1. TAULA DE PARTITS I RESULTATS (Files 0 a 4, Columnes 0 a 13)
    st.subheader("📊 Partits i Resultats")
    try:
        # Seleccionem només les primeres columnes on hi ha els camps i hores
        df_partits = df_complet.iloc[0:4, 0:13].dropna(how='all').copy()
        df_partits.columns = df_partits.iloc[0] # Primera fila com a capçalera
        df_partits = df_partits.iloc[1:].reset_index(drop=True)
        st.dataframe(df_partits, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error("Error carregant la taula de partits.")

    # 2. TAULA DE PENALITZACIONS I SOPAR (A partir de la fila 8, columnes de l'esquerra)
    st.subheader("🍽️ Penalitzacions i Sopar")
    try:
        # Busquem on comença la taula de penalitzacions per les primeres columnes
        df_penal = df_complet.iloc[8:, 0:3].copy()
        df_penal.columns = ["Jugador", "Sopar Previ", "Sopar Jornada 1"]
        df_penal = df_penal.dropna(subset=["Jugador"]).reset_index(drop=True)
        st.dataframe(df_penal, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error("Error carregant la taula de penalitzacions.")
        
else:
    st.warning("⚠️ No s'han pogut carregar les dades. Revisa els permisos del Google Sheets.")
