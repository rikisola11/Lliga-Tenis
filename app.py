import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lliga de Tenis", page_icon="🎾", layout="wide")

st.title("🎾 Lliga de Tenis - Resultats i Classificació")
st.subheader("Quadre de Partits per Camps i Resultats")

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
    # Selector de Jornada
    st.selectbox("Selecciona la Jornada", ["JORNADA 1"])
    st.markdown("### 📌 JORNADA 1")
    
    try:
        # Extraiem la taula de partits (files de la 1 a la 4, columnes de la 0 a la 12)
        df_partits = df_complet.iloc[1:4, 0:13].copy()
        
        # Assignem les capçaleres exactes que corresponen a la graella de partits
        df_partits.columns = [
            "Hora", "Camp 1", "X", "Res. C1", 
            "Camp 2", "Y", "Res. C2", 
            "Camp 3", "Z", "Res. C3", 
            "Camp 4", "W", "Res. C4"
        ]
        
        # Eliminem columnes innecessàries de separació si n'hi ha i netegem índexs
        df_partits = df_partits[["Hora", "Camp 1", "Res. C1", "Camp 2", "Res. C2", "Camp 3", "Res. C3", "Camp 4", "Res. C4"]]
        df_partits = df_partits.reset_index(drop=True)
        
        # Mostrem la taula impecable
        st.dataframe(df_partits, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error("Error al formatejar la graella de partits.")

    # A sota de tot, podem mostrar també les penalitzacions de manera neta
    with st.expander("🍽️ Veure Penalitzacions i Sopars"):
        try:
            df_penal = df_complet.iloc[8:, 0:3].copy()
            df_penal.columns = ["Jugador", "Sopar Previ", "Sopar Jornada 1"]
            df_penal = df_penal.dropna(subset=["Jugador"]).reset_index(drop=True)
            st.dataframe(df_penal, use_container_width=True, hide_index=True)
        except Exception:
            st.info("Pendent de dades de penalització.")
        
else:
    st.warning("⚠️ No s'han pogut carregar les dades. Revisa els permisos del Google Sheets.")
