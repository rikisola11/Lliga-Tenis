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
    
    # 1. TAULA DE PARTITS I RESULTATS
    st.subheader("📊 Partits i Resultats")
    # Agafem només les primeres columnes (de la 0 a la 12) i les files de partits
    if df_complet.shape[1] >= 13:
        df_partits = df_complet.iloc[0:4, 0:13].copy()
        # Posem la primera fila com a capçalera de la taula
        df_partits.columns = df_partits.iloc[0]
        df_partits = df_partits.iloc[1:].reset_index(drop=True)
        st.dataframe(df_partits, use_container_width=True, hide_index=True)
    else:
        st.warning("No s'han trobat suficients columnes per als partits.")

    # 2. TAULA DE PENALITZACIONS I SOPAR (a sota o a la dreta)
    st.subheader("🍽️ Penalitzacions i Sopar")
    try:
        # Extrec les columnes de la dreta on tens les penalitzacions i el sopar
        df_penal = df_complet.iloc[6:11, [0, 1, 2]].copy()
        df_penal.columns = ["Jugador", "Sopar Previ", "Sopar Jornada 1"]
        df_penal = df_penal.dropna(how='all').reset_index(drop=True)
        st.dataframe(df_penal, use_container_width=True, hide_index=True)
    except Exception:
        st.info("Pendent de definir el format de penalitzacions.")
        
else:
    st.warning("⚠️️ No s'han pogut carregar les dades. Revisa els permisos del Google Sheets.")
