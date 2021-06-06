from gurobipy import GRB, Model, quicksum
import pandas as pd
from read_sheet import build_params


# MODELO
model = Model(
    "Optimizacion de la ubicación de cada interno en la región del Maule considerando el centro penitenciario La Laguna"
)


# DATOS PARA GENERAR PARAMETROS DEL MODELO
BIG_M = 9999999999999


# CONJUNTOS
# internos = []
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


# PARAMETROS DEL MODELO

#### 1 Generales Sistema Penitenciario ####
p_j_l = 100  # capacidad del CP j para el segmento l
d_j_h = 100  # 1 si hospital h está asociado al CP j, 0 en otro caso
m = 1.47  # capacidad promedio de vehículo en salida a tribunal
n = 1  # capacidad promedio de vehículo en salida a hospital
mu = 2  # tasa necesaria de gendarmes necesarios en cada salida

#### 2 Viáticos ####
alpha_j_k = 100  # 1 si realizar una salida desde el CP j al tribunal k considera un viático al 100%
beta_j_k = 100  # 1 si realizar una salida desde el CP j al tribunal k considera un viático al 60%
gamma_j_k = 100  # 1 si realizar una salida desde el CP j al tribunal k considera un viático al 40%
eta_j_h = 100  # 1 si realizar una salida desde el CP j al hospital h considera un viático al 100%
zeta_j_h = 100  # 1 si realizar una salida desde el CP j al hospital h considera un viático al 60%
tau_j_h = 100  # 1 si realizar una salida desde el CP j al hospital h considera un viático al 40%
delta = 100  # costo de pagar un viático al 100%
epsilon = 100  # costo de pagar un viático al 60%
phi = 100  # costo de pagar un viático al 40%

#### 3 Costos ####
c_j_k = (
    100  # costo de realizar una movilización entre el CP j y el tribunal de justicia k
)
s_j_h = 100  # costo de realizar una movilización entre el CP j y el hospital h

#### 4  Internos ####
g_i_k = 1  # 1 si el interno i tiene asignado el tribunal de justicia k para sus audiencias, 0 en otro caso
b_i_l = 1  # 1 si interno i pertenece al segmento l, 0 en otro caso
v_i = 100  # cantidad de salidas realizadas a tribunales por el interno i en un año
u_i = 100  # cantidad de salidas realizadas a hospitales por el interno i en un año
w_i = 1  # cantidad salidas ficticias realizadas a tribunales i en un año
sigma = 0.01  # factor de ficción

#### 5 Mantenciones ####
omega_j_k = 1  # Distancia entre CP j y tribunal k
rho_j_h = 1  # Distancia entre CP j y hospital h
lambd = 1  # Cantidad de kilómetros necesarios para mantención
pipi = 1  # Costo de mantención

#### 6 Cierre de Centros Penitenciarios ####
theta_j = 1  # Costo anual de funcionamiento del CP j


(
    internos,
    centros_penitenciarios,
    hospitales,
    p_j_l,
    d_j_h,
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
    w_i,
    omega_j_k,
    rho_j_h,
    lambd,
    pipi,
    theta_j,
) = build_params()

# print(c_j_k, g_i_k, w_i, sep="\n")


# print(centros_penitenciarios)
# VARIABLES
x = model.addVars(
    internos, centros_penitenciarios, vtype=GRB.BINARY, name="x"
)  # 1 si el interno i vive en el CP j, 0 en otro caso

y = model.addVar(vtype=GRB.CONTINUOUS, name="y")  # cantidad de custodios necesarios en el sistema

# FUNCION OBJETIVO
obj = (
    quicksum(
        quicksum(
            quicksum(
                c_j_k[j][k] * x[(i, j)] * g_i_k[i][k] * v_i[i] / m for i in internos
            )
            for k in tribunales
        )
        for j in centros_penitenciarios
    )
    + quicksum(
        quicksum(
            quicksum(
                s_j_h[j][h] * x[(i, j)] * d_j_h[j][h] * u_i[i] / n for h in hospitales
            )
            for j in centros_penitenciarios
        )
        for i in internos
    )
    + quicksum(
        quicksum(
            quicksum(
                c_j_k[j][k] * x[(i, j)] * g_i_k[i][k] * sigma * w_i[i]
                for k in tribunales
            )
            for i in internos
        )
        for j in centros_penitenciarios
    )
    + quicksum(
        quicksum(
            quicksum(
                x[(i, j)]
                * g_i_k[i][k]
                * v_i[i]
                / m
                * (
                    alpha_j_k[j][k] * delta
                    + beta_j_k[j][k] * epsilon
                    + gamma_j_k[j][k] * phi
                )
                * mu
                for k in tribunales
            )
            for j in centros_penitenciarios
        )
        for i in internos
    )
    + quicksum(
        quicksum(
            quicksum(
                x[(i, j)]
                * d_j_h[j][h]
                * u_i[i]
                / n
                * (
                    eta_j_h[j][h] * delta
                    + zeta_j_h[j][h] * epsilon
                    + tau_j_h[j][h] * phi
                )
                * mu
                for h in hospitales
            )
            for j in centros_penitenciarios
        )
        for i in internos
    )
    + quicksum(
        quicksum(
            quicksum(
                x[(i, j)]
                * g_i_k[i][k]
                * sigma
                * w_i[i]
                * (
                    alpha_j_k[j][k] * delta
                    + beta_j_k[j][k] * epsilon
                    + gamma_j_k[j][k] * phi
                )
                * mu
                for k in tribunales
            )
            for j in centros_penitenciarios
        )
        for i in internos
    )
    + quicksum(
        quicksum(
            quicksum(
                x[(i, j)] * g_i_k[i][k] * v_i[i] / m * omega_j_k[j][k] / lambd * pipi
                for k in tribunales
            )
            for j in centros_penitenciarios
        )
        for i in internos
    )
    + quicksum(
        quicksum(
            quicksum(
                x[(i, j)] * d_j_h[j][h] * u_i[i] / n * rho_j_h[j][h] / lambd * pipi
                for h in hospitales
            )
            for j in centros_penitenciarios
        )
        for i in internos
    )
    + quicksum(
        quicksum(
            quicksum(
                x[(i, j)]
                * g_i_k[i][k]
                * sigma
                * w_i[i]
                * omega_j_k[j][k]
                / lambd
                * pipi
                for k in tribunales
            )
            for j in centros_penitenciarios
        )
        for i in internos
    )
)

model.setObjective(obj, GRB.MINIMIZE)

### SUPUESTOS
# proporción de capacidad por segmento de acuerdo a la proporción de los datos Reporte diario_31012019, donde si en CP0X la relación HC/HI = 0.8, esta se mantiene en el modelo.


# RESTRICCIONES



# R1: La capacidad de cada CP no debe ser excedida (para cada segmento)
model.addConstrs(
    (
        quicksum(x[(i, j)] * b_i_l[i][l] for i in internos) <= p_j_l[j][l]
        for l in segmentos
        for j in centros_penitenciarios
    ),
    name="R1",
)
# R2: Desocupación de centros penitenciarios en Talca:
model.addConstrs(
    (
        quicksum(x[(i, j)] * b_i_l[i][l] for i in internos) == 0
        for j in ["CP02", "CP03"]
        for l in segmentos
    ),
    name="R2",
)

model.addConstrs(
    (
        quicksum(x[(i, j)] for j in centros_penitenciarios) == 1
        for i in internos
    ),
    name="R3",
)


# R3: Cantidad de gendarmes necesarios:
model.addConstr(
    y == mu * quicksum((v_i[i] / m) + (u_i[i] / n) for i in internos), name="R4",
)


# RXX: Naturaleza de las variables.
model.addConstr(y >= 0, name="R5")

#######################################
###
###
###
### LISTO HASTA ACA
###
###
###
###
########################################


# Ejecución de la optimización
model.optimize()

model.printAttr("x")
model.printAttr("y")

# matrix = []

# sum_x = 0

# for i in internos:
#     matrix.append([i])
#     for j in d_i_j[i]:
#         if d_i_j[i][j] == 1:
#             matrix[-1].append(j)
#     for l in b_i_l[i]:
#         if b_i_l[i][l] == 1:
#             matrix[-1].append(l)
#     matrix[-1].append(x[i].x)
#     for j in d_i_j[i]:
#         matrix[-1].append(d_i_j[i][j])
#     sum_x += x[i].x
# matrix.append(["INICIO"])
# matrix[-1].append("")
# matrix[-1].append("")
# matrix[-1].append(0)
# for j in centros_penitenciarios:
#     suma = 0
#     for i in internos:
#         if d_i_j[i][j] == 1:
#             suma += 1
#     matrix[-1].append(suma)

# matrix.append(["FINAL"])
# matrix[-1].append("")
# matrix[-1].append("")
# matrix[-1].append(sum_x)
# for j in centros_penitenciarios:
#     suma = 0
#     for i in internos:
#         if d_i_j[i][j] == 1 and abs(x[i].x) == 0:
#             suma += 1
#     matrix[-1].append(suma)


# matrix = pd.DataFrame(matrix)

# # get column names
# columns = [
#     "ID",
#     "CP",
#     "SEG",
#     "Traslado",
#     "d_i2",
#     "d_i3",
#     "d_i4",
#     "d_i5",
#     "d_i6",
#     "d_i7",
#     "d_i8",
#     "d_i9",
#     "d_i10",
#     "d_i11",
#     "d_i12",
# ]
# matrix.columns = columns
# matrix.to_csv("matrix_result.csv", index=False)
