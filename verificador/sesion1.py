"""Ejercicios de la Sesión 1: variables, operaciones, NumPy y unidades."""

import os

from .nucleo import (Incorrecto, Sesion, ____, comparar_cantidad, comparar_numero, obtener)

sesion = Sesion("Sesión 1", "S1")
progreso = sesion.progreso
iniciar_registro = sesion.iniciar_registro

NA = 6.022e23          # mol⁻¹
MM_HCN = 27.03         # g/mol
MM_NACL = 58.44        # g/mol


# --- Ejercicio 1 -------------------------------------------------------------

def _ej1(ns):
    comparar_numero("x", obtener(ns, "x"), (8 * 10 + 2 * 11) / (20 - 4))


ej1 = sesion.agregar(
    "ej1", "Jerarquía de operaciones", _ej1,
    pista="El numerador y el denominador completos deben ir entre paréntesis: "
          "`(a + b) / (c - d)`. La multiplicación se escribe con `*`.",
    solucion="""
x = (8 * 10 + 2 * 11) / (20 - 4)
print(f"x = {x}")
""")


# --- Ejercicio 2 -------------------------------------------------------------

def _ej2a(ns):
    comparar_numero("masa_molar_hcn", obtener(ns, "masa_molar_hcn"), MM_HCN, rel=5e-3, unidades="g/mol")
    comparar_numero("moles_hcn", obtener(ns, "moles_hcn"), 10.0 / MM_HCN, rel=5e-3, unidades="mol")


ej2a = sesion.agregar(
    "ej2a", "Moles de HCN", _ej2a,
    pista="La masa molar del HCN es la suma de las masas atómicas de H, C y N "
          "(≈ 27.03 g/mol). Luego, n = m / M.",
    solucion="""
masa_hcn = 10.0          # g
masa_molar_hcn = 27.03   # g/mol  (1.008 + 12.011 + 14.007)

moles_hcn = masa_hcn / masa_molar_hcn
print(f"Moles de HCN: {moles_hcn:.4f} mol")
""")


def _ej2b(ns):
    comparar_numero("moleculas_hcn", obtener(ns, "moleculas_hcn"),
                    10.0 / MM_HCN * NA, rel=5e-3)


ej2b = sesion.agregar(
    "ej2b", "Moléculas de HCN", _ej2b,
    pista="Multiplica la cantidad de sustancia (`moles_hcn`) por la constante de "
          "Avogadro. En Python, 6.022 × 10²³ se escribe `6.022e23`.",
    solucion="""
constante_avogadro = 6.022e23   # mol⁻¹

moleculas_hcn = moles_hcn * constante_avogadro
print(f"Moléculas de HCN: {moleculas_hcn:.3e}")
""")


# --- Ejercicio 3: NumPy, matriz de rotación -----------------------------------------

def _ej3(ns):
    import numpy as np
    R = obtener(ns, "R")
    v_rotado = obtener(ns, "v_rotado")
    esperada = np.array([[0.0, -1.0], [1.0, 0.0]])
    if np.shape(R) != (2, 2):
        raise Incorrecto("`R` debe ser una matriz de 2 × 2 creada con `np.array`.")
    if np.allclose(R, [[np.cos(90), -np.sin(90)], [np.sin(90), np.cos(90)]]):
        raise Incorrecto("Usaste 90 en lugar de `theta`: `np.cos` y `np.sin` trabajan en "
                         "radianes, por eso convertimos con `np.radians(90)`.")
    if not np.allclose(R, esperada, atol=1e-9):
        raise Incorrecto("`R` no es la matriz de rotación de 90°. Revisa el orden y los signos: "
                         "[[cos θ, −sen θ], [sen θ, cos θ]].")
    if np.shape(v_rotado) != (2,) or not np.allclose(v_rotado, [-4.0, 3.0], atol=1e-9):
        raise Incorrecto("`v_rotado` no es correcto. El producto matriz-vector se escribe "
                         "`R @ v`; `R * v` multiplica elemento a elemento.")
    return "El vector (3, 4) rotado 90° es (−4, 3): conserva su longitud de 5."


ej3 = sesion.agregar(
    "ej3", "Rotación de un vector", _ej3,
    pista="`theta` ya está en radianes: usa `np.cos(theta)` y `np.sin(theta)`. El producto "
          "matriz-vector es `R @ v`.",
    solucion="""
theta = np.radians(90)
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])
v = np.array([3, 4])
v_rotado = R @ v
print(v_rotado)
""")


# --- Ejercicio 4: NumPy, regla de Cramer -------------------------------------------

def _ej4(ns):
    comparar_numero("delta", obtener(ns, "delta"), -11.0)
    for nombre, esperado in (("x", 2.0), ("y", 3.0)):
        comparar_numero(nombre, obtener(ns, nombre), esperado)
    return "x = 2 y y = 3, igual que con `np.linalg.solve`."


ej4 = sesion.agregar(
    "ej4", "Regla de Cramer", _ej4,
    pista="Δ es `np.linalg.det(A)`. Para Δy copia `A` y sustituye su **segunda** columna por b: "
          "`A_y[:, 1] = b`. Después, x = Δx / Δ y y = Δy / Δ.",
    solucion="""
A = np.array([[3, 2], [4, -1]], dtype=float)
b = np.array([12, 5], dtype=float)

delta = np.linalg.det(A)

A_x = A.copy()
A_x[:, 0] = b
A_y = A.copy()
A_y[:, 1] = b

x = np.linalg.det(A_x) / delta
y = np.linalg.det(A_y) / delta
print(f"x = {x:.4f}, y = {y:.4f}")
print("Con np.linalg.solve:", np.linalg.solve(A, b))
""")


# --- Ejercicio 5: unidades con pint -------------------------------------------------

R_ATM_EXACTA = 0.082057   # atm·L/(mol·K)


def _ej5a(ns):
    presion = obtener(ns, "presion")
    esperado = 0.250 * R_ATM_EXACTA * 298.15 / 0.500
    comparar_cantidad("presion", presion, esperado, "atm", rel=2e-3)
    presion_kpa = obtener(ns, "presion_kpa")
    comparar_cantidad("presion_kpa", presion_kpa, esperado * 101.325, "kPa", rel=2e-3)
    if f"{presion_kpa.units:~}" != "kPa":
        raise Incorrecto("`presion_kpa` tiene el valor correcto, pero exprésala en kPa con "
                         '`presion.to("kPa")`.')
    return f"P = {esperado:.2f} atm. pint convirtió los mL y los °C por ti."


ej5a = sesion.agregar(
    "ej5a", "Gas ideal con unidades", _ej5a,
    pista="Multiplica cada número por su unidad (`500 * ureg.mL`). La temperatura en °C debe "
          'convertirse antes de multiplicar: `T.to("K")`. Al final, `.to("atm")` expresa el '
          "resultado en atmósferas.",
    solucion="""
n = 0.250 * ureg.mol
T = Q_(25.0, ureg.degC)
V = 500 * ureg.mL
R = 0.082057 * ureg("L * atm / (mol * K)")

presion = (n * R * T.to("K") / V).to("atm")
presion_kpa = presion.to("kPa")
print(f"P = {presion:.3f~P} = {presion_kpa:.1f~P}")
""")


def _ej5b(ns):
    molaridad = obtener(ns, "molaridad")
    comparar_cantidad("molaridad", molaridad, 2.50 / MM_NACL / 0.250, "mol/L", rel=2e-3)
    return "Aunque el volumen estaba en mL, las unidades cuadran solas."


ej5b = sesion.agregar(
    "ej5b", "Molaridad con unidades", _ej5b,
    pista='Divide la masa entre la masa molar y entre el volumen, todos con unidades, y '
          'termina con `.to("mol/L")`. No conviertas los mL a mano.',
    solucion="""
masa = 2.50 * ureg.g
masa_molar = 58.44 * ureg("g/mol")
volumen = 250 * ureg.mL

molaridad = (masa / masa_molar / volumen).to("mol/L")
print(f"c = {molaridad:.4f~P}")
""")


# --- Autoevaluación -----------------------------------------------------------

def _auto1(ns):
    comparar_numero("T_K", obtener(ns, "T_K"), 300 + 273.15, unidades="K")


auto1 = sesion.agregar(
    "auto1", "Conversión de temperatura", _auto1,
    pista="Suma 273.15 a la temperatura en grados Celsius.",
    solucion="""
T_C = 300
T_K = T_C + 273.15
print(f"T = {T_K} K")
""")


def _auto2(ns):
    comparar_numero("C_2", obtener(ns, "C_2"), 0.5 * 10.0 / 50.0, unidades="mol/L")


auto2 = sesion.agregar(
    "auto2", "Dilución de NaOH", _auto2,
    pista="Despeja C₂ de C₁V₁ = C₂V₂. No necesitas convertir mL a L porque las "
          "unidades de volumen se cancelan.",
    solucion="""
C_1 = 0.5    # mol/L
V_1 = 10.0   # mL
V_2 = 50.0   # mL

C_2 = C_1 * V_1 / V_2
print(f"C₂ = {C_2} mol/L")
""")


def _auto3(ns):
    distancia_km = 384_400
    pasos = distancia_km * 1000 * 100 / 70
    horas = distancia_km / 5
    energia = horas * 240
    comparar_numero("numero_pasos", obtener(ns, "numero_pasos"), pasos, rel=5e-3)
    comparar_numero("tiempo_h", obtener(ns, "tiempo_h"), horas, rel=5e-3, unidades="hour")
    comparar_numero("energia_kcal", obtener(ns, "energia_kcal"), energia, rel=5e-3, unidades="kcal")
    comparar_numero("costo_por_paso", obtener(ns, "costo_por_paso"), energia / pasos, rel=5e-3)


auto3 = sesion.agregar(
    "auto3", "Caminata hasta la Luna", _auto3,
    pista="Convierte la distancia a centímetros (1 km = 100 000 cm) antes de dividir "
          "entre la longitud del paso. El tiempo es distancia / rapidez y la energía "
          "es tiempo × 240 kcal/h.",
    solucion="""
distancia_km = 384_400
paso_cm = 70
rapidez_km_h = 5.0
gasto_kcal_h = 240

numero_pasos = distancia_km * 1000 * 100 / paso_cm
tiempo_h = distancia_km / rapidez_km_h
energia_kcal = tiempo_h * gasto_kcal_h
costo_por_paso = energia_kcal / numero_pasos

print(f"Pasos: {numero_pasos:.3e}")
print(f"Tiempo: {tiempo_h:.0f} h")
print(f"Energía: {energia_kcal:.3e} kcal")
print(f"Costo por paso: {costo_por_paso:.4f} kcal/paso")
""")


def _auto4(ns):
    import numpy as np
    temperaturas = obtener(ns, "temperaturas_K")
    esperado = np.array([-78.5, 0.0, 25.0, 37.0, 100.0]) + 273.15
    if np.shape(temperaturas) != esperado.shape:
        raise Incorrecto("`temperaturas_K` debe ser un arreglo con las 5 temperaturas.")
    if not np.allclose(temperaturas, esperado):
        raise Incorrecto("`temperaturas_K` no es correcto: suma 273.15 al arreglo completo.")


auto4 = sesion.agregar(
    "auto4", "Conversión de varias temperaturas", _auto4,
    pista="Con un arreglo de NumPy, `temperaturas_C + 273.15` suma 273.15 a todos los "
          "elementos a la vez.",
    solucion="""
temperaturas_C = np.array([-78.5, 0.0, 25.0, 37.0, 100.0])
temperaturas_K = temperaturas_C + 273.15
print(temperaturas_K)
""")


def _auto5(ns):
    import numpy as np
    T = np.array([298.15, 500.0, 750.0, 1000.0, 1250.0])
    delta_g = obtener(ns, "delta_g")
    esperado = 206.1 - T * 215 / 1000
    if np.shape(delta_g) != esperado.shape:
        raise Incorrecto("`delta_g` debe ser un arreglo con un valor por temperatura.")
    if np.allclose(delta_g, 206.1 - T * 215):
        raise Incorrecto("ΔS está en J/(mol·K) y ΔH en kJ/mol: divide ΔS entre 1000.")
    if not np.allclose(delta_g, esperado, rtol=1e-3):
        raise Incorrecto("`delta_g` no es correcto. Usa ΔG = ΔH − T·ΔS con el arreglo `T`.")
    comparar_numero("T_inversion", obtener(ns, "T_inversion"), 206.1 / 0.215, rel=5e-3,
                    unidades="K")
    return "ΔG cambia de signo cerca de 959 K: a 1000 y 1250 K la reacción ya es espontánea."


auto5 = sesion.agregar(
    "auto5", "Energía libre a varias temperaturas", _auto5,
    pista="Convierte ΔS a kJ/(mol·K) dividiendo entre 1000. Con el arreglo `T`, la expresión "
          "`delta_h - T * delta_s` calcula ΔG para todas las temperaturas. Para "
          "`T_inversion`, iguala ΔG = 0: T = ΔH / ΔS.",
    solucion="""
delta_h = 206.1                 # kJ/mol
delta_s = 215 / 1000            # kJ/(mol·K)
T = np.array([298.15, 500.0, 750.0, 1000.0, 1250.0])   # K

delta_g = delta_h - T * delta_s
print(delta_g.round(1))

T_inversion = delta_h / delta_s
print(f"ΔG = 0 a {T_inversion:.1f} K")
""")


# Ejercicios adicionales del equipo docente (contenido_extra/sesion1/)
globals().update(sesion.cargar_adicionales(
    os.path.join(os.path.dirname(__file__), "adicionales_sesion1.json")))

__all__ = ["____", "progreso", "iniciar_registro"] + [e.clave for e in sesion.ejercicios]
sesion.bienvenida()
