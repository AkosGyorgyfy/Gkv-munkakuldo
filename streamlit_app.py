import streamlit as st
import re

st.set_page_config(page_title="Fuvar szöveggenerátor", page_icon="🚌", layout="centered")
st.title("Fuvar szöveggenerátor")

input_text = st.text_area("Illeszd be a sort a Google Sheets-ből (több szóközzel vagy tabbal elválasztva):")

if st.button("Szöveg generálása"):
    try:
        # Több szóköz vagy tab mentén bontja a szöveget
        parts = re.split(r'\s{2,}|\t+', input_text.strip())

        if len(parts) < 13:
            st.warning("Úgy tűnik, nem teljes a sor. Legalább 13 mező kell.")
            st.text(f"{len(parts)} mezőt találtam: {parts}")
        else:
            # Változók hozzárendelése
            munkaszam = parts[0]
            datum_indulas = parts[1]
            datum_vege = parts[2]
            orszag = parts[3]
            kiallas_idopont = parts[4]
            kiallas_hely = parts[5]
            uticel = parts[6]
            rendszam = parts[7]
            letszam = parts[8]
            vezeteknev = parts[9]
            keresztnev = parts[10]
            telefonszam = parts[11]
            diszpecser = parts[12]

            # Dátumrész a szöveg elejére
            if datum_indulas == datum_vege:
                datum_resz = f"Küldöm a munkát {datum_indulas} napra."
            else:
                datum_resz = f"Küldöm a munkát {datum_indulas} - {datum_vege} napokra."

            # Szöveg sablon
            output = f"""
            Szia, {keresztnev} 👋

            {datum_resz}

            *Kiállás időpontja:* {datum_indulas}, {kiallas_idopont}  
            *Kiállás helye:* {kiallas_hely}  
            *Úticél:* {uticel}  
            *Busz:* {rendszam}  
            *Várható végzés:* {datum_vege}  
            *Létszám:* {letszam}
            """

            st.markdown(output)

    except Exception as e:
        st.error("Valami hiba történt. Ellenőrizd a bemásolt sort.")
        st.exception(e)