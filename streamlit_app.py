import streamlit as st

st.title("🚌 Sofőrüzenet Generátor")

st.write("Másold be egy fuvar adatsorát a Google Sheets-ből (TAB-delimitált formátumban):")

input_text = st.text_area("Fuvar adatsor", height=200)

# Oszlopsorrend alapján (27+ oszlop)
column_names = [
    "Iktatószám", "Fuvar kezdete", "Fuvar vége", "Országkód", "Kiállás időpontja",
    "Kiállás helye", "Úticél", "Fuvar végének időpontja", "Rendszám", "Utánfutó",
    "UtasLétszám", "Gkv I.", "Gkv II.", "Gkv III.", "Gkv IV.",
    "Megrendelő", "Megrendelő II.", "Kapcsolattartó", "Email", "Telefonszám",
    "Fuvarozó neve", "Kü/Bf", "Ellátás típusa", "Megjegyzés 1", "Megjegyzés 2",
    "Megjegyzés 3", "Megjegyzés 4"
]

def parse_row(row_text):
    parts = row_text.strip().split("\t")
    parts += [""] * (len(column_names) - len(parts))
    return dict(zip(column_names, parts))

def generate_message(data):
    gkv = data.get("Gkv I.", "").strip()
    start_day = data.get("Fuvar kezdete", "").strip()
    end_date = data.get("Fuvar végének időpontja", "").strip()

    if not gkv:
        return "⚠️ Nincs megadva sofőr (Gkv I.)"

    # Egy napos vagy több napos
    if start_day == data.get("Fuvar vége", "").strip() or not data.get("Fuvar vége", "").strip():
        date_line = f"Küldöm a munkát {start_day} napra (egy napos munka esetén)"
    else:
        date_line = f"Küldöm a munkát {start_day} - {end_date} napokra (több napos munka esetén)"

    return f"""Szia, {gkv}  
{date_line}

*Kiállás időpontja:* {start_day}, {data.get("Kiállás időpontja", "").strip()}
*Kiállás helye:* {data.get("Kiállás helye", "").strip()}
*Úticél:* {data.get("Úticél", "").strip()}
*Busz:* {data.get("Rendszám", "").strip()}
*Várható végzés:* {end_date}
*Létszám:* {data.get("UtasLétszám", "").strip()}
*Megrendelő:* {data.get("Megrendelő", "").strip()}
"""

if input_text:
    try:
        adat = parse_row(input_text)
        uzenet = generate_message(adat)
        st.success("🎉 Üzenet legenerálva:")
        st.text_area("Sofőrnek küldendő üzenet:", value=uzenet, height=250)
    except Exception as e:
        st.error(f"Hiba történt: {e}")