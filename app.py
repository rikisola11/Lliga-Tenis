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
    st.selectbox("Selecciona la Jornada", ["JORNADA 1"])
    st.markdown("### 📌 JORNADA 1")
    
    try:
        # Creem una taula neta per als partits directament a partir de les dades del teu Excel
        # Extreiem les files de l'hora (índexs 2, 3, 4)
        brut_partits = df_complet.iloc[2:5].copy()
        
        # Unim els dos jugadors de cada camp amb un guió (ex: "RAUL" + " - " + "XIPI")
        taula_final = pd.DataFrame({
            "Hora": brut_partits.iloc[:, 0].values,
            "Camp 1": brut_partits.iloc[:, 1].astype(str) + " - " + brut_partits.iloc[:, 2].astype(str),
            "Res. C1": brut_partits.iloc[:, 3].values,
            "Camp 2": brut_partits.iloc[:, 4].astype(str) + " - " + brut_partits.iloc[:, 5].astype(str),
            "Res. C2": brut_partits.iloc[:, 6].values,
            "Camp 3": brut_partits.iloc[:, 7].astype(str) + " - " + brut_partits.iloc[:, 8].astype(str),
            "Res. C3": brut_partits.iloc[:, 9].values,
            "Camp 4": brut_partits.iloc[:, 10].astype(str) + " - " + brut_partits.iloc[:, 11].astype(str),
            "Res. C4": brut_partits.iloc[:, 12].values
        })
        
        # Mostrem la graella de partits impecable
        st.dataframe(taula_final, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Error al processar els partits: {e}")

    # Taula de Penalitzacions i Sopars a sota
    st.markdown("---")
    st.subheader("🍽️ Penalitzacions i Sopars")
    try:
        # Part inferior de l'Excel (a partir de la fila 8)
        df_penal = df_complet.iloc[8:, 0:3].copy()
        df_penal.columns = ["Jugador", "Sopar Previ", "Sopar Jornada 1"]
        df_penal = df_penal.dropna(subset=["Jugador"]).reset_index(drop=True)
        st.dataframe(df_penal, use_container_width=True, hide_index=True)
    except Exception:
        st.info("Pendent de dades de penalització.")
        
else:
    st.warning("⚠️ No s'han pogut carregar les dades. Revisa els permisos del Google Sheets.")
