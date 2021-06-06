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
    ("CONDENADO", "HOMBRE"): "HC",
    ("CONDENADO", "MUJER"): "MC",
    ("IMPUTADO", "HOMBRE"): "HI",
    ("IMPUTADO", "MUJER"): "MI",
}

#
interns = {}


CP_SEGMENTS = {
    "C.C.P. DE TALCA": {	"HC": 435,
                         "HI": 149,
                         "MC": 0,
                         "MI": 0},
    "C.P.F. DE TALCA": {	"HC": 0,
                         "HI": 0,
                         "MC": 54,
                         "MI": 36},
    "C.C.P. DE LINARES": {	"HC": 243,
                           "HI": 79,
                           "MC": 0,
                           "MI": 0},
    "C.C.P. DE CURICO": {	"HC": 334,
                          "HI": 130,
                          "MC": 0,
                          "MI": 0},
    "C.C.P. DE CAUQUENES": {	"HC": 256,
                             "HI": 56,
                             "MC": 27,
                             "MI": 13},
    "C.D.P. DE CHANCO": {	"HC": 14,
                          "HI": 0,
                          "MC": 0,
                          "MI": 0},
    "C.C.P. DE PARRAL": {	"HC": 51,
                          "HI": 36,
                          "MC": 6,
                          "MI": 1},
    "C.C.P. DE MOLINA": {	"HC": 60,
                          "HI": 2,
                          "MC": 0,
                          "MI": 0},
    "C.C.P. DE SAN JAVIER": {"HC": 0,
                             "HI": 0,
                             "MC": 0,
                             "MI": 0},
    "C.D.P. DE CUREPTO": {	"HC": 0,
                           "HI": 0,
                           "MC": 0,
                           "MI": 0},
    "C.D.P. DE CONSTITUCIÓN": {	"HC": 0,
                                "HI": 0,
                                "MC": 0,
                                "MI": 0},

}

CP_tribunales = {
    "C.C.P. DE TALCA": {	"80": "T10",
                         "10-1": "T30",
                         "10-2": "T22"},
    "C.P.F. DE TALCA": {	"80": "T10",
                         "10-1": "T30",
                         "10-2": "T07"},
    "C.C.P. DE LINARES": {	"80": "T22",
                           "10-1": "T30",
                           "10-2": "T27"},
    "C.C.P. DE CURICO": {	"80": "T01",
                          "10-1": "T07",
                          "10-2": "T10"},
    "C.C.P. DE CAUQUENES": {	"80": "T32",
                             "10-1": "T35",
                             "10-2": "T27"},
    "C.D.P. DE CHANCO": {	"80": "T35",
                          "10-1": "T32",
                          "10-2": "T18"},
    "C.C.P. DE PARRAL": {	"80": "T27",
                          "10-1": "T22",
                          "10-2": "T32"},
    "C.C.P. DE MOLINA": {	"80": "T07",
                          "10-1": "T01",
                          "10-2": "T10"},
    "C.C.P. DE SAN JAVIER": {"80": "T30",
                             "10-1": "T10",
                             "10-2": "T22"},
    "C.D.P. DE CUREPTO": {	"80": "T21",
                           "10-1": "T09",
                           "10-2": "T18"},
    "C.D.P. DE CONSTITUCIÓN": {	"80": "T18",
                                "10-1": "T35",
                                "10-2": "T09"},
}

CP_names = {
    "C.C.P. DE TALCA": 	"CP02",
    "C.P.F. DE TALCA": 	"CP03",
    "C.C.P. DE LINARES": 	"CP04",
    "C.C.P. DE CURICO": 	"CP05",
    "C.C.P. DE CAUQUENES": 	"CP06",
    "C.D.P. DE CHANCO": 	"CP07",
    "C.C.P. DE PARRAL": 	"CP08",
    "C.C.P. DE MOLINA": 	"CP09",
    "C.C.P. DE SAN JAVIER": 	"CP10",
    "C.D.P. DE CUREPTO": 	"CP11",
    "C.D.P. DE CONSTITUCIÓN": 	"CP12",
}


class Intern:

    latest_id = 0

    def update_by_tribunal(self, row):
        self.u += 1
        self.id_tribunal = self.get_tribunal_id(row)

    def get_tribunal_id(self, row):
        location = row["JUZGADO"].split("DE ")[-1]
        return ID_LOCATIONS[location]

    def update_by_hospital(self):
        self.v += 1

    def update_dummy(self):
        self.w += 1

    def get_segment(self, row):
        return ID_SEGMENTS[(row["CALIDAD_PROCESAL"], row["SEXO"])] if row["CALIDAD_PROCESAL"] in ["CONDENADO", "IMPUTADO"] else "N/A"

    def __init__(self, row):
        self.u = 0
        self.v = 0
        self.w = 0
        self.id_tribunal = ""
        self.id_segmento = self.get_segment(row)
        self.id_gendarmeria = row["COD_INT_POB_PENAL"] if row["COD_INT_POB_PENAL"] else ""
        self.current_cp = CP_names[row["EP"]]
        self.id = self.__class__.latest_id
        self.__class__.latest_id += 1
        CP_SEGMENTS[row["EP"]][self.id_segmento] -= 1

    def __repr__(self):
        # return "{}".format(self.__dict__)
        return "{},{},{},{},{},{},{}".format(self.id, self.id_tribunal, self.id_segmento, self.u, self.v, self.w, self.current_cp)


def validate_row(row, date=False, seg=False, location=False, hospital=False):
    # Anio 2019
    if date and row["FECHA_SALIDA"].split(" ")[0].split("-")[-1] != "19":
        return False
    # Mes abril
    if date and row["FECHA_SALIDA"].split(" ")[0].split("-")[-2] != "04":
        return False
    # Segmentacion existe
    if seg and (row["CALIDAD_PROCESAL"], row["SEXO"]) not in ID_SEGMENTS.keys():
        return False
    # Localidad dentro del Maule
    if location and row["JUZGADO"].split("DE ")[-1] not in ID_LOCATIONS.keys():
        return False
    # No incluir CET
    if "C.E.T." in row["EP"]:
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

# GENERACION DUMMIES


def generate_dummies():
    SEGMENTS_BY_ID = {seg_id: seg_value for seg_value,
                      seg_id in ID_SEGMENTS.items()}
    for cp, cp_capacities in CP_SEGMENTS.items():  # cp_capacities = {}
        for segment in cp_capacities.keys():
            total = cp_capacities[segment]
            while cp_capacities[segment] > 0:
                percentil = cp_capacities[segment]/total
                assigned_tribunal = set_closest_tribunal_dummy(cp, percentil)
                new_dummy_intern = Intern(
                    {"EP": cp, "CALIDAD_PROCESAL": SEGMENTS_BY_ID[segment][0], "SEXO": SEGMENTS_BY_ID[segment][1], "COD_INT_POB_PENAL": ""})
                new_dummy_intern.update_dummy()
                new_dummy_intern.id_tribunal = assigned_tribunal
                interns[new_dummy_intern.id] = new_dummy_intern


def set_closest_tribunal_dummy(CP, percentil):
    if percentil > 0.2:
        return CP_tribunales[CP]["80"]
    elif percentil > 0.1:
        return CP_tribunales[CP]["10-1"]
    else:
        return CP_tribunales[CP]["10-2"]


if __name__ == "__main__":
    # print(CP_SEGMENTS)
    get_data("salidas-tribunales.csv", "tribunal")
    get_data("salidas-hospitales.csv", "hospital")
    # print(CP_SEGMENTS)
    generate_dummies()
    for ql in interns.values():
        print(ql)
    # print(CP_SEGMENTS)
