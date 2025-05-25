import streamlit as st
import re

st.set_page_config(page_title="Fuvar szöveggenerátor", layout="centered")

st.title("🚌 szöveggenerátor")
st.write("Illeszd be a sort a Google Sheets-ből (több szóközzel vagy tabbal elválasztva):")

raw_input = st.text_area("Fuvarsor beillesztése", height=150)

def extract_fields(text):
    parts = re.split(r'\s{2,}|\t+', text.strip())

    # Rendszám
    rendszam = next((x for x in parts if re.match(r'^[A-Z]{3}-\d{3}$', x)), 'N/A')

    # Telefonszám
    telefonszam = next((x for x in parts if '+36' in x), 'N/A')

    # Időpont (pl. 7:15, 16:00)
    idopontok = [x for x in parts if re.match(r'^\d{1,2}:\d{2}$', x)]
    kiallas_ido = idopontok[0] if idopontok else 'N/A'

    # Dátum (pl. 2025.05.21)
    datumok = [x for x in parts if re.match(r'^\d{4}\.\d{2}\.\d{2}$', x)]
    if len(datumok) == 1:
        indulas = datumok[0]
        vegzes = datumok[0]
    elif len(datumok) >= 2:
        indulas = datumok[0]
        vegzes = datumok[1]
    else:
        indulas = vegzes = 'N/A'

    # Létszám: szám típusú mező
    letszam = next((x for x in parts if re.match(r'^\d+$', x)), 'N/A')

    # Sofőr név
    if telefonszam in parts:
        idx = parts.index(telefonszam)
        sofor_nev = " ".join(parts[idx - 2:idx]) if idx >= 2 else 'N/A'
        sofor_keresztnev = parts[idx - 1] if idx >= 1 else 'N/A'
    else:
        sofor_nev = sofor_keresztnev = 'N/A'

    # Úticél: az első hosszabb cím-szerű mező
    uticel = next((x for x in parts if len(x.split()) > 1 and re.search(r'[a-záéíóöőúüű]', x, re.IGNORECASE)), 'N/A')

    return {
        "sofor_teljesnev": sofor_nev,
        "sofor_keresztnev": sofor_keresztnev,
        "telefonszam": telefonszam,
        "rendszam": rendszam,
        "kiallas_datum": indulas,
        "kiallas_idopont": kiallas_ido,
        "vegzes_datum": vegzes,
        "uticel": uticel,
        "letszam": letszam
    }

if st.button("Szöveg generálása") and raw_input.strip():
    data = extract_fields(raw_input)

    if data["kiallas_datum"] == data["vegzes_datum"]:
        datum_szoveg = f"{data['kiallas_datum']} napra."
    else:
        datum_szoveg = f"{data['kiallas_datum']} - {data['vegzes_datum']} napokra."

    output = f"""Szia, {data['sofor_keresztnev']} 👋

Küldöm a munkát {datum_szoveg}

*Kiállás időpontja:* {data['kiallas_datum']}, {data['kiallas_idopont']}
*Kiállás helye:* —
*Úticél:* {data['uticel']}
*Busz:* {data['rendszam']}
*Várható végzés:* {data['vegzes_datum']}
*Létszám:* {data['letszam']}
"""

    st.markdown("### ✏️ Generált szöveg")
    st.text_area("Másolható szöveg", output, height=250)
    st.download_button("📋 Szöveg másolása", output, file_name="fuvar_szoveg.txt", mime="text/plain")