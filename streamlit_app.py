def extract_fields(text):
    parts = re.split(r'\s{2,}|\t+', text.strip())

    # Rendszám
    rendszam = next((x for x in parts if re.match(r'^[A-Z]{3}-\d{3}$', x)), 'N/A')

    # Telefonszám
    telefonszam = next((x for x in parts if '+36' in x), 'N/A')

    # Sofőr név a telefonszám előtti két mező alapján (csak ha nem szám)
    if telefonszam in parts:
        idx = parts.index(telefonszam)
        if idx >= 2 and not parts[idx - 1].isdigit():
            sofor_vezeteknev = parts[idx - 2]
            sofor_keresztnev = parts[idx - 1]
            sofor_nev = f"{sofor_vezeteknev} {sofor_keresztnev}"
        else:
            sofor_nev = sofor_keresztnev = 'N/A'
    else:
        sofor_nev = sofor_keresztnev = 'N/A'

    # Dátumok
    datumok = [x for x in parts if re.match(r'^\d{4}\.\d{2}\.\d{2}$', x)]
    if len(datumok) == 1:
        indulas = vegzes = datumok[0]
    elif len(datumok) >= 2:
        indulas = datumok[0]
        vegzes = datumok[1]
    else:
        indulas = vegzes = 'N/A'

    # Időpontok
    idopontok = [x for x in parts if re.match(r'^\d{1,2}:\d{2}$', x)]
    kiallas_ido = idopontok[0] if idopontok else 'N/A'

    # Létszám: az első szám típusú érték, ami nem telefonszám előtt van
    letszam = next((x for x in parts if re.match(r'^\d{1,3}$', x) and x != kiallas_ido.split(":")[0]), 'N/A')

    # Úticél: első cím-szerű szöveg, ami tartalmaz kisbetűt
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