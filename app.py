import os
import pandas as pd
import streamlit as st

EXCEL_PARTITS = "partits_jornada.xlsx"

st.set_page_config(page_title="Lliga de Tenis", page_icon="🎾", layout="wide")
st.title("🎾 Lliga de Tenis - Resultats i Classificació")

menu = st.sidebar.radio("Navegació", ["📅 Quadre de Partits per Camps", "🏆 Classificació General"])

if not os.path.exists(EXCEL_PARTITS):
    st.warning(f"No es troba el fitxer '{EXCEL_PARTITS}' a la carpeta.")
    st.stop()

try:
    df_excel = pd.read_excel(EXCEL_PARTITS, header=None, engine='openpyxl')
except Exception as e:
    st.error(f"Error al llegir l'Excel: {e}")
    st.stop()

def obtenir_estructura_completa(df):
    jornades = {}
    jornada_actual = None
    taula_visual = []
    partits_calcul = []
    
    # 1. Llegim partits i jornades (ignorant la secció de sopars)
    for idx, row in df.iterrows():
        val_a = str(row.iloc[0]).strip().upper()
        
        if "PENALITZACIONS" in val_a or "SOPAR" in val_a:
            break # Si comença la taula de sopars, tallem la lectura de partits d'aquesta passada
            
        if "JORNADA" in val_a:
            if jornada_actual:
                jornades[jornada_actual] = {
                    "visual": pd.DataFrame(taula_visual),
                    "calcul": partits_calcul
                }
            jornada_actual = val_a
            taula_visual = []
            partits_calcul = []
        elif jornada_actual:
            hora = row.iloc[0]
            if not pd.isna(hora) and str(hora) != "Hora" and not str(hora).startswith("CAMP"):
                fila_v = {"Hora": hora}
                col = 1
                camp_num = 1
                while col + 2 < df.shape[1]:
                    e1 = row.iloc[col]
                    e2 = row.iloc[col + 1]
                    res = row.iloc[col + 2]
                    
                    e1_s = str(e1).strip() if not pd.isna(e1) else ""
                    e2_s = str(e2).strip() if not pd.isna(e2) else ""
                    r_s = str(res).strip() if not pd.isna(res) else ""
                    
                    if e1_s and e2_s:
                        celda_partit = f"{e1_s} - {e2_s}"
                        partits_calcul.append({
                            "Equip 1": e1_s,
                            "Equip 2": e2_s,
                            "Resultat": r_s
                        })
                    else:
                        celda_partit = "-"
                        
                    fila_v[f"Camp {camp_num}"] = celda_partit
                    fila_v[f"Res. C{camp_num}"] = r_s if r_s else "-"
                    
                    col += 3
                    camp_num += 1
                taula_visual.append(fila_v)
                
    if jornada_actual and jornada_actual not in jornades:
        jornades[jornada_actual] = {
            "visual": pd.DataFrame(taula_visual),
            "calcul": partits_calcul
        }
        
    # 2. Llegim de manera independent la taula de penalitzacions/sopars per a la visualització i càlcul
    llegint_sopars = False
    columnes_sopars = []
    files_sopars_visual = []
    sopars_data = {}
    
    for idx, row in df.iterrows():
        val_a = str(row.iloc[0]).strip()
        val_b = str(row.iloc[1]).strip() if len(row) > 1 else ""
        
        if "PENALITZACIONS" in val_a.upper() or "SOPAR" in val_b.upper():
            llegint_sopars = True
            # Recollim les columnes de sopars (capçaleres)
            columnes_sopars = [str(row.iloc[c]).strip() for c in range(1, len(row)) if not pd.isna(row.iloc[c]) and str(row.iloc[c]).strip() != ""]
            continue
            
        if llegint_sopars:
            if val_a == "" or val_a.lower() == "nan":
                continue
            
            jugador = val_a.upper()
            fila_sop = {"Jugador": jugador}
            total_jugador_sopar = 0
            
            for c_idx, col_name in enumerate(columnes_sopars):
                val_celda = row.iloc[c_idx + 1]
                v_num = 0
                try:
                    if not pd.isna(val_celda):
                        v_num = int(float(val_celda))
                except:
                    pass
                
                fila_sop[col_name] = v_num
                total_jugador_sopar += v_num
                
            files_sopars_visual.append(fila_sop)
            sopars_data[jugador] = total_jugador_sopar

    df_sopars_visual = pd.DataFrame(files_sopars_visual) if files_sopars_visual else pd.DataFrame()

    return jornades, df_sopars_visual, sopars_data

dades_jornades, df_sopars_vis, dades_sopars = obtenir_estructura_completa(df_excel)

if menu == "📅 Quadre de Partits per Camps":
    st.header("Quadre de Partits per Camps i Resultats")
    
    if not dades_jornades:
        st.warning("No s'han trobat dades a l'Excel.")
    else:
        noms_jornades = list(dades_jornades.keys())
        jornada_sel = st.selectbox("Selecciona la Jornada", noms_jornades)
        
        st.subheader(f"📌 {jornada_sel} - Partits")
        df_v = dades_jornades[jornada_sel]["visual"]
        st.dataframe(df_v, use_container_width=True)
        
        if not df_sopars_vis.empty:
            st.markdown("---")
            st.subheader("🍽️ Penalitzacions i Assistència Sopars")
            st.dataframe(df_sopars_vis, use_container_width=True)

elif menu == "🏆 Classificació General":
    st.header("Classificació General Individual (Partits + Sopars)")
    
    ranking = {}

    def assegurar_jugador(j):
        if j not in ranking:
            ranking[j] = {"Punts": 0, "Punts Partits": 0, "Punts Sopars": 0, "Partits Jugats": 0, "Victòries": 0, "Empats": 0, "Derrotes": 0}

    def sumar_punts_jugadors(equip_str, punts, es_victoria, es_empat):
        jugadors = [j.strip() for j in equip_str.split("/") if j.strip()]
        for j in jugadors:
            assegurar_jugador(j)
            ranking[j]["Punts"] += punts
            ranking[j]["Punts Partits"] += punts
            ranking[j]["Partits Jugats"] += 1
            if es_victoria:
                ranking[j]["Victòries"] += 1
            elif es_empat:
                ranking[j]["Empats"] += 1
            else:
                ranking[j]["Derrotes"] += 1

    # 1. Calculem punts de partits
    for j_nom, info in dades_jornades.items():
        for p in info["calcul"]:
            e1 = p["Equip 1"]
            e2 = p["Equip 2"]
            res = p["Resultat"]
            
            if "-" in res:
                try:
                    j1, j2 = map(int, res.split("-"))
                    if j1 > j2:
                        sumar_punts_jugadors(e1, 3, True, False)
                        sumar_punts_jugadors(e2, 0, False, False)
                    elif j2 > j1:
                        sumar_punts_jugadors(e2, 3, True, False)
                        sumar_punts_jugadors(e1, 0, False, False)
                    else:
                        sumar_punts_jugadors(e1, 2, False, True)
                        sumar_punts_jugadors(e2, 2, False, True)
                except:
                    pass

    # 2. Afegim els punts de sopars
    for jugador, pts_sopars in dades_sopars.items():
        assegurar_jugador(jugador)
        ranking[jugador]["Punts"] += pts_sopars
        ranking[jugador]["Punts Sopars"] = pts_sopars

    if ranking:
        df_ranking = pd.DataFrame.from_dict(ranking, orient='index')
        
        # Forcem a format enter (sense decimals) totes les columnes numèriques
        cols_numeriques = ["Punts", "Punts Partits", "Punts Sopars", "Partits Jugats", "Victòries", "Empats", "Derrotes"]
        for c in cols_numeriques:
            if c in df_ranking.columns:
                df_ranking[c] = df_ranking[c].fillna(0).astype(int)
                
        df_ranking = df_ranking.sort_values(by=["Punts", "Victòries"], ascending=False).reset_index()
        df_ranking.rename(columns={"index": "Jugador"}, inplace=True)
        
        df_ranking.index = df_ranking.index + 1
        df_ranking.index.name = "Pos."
        
        st.table(df_ranking)
    else:
        st.info("Encara no hi ha dades suficients per calcular la classificació.")