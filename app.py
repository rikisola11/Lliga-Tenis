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
        # Intentem carregar per nom de pestanya
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nom_pestanya}"
        df = pd.read_csv(url, header=None)
        if df.empty or len(df) < 2:
            raise Exception("Full buit")
        return df
    except Exception:
        try:
            # Fallback: si falla el nom, carreguem el document principal per defecte
            url_base = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
            df = pd.read_csv(url_base, header=None)
            return df
        except Exception as e:
            st.error(f"Error en la connexió amb Google Sheets: {e}")
            return None

df_jornada = carregar_pestanya(jornada_seleccionada)

if df_jornada is not None and not df_jornada.empty:
    st.markdown(f"### 📌 {jornada_seleccionada.upper()}")
    
    try:
        partits_data = []
        for i in range(3, min(6, len(df_jornada))):
            hora = df_jornada.iloc[i, 1] if df_jornada.shape[1] > 1 else ""
            c1_a = df_jornada.iloc[i, 2] if df_jornada.shape[1] > 2 else ""
            c1_b = df_jornada.iloc[i, 3] if df_jornada.shape[1] > 3 else ""
            res_c1 = df_jornada.iloc[i, 4] if df_jornada.shape[1] > 4 else ""
            
            c2_a = df_jornada.iloc[i, 5] if df_jornada.shape[1] > 5 else ""
            c2_b = df_jornada.iloc[i, 6] if df_jornada.shape[1] > 6 else ""
            res_c2 = df_jornada.iloc[i, 7] if df_jornada.shape[1] > 7 else ""
            
            c3_a = df_jornada.iloc[i, 8] if df_jornada.shape[1] > 8 else ""
            c3_b = df_jornada.iloc[i, 9] if df_jornada.shape[1] > 9 else ""
            res_c3 = df_jornada.iloc[i, 10] if df_jornada.shape[1] > 10 else ""
            
            c4_a = df_jornada.iloc[i, 11] if df_jornada.shape[1] > 11 else ""
            c4_b = df_jornada.iloc[i, 12] if df_jornada.shape[1] > 12 else ""
            res_c4 = df_jornada.iloc[i, 13] if df_jornada.shape[1] > 13 else ""

            partits_data.append({
                "Hora": str(hora),
                "Camp 1": f"{c1_a} / {c1_b}",
                "Res. C1": str(res_c1),
                "Camp 2": f"{c2_a} / {c2_b}",
                "Res. C2": str(res_c2),
                "Camp 3": f"{c3_a} / {c3_b}",
                "Res. C3": str(res_c3),
                "Camp 4": f"{c4_a} / {c4_b}",
                "Res. C4": str(res_c4)
            })
            
        df_partits = pd.DataFrame(partits_data)
        st.dataframe(df_partits, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Error al carregar els partits: {e}")

    st.markdown("---")
    st.subheader(f"🍽️ Penalitzacions i Classificació - {jornada_seleccionada}")
    
    try:
        if len(df_jornada) > 9:
            df_penal = df_jornada.iloc[9:, [1, 2]].copy()
            df_penal.columns = ["Jugador", f"Sopar {jornada_seleccionada}"]
            df_penal = df_penal.dropna(subset=["Jugador"])
            df_penal = df_penal[df_penal["Jugador"].str.strip() != ""]
            df_penal = df_penal.reset_index(drop=True)
            
            if not df_penal.empty:
                st.dataframe(df_penal, use_container_width=True, hide_index=True)
            else:
                st.info("No hi ha dades de classificació en aquesta pestanya.")
        else:
            st.info("No s'ha trobat la taula inferior.")
            
    except Exception:
        pass
        
else:
    st.warning("⚠️ No s'han pogut carregar les dades. Si us plau, comprova que Google Sheets estigui compartit públicament.")
