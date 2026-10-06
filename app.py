import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Lliga de Tenis", page_icon="🎾", layout="wide")

st.title("🎾 Lliga de Tenis - Resultats i Classificació")
st.subheader("Quadre de Partits per Camps i Resultats")

SHEET_ID = "1Pw6HpqMFJl_tO3XUfS_egKvF9rD_HBgD"

jornades_disponibles = ["Jornada 1", "Jornada 2", "Jornada 3", "Jornada 4", "Jornada 5"]
jornada_seleccionada = st.selectbox("Selecciona la Jornada", jornades_disponibles)

@st.cache_data(ttl=60)
def carregar_pestanya_per_nom(nom_pestanya):
    try:
        # Codifiquem el nom de la pestanya per a la URL (ex: "Jornada 1" -> "Jornada%201")
        nom_encoded = urllib.parse.quote(nom_pestanya)
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={nom_encoded}"
        df = pd.read_csv(url, header=None)
        return df
    except Exception as e:
        return None

df_jornada = carregar_pestanya_per_nom(jornada_seleccionada)

if df_jornada is not None and not df_jornada.empty:
    st.markdown(f"### 📌 {jornada_seleccionada.upper()}")
    
    try:
        # Comprovació de seguretat: si el DataFrame té dades, mostrem directament la taula neta dels partits 
        # (agafant les files de partits segons la teva estructura visual on les hores comencen a la fila 3)
        partits_data = []
        for i in range(len(df_jornada)):
            val_col_0 = str(df_jornada.iloc[i, 0]).strip() if df_jornada.shape[1] > 0 else ""
            val_col_1 = str(df_jornada.iloc[i, 1]).strip() if df_jornada.shape[1] > 1 else ""
            
            # Detectem si és una fila de hora (ex: 19:15)
            if ":" in val_col_1 or ":" in val_col_0:
                fila_idx = i
                hora = val_col_1 if ":" in val_col_1 else val_col_0
                
                # Extracció robusta de camps i resultats per a aquesta hora
                c1_a = str(df_jornada.iloc[i, 2]) if df_jornada.shape[1] > 2 else ""
                c1_b = str(df_jornada.iloc[i, 3]) if df_jornada.shape[1] > 3 else ""
                res_c1 = str(df_jornada.iloc[i, 4]) if df_jornada.shape[1] > 4 else ""
                
                c2_a = str(df_jornada.iloc[i, 5]) if df_jornada.shape[1] > 5 else ""
                c2_b = str(df_jornada.iloc[i, 6]) if df_jornada.shape[1] > 6 else ""
                res_c2 = str(df_jornada.iloc[i, 7]) if df_jornada.shape[1] > 7 else ""
                
                c3_a = str(df_jornada.iloc[i, 8]) if df_jornada.shape[1] > 8 else ""
                c3_b = str(df_jornada.iloc[i, 9]) if df_jornada.shape[1] > 9 else ""
                res_c3 = str(df_jornada.iloc[i, 10]) if df_jornada.shape[1] > 10 else ""
                
                c4_a = str(df_jornada.iloc[i, 11]) if df_jornada.shape[1] > 11 else ""
                c4_b = str(df_jornada.iloc[i, 12]) if df_jornada.shape[1] > 12 else ""
                res_c4 = str(df_jornada.iloc[i, 13]) if df_jornada.shape[1] > 13 else ""

                partits_data.append({
                    "Hora": hora,
                    "Camp 1": f"{c1_a} / {c1_b}".replace("nan", "").strip(" /"),
                    "Res. C1": res_c1.replace("nan", ""),
                    "Camp 2": f"{c2_a} / {c2_b}".replace("nan", "").strip(" /"),
                    "Res. C2": res_c2.replace("nan", ""),
                    "Camp 3": f"{c3_a} / {c3_b}".replace("nan", "").strip(" /"),
                    "Res. C3": res_c3.replace("nan", ""),
                    "Camp 4": f"{c4_a} / {c4_b}".replace("nan", "").strip(" /"),
                    "Res. C4": res_c4.replace("nan", "")
                })

        if len(partits_data) > 0:
            df_partits = pd.DataFrame(partits_data)
            st.dataframe(df_partits, use_container_width=True, hide_index=True)
        else:
            # Fallback visual directe si no troba les hores automàticament
            st.info("Mostrant estructura de partits de la pestanya...")
            st.dataframe(df_jornada.iloc[2:6, 1:14], use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Error al carregar els partits: {e}")

    st.markdown("---")
    st.subheader(f"🍽️ Penalitzacions i Classificació - {jornada_seleccionada}")
    
    try:
        # Busquem la taula inferior de penalitzacions/sopars de manera dinàmica
        found_penal = False
        for i in range(len(df_jornada)):
            cell_val = str(df_jornada.iloc[i, 1]) if df_jornada.shape[1] > 1 else ""
            if "Sopar" in cell_val or "Penalitzacions" in cell_val:
                start_idx = i + 1
                df_penal = df_jornada.iloc[start_idx:start_idx+15, [1, 2]].copy()
                df_penal.columns = ["Jugador", f"Sopar {jornada_seleccionada}"]
                df_penal = df_penal.dropna(subset=["Jugador"])
                df_penal = df_penal[df_penal["Jugador"].astype(str).str.strip() != ""]
                df_penal = df_penal[df_penal["Jugador"].astype(str).str.lower() != "nan"]
                df_penal = df_penal.reset_index(drop=True)
                
                if not df_penal.empty:
                    st.dataframe(df_penal, use_container_width=True, hide_index=True)
                    found_penal = True
                    break
        
        if not found_penal and len(df_jornada) > 9:
            df_penal = df_jornada.iloc[9:, [1, 2]].copy()
            df_penal.columns = ["Jugador", f"Sopar {jornada_seleccionada}"]
            df_penal = df_penal.dropna(subset=["Jugador"])
            df_penal = df_penal[df_penal["Jugador"].astype(str).str.strip() != ""]
            df_penal = df_penal.reset_index(drop=True)
            st.dataframe(df_penal, use_container_width=True, hide_index=True)
            
    except Exception:
        pass
        
else:
    st.warning("⚠️ No s'han pogut carregar les dades de Google Sheets. Comprova que el document sigui públic.")
