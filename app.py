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
        # Busquem on està la fila de "CAMP 1"
        mask_camp = df_complet.apply(lambda row: row.astype(str).str.contains("CAMP 1", case=False).any(), axis=1)
        idx_camp = df_complet[mask_camp].index
        
        if len(idx_camp) > 0:
            fila_camp = idx_camp[0]
            # Els partits estan a les 3 files exactament posteriors a la fila de "CAMP 1"
            brut_partits = df_complet.iloc[fila_camp + 1 : fila_camp + 4, :].copy()
            
            taula_final = pd.DataFrame({
                "Hora": brut_partits.iloc[:, 0].values,
                "Camp 1": brut_partits.iloc[:, 1].astype(str).str.strip() + " / " + brut_partits.iloc[:, 2].astype(str).str.strip(),
                "Res. C1": brut_partits.iloc[:, 3].values,
                "Camp 2": brut_partits.iloc[:, 4].astype(str).str.strip() + " / " + brut_partits.iloc[:, 5].astype(str).str.strip(),
                "Res. C2": brut_partits.iloc[:, 6].values,
                "Camp 3": brut_partits.iloc[:, 7].astype(str).str.strip() + " / " + brut_partits.iloc[:, 8].astype(str).str.strip(),
                "Res. C3": brut_partits.iloc[:, 9].values,
                "Camp 4": brut_partits.iloc[:, 10].astype(str).str.strip() + " / " + brut_partits.iloc[:, 11].astype(str).str.strip(),
                "Res. C4": brut_partits.iloc[:, 12].values
            })
            
            st.dataframe(taula_final, use_container_width=True, hide_index=True)
        else:
            st.warning("No s'ha trobat la taula de partits.")
            
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
    except Exception:
        pass
        
else:
    st.warning("⚠️ No s'han pogut carregar les dades. Revisa els permisos del Google Sheets.")
