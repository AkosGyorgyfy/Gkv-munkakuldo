import streamlit as st
from datetime import datetime

st.title("🚌 Sofőrüzenet Generátor")

st.write("Másold be egy fuvar adatsorát a Google Sheets-ből (TAB-delimitált formátumban):")

input_text = st.text_area("Fuvar adatsor", height=200)

# Oszlopsorrend alapján (27+ oszlop)
column_names = [
    "Iktatószám", "Fuvar kezdete", "Fuvar vége", "Országkód", "Kiállás időpontja",
    "Kiállás helye", "Úticél", "Fuvar végének időpontja", "Rendszám", "Utánfutó",
    "UtasLétszám", "Gkv I.", "Gkv II.", "Gkv III.", "Gkv IV.",
    "Fuvarozó", "Megrendelő", "Kapcsolattartó", "Email", "Telefonszám",
    "Fuvarozó neve", "Kü/Bf", "Ellátás típusa", "Megjegyzés 1", "Megjegyzés 2",
    "Megjegyzés 3", "Megjegyzés 4"
]

def parse_row(row_text):
    parts = row_text.strip().split("\t")
    # Kiegészítjük üres mezőkkel, ha kevesebb van
    parts += [""] * (len(column_names) - len(parts))
    return dict(zip(column_names, parts))

def generate_message(data):
    gkv = data.get("Gkv I.", "").strip()
    if not gkv:
        return "⚠️ Nincs megadva sofőr (Gkv I.)"

    start_day = data.get("Fuvar kezdete", "").strip()
    end_day = data.get("Fuvar vége", "").strip()
    vege_ido = data.get("Fuvar végének időpontja", "").strip()
    
    if start_day == end_day or not end_day:
        date_part = f"Küldöm a munkát {start_day} napra"
    else:
        date_part = f"Küldöm a munkát {start_day} - {end_day} napokra"

    return f"""Szia,

{date_part}

*Kiállás időpontja:* {start_day}, {data.get('Kiállás időpontja', '').strip()}
*Kiállás helye:* {data.get('Kiállás helye', '').strip()}
*Úticél:* {data.get('Úticél', '').strip()}
*Program:* 
*Szükséges útdíjak:* Magyar
*Szállás/ellátás:* 
*Tankolás:* 
*Busz:* {data.get('Rendszám', '').strip()}
*Várható végzés:* {vege_ido}
*Létszám:* {data.get('UtasLétszám', '').strip()}
*Megrendelő:* {data.get('Megrendelő', '').strip()}

Bármi komolyabb program változás van, azt kérjük azonnal jelezni!!!

Tankolókártyákat, bankkártyákat, mikrofont, úti okmányaidat (ÚTLEVÉL!), indulás előtt, otthon is ellenőrizni!
A FUVAR VÉGÉN KÉRJÜK AZ AUTÓBUSZT MINDIG MEGTANKOLVA ÉS KITAKARÍTVA LETENNI!

BÁRMILYEN FELMERÜLŐ MŰSZAKI HIBÁT KÉRJÜK AZONNAL JELEZNI!
"""

if input_text:
    try:
        adat = parse_row(input_text)
        uzenet = generate_message(adat)
        st.success("🎉 Üzenet legenerálva:")
        st.text_area("Sofőrnek küldendő üzenet:", value=uzenet, height=200)
    except Exception as e:
        st.error(f"Hiba történt: {e}")