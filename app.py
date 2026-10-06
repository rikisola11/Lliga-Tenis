import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lliga de Tenis", page_icon="🎾", layout="wide")

st.title("🎾 Lliga de Tenis - Resultats i Classificació")
st.subheader("Quadre de Partits per Camps i Resultats")

SHEET_ID = "1Pw6HpqMFJl_tO3XUfS_egKvF9rD_HBgD"

jornades_disponibles = ["Jornada 1", "Jornada 2", "Jornada 3", "Jornada 4", "Jornada 5"]
jornada_seleccionada = st.selectbox("Selecciona la Jornada", jornades_disponibles)

@st.cache_data(ttl=60)
def carregar_pestanya(nom_pestanya):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nom_pestanya}"
        df = pd.read_csv(url, header=None)
        return df
    except Exception as e:
        return None

df_jornada = carregar_pestanya(jornada_seleccionada)

if df_jornada is not None and not df_jornada.empty:
    st.markdown(f"### 📌 {jornada_seleccionada.upper()}")
    
    try:
        # Construcció de la taula de partits segons la teva estructura visual (Fila 2 a 4 de l'Excel)
        partits_data = []
        for i in range(2, min(5, len(df_jornada))):
            hora = df_jornada.iloc[i, 0] if pd.notna(df_jornada.iloc[i, 0]) else ""
            c1 = df_jornada.iloc[i, 1] if pd.notna(df_jornada.iloc[i, 1]) else ""
            c2 = df_jornada.iloc[i, 2] if pd.notna(df_jornada.iloc[i, 2]) else ""
            res1 = df_jornada.iloc[i, 3] if pd.notna(df_jornada.iloc[i, 3]) else ""
            
            c3 = df_jornada.iloc[i, 4] if pd.notna(df_jornada.iloc[i, 4]) else ""
            c4 = df_jornada.iloc[i, 5] if pd.notna(df_jornada.iloc[i, 5]) else ""
            res2 = df_jornada.iloc[i, 6] if pd.notna(df_jornada.iloc[i, 6]) else ""
            
            c5 = df_jornada.iloc[i, 7] if pd.notna(df_jornada.iloc[i, 7]) else ""
            c6 = df_jornada.iloc[i, 8] if pd.notna(df_jornada.iloc[i, 8]) else ""
            res3 = df_jornada.iloc[i, 9] if pd.notna(df_jornada.iloc[i, 9]) else ""
            
            c7 = df_jornada.iloc[i, 10] if pd.notna(df_jornada.iloc[i, 10]) else ""
            c8 = df_jornada.iloc[i, 11] if pd.notna(df_jornada.iloc[i, 11]) else ""
            res4 = df_jornada.iloc[i, 12] if pd.notna(df_jornada.iloc[i, 12]) else ""

            partits_data.append({
                "Hora": str(hora),
                "Camp 1": f"{c1} / {c2}",
                "Res. C1": str(res1),
                "Camp 2": f"{c3} / {c4}",
                "Res. C2": str(res2),
                "Camp 3": f"{c5} / {c6}",
                "Res. C3": str(res3),
                "Camp 4": f"{c7} / {c8}",
                "Res. C4": str(res4)
            })
            
        df_partits = pd.DataFrame(partits_data)
        st.dataframe(df_partits, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Error al carregar els partits: {e}")

    st.markdown("---")
    st.subheader(f"🍽️ Penalitzacions i Classificació - {jornada_seleccionada}")
    
    try:
        # Extracció de la taula inferior de jugadors i sopars (a partir de la fila 9)
        if len(df_jornada) > 9:
            df_penal = df_jornada.iloc[9:, [0, 1]].copy()
            df_penal.columns = ["Jugador", f"Sopar {jornada_seleccionada}"]
            df_penal = df_penal.dropna(subset=["Jugador"])
            df_penal = df_penal[df_penal["Jugador"].astype(str).str.strip() != ""]
            df_penal = df_penal.reset_index(drop=True)
            
            if not df_penal.empty:
                st.dataframe(df_penal, use_container_width=True, hide_index=True)
            else:
                st.info("No hi ha dades de classificació en aquesta pestanya.")
        else:
            st.info("No s'ha trobat la taula inferior.")
            
    except Exception as e:
        st.info("Carregant dades de classificació...")
        
else:
    st.warning("⚠️ No s'han pogut carregar les dades de Google Sheets.")
