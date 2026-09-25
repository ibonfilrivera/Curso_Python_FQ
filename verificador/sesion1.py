"""Ejercicios de la Sesión 1: variables, operaciones, condicionales y funciones."""

from .nucleo import (Sesion, ____, comparar_numero, normalizar_texto,
                     obtener, obtener_funcion, probar_funcion)

sesion = Sesion("Sesión 1", "S1")
progreso = sesion.progreso
iniciar_registro = sesion.iniciar_registro

NA = 6.022e23          # mol⁻¹
MM_HCN = 27.03         # g/mol
MM_AGUA = 18.015       # g/mol
R_ATM = 0.0821         # atm·L/(mol·K)


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
    comparar_numero("masa_molar_hcn", obtener(ns, "masa_molar_hcn"), MM_HCN, rel=5e-3)
    comparar_numero("moles_hcn", obtener(ns, "moles_hcn"), 10.0 / MM_HCN, rel=5e-3)


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


# --- Ejercicio 3 -------------------------------------------------------------

def _mismo_enlace(obtenido, esperado):
    if not isinstance(obtenido, str):
        return False
    texto = normalizar_texto(obtenido)
    if texto.startswith("enlace "):
        texto = texto[len("enlace "):]
    return texto == normalizar_texto(esperado)


def _ej3(ns):
    funcion = obtener_funcion(ns, "clasificar_enlace")
    casos = [
        ((0.0,), {}, "covalente no polar"),
        ((0.35,), {}, "covalente no polar"),
        ((0.5,), {}, "covalente polar"),
        ((1.2,), {}, "covalente polar"),
        ((1.7,), {}, "iónico"),
        ((2.1,), {}, "iónico"),
    ]
    probar_funcion("clasificar_enlace", funcion, casos, comparar=_mismo_enlace)
    return "Tu función clasifica correctamente todos los casos, incluidos los límites 0.5 y 1.7."


ej3 = sesion.agregar(
    "ej3", "Clasificación de enlaces", _ej3,
    pista="Usa `if`, `elif` y `else` dentro de la función y devuelve el texto con "
          "`return`. Cuida los límites: 0.5 ya es *covalente polar* y 1.7 ya es *iónico*.",
    solucion="""
def clasificar_enlace(delta_chi):
    if delta_chi < 0.5:
        return "covalente no polar"
    elif delta_chi < 1.7:
        return "covalente polar"
    else:
        return "iónico"

print("Na–Cl:", clasificar_enlace(abs(chi_Na - chi_Cl)))
""")


# --- Ejercicio 4 -------------------------------------------------------------

def _ej4(ns):
    n_agua = obtener(ns, "n_agua")
    comparar_numero("n_agua", n_agua, 50.0 / MM_AGUA, rel=5e-3)
    funcion = obtener_funcion(ns, "calcular_temperatura")
    casos = [
        ((1.0, 22.4, 1.0), {}, 1.0 * 22.4 / (1.0 * R_ATM)),
        ((3.0, 20.0, 2.0), {}, 3.0 * 20.0 / (2.0 * R_ATM)),
        ((6.3, 1.2, 0.5), {}, 6.3 * 1.2 / (0.5 * R_ATM)),
    ]
    probar_funcion("calcular_temperatura", funcion, casos,
                   comparar=lambda o, e: abs(o - e) / e < 2e-3)
    n = 50.0 / MM_AGUA
    comparar_numero("T1", obtener(ns, "T1"), 3.0 * 20.0 / (n * R_ATM), rel=5e-3)
    comparar_numero("T2", obtener(ns, "T2"), 6.3 * 1.2 / (n * R_ATM), rel=5e-3)


ej4 = sesion.agregar(
    "ej4", "Temperatura de un gas ideal", _ej4,
    pista="Despeja T de PV = nRT: T = PV / (nR). Calcula primero `n_agua` a partir de "
          "50.0 g de agua (M ≈ 18.015 g/mol) y luego llama a tu función dos veces.",
    solucion="""
m_agua = 50.0      # g
MM_agua = 18.015   # g/mol
n_agua = m_agua / MM_agua

def calcular_temperatura(P, V, n, R=0.0821):
    return (P * V) / (n * R)

T1 = calcular_temperatura(P=3.0, V=20.0, n=n_agua)
T2 = calcular_temperatura(P=6.3, V=1.2, n=n_agua)
print(f"T1 = {T1:.2f} K, T2 = {T2:.2f} K")
""")


# --- Autoevaluación -----------------------------------------------------------

def _auto1(ns):
    comparar_numero("T_K", obtener(ns, "T_K"), 300 + 273.15)


auto1 = sesion.agregar(
    "auto1", "Conversión de temperatura", _auto1,
    pista="Suma 273.15 a la temperatura en grados Celsius.",
    solucion="""
T_C = 300
T_K = T_C + 273.15
print(f"T = {T_K} K")
""")


def _auto2(ns):
    comparar_numero("C_2", obtener(ns, "C_2"), 0.5 * 10.0 / 50.0)


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
    comparar_numero("tiempo_h", obtener(ns, "tiempo_h"), horas, rel=5e-3)
    comparar_numero("energia_kcal", obtener(ns, "energia_kcal"), energia, rel=5e-3)
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
    funcion = obtener_funcion(ns, "formula_gauss")
    casos = [((n,), {}, n * (n + 1) // 2) for n in (1, 10, 100, 1000)]
    probar_funcion("formula_gauss", funcion, casos)
    for n in (100, 200, 300):
        comparar_numero(f"suma_{n}", obtener(ns, f"suma_{n}"), n * (n + 1) // 2)


auto4 = sesion.agregar(
    "auto4", "Fórmula de Gauss", _auto4,
    pista="La función debe devolver `n * (n + 1) / 2`. Usa `//` (división entera) si "
          "quieres obtener un `int` en lugar de un `float`.",
    solucion="""
def formula_gauss(n):
    return n * (n + 1) // 2

suma_100 = formula_gauss(100)
suma_200 = formula_gauss(200)
suma_300 = formula_gauss(300)
print(suma_100, suma_200, suma_300)
""")


def _mismo_criterio(obtenido, esperado):
    return isinstance(obtenido, str) and normalizar_texto(obtenido).removeprefix("en ") == esperado


def _auto5(ns):
    delta_g = obtener_funcion(ns, "calcular_delta_g")
    casos = [
        ((206.1, 215, 298.15), {}, 206.1 - 298.15 * 0.215),
        ((-100.0, -50.0, 300.0), {}, -100.0 - 300.0 * -0.050),
        ((10.0, 100.0, 100.0), {}, 0.0),
    ]
    probar_funcion("calcular_delta_g", delta_g, casos,
                   comparar=lambda o, e: abs(o - e) < 1e-3 * max(1, abs(e)))
    clasificar = obtener_funcion(ns, "clasificar_reaccion")
    casos = [((-5.0,), {}, "espontanea"), ((0.0,), {}, "equilibrio"),
             ((12.5,), {}, "no espontanea")]
    probar_funcion("clasificar_reaccion", clasificar, casos, comparar=_mismo_criterio)
    comparar_numero("delta_g_25", obtener(ns, "delta_g_25"), 206.1 - 298.15 * 0.215)
    comparar_numero("T_inversion", obtener(ns, "T_inversion"), 206.1 / 0.215, rel=5e-3)
    return ("A 25 °C la reacción no es espontánea; por encima de ≈ 959 K el término "
            "TΔS domina y ΔG se vuelve negativo.")


auto5 = sesion.agregar(
    "auto5", "Espontaneidad de una reacción", _auto5,
    pista="ΔS está en J/(mol·K) y ΔH en kJ/mol: divide ΔS entre 1000 dentro de la "
          "función. Para `T_inversion` iguala ΔG = 0 y despeja T = ΔH / ΔS.",
    solucion="""
def calcular_delta_g(delta_h, delta_s, T):
    \"\"\"ΔG en kJ/mol a partir de ΔH (kJ/mol), ΔS (J/(mol·K)) y T (K).\"\"\"
    return delta_h - T * delta_s / 1000

def clasificar_reaccion(delta_g):
    if delta_g < 0:
        return "espontánea"
    elif delta_g == 0:
        return "equilibrio"
    else:
        return "no espontánea"

delta_g_25 = calcular_delta_g(206.1, 215, 25 + 273.15)
print(f"ΔG = {delta_g_25:.2f} kJ/mol → {clasificar_reaccion(delta_g_25)}")

T_inversion = 206.1 / (215 / 1000)
print(f"La reacción es espontánea por encima de {T_inversion:.1f} K")
""")


__all__ = ["____", "progreso", "iniciar_registro"] + [e.clave for e in sesion.ejercicios]
sesion.bienvenida()
