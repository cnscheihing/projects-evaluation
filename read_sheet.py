import pandas as pd

SHEET_ID = "1ZUP4wQa5VLBaBSyNVP77F0uBzfHPDauE4Gp4b623XL0"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

SHEET_IDS = {
    "Datos generales": "2030723865",
    "Internos": "887695939",
    "CP": "1090322878",
    "H": "776766230",
    "Distancias CP-Tribunal": "626115897",
    "Costo CP-Tribunal": "882126144",
    "Viático CP-hospital": "1854938359",
    "Viático CP-tribunal": "1125681942",
    "Tribunal representante": "319525477",
}

CANTIDAD_INTERNOS_30_04_2019 = 1982


# CONJUNTOS
internos = [i for i in range(CANTIDAD_INTERNOS_30_04_2019)]
centros_penitenciarios = []
hospitales = []
tribunales = [
    "T01",
    "T02",
    "T03",
    "T04",
    "T05",
    "T06",
    "T07",
    "T08",
    "T09",
    "T10",
    "T11",
    "T12",
    "T13",
    "T14",
    "T15",
    "T16",
    "T17",
    "T18",
    "T19",
    "T20",
    "T21",
    "T22",
    "T23",
    "T24",
    "T25",
    "T26",
    "T27",
    "T28",
    "T29",
    "T30",
    "T31",
    "T32",
    "T33",
    "T34",
    "T35",
]
segmentos = ["MI", "MC", "HI", "HC"]


p_j_l = {}
d_j_h = {}
m = 1.47
n = 1
mu = 2

#### 2 Viáticos ####
alpha_j_k = (
    {}
)  # 1 si realizar una salida desde el CP j al tribunal k considera un viático al 100%
beta_j_k = (
    {}
)  # 1 si realizar una salida desde el CP j al tribunal k considera un viático al 60%
gamma_j_k = (
    {}
)  # 1 si realizar una salida desde el CP j al tribunal k considera un viático al 40%
eta_j_h = (
    {}
)  # 1 si realizar una salida desde el CP j al hospital h considera un viático al 100%
zeta_j_h = (
    {}
)  # 1 si realizar una salida desde el CP j al hospital h considera un viático al 60%
tau_j_h = (
    {}
)  # 1 si realizar una salida desde el CP j al hospital h considera un viático al 40%
delta = 100  # costo de pagar un viático al 100%
epsilon = 100  # costo de pagar un viático al 60%
phi = 100  # costo de pagar un viático al 40%

#### 3 Costos ####
c_j_k = {}
s_j_h = {}  # costo de realizar una movilización entre el CP j y el hospital h

#### 4  Internos ####
g_i_k = (
    {}
)  # 1 si el interno i tiene asignado el tribunal de justicia k para sus audiencias, 0 en otro caso
b_i_l = {}  # 1 si interno i pertenece al segmento l, 0 en otro caso
v_i = {}  # cantidad de salidas realizadas a tribunales por el interno i en un año
u_i = {}  # cantidad de salidas realizadas a hospitales por el interno i en un año

#### 5 Mantenciones ####
omega_j_k = {}  # Distancia entre CP j y tribunal k
rho_j_h = {}  # Distancia entre CP j y hospital h
lambd = 1  # Cantidad de kilómetros necesarios para mantención
pipi = 1  # Costo de mantención

#### 6 Cierre de Centros Penitenciarios ####
theta_j = {}  # Costo anual de funcionamiento del CP j


def load_cp_h_data():
    df = pd.read_csv(f"{URL}&gid={SHEET_IDS['CP']}")
    records = df.to_dict("records")
    for record in records:
        centros_penitenciarios.append(record["id_CP"])

    df = pd.read_csv(f"{URL}&gid={SHEET_IDS['H']}")
    records = df.to_dict("records")
    for record in records:
        hospitales.append(record["id_hospital"])

    for i in internos:
        g_i_k[i] = {}
        b_i_l[i] = {}
        v_i[i] = 0
        u_i[i] = 0
        for k in tribunales:
            g_i_k[i][k] = 0
        for l in segmentos:
            b_i_l[i][l] = 0
    for j in centros_penitenciarios:
        p_j_l[j] = {}
        d_j_h[j] = {}
        alpha_j_k[j] = {}
        beta_j_k[j] = {}
        gamma_j_k[j] = {}
        eta_j_h[j] = {}
        zeta_j_h[j] = {}
        tau_j_h[j] = {}
        c_j_k[j] = {}
        s_j_h[j] = {}
        omega_j_k[j] = {}
        rho_j_h[j] = {}
        theta_j[j] = 0
        for k in tribunales:
            alpha_j_k[j][k] = 0
            beta_j_k[j][k] = 0
            gamma_j_k[j][k] = 0
            c_j_k[j][k] = 0
            omega_j_k[j][k] = 0
        for h in hospitales:
            d_j_h[j][h] = 0
            eta_j_h[j][h] = 0
            zeta_j_h[j][h] = 0
            tau_j_h[j][h] = 0
            s_j_h[j][h] = 0
            rho_j_h[j][h] = 0
        for l in segmentos:
            p_j_l[j][l] = 0


def read_sheet():
    for sheet in SHEET_IDS:
        df = pd.read_csv(f"{URL}&gid={SHEET_IDS[sheet]}")
        records = df.to_dict("records")
        for record in records:  # cada linea en la hoja
            if sheet == "Datos generales":
                if record["param"] == "m":
                    m = float(record["valor"].replace(",", "."))
                elif record["param"] == "n":
                    n = float(record["valor"])
                elif record["param"] == "mu":
                    mu = float(record["valor"])
                elif record["param"] == "delta":
                    delta = float(record["valor"])
                elif record["param"] == "epsilon":
                    epsilon = float(record["valor"])
                elif record["param"] == "phi":
                    phi = float(record["valor"])
                elif record["param"] == "pi":
                    pipi = float(record["valor"])
                elif record["param"] == "lambda":
                    lambd = float(record["valor"])
            elif sheet == "Internos":
                g_i_k[record["id_interno"]][record["id_tribunal_asignado"]] = 1
                b_i_l[record["id_interno"]][record["id_segmento_asignado"]] = 1
                v_i[record["id_interno"]] = record["v"]
                u_i[record["id_interno"]] = record["u"]
            elif sheet == "CP":
                p_j_l[record["id_CP"]]["HC"] = record["capacidad_segmento_HC"]
                p_j_l[record["id_CP"]]["HI"] = record["capacidad_segmento_HI"]
                p_j_l[record["id_CP"]]["MC"] = record["capacidad_segmento_MC"]
                p_j_l[record["id_CP"]]["MI"] = record["capacidad_segmento_MI"]
                d_j_h[record["id_CP"]][record["id_hospital_asociado"]] = 1
                rho_j_h[record["id_CP"]][record["id_hospital_asociado"]] = float(
                    record["distacia_hospital_asociado"].replace(",", ".")
                )
                s_j_h[record["id_CP"]][record["id_hospital_asociado"]] = float(
                    record["costo_hospital_asociado"].replace(",", ".")
                )
            elif sheet == "Distancias CP-Tribunal":
                for k in tribunales:
                    omega_j_k[record["id_CP/id_tribunal"]][k] = float(
                        str(record[k]).replace(",", ".")
                    )
            elif sheet == "Costo CP-Tribunal":
                for k in tribunales:
                    c_j_k[record["id_CP/id_tribunal"]][k] = float(
                        record[k].replace(",", ".")
                    )
            elif sheet == "Viático CP-hospital":
                for h in hospitales:
                    if record[h] == 10:
                        eta_j_h[record["id_CP/id_hospital"]][h] = 1
                    elif record[h] == 6:
                        zeta_j_h[record["id_CP/id_hospital"]][h] = 1
                    elif record[h] == 4:
                        tau_j_h[record["id_CP/id_hospital"]][h] = 1
            elif sheet == "Viático CP-tribunal":
                for k in tribunales:
                    # print(record)
                    if record[k] == 10:  # TBD
                        alpha_j_k[record["id_CP/id_tribunal"]][k] = 1
                    elif record[k] == 6:
                        beta_j_k[record["id_CP/id_tribunal"]][k] = 1
                    elif record[k] == 4:
                        gamma_j_k[record["id_CP/id_tribunal"]][k] = 1
    return (
        internos,
        centros_penitenciarios,
        hospitales,
        alpha_j_k,
        beta_j_k,
        gamma_j_k,
        eta_j_h,
        zeta_j_h,
        tau_j_h,
        delta,
        epsilon,
        phi,
        c_j_k,
        s_j_h,
        g_i_k,
        b_i_l,
        v_i,
        u_i,
        omega_j_k,
        rho_j_h,
        lambd,
        pipi,
        theta_j,
    )


def build_params():
    load_cp_h_data()
    return read_sheet()


if __name__ == "__main__":
    load_cp_h_data()
    read_sheet()
