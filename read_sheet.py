import pandas as pd
SHEET_ID = '1ZUP4wQa5VLBaBSyNVP77F0uBzfHPDauE4Gp4b623XL0'
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

SHEET_IDS = {
    "Datos generales": "2030723865",
    "Internos": "887695939",
    "CP": "1090322878",
    "Distancias CP-Tribunal": "626115897",
    "Costo CP-Tribunal": "882126144",
    "Viático CP-hospital": "1854938359",
    "Viático CP-tribunal": "1125681942",
    "Tribunal representante": "319525477"
}

def read_sheet():
    for sheet in SHEET_IDS:
        df = pd.read_csv(f"{URL}&gid={SHEET_IDS[sheet]}")
        records = df.to_dict("records")
        for record in records: # cada linea en la hoja
            print(record)



if __name__ == "__main__":
    read_sheet()
