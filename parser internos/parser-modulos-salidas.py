import csv

# Palabras para reconocer si es que el la "Salida Con Retorno" fue por una razon medica
HOSPITALS = ["HOSPITAL", "CESFAM", "CONSULTA", "CONSULTORIO", "SML", "CLINICA",
             "URGENCIA", "POSTA", "MEDICO", "HOSP", "S.A.R", "HOSPITALARIA", "MEDICA", "SAPU"]

# Que validaciones utilizar segun cada archivo
VALIDATIONS = {"hospital": {"hospital": True}, "tribunal": {"location": True}}

# IDs de localidades para tribunales
ID_LOCATIONS = {
    "TALCA": "T10",
    "CAUQUENES": "T32",
    "SAN JAVIER": "T30",
    "CONSTITUCION": "T18",
    "LINARES": "T22",
    "CURICO": "T01",
    "MOLINA": "T07",
    "PARRAL": "T27",
    "CHANCO": "T35",
    "CUREPTO": "T21",
    "LICANTEN": "T09",
    "SAN CLEMENTE": "T10",
    "LONTUE (MOLINA)": "T07"
}

# IDs segmentos
ID_SEGMENTS = {
    ("CONDENADO", "HOMBRE"): "S01",
    ("CONDENADO", "MUJER"): "S02",
    ("IMPUTADO", "HOMBRE"): "S03",
    ("IMPUTADO", "MUJER"): "S04",
}

#
interns = {}


class Intern:

    latest_id = 1

    def update_by_tribunal(self, row):
        self.u += 1
        self.id_tribunal = self.get_tribunal_id(row)

    def get_tribunal_id(self, row):
        location = row["JUZGADO"].split("DE ")[-1]
        return ID_LOCATIONS[location]

    def update_by_hospital(self):
        self.v += 1

    def get_segment(self, row):
        return ID_SEGMENTS[(row["CALIDAD_PROCESAL"], row["SEXO"])] if row["CALIDAD_PROCESAL"] in ["CONDENADO", "IMPUTADO"] else "N/A"

    def __init__(self, row):
        self.u = 0
        self.v = 0
        self.id_tribunal = ""
        self.id_segmento = self.get_segment(row)
        self.id_gendarmeria = row["COD_INT_POB_PENAL"]
        self.id = "I{}".format(self.__class__.latest_id)
        self.__class__.latest_id += 1

    def __repr__(self):
        # return "{}".format(self.__dict__)
        return "{},{},{},{},{}".format(self.id, self.id_tribunal, self.id_segmento, self.u, self.v)


def validate_row(row, date=False, seg=False, location=False, hospital=False):
    # Anio 2019
    if date and row["FECHA_SALIDA"].split(" ")[0].split("-")[-1] != "19":
        return False
    # Segmentacion existe
    if seg and (row["CALIDAD_PROCESAL"], row["SEXO"]) not in ID_SEGMENTS.keys():
        return False
    # Localidad dentro del Maule
    if location and row["JUZGADO"].split("DE ")[-1] not in ID_LOCATIONS.keys():
        return False
    # Salida a hospital
    if hospital:
        medical = False
        for word in HOSPITALS:
            if word in row["MOTIVO_SALIDA"]:
                medical = True
                break
        if not medical:
            return False
    return True


def parse_row(row, type):
    if not row["COD_INT_POB_PENAL"] in interns.keys():
        new_intern = Intern(row)
        if type == "tribunal":
            new_intern.update_by_tribunal(row)
        elif type == "hospital":
            new_intern.update_by_hospital()
        interns[row["COD_INT_POB_PENAL"]] = new_intern
    else:
        if type == "tribunal":
            interns[row["COD_INT_POB_PENAL"]].update_by_tribunal(row)
        elif type == "hospital":
            interns[row["COD_INT_POB_PENAL"]].update_by_hospital()


def get_data(filename, type):
    with open(filename, "r") as file:
        dict_file = csv.DictReader(file, delimiter=";")
        for row in dict_file:
            if validate_row(row, date=True, seg=True, **VALIDATIONS[type]):
                parse_row(row, type)


if __name__ == "__main__":
    get_data("salidas-tribunales.csv", "tribunal")
    get_data("salidas-hospitales.csv", "hospital")
    for ql in interns.values():
        print(ql)
