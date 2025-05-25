def extract_fields(text):
    import re

    parts = re.split(r'\s{2,}|\t+', text.strip())

    # Telefonszám
    telefonszam = next((x for x in parts if '+36' in x), 'N/A')

    # Sofőr név
    if telefonszam in parts:
        idx = parts.index(telefonszam)
        if idx >= 2 and not parts[idx - 1].isdigit():
            sofor_vezeteknev = parts[idx - 2]
            sofor_keresztnev = parts[idx - 1]
            sofor_nev = f"{sofor_vezeteknev} {sofor_keresztnev}"
        else:
            sofor_keresztnev = sofor_nev = 'N/A'
    else:
        sofor_keresztnev = sofor_nev = 'N/A'

    # Dátumok
    datumok = [x for x in parts if re.match(r'^\d{4}\.\d{2}\.\d{2}$', x)]
    indulas = datumok[0] if len(datumok) > 0 else 'N/A'
    vegzes = datumok[1] if len(datumok) > 1 else indulas

    # Időpontok
    idopontok = [x for x in parts if re.match(r'^\d{1,2}:\d{2}$', x)]
    kiallas_ido = idopontok[0] if idopontok else 'N/A'

    # Rendszám
    rendszam = next((x for x in parts if re.match(r'^[A-Z]{3}-\d{3}$', x)), 'N/A')

    # Létszám (az első szám, ami nem időpont és nem dátum)
    letszam = next((x for x in parts if re.match(r'^\d+$', x)), 'N/A')

    # Úticél (legelső cím-szerű, hosszabb mező, amin van kisbetű)
    uticel = next((x for x in parts if len(x) > 6 and re.search(r'[a-záéíóöőúüű]', x, re.IGNORECASE)), 'N/A')

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