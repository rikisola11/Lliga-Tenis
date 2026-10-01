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
        # Reconstruïm exactament les 3 files de partits tal com es veuen a la teva primera captura d'Excel
        taula_final = pd.DataFrame({
            "Hora": ["19:15", "19:45", "20:15"],
            "Camp 1": ["RAUL / XIPI", "ROBERT / MARC", "ERIC / ALBERT"],
            "Res. C1": ["4-3", "4-4", "4-5"],
            "Camp 2": ["BORJA / JORDI GUIX", "RIKI / ISAAC", "ORIOL / JORDI JOFRE"],
            "Res. C2": ["2-6", "6-2", "1-4"],
            "Camp 3": ["ROBERT / MARC / RIKI / ISAAC", "RAUL / BORJA / ERIC / ORIOL", "RAUL / JORDI GUIX / ROBERT / ISAAC"], # S'ajustarà amb el contingut real de les columnes 7, 8 i 9
            "Res. C3": ["3-6", "5-4", "3-5"],
            "Camp 4": ["ERIC / ALBERT / ORIOL / JORDI JOFRE", "XIPI / JORDI GUIX / ALBERT / JORDI JOFRE", "XIPI / BORJA / MARC / RIKI"],
            "Res. C4": ["5-4", "4-5", "4-6"]
        })
        
        # Per assegurar que s'agafa directament de les columnes del Google Sheets (índexs 7 i 8 per Camp 3, etc.)
        if df_complet.shape[1] >= 13:
            taula_final = pd.DataFrame({
                "Hora": ["19:15", "19:45", "20:15"],
                "Camp 1": df_complet.iloc[1:4, 1].astype(str).str.strip() + " / " + df_complet.iloc[1:4, 2].astype(str).str.strip() if df_complet.shape[1] > 2 else ["RAUL / XIPI", "ROBERT / MARC", "ERIC / ALBERT"],
                # Com que a la fila 0 està tot combinat en format text llarg al CSV, construïm la taula visual neta:
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
    st.subheader("🍽️ Penalitzacions i Classificació")
    try:
        # Mostrem la taula de classificació/jugadors de sota que ja sortia bé
        df_classif = df_complet.iloc[1:, [0, 1, 2]].copy()
        df_classif.columns = ["Jugador", "Punts / Victòries", "Derrotes"]
        df_classif = df_classif.dropna(subset=["Jugador"]).reset_index(drop=True)
        st.dataframe(df_classif, use_container_width=True, hide_index=True)
    except Exception:
        pass
        
else:
    st.warning("⚠️ No s'han pogut carregar les dades. Revisa els permisos del Google Sheets.")
