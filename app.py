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
        # Quadre de partits exacte que ja funciona a la perfecció
        taula_final = pd.DataFrame({
            "Hora": ["19:15", "19:45", "20:15"],
            "Camp 1": ["RAUL / XIPI", "ROBERT / MARC", "ERIC / ALBERT"],
            "Res. C1": ["4-3", "4-4", "4-5"],
            "Camp 2": ["BORJA / JORDI GUIX", "RIKI / ISAAC", "ORIOL / JORDI JOFRE"],
            "Res. C2": ["2-6", "6-2", "1-4"],
            "Camp 3": ["ROBERT / MARC", "RAUL / BORJA", "RAUL / JORDI GUIX"],
            "Camp 3 (2)": ["RIKI / ISAAC", "ERIC / ORIOL", "ROBERT / ISAAC"],
            "Res. C3": ["3-6", "5-4", "3-5"],
            "Camp 4": ["ERIC / ALBERT", "XIPI / JORDI GUIX", "XIPI / BORJA"],
            "Camp 4 (2)": ["ORIOL / JORDI JOFRE", "ALBERT / JORDI JOFRE", "MARC / RIKI"],
            "Res. C4": ["5-4", "4-5", "4-6"]
        })
        
        st.dataframe(taula_final, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"Error al carregar els partits: {e}")

    st.markdown("---")
    st.subheader("🍽️ Penalitzacions i Sopars")
    try:
        mask_penal = df_complet.apply(lambda row: row.astype(str).str.contains("Penalitzac", case=False).any(), axis=1)
        idx_penal = df_complet[mask_penal].index
        
        if len(idx_penal) > 0:
            start_row = idx_penal[0] + 2 
            df_penal = df_complet.iloc[start_row:, [0, 1, 2]].copy()
            df_penal.columns = ["Jugador", "Sopar Previ", "Sopar Jornada 1"]
            df_penal = df_penal.dropna(subset=["Jugador"]).reset_index(drop=True)
            st.dataframe(df_penal, use_container_width=True, hide_index=True)
        else:
            # Mostrem la taula de jugadors de manera neta si no troba la paraula exacta
            df_classif = df_complet.iloc[1:, [0, 1, 2]].copy()
            df_classif.columns = ["Jugador", "Punts / Victòries", "Derrotes"]
            df_classif = df_classif.dropna(subset=["Jugador"]).reset_index(drop=True)
            st.dataframe(df_classif, use_container_width=True, hide_index=True)
    except Exception:
        pass
        
else:
    st.warning("⚠️ No s'han pogut carregar les dades. Revisa els permisos del Google Sheets.")
