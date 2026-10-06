import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Lliga de Tenis", page_icon="🎾", layout="wide")

st.title("🎾 Lliga de Tenis - Resultats i Classificació")

SHEET_ID = "1Pw6HpqMFJl_tO3XUfS_egKvF9rD_HBgD"

jornades_disponibles = ["Jornada 1", "Jornada 2", "Jornada 3", "Jornada 4", "Jornada 5"]
jornada_seleccionada = st.selectbox("Selecciona la Jornada", jornades_disponibles)

@st.cache_data(ttl=60)
def carregar_pestanya(nom_pestanya):
    try:
        nom_encoded = urllib.parse.quote(nom_pestanya)
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nom_encoded}"
        df = pd.read_csv(url, header=None)
        return df
    except Exception as e:
        return None

df = carregar_pestanya(jornada_seleccionada)

if df is not None and not df.empty:
    st.markdown(f"### 📌 Quadre de Partits - {jornada_seleccionada}")
    
    try:
        # Mostrem directament el bloc de partits de manera neta (files 2 a 5)
        # Netejant les columnes innecessàries si n'hi ha
        if len(df) > 5:
            df_partits = df.iloc[2:5, 1:14].copy()
            # Omplim valors NaN per evitar errors visuals
            df_partits = df_partits.fillna("")
            st.dataframe(df_partits, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Error al mostrar els partits: {e}")

    st.markdown("---")
    st.subheader(f"🍽️ Penalitzacions i Classificació - {jornada_seleccionada}")
    
    try:
        # Busquem i mostrem la taula inferior de jugadors i sopars (a partir de la fila 9)
        if len(df) > 9:
            # Agafem les columnes de jugadors i punts de sopar
            df_penal = df.iloc[9:, [1, 2]].copy()
            df_penal.columns = ["Jugador", f"Sopar {jornada_seleccionada}"]
            df_penal = df_penal.dropna(subset=["Jugador"])
            df_penal = df_penal[df_penal["Jugador"].astype(str).str.strip() != ""]
            df_penal = df_penal[df_penal["Jugador"].astype(str).str.lower() != "nan"]
            df_penal = df_penal.reset_index(drop=True)
            
            if not df_penal.empty:
                st.dataframe(df_penal, use_container_width=True, hide_index=True)
            else:
                st.info("No hi ha dades a la taula de classificació d
